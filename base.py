class Base:
    @property
    def left(self):
        return self.pos.x

    @property
    def right(self):
        return self.pos.x + self.size.x

    @property
    def bottom(self):
        return self.pos.y + self.size.y

    @property
    def top(self):
        return self.pos.y

    @property
    def center(self):
        return self.pos + (self.size*0.5)
