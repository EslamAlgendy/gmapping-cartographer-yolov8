#!/usr/bin/env python3
import os
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from tf2_ros import Buffer, TransformListener, TransformException

class SlamTfLogger(Node):
    def __init__(self):
        super().__init__("log_slam_pose")

        # declare only our own params (do NOT declare use_sim_time again)
        self.declare_parameter("map_frame", "map")
        self.declare_parameter("base_frame", "base_link")
        self.declare_parameter("outfile", os.path.expanduser("~/gmapping_ws/metrics/slam_tum.txt"))
        self.declare_parameter("rate_hz", 20.0)

        # ensure sim time ON
        self.set_parameters([Parameter("use_sim_time", Parameter.Type.BOOL, True)])

        self.map_frame = self.get_parameter("map_frame").value
        self.base_frame = self.get_parameter("base_frame").value
        self.outfile = self.get_parameter("outfile").value
        self.rate_hz = float(self.get_parameter("rate_hz").value)

        os.makedirs(os.path.dirname(self.outfile), exist_ok=True)
        self.f = open(self.outfile, "w")

        self.get_logger().info(f"SLAM TF: {self.map_frame} -> {self.base_frame}")
        self.get_logger().info(f"Writing: {self.outfile}")

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.timer = self.create_timer(1.0 / self.rate_hz, self.tick)

    def tick(self):
        try:
            tr = self.tf_buffer.lookup_transform(self.map_frame, self.base_frame, rclpy.time.Time())
            stamp = tr.header.stamp
            t = tr.transform.translation
            q = tr.transform.rotation
            ts = stamp.sec + stamp.nanosec * 1e-9
            self.f.write(f"{ts:.9f} {t.x:.6f} {t.y:.6f} {t.z:.6f} {q.x:.6f} {q.y:.6f} {q.z:.6f} {q.w:.6f}\n")
            self.f.flush()
        except TransformException:
            pass

    def destroy_node(self):
        try:
            self.f.close()
        except Exception:
            pass
        super().destroy_node()

def main():
    rclpy.init()
    node = SlamTfLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
