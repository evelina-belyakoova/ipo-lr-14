from packet.ImageHandler import ImageHandler
from packet.ImageProcessor import ImageProcessor
import os

def main():
    image_path = input("Укажите путь к картинке:").strip()
    if not os.path.isfile(image_path):
        print(f"Такого файла нету")
        return
    handler = ImageHandler(image_path)
    print("Загрузил изображение")

    new_path = handler.save_image("kartinka")
    print(f"Уменьшил изображение и сохранил как {new_path}")

    processor = ImageProcessor(handler.image)
    processor.contour()
    print("Применили фильтр контура")

    processor.text()
    print(f"Добавили текст по центру")

    end = new_path.replace(".jpg","_processed.jpg")
    processor.image.save(end)
    print(f"Сохранили изображение как {end}")

if __name__ == "__main__":
    main()