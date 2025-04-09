from yourdfpy import URDF
from mujoco import MjModel
import os

"""
该脚本用于将URDF文件格式的机械臂加载到Mujoco环境中并进行可视化。
机械臂的文件夹推荐存储在robot_arms文件夹下，并以这种形式组织:
<RobotName>
 ├─<RobotName>.urdf
 └─meshes
    ├─visual
    │   ├─baselink.STL
    │   ├─link1.STL
    │   ├─link2.STL
    │   └─...
    └─collision
        ├─baselink.STL
        ├─link1.STL
        ├─link2.STL
        └─...
其中<RobotName>为该机械臂的名称。
"""

model = MjModel.from_xml_path("robot_arms/dofbot/dofbot.xml")