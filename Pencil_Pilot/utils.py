import os, pygame

def data_parser(file_name, img_dict1):
	'''Parse the .pack file to get the image infos

	Input : file_name is the .pack file's name, must be compatible with the picture of the same name
	Output : img_dict is a dict of format 'str : pygame.Rect'
	'''

	# Base folder
	img_folder = 'resource'

	# Open file
	inputfile = open(os.path.join(img_folder, file_name))

	img_dict = {}
	# Read the whole lines
	lines = inputfile.readlines()
	for line in lines[5:]:
		if ':' not in line:
			name = line[:len(line)-1]
			img_dict[name] = []
		elif ':' in line and 'xy' in line:
			xy = line.split(':')[1].split(',')
			img_dict[name].append([int(xy[0]), int(xy[1])])
		elif ':' in line and 'size' in line:
			sz = line.split(':')[1].split(',')
			img_dict[name].append([int(sz[0]), int(sz[1])])

	# Restore the img_dict to img_dict1 
	# img_dict = {img_name : list[2]}
	# img_dict1 = {img_name : pygame.Rect}
	for name, value in img_dict.items():
		img_dict1[name] = pygame.Rect(value[0][0], value[0][1], value[1][0], value[1][1])

if __name__ == '__main__':
	dic = {}
	data_parser('shoot.pack', dic)

	for name, value in dic.items():
		print name, value