from  src.entity import Entity
from  src.person import Person

class Contract():
    entity1 = None
    entity2 = None

    money1 = 0
    money2 = 0

    item1 = None
    item2 = None

    item1_quantity = 0
    item2_quantity = 0

    time = 10
    fine = 100

    def __init__(self, entity1, entity2, money1, money2, item1, item2, item1_quantity, item2_quantity, time=10, fine=100):
        self.entity1 = entity1
        self.entity2 = entity2
        self.money1 = money1
        self.money2 = money2
        self.item1 = item1
        self.item2 = item2
        self.item1_quantity = item1_quantity
        self.item2_quantity = item2_quantity
        self.time = time
        self.fine = fine
    
    def __str__(self):
        return f"{self.entity2.name} in {self.entity1.name} for {self.money1} money and {self.time} years"
        # return f"Entity: {self.entity1.name} Money: {self.money1} Item: {self.item1} Quantity: {self.item1_quantity} \n     Entity: {self.entity2.name} Money: {self.money2} Item: {self.item2} Quantity: {self.item2_quantity} \n      Time: {self.time}"
    
    def fullfill(self):
        if self.time <= 0:
            return None
        if isinstance(self.entity1, Person):
            if self.entity1.dead:
                return None
        if isinstance(self.entity2, Person):
            if self.entity2.dead:
                return None
        
        part1 = False
        part2 = False
        part1a = False
        part1b = False
        part2a = False
        part2b = False

        # if self.item1
        part1a = self.entity1.subtract_item(self.item1, self.item1_quantity) 
        part1b = self.entity1.subtract_money(self.money1)

        part2a = self.entity2.subtract_item(self.item2, self.item2_quantity) 
        part2b = self.entity2.subtract_money(self.money2)

        #print("LAS PARTES: ", part1, part2)
        if part1a and part1b and part2a and part2b:
            # Dar el dinero y los items
            self.entity1.add_money(self.money2)
            self.entity1.add_item(self.item2, self.item2_quantity)
            self.entity2.add_money(self.money1)
            self.entity2.add_item(self.item1, self.item1_quantity)
            self.time -= 1
            if self.time <= 0:
                # if entity1 is person
                if isinstance(self.entity1, Person):
                    self.entity1.contract = None
                if isinstance(self.entity2, Person):
                    self.entity2.contract = None
                return None
            return self
            
        else:
            if not part1a and not part1b and not part2a and not part2b:
                # print("Contrato no cumplido por ambas partes")
                self.time = 0
                return None
            elif not part1a and not part1b:
                # print("Contrato no cumplido por la primera parte")
                # Devolver lo quitado a la segunda parte y cancelar el contrato
                self.entity2.add_item(self.item2, self.item2_quantity)
                self.entity2.add_money(self.money2)

                # Si primera parte puede pagar multa la paga
                if self.entity1.subtract_money(self.fine):
                    self.entity2.add_money(self.fine)
                self.time = 0
                return None
                # return Contract(self.entity2, self.entity1, 0, self.fine, None, None, 0, 0, 1, self.fine + self.fine/20)
            elif not part2a and not part2b:
                # print("Contrato no cumplido por la segunda parte")
                # Devolver lo quitado a la primera parte y cancelar el contrato
                self.entity1.add_item(self.item1, self.item1_quantity)
                self.entity1.add_money(self.money1)
                # Si segunda parte puede pagar multa la paga
                if self.entity2.subtract_money(self.fine):
                    self.entity1.add_money(self.fine)
                self.time = 0
                return None
                # return Contract(self.entity1, self.entity2, 0, self.fine, None, None, 0, 0, 1, self.fine + self.fine/20)
            else: return None
        self.time -= 1
        
        return None
    
    def check_if_done(self):
        if self.time <= 0:
            return True
        return False
    

