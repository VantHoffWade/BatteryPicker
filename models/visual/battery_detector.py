from ultralytics import YOLO

# 这是用YOLO来实现电池类型识别的代码

# 根据yaml文件构建一个新模型，然后将预训练模型的参数转移到新模型中
model = YOLO('yolov5n.pt')

# 查看预训练模型的类别名称
print(model.names)

# 通过yolo模型对照片进行预测
result = model(["bicycle.jpg"])

print(result[0].boxes)