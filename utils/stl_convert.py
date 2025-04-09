import os
import trimesh

"""
此脚本目的在于将ASCII STL文件转为Binary STL文件以满足Mujoco对mesh的要求
"""

def simplify_stl(stl_dir, limit=200_000):
    # 遍历输入文件夹下的所有文件
    for root, dirs, files in os.walk(stl_dir):
        for file in files:
            # 如果发现当前遍历到的文件为STL文件
            if os.path.splitext(file)[1].lower() == '.stl':
                # 目标路径
                path = os.path.join(root, file)
                try:
                    # 打开stl文件
                    mesh = trimesh.load(str(path), force="mesh")
                    # 检查stl文件的面数是否大于规定的最大面数
                    if len(mesh.faces) > limit:
                        # 如果面数大于限制则进行简化
                        reduced_mesh = mesh.simplify_quadric_decimation(face_count=limit)
                        # 将简化后的模型保存到原来的文件中
                        reduced_mesh.export(path)
                        # 输出简化后的面数
                        print(f"{path}的面数原本为{len(mesh.faces)}, 现在简化为{len(reduced_mesh.faces)}")
                except Exception as e:
                    # 报错提示
                    print(f"{path}简化失败, {e}")

if __name__ == "__main__":
    simplify_stl("../models/sim/robot_arms")