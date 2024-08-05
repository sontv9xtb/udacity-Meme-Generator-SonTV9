"""Author by SonTV9"""
import os

from PIL import Image, ImageDraw, ImageFont
import random


class MemeGenerator:

    def __init__(self, output_dir='./output'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def make_meme(self, img_path, text, author, width=500):
        try:
            # Open the image
            with Image.open(img_path) as img:
                real_width, real_height = img.size
                height = int(real_height * width / real_width)
                img.thumbnail((width, height))

                # Determine text position
                row_text_position = random.randint(10, height - 50)
                column_text_position = random.randint(10, width - 100)

                # Draw text on the image
                draw = ImageDraw.Draw(img)
                # Use default font
                body_font = ImageFont.load_default()
                author_font = ImageFont.load_default()

                draw.text((column_text_position, row_text_position), text, font=body_font, fill='white')
                draw.text((column_text_position, row_text_position + 25), author, font=author_font, fill='white')

                # Generate output file path
                outfile = os.path.join(self.output_dir, f'temp-{random.randint(0, 1000000)}.jpg')

                # Save the image
                img.save(outfile)
                print(f'Meme saved to {outfile}')
                return outfile

        except IOError as e:
            print(f"Error: {e}")
            return None
