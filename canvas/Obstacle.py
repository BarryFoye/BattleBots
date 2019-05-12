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
    
    
    def __init__(self):
        self.position = PVector(floor(random(120, 280)), floor(random(120, 280)))#120 and 280 means th food will fall within a border 120 pix insids the screen
        self.rotation = random(0, TWO_PI)
        self.bignessX = floor(random(20, 60))
        self.bignessY = floor(random(20, 60))
    
    def show(self):        
        pushMatrix();
        noStroke()
        fill(0, 200)
        translate(self.position.x, self.position.y)        
        rotate(self.rotation)
        rect(0, 0, self.bignessX, self.bignessY)
        popMatrix()
        stroke(255)
        ellipse(self.ax, self.ay, 2, 2)
        stroke(255, 0 , 0)
        ellipse(self.bx, self.by, 2, 2)
        stroke(0, 255, 0)
        ellipse(self.cx, self.cy, 2, 2)
        stroke(0, 0, 255)
        ellipse(self.dx, self.dy, 2, 2)
        #
        newx = self.ax * cos(self.rotation) - self.ay * sin(self.rotation)
        newy = self.ax * sin(self.rotation) + self.ay * cos(self.rotation)
        stroke(50, 50, 50)
        ellipse(newx, newy, 4, 4)
        line(self.ax, self.ay, newx, newy)
        print(dist(self.ax, self.ay, newx, newy))
        print(dist(self.ax, self.ay, self.bx, self.by))
        #
        #
        #
        #
        #
        
    
    def add_taboo(self):
        # calculate the area of the object
        area = self.bignessX * self.bignessY
        # calculate the position of each corner
        self.ax = self.position.x
        self.ay = self.position.y
        self.bx = self.ax + self.bignessX
        self.by = self.ay
        self.cx = self.ax
        self.cy = self.ay + self.bignessY
        self.dx = self.ax + self.bignessX
        self.dy = self.ay + self.bignessY
        print("bignessX & bignessY = {} {}".format(self.bignessX, self.bignessY))
        print("area = bignessX * bignessY = {}".format(area))
        print("ax = {}".format(self.ax))
        print("ay = {}".format(self.ay))
        print("bx = ax + self.bignessX = {}".format(self.bx))
        print("by = ay = {}".format(self.by))        
        print("cx = ax = {}".format(self.cx))
        print("cy = ay + self.bignessY = {}".format(self.cy))
        print("dx = ax + self.bignessX = {}".format(self.dx))
        print("dy = ay + self.bignessY = {}".format(self.dy))

        
