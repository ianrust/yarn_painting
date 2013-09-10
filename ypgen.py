import itertools,sys,argparse,math

def parseArgs():
    parser=argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-s','--size',nargs=2,dest='size',help='size in meters of the canvas [height,width]',default = [1.0,2.0],type=float)
    parser.add_argument('-i','--img','--image',dest='image_filename',help='image file to be yarn-paint-processed')
    parser.add_argument('-is','--imsize',nargs=2,dest='image_size',default=[0.5,1.0],help='size of image in meters [vertical,horizontal]')
    parser.add_argument('-r','--resolution',nargs=2,dest='res',default=[50,100],help='resolution in pixels of yarn image reconstruction[vertical,horizontal]')
    parser.add_argument('-p','--pegs',nargs=2,dest='pegs',help='number of pegs on each edge [vertical,horizontal]',default = [100,100],type=int)
    parser.add_argument('-d','--disp',dest='disp',help='should we display the processed image?',default=False,action='store_true')
    parser.add_argument('-o','--out','--outimage',dest='out_image_filename',help='image file to be saved as')
    args= parser.parse_args()
    return args

def generateDecisionYarns(args,image_grid):
    peg_grid=generateGrid(args.pegs[0],args.pegs[1],xscale=args.size[1]/args.pegs[1],yscale=args.size[0]/args.pegs[0],edges=True)
    peg_combos=itertools.combinations(peg_grid,2)
    yarns = [yarn(combo[0],combo[1],1) for combo in peg_combos]
    i=0
    for yarner in yarns:
        image_grid=yarner.setContributingPoints(dist=(args.image_size[0]/args.res[1]+args.image_size[1]/args.res[1]),grid=image_grid)
        i=i+1
        # print i/float(len(yarns))
        # print str(yarner.start)+','+str(yarner.finish)
    for pixel in image_grid:
		print pixel.num_pyarns
    return image_grid,yarns

def generateGrid(verticalSteps,horizontalSteps,xscale=1,yscale=1,edges=False):
    return_grid=[]
    for x in range(horizontalSteps):
        for y in range(verticalSteps):
            if not edges or (x == 0 or x == horizontalSteps-1 or y == 0 or y == verticalSteps-1):
                return_grid.append(pixel(x*xscale,y*yscale,0,[])) # xpos,ypos, num strings going through,array of yarns going through
    return return_grid

def getPerpDistance(point,start,end):
    Dp=start.x-end.x
    Dq=start.y-end.y
    distance = math.fabs(Dq*point.x-Dp*point.y+start.x*end.y-start.y*end.x)/math.sqrt(Dp**2+Dq**2)
    return distance

class yarn():
    def __init__(self,start,finish,num_channels):
        self.start=start
        self.finish=finish
        self.channels=[]
        for a in range(num_channels):
            self.channels.append(True)
    def setContributingPoints(self,dist,grid):
        self.cont_points=[]
        i=0
		#make this the one that gives index
        for point in grid:
            if getPerpDistance(point,self.start,self.finish)<=dist:
                self.cont_points.append((point,getPerpDistance(point,self.start,self.finish)))
                point.num_pyarns=point.num_pyarns+1
                point.pyarns.append(self)
            i=i+1		
	return grid

class pixel():
	def __init__(self,x,y,num_through,which_through):
		self.x=x
		self.y=y
		self.num_pyarns=num_through
		self.pyarns=which_through
		
def main():
    args=parseArgs()
    image_grid=generateGrid(args.res[0],args.res[1],xscale=args.image_size[1]/args.res[1],yscale=args.image_size[0]/args.res[0])
    image_grid,yarns=generateDecisionYarns(args,image_grid)
	   
if __name__ == "__main__":
    main()