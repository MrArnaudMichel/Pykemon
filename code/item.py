class Item:
    def __init__(self, name: str, type: str, description: str, value: int):
        self.name = name
        self.type = type
        self.description = description
        self.value = value

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_description(self):
        return self.description

    def get_value(self):
        return self.value

    def __str__(self):
        return f"{self.name}\n=====\n{self.description}\nValue: {self.value}"
