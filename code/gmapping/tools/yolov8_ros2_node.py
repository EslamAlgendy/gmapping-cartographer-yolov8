#!/usr/bin/env python3

import time
from typing import List

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO


def parse_classes(value: str) -> List[int]:
    if value is None or value.strip() == "":
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip() != ""]


class YoloV8Ros2Node(Node):
    def __init__(self) -> None:
        super().__init__("yolov8_ros2_node")

        self.declare_parameter("image_topic", "/camera/image")
        self.declare_parameter("annotated_topic", "/yolo/annotated_image")
        self.declare_parameter("detections_topic", "/yolo/detections_text")
        self.declare_parameter("weights", "yolov8n.pt")
        self.declare_parameter("conf", 0.35)
        self.declare_parameter("device", "cpu")
        self.declare_parameter("rate_hz", 10.0)
        self.declare_parameter("classes", "")
        self.declare_parameter("publish_annotated", True)
        self.declare_parameter("publish_text", True)

        self.image_topic = self.get_parameter("image_topic").get_parameter_value().string_value
        self.annotated_topic = self.get_parameter("annotated_topic").get_parameter_value().string_value
        self.detections_topic = self.get_parameter("detections_topic").get_parameter_value().string_value
        self.weights = self.get_parameter("weights").get_parameter_value().string_value
        self.conf = self.get_parameter("conf").get_parameter_value().double_value
        self.device = self.get_parameter("device").get_parameter_value().string_value
        self.rate_hz = self.get_parameter("rate_hz").get_parameter_value().double_value
        self.classes_str = self.get_parameter("classes").get_parameter_value().string_value
        self.publish_annotated = self.get_parameter("publish_annotated").get_parameter_value().bool_value
        self.publish_text = self.get_parameter("publish_text").get_parameter_value().bool_value

        self.allowed_classes = parse_classes(self.classes_str)
        self.bridge = CvBridge()
        self.last_infer_time = 0.0
        self.min_period = 1.0 / self.rate_hz if self.rate_hz > 0.0 else 0.0

        self.get_logger().info(f"Loading YOLOv8 model: {self.weights}")
        self.model = YOLO(self.weights)

        self.image_sub = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            10,
        )

        self.annotated_pub = self.create_publisher(Image, self.annotated_topic, 10)
        self.text_pub = self.create_publisher(String, self.detections_topic, 10)

        self.get_logger().info(
            f"YOLO node started | image_topic={self.image_topic} "
            f"| annotated_topic={self.annotated_topic} "
            f"| conf={self.conf} | device={self.device} "
            f"| classes={self.allowed_classes if self.allowed_classes else 'all'}"
        )

    def image_callback(self, msg: Image) -> None:
        now = time.time()
        if self.min_period > 0.0 and (now - self.last_infer_time) < self.min_period:
            return
        self.last_infer_time = now

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as exc:
            self.get_logger().error(f"cv_bridge conversion failed: {exc}")
            return

        try:
            results = self.model.predict(
                source=frame,
                conf=self.conf,
                device=self.device,
                classes=self.allowed_classes if self.allowed_classes else None,
                verbose=False,
            )
        except Exception as exc:
            self.get_logger().error(f"YOLO inference failed: {exc}")
            return

        if not results:
            return

        result = results[0]
        annotated = frame.copy()
        det_lines = []

        names = result.names if hasattr(result, "names") else self.model.names

        if result.boxes is not None and len(result.boxes) > 0:
            boxes_xyxy = result.boxes.xyxy.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy().astype(int)
            confs = result.boxes.conf.cpu().numpy()

            for i, box in enumerate(boxes_xyxy):
                x1, y1, x2, y2 = map(int, box.tolist())
                cls_id = int(classes[i])
                score = float(confs[i])
                label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else str(cls_id)

                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                text = f"{label} {score:.2f}"
                cv2.putText(
                    annotated,
                    text,
                    (x1, max(20, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

                det_lines.append(
                    f"class_id={cls_id}, label={label}, conf={score:.3f}, "
                    f"bbox=[{x1},{y1},{x2},{y2}]"
                )
        else:
            det_lines.append("no_detections")

        if self.publish_annotated:
            try:
                annotated_msg = self.bridge.cv2_to_imgmsg(annotated, encoding="bgr8")
                annotated_msg.header = msg.header
                self.annotated_pub.publish(annotated_msg)
            except Exception as exc:
                self.get_logger().error(f"Annotated image publish failed: {exc}")

        if self.publish_text:
            text_msg = String()
            text_msg.data = "\n".join(det_lines)
            self.text_pub.publish(text_msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = YoloV8Ros2Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()