#!/usr/bin/env python3
"""Read-only live ROS 2 smoke test (new script, not yet tested on author workstation)."""
import argparse, json, time

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--algorithm',choices=('gmapping','cartographer'),required=True)
    ap.add_argument('--with-yolo',action='store_true')
    ap.add_argument('--timeout',type=float,default=60.0)
    ap.add_argument('--out',help='JSON evidence file, optional')
    opts=ap.parse_args()
    if opts.timeout <= 0: ap.error('timeout must be positive')
    import rclpy
    from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
    from nav_msgs.msg import OccupancyGrid
    from sensor_msgs.msg import Image
    from std_msgs.msg import String
    if opts.algorithm=='cartographer':
        from cartographer_ros_msgs.msg import SubmapList
    rclpy.init()
    node=rclpy.create_node('zenodo_runtime_validator')
    readings={'map':None,'submap_messages':0,'annotated_images':0,'detection_messages':0,'detection_sample':None}
    def on_map(msg):
        d=msg.data
        readings['map']={'frame_id':msg.header.frame_id,'width':msg.info.width,'height':msg.info.height,
             'resolution_m_per_cell':float(msg.info.resolution),'cells':len(d),
             'known_cells':sum(v>=0 for v in d),'occupied_cells':sum(v>50 for v in d)}
    def on_submap(msg): readings['submap_messages']+=1
    def on_img(msg): readings['annotated_images']+=1
    def on_text(msg):
        readings['detection_messages']+=1
        if readings['detection_sample'] is None: readings['detection_sample']=msg.data[:512]
    map_qos=QoSProfile(depth=1,reliability=ReliabilityPolicy.RELIABLE,
                       durability=DurabilityPolicy.TRANSIENT_LOCAL)
    subs=[node.create_subscription(OccupancyGrid,'/map',on_map,map_qos)]
    if opts.algorithm=='cartographer':
        subs.append(node.create_subscription(SubmapList,'/submap_list',on_submap,10))
    if opts.with_yolo:
        subs.extend([node.create_subscription(Image,'/yolo/annotated_image',on_img,10),
                     node.create_subscription(String,'/yolo/detections_text',on_text,10)])
    deadline=time.monotonic()+opts.timeout
    passed=False
    while time.monotonic()<deadline:
        rclpy.spin_once(node,timeout_sec=0.6)
        nodes={name for name,_ in node.get_node_names_and_namespaces()}
        slam='slam_gmapping' if opts.algorithm=='gmapping' else 'cartographer_node'
        m=readings['map']
        map_pass=bool(m and m['cells']==m['width']*m['height'] and m['known_cells']>0)
        submap_pass=(opts.algorithm!='cartographer' or readings['submap_messages']>0)
        yolo_pass=(not opts.with_yolo or readings['annotated_images']>0 and readings['detection_messages']>0)
        passed=(slam in nodes and map_pass and submap_pass and yolo_pass and
                ('yolov8_ros2_node' in nodes)==opts.with_yolo and node.count_publishers('/map')==1)
        if passed: break
    report={'algorithm':opts.algorithm,'with_yolo':opts.with_yolo,'pass':passed,
        'nodes':sorted({n for n,_ in node.get_node_names_and_namespaces()}),
        'map_publishers':node.count_publishers('/map'),
        'scan_publishers':node.count_publishers('/scan'),**readings,
        'qualification':'ROS topic smoke test, not a proof of algorithmic improvement or positive detections'}
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if opts.out:
        with open(opts.out,'w',encoding='utf8') as f: json.dump(report,f,indent=2,ensure_ascii=False)
    node.destroy_node();rclpy.shutdown()
    return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
