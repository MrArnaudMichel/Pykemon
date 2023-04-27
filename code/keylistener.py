class KeyListener:
    def __init__(self):
        self.pressed = []

    def key_pressed(self, key):
        if key in self.pressed:
            return True
        return False
    def addkey(self, key):
        self.pressed.append(key)

    def removekey(self, key):
        self.pressed.remove(key)

    def get(self):
        return self.pressed

    def clear(self):
        self.pressed.clear()

    def exist(self):
        if len(self.pressed) > 0:
            return True
        return False
