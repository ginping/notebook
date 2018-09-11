from PIL import Image


def produceImage(file_in, width, height, file_out):
	image = Image.open(file_in)
	resized_image = image.resize((width, height), Image.ANTIALIAS)
	resized_image.save(file_out)


if __name__ == '__main__':
	file_in = r'C:\Users\Ph\Pictures\Saved Pictures\壁纸\Konachan.com - 132445 animal clouds dontakku dress flowers grass original scenic sky tree white_hair.jpg'
	width = 2384
	height = 1207
	file_out = r'C:\Users\Ph\Pictures\Saved Pictures\壁纸\132445.jpg'
	produceImage(file_in, width, height, file_out)