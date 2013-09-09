import itertools,sys,argparse,math



def parseArgs():
    parser=argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-s','--size',nargs=2,dest='size',help='size in meters of the canvas [height,width]',default = [1.0,2.0],type=float)
    parser.add_argument('-i','--img','--image',dest='image_filename',help='image file to be yarn-paint-processed')
    parser.add_argument('-p','--pegs',nargs=2,dest='pegs',help='number of pegs on each edge [vertical,horizontal]',default = [100,100],type=int)
    parser.add_argument('-d','--disp',dest='disp',help='should we display the processed image?',default=False,action='store_true')
    parser.add_argument('-o','--out','--outimage',dest='out_image_filename',help='image file to be saved as')
    args= parser.parse_args()
    return args

def generateDecisionYarns(args,image_grid):
    peg_grid=generateGrid(args.pegs[0],args.pegs[1],xscale=args.size[0]/args.pegs[0],yscale=args.size[0]/args.pegs[1],edges=True)
    peg_combos=itertools.combinations(peg_grid,2)
    yarns = [yarn(combo[0],combo[1]) for combo in peg_combos]
    for yarner in yarns:
        yarner.setContributingPoints(dist=1.0,grid=image_grid)
        print str(yarner.start)+','+str(yarner.finish)+'x'+str(yarner.cont_points)

def generateGrid(verticalSteps,horizontalSteps,xscale=1,yscale=1,edges=False):
    return_grid=[]
    for x in range(horizontalSteps):
        for y in range(verticalSteps):
            if not edges or (x == 0 or x == horizontalSteps-1 or y == 0 or y == verticalSteps):
                return_grid.append((x*xscale,y*yscale))
    return return_grid

def getPerpDistance(point,start,end):
    Dp=start[0]-end[0]
    Dq=start[1]-end[1]
    distance = math.fabs(Dq*point[0]-Dp*point[1]+start[0]*end[1]-start[1]*end[0])/math.sqrt(Dp**2+Dq**2)
    return distance

class yarn():
    def __init__(self,start,finish):
        self.start=start
        self.finish=finish
    def setContributingPoints(self,dist,grid) :
        self.cont_points=[]
        for point in grid:
            if getPerpDistance(point,self.start,self.finish)<=dist:
                self.cont_points.append((point,getPerpDistance(point,self.start,self.finish)))
def main():
    args=parseArgs()
    image_grid=generateGrid(args.pegs[0],args.pegs[1],xscale=args.size[0]/args.pegs[0],yscale=args.size[0]/args.pegs[1])
    generateDecisionYarns(args,image_grid)
    
    

if __name__ == "__main__":
    main()
