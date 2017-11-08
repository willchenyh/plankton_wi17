import matplotlib.pyplot as plt
import glob
import numpy as np


# random select n images from directory
def random_choice(n, directory):
	files = glob.glob(directory + 'train/*.png')
	choices = map(lambda fn: fn.split('/')[-1], np.random.choice(files, n))
	cls = directory.split('/')[-2]
	with open('%s_index.txt' % cls, 'w') as f:
		for i, choice in enumerate(choices):
			f.writelines(choice + '\n')


# pad row * col image files to form a large padded image
def padding(files, row, col):
	space = 20
	images = [plt.imread(file) for file in files]
	max_height, max_width = max(map(lambda img: img.shape[0], images)), max(map(lambda img: img.shape[1], images))
	mh, mw = max_height + space, max_width + space
	im = np.zeros((mh * row, mw * col, 3))
	for i in range(row):
		for j in range(col):
			img = images[i]
			h, w, _ = img.shape
			top, left = (max_height - h) / 2, (max_width - w) / 2

			padded_img = np.ones((mh, mw, 3))
			padded_img[:max_height, :max_width, :] = np.zeros((max_height, max_width, 3))
			padded_img[top:top + h, left:left + w, :] = img

			im[mh * i:mh * (i + 1), mw * j:mw * (j + 1)] = padded_img

	return im


if __name__ == '__main__':
    directory = '/Users/apple/Google Drive/turk/subclass00/'
    random_choice(501, directory)
    with open('%s_index.txt' % 'subclass00', 'rb') as f:
    	files = [directory + 'train/' + line[:-1] for line in f]
    	padded_image = padding(files, 8, 1)
    	# plt.imsave('padded_image.png', padded_image)
    	plt.imshow(padded_image)
    	plt.axis('off')
    	plt.show()