#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
from vision_msgs.msg import BoundingBox2D

from cv_bridge import CvBridge
from ultralytics import YOLO


class YoloDetector(Node):

    def __init__(self):
        super().__init__("yolo_detector")

        self.declare_parameter("image_topic", "/camera/image")
        self.declare_parameter("detections_topic", "/yolo/detections")
        self.declare_parameter("weights", "yolov8n.pt")
        self.declare_parameter("conf", 0.35)

        image_topic = self.get_parameter("image_topic").value
        detections_topic = self.get_parameter("detections_topic").value
        weights = self.get_parameter("weights").value
        self.conf = float(self.get_parameter("conf").value)

        self.bridge = CvBridge()

        self.get_logger().info("Loading YOLO model...")
        self.model = YOLO(weights)

        self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )

        self.pub = self.create_publisher(
            Detection2DArray,
            detections_topic,
            10
        )

        self.get_logger().info("YOLO detector node started")

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        results = self.model(frame, conf=self.conf)[0]

        detection_array = Detection2DArray()
        detection_array.header = msg.header

        for box in results.boxes:

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls = int(box.cls[0])
            score = float(box.conf[0])

            detection = Detection2D()
            detection.header = msg.header

            bbox = BoundingBox2D()
            bbox.center.x = (x1 + x2) / 2
            bbox.center.y = (y1 + y2) / 2
            bbox.size_x = (x2 - x1)
            bbox.size_y = (y2 - y1)

            detection.bbox = bbox

            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = str(cls)
            hyp.hypothesis.score = score

            detection.results.append(hyp)

            detection_array.detections.append(detection)

        self.pub.publish(detection_array)


def main(args=None):

    rclpy.init(args=args)

    node = YoloDetector()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()