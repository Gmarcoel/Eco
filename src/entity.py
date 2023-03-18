from  src.trade import Trade
from  src.job import Job

class Entity():

    def __init__(self, money=0):
        self.money = 0
        self.items = {}
        self.items_price = {}
        self.contracts_price = {}
        # Balance of the last 3 turns
        self.balance = [0,0,0]
        self.earnings = [0,0,0]
        self.businesses = []
        # Manager
        self.manager = None
        # Economic stuff
        self.sum_money = 0
        self.sub_money = 0
        self.total_sum_money = []
        self.total_sub_money = []
        self.investment_pool = 0
        self.last_ammount_traded = {}
        self.subsidized = False
        self.subsidizing = {}
        self.active = True
        self.money = money
        self.items = {}
        self.items_price = {}
        self.contracts_price = {}
        self.balance = [0,0,0]
        self.earnings = [0,0,0]
        self.businesses = []

        self.total_sum_money = []
        self.total_sub_money = []
        self.last_ammount_traded = {}
    
    def __str__(self):
        return f"{self.money} {self.items}"
    
    def trade(self, product, price, sell, quantity):
        # self.last_ammount_traded[product] = 0
        if not product in self.last_ammount_traded:
            self.last_ammount_traded[product] = 0

        if not product in self.items:
            self.items[product] = 0
            self.items_price[product] = 1
        # Sell a product
        if sell and self.items[product] >= quantity:
            self.items[product] = round(self.items[product]-quantity,2)
            return Trade(self, price, sell, quantity, product)
        # Buy a product
        elif not sell and self.money >= price * quantity:
            self.subtract_money(price * quantity)
            return Trade(self, price, sell, quantity, product)
        elif not sell and self.money >= price:
            buyable_ammount = 1
            while self.money >= price * (buyable_ammount + 1):
                self.subtract_money(price * buyable_ammount)
            return Trade(self, price, sell, buyable_ammount, product)

        else:
            # print("Trade went wrong")
            # print("************************")
            # print("Sell: ", sell, "Price: ", price, "Quantity: ", quantity, "Product: ", product)
            # print("************************")

            return None
    
    def create_job(self, salary, time, specialization, contractor):
        return Job(self, salary, time, specialization, contractor)
    
    def pay_taxes(self, taxes):
        self.subtract_money(taxes)
    
    def get_expected_price(self, item):
        if not item in self.items_price:
            self.items_price[item] = 1 # ESTA FUNCION ENTERA ES BASURA
        if self.items_price[item] <= 0:
            self.items_price[item] = 0.2
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
            # print("No hay suficiente producto")
            return False
        return True

    def add_money(self, money):
        self.sum_money = round(self.sum_money + money,2)
        self.money = round(self.money + money,2)
    
    def subtract_money(self, money):
        if self.money >= money:
            self.sub_money = round(self.sub_money + money,2)
            self.money = round(self.money - money,2)
        else:
            # print("No hay suficiente dinero")
            return False
        return True
    
    def tax(self, tax_rate):
        tax = round(self.balance[-1] * tax_rate,2)
        if tax > 10000: print("                ", self.money, tax_rate, self.balance[-1], tax)
        if tax <= 0:
            return 0
        if self.money >= tax:
            self.subtract_money(tax)
        else:
            tax = self.money
            self.money = 0
        return tax
    
    def subsidize(self, entity, money):
        entity.subsidized = True
        self.subsidizing[entity] = money
    
    def unsubsidize(self, entity):
        entity.subsidized = False
        del self.subsidizing[entity]


    def pay_subsidies(self):
        aux = {}
        for entity in self.subsidizing:
            if not entity.active:
                entity.subsidized = False
                continue
            if self.money >= self.subsidizing[entity]:
                self.subtract_money(self.subsidizing[entity])
                entity.add_money(self.subsidizing[entity])
            else:
                self.subsidizing[entity] = round(self.subsidizing[entity] - self.money,2)
                self.money = 0
            aux[entity] = self.subsidizing[entity]
        self.subsidizing = aux
        
    def pay_subsidy(self, entity):
        if self.money >= self.subsidizing[entity]:
                self.subtract_money(self.subsidizing[entity])
                entity.add_money(self.subsidizing[entity])
                del self.subsidizing[entity]
        else:
            self.subsidizing[entity] = round(self.subsidizing[entity] - self.money,2)
            self.money = 0

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
        if self.total_sum_money == []:
            self.total_sum_money.append(0)
            self.total_sub_money.append(0)
        else:
            self.total_sum_money.append(self.sum_money)
            self.total_sub_money.append(self.sub_money)
        self.sum_money = 0
        self.sub_money = 0


        for price in self.items_price:
            if self.items_price[price] < 0.1:
                self.items_price[price] = 0.2
