class Project():
    entity = None
    name = ""
    money = 0
    resources = {}
    time = 1
    owner = None

    def __init__(self, name="", entity=None, owner=None, money=0, resources={}, time=1):
        self.name = name
        self.entity = entity
        self.money = money
        self.resources = resources
        self.time = time

    def __str__(self):
        return f"Proyecto {self.name} Falta: Dinero {self.money}, recursos {self.resources}"

    def accomplish(self, entity):
        if entity.money >= self.money:
            entity.money = round(entity.money - self.money,2)
            self.money = 0
        completed = []
        for key in self.resources:
            if key not in entity.items:
                entity.items[key] = 0
            if entity.items[key] >= self.resources[key]:
                entity.items[key] -= self.resources[key]
                self.resources[key] = 0
                completed.append(key)

            else:
                self.resources[key] -= entity.items[key]
                entity.items[key] = 0
        # remove completed resources from the project
        for key in completed:
            del self.resources[key]
        if not self.resources and self.money == 0:
            return True
        return False