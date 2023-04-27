from item import Item


class Inventory:
    def __init__(self):
        self.items: dict[Item, int] = {}

    def getItemFromType(self, type: str) -> list[Item]:
        return [item for item in self.items if item.get_type() == type]

    def addItem(self, item: Item, quantity: int = 1):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def removeItem(self, item: Item, quantity: int = 1):
        if item in self.items:
            self.items[item] -= quantity
            if self.items[item] <= 0:
                del self.items[item]

    def __str__(self):
        return "\n".join([f"{item} ({quantity})" for item, quantity in self.items.items()])