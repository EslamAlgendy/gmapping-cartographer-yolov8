#!/usr/bin/env python3

import math
import numpy as np

import rclpy
import tf2_ros

from rclpy.node import Node
from cv_bridge import CvBridge

from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Point, PointStamped
from vision_msgs.msg import Detection2DArray
from visualization_msgs.msg import Marker, MarkerArray
from tf2_geometry_msgs import do_transform_point


class SemanticMapper(Node):
    def __init__(self):
        super().__init__("semantic_mapper")

        self.declare_parameter("detections_topic", "/yolo/detections")
        self.declare_parameter("depth_topic", "/camera/depth/image_raw")
        self.declare_parameter("camera_info_topic", "/camera/camera_info")
        self.declare_parameter("marker_topic", "/semantic_detections")
        self.declare_parameter("map_frame", "map")
        self.declare_parameter("camera_frame", "camera_link")
        self.declare_parameter("min_depth", 0.15)
        self.declare_parameter("max_depth", 8.0)
        self.declare_parameter("stride", 4)

        self.detections_topic = self.get_parameter("detections_topic").value
        self.depth_topic = self.get_parameter("depth_topic").value
        self.camera_info_topic = self.get_parameter("camera_info_topic").value
        self.marker_topic = self.get_parameter("marker_topic").value
        self.map_frame = self.get_parameter("map_frame").value
        self.camera_frame = self.get_parameter("camera_frame").value
        self.min_depth = float(self.get_parameter("min_depth").value)
        self.max_depth = float(self.get_parameter("max_depth").value)
        self.stride = int(self.get_parameter("stride").value)

        self.bridge = CvBridge()
        self.depth_image = None
        self.have_camera_info = False

        self.fx = None
        self.fy = None
        self.cx = None
        self.cy = None

        self.marker_pub = self.create_publisher(MarkerArray, self.marker_topic, 10)

        self.create_subscription(Image, self.depth_topic, self.depth_cb, 10)
        self.create_subscription(CameraInfo, self.camera_info_topic, self.camera_info_cb, 10)
        self.create_subscription(Detection2DArray, self.detections_topic, self.detection_cb, 10)

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.get_logger().info("Semantic mapper with real 3D bbox edges started")

    def camera_info_cb(self, msg: CameraInfo):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]
        self.have_camera_info = True

    def depth_cb(self, msg: Image):
        try:
            self.depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        except Exception as e:
            self.get_logger().error(f"Depth conversion failed: {e}")

    def pixel_to_3d(self, u, v, z):
        x = (u - self.cx) * z / self.fx
        y = (v - self.cy) * z / self.fy
        return x, y, z

    def transform_xyz(self, x, y, z, stamp):
        p = PointStamped()
        p.header.frame_id = self.camera_frame
        p.header.stamp = stamp
        p.point.x = float(x)
        p.point.y = float(y)
        p.point.z = float(z)

        tf_msg = self.tf_buffer.lookup_transform(
            self.map_frame,
            self.camera_frame,
            rclpy.time.Time()
        )
        p_out = do_transform_point(p, tf_msg)
        return np.array([p_out.point.x, p_out.point.y, p_out.point.z], dtype=np.float32)

    def make_box_corners(self, xmin, xmax, ymin, ymax, zmin, zmax):
        return [
            (xmin, ymin, zmin),
            (xmax, ymin, zmin),
            (xmax, ymax, zmin),
            (xmin, ymax, zmin),
            (xmin, ymin, zmax),
            (xmax, ymin, zmax),
            (xmax, ymax, zmax),
            (xmin, ymax, zmax),
        ]

    def add_line_box(self, marker_array, corners, ns, marker_id, label_text):
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        line_marker = Marker()
        line_marker.header.frame_id = self.map_frame
        line_marker.header.stamp = self.get_clock().now().to_msg()
        line_marker.ns = ns
        line_marker.id = marker_id
        line_marker.type = Marker.LINE_LIST
        line_marker.action = Marker.ADD
        line_marker.scale.x = 0.03
        line_marker.color.r = 0.0
        line_marker.color.g = 1.0
        line_marker.color.b = 0.0
        line_marker.color.a = 1.0
        line_marker.lifetime.sec = 1

        for i, j in edges:
            p1 = Point()
            p1.x, p1.y, p1.z = corners[i]
            p2 = Point()
            p2.x, p2.y, p2.z = corners[j]
            line_marker.points.append(p1)
            line_marker.points.append(p2)

        marker_array.markers.append(line_marker)

        corner_marker = Marker()
        corner_marker.header.frame_id = self.map_frame
        corner_marker.header.stamp = self.get_clock().now().to_msg()
        corner_marker.ns = ns + "_corners"
        corner_marker.id = 10000 + marker_id
        corner_marker.type = Marker.SPHERE_LIST
        corner_marker.action = Marker.ADD
        corner_marker.scale.x = 0.05
        corner_marker.scale.y = 0.05
        corner_marker.scale.z = 0.05
        corner_marker.color.r = 1.0
        corner_marker.color.g = 0.2
        corner_marker.color.b = 0.2
        corner_marker.color.a = 1.0
        corner_marker.lifetime.sec = 1

        for c in corners:
            p = Point()
            p.x, p.y, p.z = c
            corner_marker.points.append(p)

        marker_array.markers.append(corner_marker)

        cx = sum([c[0] for c in corners]) / 8.0
        cy = sum([c[1] for c in corners]) / 8.0
        cz = max([c[2] for c in corners]) + 0.15

        text = Marker()
        text.header.frame_id = self.map_frame
        text.header.stamp = self.get_clock().now().to_msg()
        text.ns = ns + "_labels"
        text.id = 20000 + marker_id
        text.type = Marker.TEXT_VIEW_FACING
        text.action = Marker.ADD
        text.pose.position.x = cx
        text.pose.position.y = cy
        text.pose.position.z = cz
        text.pose.orientation.w = 1.0
        text.scale.z = 0.18
        text.color.r = 1.0
        text.color.g = 1.0
        text.color.b = 1.0
        text.color.a = 1.0
        text.text = label_text
        text.lifetime.sec = 1
        marker_array.markers.append(text)

    def detection_cb(self, msg: Detection2DArray):
        if self.depth_image is None or not self.have_camera_info:
            return

        marker_array = MarkerArray()
        marker_id = 0

        h, w = self.depth_image.shape[:2]

        for det in msg.detections:
            try:
                cx = float(det.bbox.center.position.x)
                cy = float(det.bbox.center.position.y)
            except Exception:
                cx = float(det.bbox.center.x)
                cy = float(det.bbox.center.y)

            sx = float(det.bbox.size_x)
            sy = float(det.bbox.size_y)

            x1 = max(0, int(cx - sx / 2))
            y1 = max(0, int(cy - sy / 2))
            x2 = min(w - 1, int(cx + sx / 2))
            y2 = min(h - 1, int(cy + sy / 2))

            if x2 <= x1 or y2 <= y1:
                continue

            roi_points_map = []

            for v in range(y1, y2, self.stride):
                for u in range(x1, x2, self.stride):
                    z = float(self.depth_image[v, u])

                    if math.isnan(z) or z <= 0.0:
                        continue

                    if z > 20.0:
                        z = z / 1000.0

                    if z < self.min_depth or z > self.max_depth:
                        continue

                    x, y, z = self.pixel_to_3d(u, v, z)

                    try:
                        p_map = self.transform_xyz(x, y, z, msg.header.stamp)
                        roi_points_map.append(p_map)
                    except Exception:
                        continue

            if len(roi_points_map) < 20:
                continue

            pts = np.array(roi_points_map, dtype=np.float32)

            center = np.median(pts, axis=0)
            d = np.linalg.norm(pts - center, axis=1)
            pts = pts[d < np.percentile(d, 85)]

            if pts.shape[0] < 10:
                continue

            xmin, ymin, zmin = np.min(pts, axis=0)
            xmax, ymax, zmax = np.max(pts, axis=0)

            if (xmax - xmin) < 0.03 or (ymax - ymin) < 0.03 or (zmax - zmin) < 0.03:
                continue

            label = "object"
            score = 0.0
            if len(det.results) > 0:
                hyp = det.results[0].hypothesis
                label = str(hyp.class_id)
                score = float(hyp.score)

            corners = self.make_box_corners(xmin, xmax, ymin, ymax, zmin, zmax)
            self.add_line_box(
                marker_array,
                corners,
                ns="semantic_3d_boxes",
                marker_id=marker_id,
                label_text=f"{label} {score:.2f}"
            )

            marker_id += 1

        self.marker_pub.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = SemanticMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()