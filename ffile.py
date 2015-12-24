# -*- coding: UTF-8 -*-

# python view file size

import os

# FILE_NAME = './README'
FILE_NAME = "/Users/liguangming/gm_self/Lee's photo/wedding.zip"
FILE_10M = 10 * 1000 * 1000 # file size 10 Megabytes


def FileSize2Str(file_size):
	if file_size > 1000:
		file_size = file_size/1000
		pass
	else:
		return str(file_size) + "B"
		pass

	if file_size > 1000:
		file_size = file_size/1000
		pass
	else:
		return str(file_size) + "KB"
		pass

	if file_size > 1000:
		file_size = file_size/1000
		pass
	else:
		return str(file_size) + "MB"
		pass

	if file_size > 1000:
		file_size = file_size/1000
		pass
	else:
		return str(file_size) + "GB"
		pass

	pass


def FileSizeCheck(file_name):
	file_size = os.path.getsize(file_name)	
	if file_size >= FILE_10M:
		print 'File size over 10M.'
		print FileSize2Str(file_size)
		return False
	else:
		print 'File size is OK.'
		print FileSize2Str(file_size)
		return True
	pass



if __name__ == '__main__':
	FileSizeCheck(FILE_NAME)



