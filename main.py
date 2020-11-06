import re
from PIL import Image

def first_pixel(image):
	image_grey= image.convert('1')
	value = image_grey.load()
	width, height = image.size
	for y in range(0, height):
		for x in range(0, width):
			#print(value[x, y], end=', ')
			if value[x, y] == 0:
				return y

def last_pixel(image):
	image_grey= image.convert('1')
	value = image_grey.load()
	width, height = image.size
	for y in range(height-1, 0, -1):
		for x in range(0, width):
			#print(value[x, y], end=', ')
			if value[x, y] == 0:
				return y

if __name__ == '__main__':
	image = Image.open(input("Picture name: "))
	name = input("Picture word: ").lower()
	print("\nUse letters only from picture word!")
	word = input("Your funny word: ").lower()
	img_name = {}
	width, height = image.size
	crop_from_top = first_pixel(image)
	crop_from_bottom = last_pixel(image)
	image = image.crop((0, crop_from_top, width, crop_from_bottom))
	width, height = image.size
	block_height = height // len(name)
	re_name = re.compile(r'(.)\1{1,}', re.IGNORECASE).sub(r'\1', name)
	block_first = 0
	for i in range(0, len(re_name)):
		img_name.update({re_name[i]:[block_first, block_height+block_first]})
		block_first += block_height
	#print(img_name)
	final_image = []
	for i in word:
		final_image.append(image.crop((0, img_name[i][0], width, img_name[i][1])))
	img = Image.new('RGB', (width, block_height*len(word)))
	block_first = 0
	for i in range(0, len(final_image)):
		img.paste(final_image[i], (0, block_first))
		block_first += block_height
	img.save("out.jpg")
	print("Saved to out.jpg")
