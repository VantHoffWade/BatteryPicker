import mujoco
import mujoco.viewer
import time
import numpy as np

# 加载模型和数据
model = mujoco.MjModel.from_xml_path("../robot_arms/dofbot/dofbot.xml")
data = mujoco.MjData(model)

# 控制目标（假设 actuator 控制了 joint0）
target = 0.5  # 想让 joint 旋转到 0.5 弧度（约28度）

# 可视化窗口（也可以不启用）
with mujoco.viewer.launch_passive(model, data) as viewer:
    print("接触数量:", data.ncon)
    for step in range(1000):  # 仿真1000步（时间 = 1000*timestep）
        # 控制器：将第0个 actuator 的目标设为 target
        data.ctrl[0] = target
        data.ctrl[1] = -target
        data.ctrl[2] = target

        # 运行一步仿真
        mujoco.mj_step(model, data)

        # 可选：每步之间 sleep 一点时间（控制速度）
        time.sleep(model.opt.timestep)
