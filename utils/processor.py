import os
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from imagehash import phash, dhash, colorhash, average_hash
import filetype

"""
所有有关于图片处理的方法：
1. VLM_processor: 用CLIP模型对电池图片数据集进行初步筛选和分类，过滤掉非写实类图片并将所有图片分为三
                  类: 分别为"cylindrical", "prismatic" 和 "pouch"。
2. hash_processor: 使用imagehash模块计算各个图片的哈希值并进行去重处理。
"""

# 查看是否为图片类型
def is_image(file_path):
    kind = filetype.guess(file_path)
    if kind is not None and "image" in kind.mime:
        return True
    return False

# 获取当前文件夹下所有图片的路径
def get_images(dir_path):
    # 定义返回值列表
    img_paths = []
    # 遍历该文件夹下所有文件并拼接为完整的文件路径
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            filepath = os.path.join(root, file)
            # 如果这一文件为图片类型，则加入到返回值列表中
            if is_image(filepath):
                img_paths.append(filepath)
    return img_paths

# 将图片保存到指定规则的路径上
def save_image(image, img_path, output_path, idx):
    # 获取图片的后缀名
    ext = os.path.splitext(img_path)[1]
    # 为该文件进行命名
    filename =  f"{str(idx).zfill(5)}{ext}"
    # 生成完整的保存路径
    save_path = os.path.join(output_path, filename)
    # 保存图片
    image.save(save_path)

# 定义HashProcessor类用于图片的哈希值计算
class HashProcessor:
    def __init__(self, hash_mode):
        # 指定计算哈希值时所使用的算法: 1. 感知哈希 2. 差值哈希 3. 颜色哈希 4. 均值哈希
        self.hash_mode = hash_mode
        self.hash_modes = {
            "perceptual": phash,
            "differential": dhash,
            "color": colorhash,
            "average": average_hash
        }
        # 哈希值的集合和当前保存图片命名的序号
        self.hashes = set()
        self.idx = 0

    def process(self, input_path="./data/raw/", output_path="./data/cleaned/hash_processed/"):
        # 获取输入文件夹下所有图片路径
        img_list = get_images(input_path)
        # 遍历全部图片并进行识别
        for img_path in img_list:
            # 打开图片
            image = Image.open(img_path)
            # 根据所选模式计算哈希值
            hash_value = self.hash_modes[self.hash_mode](image)
            # 如果该哈希值之前没有出现过
            if hash_value not in self.hashes:
                # 图片进行保存
                save_image(image, img_path, output_path, self.idx)
                # 将哈希值添加到集合中
                self.hashes.add(hash_value)
                # 图片命名序号自增
                self.idx = self.idx + 1

# 定义VLMProcessor类用于图片过滤和分类
class VLMProcessor:
    def __init__(self):
        # 定义处理器使用的模型和图片的预处理器
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        # 为VLM准备的prompt从而对图片进行分类
        self.prompts = [
            "this is an image of a cylindrical lithium-ion battery", # "cylindrical": positive
            "this is an image of a prismatic lithium battery cell", # "prismatic": positive
            "this is an image of a flexible pouch battery used in electronics", # "pouch": positive
            "this is a diagram showing the internal structure of a battery", # "internal structure": negative
            "this is a schematic diagram of a lithium-ion battery reaction", # "schematic diagram": negative
            "this is a photo of multiple battery cells connected in a pack" # "battery pack": negative
        ]
        # 当前保存图片命名的序号
        self.idx = 0

    def process(self, input_path="./data/cleaned/hash_processed/", output_path="./data/cleaned/vlm_processed/"):
        # 获取输入文件夹下所有图片路径
        img_list = get_images(input_path)
        # 遍历全部图片并进行识别
        for img_path in img_list:
            # 打开图片
            image = Image.open(img_path)
            # 对图片进行处理，并指定提示词将其转化为inputs
            inputs = self.processor(text=self.prompts, images=image, return_tensors="pt", padding=True)
            # 将inputs输入VLM模型中查看prompt所对应的image-text相似性的得分,并依次进行过滤和分类处理
            outputs = self.model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            # 如果probs中最大的值的index值在0~2之间，则表示其可以作为训练样本
            max_index = probs.argmax(dim=1).item()
            if max_index < 3:
                # 保存图片到指定路径
                save_image(image, img_path, output_path, self.idx)
                # 图片命名序号自增
                self.idx = self.idx + 1



if __name__ == '__main__':
    # 创建哈希处理器，设置模式为感知哈希模式
    hash_processor = HashProcessor("perceptual")
    hash_processor.process()
    # 创建VLM处理器，对非预期的图片进行过滤
    vlm_processor = VLMProcessor()
    vlm_processor.process()


