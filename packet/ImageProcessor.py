from PIL import ImageFilter, ImageDraw, ImageFont

class ImageProcessor: 
    def __init__(self,image):
        self.image = image
    def contour(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        return self.image
    def text(self,text="Вариант 3"):
        size = self.image.size
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.load_default()

        bbox = draw.textbbox((0,0),text,font = font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.image.width - text_width) // 2
        y = (self.image.height - text_height) // 2
        draw.text((x, y), text, font = font, fill="black")

        return self.image