from PIL import Image


def convert_jpg_to_ico(jpg_path, ico_path, sizes=[(16, 16), (32, 32), (64, 64)]):
    """
    将JPG文件转换为ICO格式
    :param jpg_path: JPG文件路径
    :param ico_path: 输出的ICO文件路径
    :param sizes: 需要生成的ICO尺寸列表
    """
    try:
        # 打开JPG文件
        with Image.open(jpg_path) as img:
            # 调整图像尺寸并保存为ICO
            img.save(ico_path, format="ICO", sizes=sizes)
        print(f"成功生成ICO文件: {ico_path}")
    except Exception as e:
        print(f"转换失败: {e}")


# 示例调用
if __name__ == "__main__":
    jpg_file = "input.jpg"  # 输入的JPG文件路径
    ico_file = "favicon.ico"  # 输出的ICO文件路径
    convert_jpg_to_ico(jpg_file, ico_file)
