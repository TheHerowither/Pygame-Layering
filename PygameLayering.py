import pygame as pg




class Vector2:
    def __init__(self, x : float, y : float):
        self.x, self.y = x, y
    def __repr__(self) -> tuple:
        return self._
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
class Vector3:
    def __init__(self, x : float, y : float, z : float):
        self.x, self.y, self.z = x, y, z
    def __repr__(self):
        return (self.x, self.y, self.z)
    def __str__(self):
        return f"Vector2({self.x}, {self.y}, {self.z})"
class Circle:
    def __init__(self, center : Vector2, radius : float):
        self.center = center
        self.radiusf = radius
        self.radius = round(radius)
    def __str__(self):
        return f"Circle(center = {self.center} adius = {self.radiusf})"

class LayeredEntity:
    def __init__(self, object_to_layer, object_type : str, color : Vector3, draw_layer : int, window : pg.Surface):
        self.color = color.x, color.y, color.z
        self.layered_object = object_to_layer
        self._draw_layer = draw_layer
        self._app = window
        self._type = object_type
    def draw(self):
        if self._type != "circle":
            exec(f"pg.draw.{self._type}(self._app, self.color, self.layered_object)")
        else:
            pg.draw.circle(self._app, self.color, (self.layered_object.center.x, self.layered_object.center.y), self.layered_object.radius)


class DrawQueue:
    def __init__(self, background_color : Vector3):
        self._queue = []
        self._sorted = self._queue
        self._bg = background_color
        
    def append(self, entity : LayeredEntity):
        self._queue.append(entity)
    def remove(self, entity : LayeredEntity):
        try: self._queue.pop(self._queue.index(entity))
        except ValueError: print(entity, "is not in queue anymore")
    def add(self, entity : LayeredEntity): self.append(entity) 
    def rm(self, entity : LayeredEntity): self.remove(entity)
    def draw_frame(self):
        self._queue[0]._app.fill((self._bg.x, self._bg.y, self._bg.z))
        self._sorted = self._queue
        for i in range(1, len(self._queue)):
            temp = self._queue[i]
            j = i-1
            while j >=0 and temp._draw_layer < self._queue[j]._draw_layer :
                    self._sorted[j+1] = self._queue[j]
                    j -= 1
            self._sorted[j+1] = temp
        for to_be_drawn in self._sorted:
            to_be_drawn.draw()
        pg.display.flip()



if __name__ == "__main__":
    app = pg.display.set_mode((1080,720))


    queue = DrawQueue(Vector3(0,0,0))

    test_entity = LayeredEntity(pg.Rect((150,100), (100,100)), "rect", Vector3(255,255,255), 0, app)
    queue.append(test_entity)
    c = Circle(Vector2(150,150), 50)
    test_entity1 = LayeredEntity(c, "circle", Vector3(0,255,255), 1, app)
    queue.append(test_entity1)

    running = True
    while running:
        queue.draw_frame()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    if test_entity._draw_layer == 1:
                        test_entity._draw_layer = 0
                    else:
                        test_entity._draw_layer = 1
                    
                    if test_entity1._draw_layer == 1:
                        test_entity1._draw_layer = 0
                    else:
                        test_entity1._draw_layer = 1
                if event.key == pg.K_d:
                    queue.remove(test_entity)
                if event.key == pg.K_a:
                    queue.append(test_entity)