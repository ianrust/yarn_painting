import itertools,sys,argparse,math,time,random
import numpy as np
from scipy import misc
from matplotlib import pyplot as plt

def parseArgs():
	parser=argparse.ArgumentParser(prog=sys.argv[0])
	parser.add_argument('-s','--size',nargs=2,dest='size',help='size in meters of the canvas [height,width]',default = [1.0,2.0],type=float)
	parser.add_argument('-i','--img','--image',dest='image_filename',help='image file to be yarn-paint-processed',default='download.jpg')
	parser.add_argument('-is','--imsize',dest='image_size',default=0.5,help='size of image in meters vertical side')
	parser.add_argument('-p','--pegs',nargs=2,dest='pegs',help='number of pegs on each edge [vertical,horizontal]',default = [100,100],type=int)
	parser.add_argument('-d','--disp',dest='disp',help='should we display the processed image?',default=False,action='store_true')
	parser.add_argument('-o','--out','--outimage',dest='out_image_filename',help='image file to be saved as')
	args= parser.parse_args()
	return args

def getIndexAtValue(image_matrix,search_val):
	# print search_val
	# new_mat = image_matrix.copy()*0

	size = image_matrix.shape

	value_points = []

	for row in range(size[0]):
		for col in range(size[1]):
			val = image_matrix[row][col]
			if val == search_val:
				loc = (row,col)
				value_points.append(loc)
			# 	new_mat[row][col] = 255
			# 	print search_val

	return value_points
	# plt.ion()			
	# plt.imshow(new_mat)
	# plt.show()
	# plt.draw()
	# time.sleep(0.25)

def generatePointPairs(points):

	random.shuffle(points)
	# get pars
	# pairs = list(itertools.permutations(points))
	return points
		
def main():
	global yarns_opt,image_opt
	args=parseArgs()
	print args.image_filename
	# image_matrix=misc.imread(args.image_filename)
	image_matrix = misc.lena()
	print type(image_matrix)
	print image_matrix.shape
	print image_matrix[0][0]

	yarn_image = image_matrix.copy()*0

	for s_val in range(255):
		print s_val
		points = getIndexAtValue(image_matrix,s_val)
		print len(points)
		if len(points)>1:
			pairs = generatePointPairs(points)
			print pairs

		# for pair in pairs:
			# draw line on empty frame that goes through the points

	plt.figure(0)
	# display approximation

	plt.figure(1)
	plt.gray()
	plt.imshow(image_matrix)
	plt.show()


if __name__ == "__main__":
	main()