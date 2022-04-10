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
    businesses = []

    # Manager
    manager = None

    # Economic stuff
    sum_money = 0
    sub_money = 0
    total_sum_money = []
    total_sub_money = []
    


    def __init__(self, money=0):
        self.money = money
        self.items = {}
        self.items_price = {}
        self.contracts_price = {}
        self.balance = [0,0,0]
        self.earnings = [0,0,0]
        self.businesses = []

        self.total_sum_money = []
        self.total_sub_money = []
    
    def __str__(self):
        return f"{self.money} {self.items}"
    
    def trade(self, product, price, sell, quantity):
        if not product in self.items:
            self.items[product] = 0
            self.items_price[product] = 1
        # Sell a product
        if sell and self.items[product] >= quantity:
            self.items[product] = round(self.items[product]-quantity,2)
            return Trade(self, price, sell, quantity, product)
        # Buy a product
        elif not sell and self.money >= price * quantity:
            ## self.money = round(self.money - (price * quantity),2)
            self.subtract_money(price * quantity)
            return Trade(self, price, sell, quantity, product)
        elif not sell and self.money >= price:
            buyable_ammount = 1
            while self.money >= price * (buyable_ammount + 1):
                buyable_ammount += 1
            ## self.money = round(self.money - (price * buyable_ammount),2)
            self.subtract_money(price * buyable_ammount)
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
    
    def add_item(self, item, quantity):
        if not item in self.items:
            self.items[item] = 0
        self.items[item] += quantity
    
    def subtract_item(self, item, quantity):
        # print("item: ", item, "quantity: ", quantity, "items: ", self.items)
        if item == None:
            return True
        if self.items[item] >= quantity:
            self.items[item] -= quantity
        else:
            print("No hay suficiente producto")
            return False
        return True

    def add_money(self, money):
        self.sum_money = round(self.sum_money + money,2)
        self.money = round(self.money +money,2)
    
    def subtract_money(self, money):
        if self.money >= money:
            self.sub_money = round(self.sub_money - money,2)
            self.money =round(self.money- money,2)
        else:
            print("No hay suficiente dinero")
            return False
        return True
    
    def tax(self, tax_rate):
        if self.balance[0] < 0:
            return 0
        # tax = round(self.balance[0] * tax_rate,2)
        tax = round(self.balance[0] * tax_rate,2)
        if tax <= 0:
            return 0
        if self.money >= tax:
            self.money = round(self.money - tax,2)
        else:
            tax = self.money
            self.money = 0
        return tax
    
    def subsidize(self, entity, money):
        if self.money < money:
            print("No hay suficiente dinero")
            return False
        self.money = round(self.money - money,2)
        entity.money = round(entity.money + money,2)
        return True
    
    def check_balance(self):
        if self.balance[-1] >= 0 and self.balance[-2] >= 0 and self.balance[-3] >= 0:
            return True
        return False
    
    def last_balance(self):
        return self.balance[-1]
    
    def add_balance(self):
        self.balance.append(self.earnings[-1] - self.earnings[-2])
        if len(self.balance) > 100:
            self.balance.pop(0)
    
    def add_earnings(self, earnings):
        self.earnings.append(earnings)
        if len(self.earnings) > 100:
            self.earnings.pop(0)

    def restart_economics(self):
        self.total_sum_money.append(self.sum_money)
        self.total_sub_money.append(self.sub_money * -1)

        
        self.sum_money = 0
        self.sub_money = 0