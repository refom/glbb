
import math

class Vector2D:
    def __init__(self, x_or_pair, y=None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
        
        self.xy = (self.x, self.y)
    
    def __str__(self):
        return f"Vector2D: ({self.x}, {self.y})"
    
    def __add__(self, vec_B):
        return Vector2D(self.x + vec_B.x, self.y + vec_B.y)
    
    def __sub__(self, vec_B):
        return Vector2D(self.x - vec_B.x, self.y - vec_B.y)

    def __mul__(self, scale):
        return Vector2D(self.x * scale, self.y * scale)
    def __div__(self, scale):
        return Vector2D(self.x / scale, self.y / scale)
    

    def rotate(self, angle_degrees, sameVector=False):
        angle_radians = math.radians(angle_degrees)
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)

        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos

        if sameVector:
            self.x = x
            self.y = y
            self.xy = (self.x, self.y)
        else:
            return Vector2D(x, y)


