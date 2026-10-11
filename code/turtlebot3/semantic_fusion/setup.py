from setuptools import find_packages, setup

package_name = 'semantic_fusion'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Eslam Ibrahem Hamed',
    maintainer_email='eslam.hamed@must.edu.eg',
    description='ROS 2 experimental YOLO detection and RGB/depth overlay nodes; no validated SLAM fusion.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'yolo_node = semantic_fusion.yolo_node:main',
        'fusion_node_master = semantic_fusion.fusion_node:main',
        ],
    },
)
