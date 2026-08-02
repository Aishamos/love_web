from PIL import Image, ImageOps
import os


def create_thumbnail(src_path, dst_path, size=(400, 400)):
    """生成缩略图，保持宽高比"""
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)
    img.thumbnail(size)
    img.save(dst_path, quality=85)
    return img.width, img.height


def get_image_size(path):
    """获取图片尺寸"""
    with Image.open(path) as img:
        return img.size
