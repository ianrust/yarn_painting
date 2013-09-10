import itertools,sys,argparse,math,Image,time
import numpy as np

def parseArgs():
	parser=argparse.ArgumentParser(prog=sys.argv[0])
	parser.add_argument('-s','--size',nargs=2,dest='size',help='size in meters of the canvas [height,width]',default = [1.0,2.0],type=float)
	parser.add_argument('-i','--img','--image',dest='image_filename',help='image file to be yarn-paint-processed')
	parser.add_argument('-is','--imsize',dest='image_size',default=0.5,help='size of image in meters vertical side')
	parser.add_argument('-p','--pegs',nargs=2,dest='pegs',help='number of pegs on each edge [vertical,horizontal]',default = [100,100],type=int)
	parser.add_argument('-d','--disp',dest='disp',help='should we display the processed image?',default=False,action='store_true')
	parser.add_argument('-o','--out','--outimage',dest='out_image_filename',help='image file to be saved as')
	args= parser.parse_args()
	return args

def generateDecisionYarns(args,image_grid,image_matrix):
	peg_grid=generateGrid(args.pegs[0],args.pegs[1],xscale=args.size[1]/args.pegs[1],yscale=args.size[0]/args.pegs[0],edges=True)
	peg_combos=itertools.combinations(peg_grid,2)
	yarns = [yarn(combo[0],combo[1],1) for combo in peg_combos]
	i=0
	for yarner in yarns:
		image_grid=yarner.setContributingPoints(dist=image_matrix.shape[0]/args.image_size,grid=image_grid)
		i=i+1
		print str(int(i/float(len(yarns))*100))+"%"
		# print str(yarner.start)+','+str(yarner.finish)
	# for pixel in image_grid:
		# print pixel.num_pyarns
	return image_grid,yarns

def generateGrid(verticalSteps,horizontalSteps,xscale=1,yscale=1,edges=False,image_matrix=[]):
	return_grid=[]
	for x in range(horizontalSteps):
		for y in range(verticalSteps):
			if not edges or (x == 0 or x == horizontalSteps-1 or y == 0 or y == verticalSteps-1):
				if edges:
					color=[0,0,0]
				else:
					color=image_matrix[x][y]
				return_grid.append(pixel(x*xscale,y*yscale,0,[],color[0],color[1],color[2])) # xpos,ypos, num strings going through,array of yarns going through
	return return_grid

def getPerpDistance(point,start,end):
	Dp=start.x-end.x
	Dq=start.y-end.y
	distance = math.fabs(Dq*point.x-Dp*point.y+start.x*end.y-start.y*end.x)/math.sqrt(Dp**2+Dq**2)
	return distance

def getObjectiveFunction(yarns,image_act):
	score=0.0
	for yarn in yarns:
		for point in yarn.cont_points:
			score=score+math.exp(-(point[1])**2)/(point[0].r+1)# also multiply by difference between actual RGB value and non in exponent
	return score/(len(yarns)*len(image_act))
	
class yarn():
	def __init__(self,start,finish,num_channels):
		self.start=start
		self.finish=finish
		self.channels=[]
		for a in range(num_channels):
			self.channels.append(True)
	def setContributingPoints(self,dist,grid):
		self.cont_points=[]
		#make this the one that gives index
		for i,point in enumerate(grid):
			# if getPerpDistance(point,self.start,self.finish)<=dist:
			self.cont_points.append((point,getPerpDistance(point,self.start,self.finish)))
			point.num_pyarns=point.num_pyarns+1
			point.pyarns.append(self)
		return grid

class pixel():
	def __init__(self,x,y,num_through,which_through,red,green,blue):
		self.x=x
		self.y=y
		self.num_pyarns=num_through
		self.pyarns=which_through
		self.r=red
		self.g=green
		self.b=blue
		
def main():
	args=parseArgs()
	image=Image.open(args.image_filename)
	image_matrix=np.asarray(image)
	image_matrix.shape
	image_grid=generateGrid(image_matrix.shape[0],image_matrix.shape[1],xscale=image_matrix.shape[0]/args.image_size,yscale=image_matrix.shape[0]/args.image_size,image_matrix=image_matrix)
	image_grid,yarns=generateDecisionYarns(args,image_grid,image_matrix)
	print getObjectiveFunction(yarns,image_matrix)
	   
if __name__ == "__main__":
	main()