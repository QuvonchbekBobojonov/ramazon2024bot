from PIL import Image, ImageDraw, ImageFont


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def create_image(name, author, design):
    color = "#ffffff"
    font_size = 208.59
    font_size_2 = 132.58

    font_type = ImageFont.truetype("fonts/ofont.ru_Appetite.ttf", font_size)
    font_type_2 = ImageFont.truetype("fonts/ofont.ru_Appetite.ttf", font_size_2)

    if design == "design_1":
        image = Image.open("images/greeting_card/001.jpg")

    elif design == "design_2":
        image = Image.open("images/greeting_card/002.jpg")
        color = "#000000"

    elif design == "design_3":
        image = Image.open("images/greeting_card/003.jpg")

    draw = ImageDraw.Draw(image)

    text_size = textsize(name, font_type)
    text_size_2 = textsize(author, font_type_2)

    x = (image.width - text_size[0]) / 2
    x_2 = (image.width - text_size_2[0]) / 2

    draw.text(xy=(x, 1400.28), text=name.title(), font=font_type, fill=color, align="center")
    draw.text(xy=(x_2, 3180), text=author.title(), font=font_type_2, fill=color, align="center")

    image.save(f"{name}.jpg")


if __name__ == "__main__":
    create_image("John Doe", "Jane Doe", "design_2")
