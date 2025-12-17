from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
class ImageHandler:
    def __init__(self, image_path):
          self.image_path = image_path
          self.image = None
          self.load_image()

    def load_image(self):
        self.image = Image.open(self.image_path)
        print(f"Изображение загружено")

    def save_image(self, name = "kartinkaa"): 
            dir_name, filename = os.path.split(self.image_path)
            name, ext = os.path.splitext(filename)
            rename = f"{name}{ext}"
            new_path = os.path.join(dir_name,rename)
            self.image.save(new_path)
            return new_path
       
    def size_image(self, max_size=(200, 200)):
        if self.image is not None: 
            self.image.thumbnail(max_size) 
            print(f"Изображение изменено")
        else:
            print("Ошибка: Изображение не загружено.")

    def get_image(self): 
        return self.image 