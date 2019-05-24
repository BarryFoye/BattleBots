class Obstacle:
    position = 0
    rotation = 0
    bignessX = 0
    bignessY = 0
    
    ax = 0
    ay = 0
    bx = 0
    by = 0
    cx = 0
    cy = 0
    dx = 0
    dy = 0
    coordsX = []
    coordsY = []
    oddNodes = False
    
    def __init__(self):
        #self.position = PVector(floor(random(120, 280)), floor(random(120, 280)))#120 and 280 means th food will fall within a border 120 pix insids the screen
        self.position = PVector(200, 200)
        self.rotation = random(0, TWO_PI)
        self.bignessX = floor(random(20, 60))
        self.bignessY = floor(random(20, 60))
        
    
    def show(self):        
        pushMatrix()
        noStroke()
        fill(240, 240)
        translate(self.position.x, self.position.y)        
        rotate(self.rotation)
        rect(0, 0, self.bignessX, self.bignessY)
        popMatrix()
        # stroke(0)
        # ellipse(self.ax, self.ay, 2, 2)
        # stroke(255, 0 , 0)
        # ellipse(self.bx, self.by, 2, 2)
        # stroke(0, 255, 0)
        # ellipse(self.cx, self.cy, 2, 2)
        # stroke(0, 0, 255)
        # ellipse(self.dx, self.dy, 2, 2)
        stroke(50, 50, 50)
        line(self.ax, self.ay, self.bx, self.by)
        line(self.ax, self.ay, self.cx, self.cy)
        line(self.cx, self.cy, self.dx, self.dy)
        line(self.dx, self.dy, self.bx, self.by)
        
    
    def hitbox(self): 
        self.ax = self.position.x  
        self.ay = self.position.y
        self.bx = self.ax + self.bignessX
        self.by = self.ay
        self.cx = self.ax
        self.cy = self.ay + self.bignessY
        self.dx = self.ax + self.bignessX
        self.dy = self.ay + self.bignessY 
        #calculate the rotation
        self.bx = self.bx - self.ax
        self.by = self.by - self.ay
        newx = self.bx * cos(self.rotation) - self.by * sin(self.rotation)
        newy = self.by * cos(self.rotation) + self.bx * sin(self.rotation)
        self.bx = newx + self.ax
        self.by = newy + self.ay
        
        self.cx = self.cx - self.ax
        self.cy = self.cy - self.ay
        newx = self.cx * cos(self.rotation) - self.cy * sin(self.rotation)
        newy = self.cy * cos(self.rotation) + self.cx * sin(self.rotation)
        self.cx = newx + self.ax
        self.cy = newy + self.ay
        
        self.dx = self.dx - self.ax
        self.dy = self.dy - self.ay
        newx = self.dx * cos(self.rotation) - self.dy * sin(self.rotation)
        newy = self.dy * cos(self.rotation) + self.dx * sin(self.rotation)
        self.dx = newx + self.ax
        self.dy = newy + self.ay
        self.coordsX.append(self.ax)
        self.coordsY.append(self.ay)
        self.coordsX.append(self.bx)
        self.coordsY.append(self.by)
        self.coordsX.append(self.cx)
        self.coordsY.append(self.cy)
        self.coordsX.append(self.dx)
        self.coordsY.append(self.dy)
        

    def isTouching(self, posX, posY):        
        j=3
        self.oddNodes = False
        for i in range(0, j):
            #print("self.coordsY[i] = {} posY = {} self.coordsY[j] = {}").format(self.coordsY[i], posY, self.coordsY[j])
            if(self.coordsY[i] < posY and self.coordsY[j] >= posY or self.coordsY[j] < posY and self.coordsY[i] >= posY):
                #print("self.coordsX[i] = {} (posY - self.coordsY[i])/(self.coordsY[j] - self.coordsY[i] - self.coordsX[i])  = {} posX = {}").format(self.coordsX[i], (posY - self.coordsY[i])/(self.coordsY[j] - self.coordsY[i] - self.coordsX[i]), posX)
                if(self.coordsX[i] + (posY - self.coordsY[i])/(self.coordsY[j] - self.coordsY[i] - self.coordsX[i]) < posX):                         
                    self.oddNodes = not(self.oddNodes)
                pass
            pass
            j=i
            #print(j)    
        return self.oddNodes
