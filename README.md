# 项目介绍
    本项目用于实现机械臂对电池的仿真和抓取过程。
    
    其主要功能在于用yolo框架对锂离子电池进行识别和定位，通过模版匹配的方法实现对电池的位姿估计，
    从而实现电池的平面抓取。同时，还要实现对不同检测装置标识的识别，并控制机械臂将电池移动到指定
    的位置。

# 环境依赖
    python==3.11
    icrawler==0.6.10
    pytorch==2.4.1 + cuda12.1
    

# 目录结构
    BatteryPicker
    ├─dataset
    │  ├─images
    │  │  ├─train
    │  │  └─val
    │  └─labels
    │      ├─train
    │      └─val
    ├─Test
    └─utils
        └─data
            ├─cleaned
            ├─labeled
            └─raw
                ├─baidu
                ├─bing
                └─google

# 使用说明
    说明

# 版本更新

    