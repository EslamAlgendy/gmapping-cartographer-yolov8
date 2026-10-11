#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener

class SlamPoseLogger(Node):
    def __init__(self):
        super().__init__('slam_pose_logger')
        self.declare_parameter('base_frame', 'base_link')
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('rate_hz', 10.0)
        self.declare_parameter('outfile', '/tmp/slam_tum.txt')

        self.base = self.get_parameter('base_frame').get_parameter_value().string_value
        self.mapf = self.get_parameter('map_frame').get_parameter_value().string_value
        self.rate = self.get_parameter('rate_hz').get_parameter_value().double_value
        self.outfile = self.get_parameter('outfile').get_parameter_value().string_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.f = open(self.outfile, 'w')
        self.timer = self.create_timer(1.0 / self.rate, self.tick)
        self.get_logger().info(f'Logging SLAM (TF) {self.mapf} -> {self.base} to {self.outfile}')

    def tick(self):
        try:
            t = self.tf_buffer.lookup_transform(self.mapf, self.base, rclpy.time.Time())
            ts = self.get_clock().now().nanoseconds * 1e-9
            tr = t.transform.translation
            q  = t.transform.rotation
            self.f.write(f"{ts:.9f} {tr.x:.6f} {tr.y:.6f} {tr.z:.6f} "
                         f"{q.x:.6f} {q.y:.6f} {q.z:.6f} {q.w:.6f}\n")
            self.f.flush()
        except Exception:
            pass

    def destroy_node(self):
        try:
            self.f.flush(); self.f.close()
        except:
            pass
        super().destroy_node()

def main():
    rclpy.init()
    node = SlamPoseLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
