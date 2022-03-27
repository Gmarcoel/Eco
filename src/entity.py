from  src.trade import Trade
from  src.job import Job

class Entity():
    money = 0
    items = {}
    items_price = {}
    contracts_price = {}
    # Balance of the last 3 turns
    balance = [0,0,0]
    earnings = [0,0,0]
    


    def __init__(self, money=0):
        self.money = money
        self.items = {}
        self.items_price = {}
        self.contracts_price = {}
        self.balance = [0,0,0]
        self.earnings = [0,0,0]
    
    def __str__(self):
        return f"{self.money} {self.items}"
    
    def trade(self, product, price, sell, quantity):
        # Sell a product
        if sell and self.items[product] >= quantity:
            self.items[product] = round(self.items[product]-quantity,2)
            return Trade(self, price, sell, quantity, product)
        # Buy a product
        elif not sell and self.money >= price * quantity:
            self.money = round(self.money - (price * quantity),2)
            return Trade(self, price, sell, quantity, product)
        elif not sell and self.money >= price:
            buyable_ammount = 1
            while self.money >= price * (buyable_ammount + 1):
                buyable_ammount += 1
            self.money = round(self.money - (price * buyable_ammount),2)
            return Trade(self, price, sell, buyable_ammount, product)

        else:
            print("Trade went wrong")
            print("************************")
            print("Sell: ", sell, "Price: ", price, "Quantity: ", quantity, "Product: ", product)
            print("************************")

            return None
    
    def create_job(self, salary, time, specialization, contractor):
        return Job(self, salary, time, specialization, contractor)
    
    def pay_taxes(self, taxes):
        self.money = round(self.money - taxes,2)
    
    def get_expected_price(self, item):
        if not item in self.items_price:
            self.items_price[item] = 1 # ESTA FUNCION ENTERA ES BASURA
        return self.items_price[item]
    


    def add_money(self, money):
        self.money = round(self.money +money,2)
    
    def subtract_money(self, money):
        if self.money >= money:
            self.money =round(self.money- money,2)
        else:
            print("No hay suficiente dinero")
            return False
        return True
    
    def tax(self, tax_rate):
        tax = round(self.money * tax_rate,2)
        self.money = round(self.money - tax,2)
        return tax
    
    def subsidize(self, entity, money):
        if self.money < money:
            print("No hay suficiente dinero")
            return False
        self.money = round(self.money - money,2)
        entity.money = round(entity.money + money,2)
        return True
    
    def check_balance(self):
        if self.balance[0] >= 0 and self.balance[1] >= 0 and self.balance[2] >= 0:
            return True
        return False

