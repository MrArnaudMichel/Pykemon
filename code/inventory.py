from item import Item


class Inventory:
    def __init__(self):
        self.items: dict[Item, int] = {}

    def getItemFromType(self, type: str) -> list[Item]:
        return [item for item in self.items if item.get_type() == type]

    def addItem(self, item: Item, quantity: int = 1):
        for key in self.items.keys():
            if key.name == item.name:
                self.items[key] += quantity
                return
        self.items[item] = quantity


    def removeItem(self, item: Item, quantity: int = 1):
        for key in self.items.keys():
            if key.name == item.name:
                self.items[key] -= quantity
                if self.items[key] <= 0:
                    self.items.pop(key)
                return

    def __str__(self):
        return "\n".join([f"{item} ({quantity})" for item, quantity in self.items.items()])