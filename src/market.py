from math import prod
import random

# from more_itertools import last


from  src.entity import Entity
from  src.trade import Trade

class MarketDatabase():

    traded_goods = []

    # For each good, the amount of money spent on buying and selling
    total_value = {}
    previous_value = {}

    

    # For each good, the average price of buying and selling
    average_price = {}
    previous_average_price = {}

    # For each good, the amount of goods bought and sold
    amount = {}
    previous_amount = {}

    # Data for the last 100 average price
    last_average_price = {}

    # Offer and demand of each product
    offer = {}
    demand = {}
    last_offer = {}
    last_demand = {}
    all_existing_goods = []

    def __init__(self):
        self.all_existing_goods = ["food", "build", "wood", "iron", "chocolate", "house", "furniture", "science", "medicament", "health", "good", "copper", "electricity", "oil", "gas", "engine"]

        self.traded_goods = []

        # For each good, the amount of money spent on buying and selling
        self.total_value = {}
        self.previous_value = {}

        

        # For each good, the average price of buying and selling
        self.average_price = {}
        self.previous_average_price = {}

        # For each good, the amount of goods bought and sold
        self.amount = {}
        self.previous_amount = {}

        # Data for the last 100 average price
        self.last_average_price = {}

        # Offer and demand of each product
        self.offer = {}
        self.demand = {}
        for good in self.all_existing_goods:
            self.offer[good] = []
            self.demand[good] = []
        
        # Buy and sell price of each product
        self.buy_price   = {}
        self.sell_price  = {}
        self.buy_prices  = {}
        self.sell_prices = {}

    def add_transaction(self, good, price, quantity):
        # Initialize the good if it is not in the database
        if good not in self.traded_goods:
            self.traded_goods.append(good)
            self.average_price[good] = 0
            self.amount[good]       = 0
            self.total_value[good]   = 0
        
        # Add the transaction to the database
        self.total_value[good] = round(self.total_value[good] + price * quantity,2)
        self.amount[good]     = round(self.amount[good] +quantity,2)

        # Calculate the average price (legacy)
        if self.amount[good] != 0:
            self.average_price[good] = round(self.total_value[good] / self.amount[good],2)

    
    # Funcion para obtener un sueldo orientativo teniendo en cuenta el precio de compra de
    # la comida, el chocolate, los bienes y la salud (si existen)
    def get_expected_salary(self):
        food_price = self.get_average_buy_price("food")
        chocolate_price = self.get_average_buy_price("chocolate")
        goods_price = self.get_average_buy_price("good")
        health_price = self.get_average_buy_price("health")

        expected = round((food_price + chocolate_price + goods_price + health_price) * 1.2,2)
        if expected < food_price * 2:
            expected = food_price * 2
        
        return expected
    
    def __srt__(self):
        return f"{self.traded_goods} value: {self.total_value} price: {self.average_price} amount: {self.amount}"
    
    def print_database(self):
        print(f"{self.traded_goods} value: {self.total_value} price: {self.average_price} amount: {self.amount}")
    
    def add_last_average_price(self):
        # If no sell or buy, the price the same as last
        for good in self.previous_amount:
            if not good in self.amount:
                self.total_value[good] = 0
                self.amount[good] = 0
                # self.average_price[good] = self.previous_average_price[good]
                



        for good in self.average_price:
            if good not in self.last_average_price:
                self.last_average_price[good] = []
            self.last_average_price[good].append(self.average_price[good])
            if len(self.last_average_price[good]) > 100:
                self.last_average_price[good].pop(0)
        
        self.previous_value = self.total_value.copy()
        self.previous_amount = self.amount.copy()
        self.previous_average_price = self.average_price.copy()

        self.total_value = {}
        self.amount = {}
        self.traded_goods = []
    
    def add_offer_demand(self, trades):
        # Initialize
        for p in self.all_existing_goods:
            self.offer[p].append(0)
            self.demand[p].append(0)
            self.buy_price[p] = 0
            self.sell_price[p] = 0
            if not p in self.buy_prices:
                self.buy_prices[p]  = []
                self.sell_prices[p] = []
        
        # Add the offer and demand
        for product in trades:
            buys = 0
            sells = 0
            for trade in trades[product]:
                if trade.sell:
                    self.offer[trade.product][-1] += trade.quantity
                    self.sell_price[trade.product] += trade.price * trade.quantity
                    sells += trade.quantity

                else:
                    self.demand[trade.product][-1] += trade.quantity
                    self.buy_price[trade.product] += trade.price * trade.quantity
                    buys += trade.quantity
            
            print("AAAAAAAAAAAAAAAAA", product, self.offer[product][-1], self.demand[product][-1])
            # Round the offer and demand
            self.offer[product][-1]   = round(self.offer[product][-1],2)
            self.demand[product][-1]  = round(self.demand[product][-1],2)
            self.last_offer[product]  = self.offer[product][-1]
            self.last_demand[product] = self.demand[product][-1]

            # Round the buy and sell price
            if sells != 0:
                self.sell_price[product] = round(self.sell_price[product] / sells,2)
                self.sell_prices[product].append(self.sell_price[product])
            if buys != 0:
                self.buy_price[product] = round(self.buy_price[product] / buys,2)
                self.buy_prices[product].append(self.buy_price[product])
        # print("********************************************************")
        # print(self.last_offer)
        # print(self.last_demand)
    
    def get_buy_price(self, product):
        if product in self.buy_price:
            return self.buy_price[product]
        else:
            return 0
    
    def get_sell_price(self, product):
        if product in self.sell_price:
            return self.sell_price[product]
        else:
            return 0

    def get_average_buy_price(self, product):
        if not product in self.buy_prices:
            return 1
        num = 5
        if len(self.buy_prices[product]) < num:
            num = len(self.buy_prices[product])
        if num == 0:
            return 5
        return round(sum(self.buy_prices[product][-num:]) / num,2)

    def get_average_sell_price(self, product):
        if not product in self.sell_prices:
            return 1
        num = 5
        if len(self.sell_prices[product]) < num:
            num = len(self.sell_prices[product])
        if num == 0:
            return 5
        return round(sum(self.sell_prices[product][-num:]) / num,2)
    
    def get_average_demand(self, product):
        if not product in self.demand:
            return 1
        num = 5
        if len(self.demand[product]) < num:
            num = len(self.demand[product])
        if num == 0:
            return 5
        return round(sum(self.demand[product][-num:]) / num,2)

    def get_average_offer(self, product):
        if not product in self.offer:
            return 1
        num = 5
        if len(self.offer[product]) < num:
            num = len(self.offer[product])
        if num == 0:
            return 5
        return round(sum(self.offer[product][-num:]) / num,2)

        
        




class Market(Entity):
    name = "Market"
    business = []
    people = []
    owner = None
    money = 0
    tax_rate = 0.1
    trades = {}
    products = {}
    database = MarketDatabase()

    def __init__(self, name, owner, money, tax_rate):
        self.name = name
        self.owner = owner
        self.money = money
        self.tax_rate = tax_rate
        self.trades = {}
        self.products = {}

    def __str__(self):
        return f"{self.name} has {len(self.business)} businesses and {len(self.people)} people"

    def add_business(self, business):
        self.business.append(business)

    def add_person(self, person):
        self.people.append(person)

    # Se puede añadir trade sin product aqui entonces feo pero weno
    def add_product(self, product, initial_price):
        self.products[product.name] = product.value

    def add_trade(self, trade):
        if not trade:
            return 0
        if not trade.product in self.trades:
            self.trades[trade.product] = []
        self.trades[trade.product].append(trade)

    def sort_trade(self, trade):
        return trade.price

    def clean_market(self):
        for product in self.trades:
            b = 0
            s = 0
            for t in self.trades[product]:
                if t.quantity > 0 and t.sell:
                    s += 1
                if t.quantity > 0 and not t.sell:
                    b += 1
            for trade in self.trades[product]:
                if trade.quantity > 0:
                    if trade.sell and s != 1: # and b != 0 and round(trade.price - (trade.price * 0.05))!=0: # Solo baja si había más compradores
                        trade.entity.items_price[trade.product] = round(trade.price - (trade.price * 0.1),2) # 0.05
                    elif trade.sell and s == 1: # Si es el único vendedor sube
                        trade.entity.items_price[trade.product] = round(trade.price + (trade.price * 0.1),2)
                    elif not trade.sell: # Solo sube si había más vendedores
                        trade.entity.items_price[trade.product] = round(trade.price + (trade.price * 1000),2) # Antes a 0.12 luego 0.5

                trade.cancel()
            self.trades[product] = []

    def sort_trade(self, trade):
        return trade.price

    # Function to make all trades on a free market
    def free_commerce(self):
        # Add info of offer and demand
        self.database.add_offer_demand(self.trades)

        free_comerce_data = ""
        # For each product on market
        for product in self.trades:
            # Get all buy trades on market
            buy_trades = []
            buy_amount = 0
            for trade in self.trades[product]:
                if not trade.sell:
                    buy_trades.append(trade)
                    buy_amount += trade.quantity
            # Get all sell trades on market
            sell_trades = []
            sell_amount = 0
            for trade in self.trades[product]:
                if trade.sell:
                    sell_trades.append(trade)
                    sell_amount += trade.quantity
            """
            ("RECURSO ", product)
            free_comerce_data = free_comerce_data + "===========================" + "\n"
            free_comerce_data = free_comerce_data + "COMPRAS" + "\n"
            free_comerce_data = free_comerce_data + "-------" + "\n"
            for t in buy_trades:
                free_comerce_data = free_comerce_data + str(t) + "\n"
            free_comerce_data = free_comerce_data + "VENTAS" + "\n"
            free_comerce_data = free_comerce_data + "-------" + "\n"
            for t in sell_trades:
                free_comerce_data = free_comerce_data + str(t) + "\n"
            """
            
            """
            # If more sells than buys buyer decide price
            if sell_amount > buy_amount:
                # Shuffle order of trades
                random.shuffle(buy_trades)
                # random.shuffle(sell_trades)
                sell_trades.sort(key=self.sort_trade)
            # If more buys than sells seller decide price
            elif buy_amount > sell_amount:
                # Shuffle order of trades
                random.shuffle(sell_trades)
                # random.shuffle(buy_trades)
                buy_trades.sort(key=self.sort_trade, reverse=True)
            # If equal amount of buys and sells
            else:
                # Shuffle order of trades
                random.shuffle(buy_trades)
                random.shuffle(sell_trades)
            """
            # Shuffle order of trades
            random.shuffle(buy_trades)
            # random.shuffle(sell_trades)
            sell_trades.sort(key=self.sort_trade)


            # Loop trough all the buy trades
            for trade in buy_trades:
                # Variable to check if the price has gone up
                price_up = False
                # Loop through all the sell trades
                for sell_trade in sell_trades:
                    # If the buy price is higher or equal than the sell price
                    if trade.price >= sell_trade.price:
                        # If the buy quantity is higher than the sell quantity
                        if trade.quantity > sell_trade.quantity:
                            # Buy the quantity of the sell trade
                            if not product in trade.entity.items:
                                trade.entity.items[product] = 0
                            trade.entity.items[product] = round(trade.entity.items[product] + sell_trade.quantity,2)
                            # Add transaction to the database
                            self.database.add_transaction(product, sell_trade.price, sell_trade.quantity)
                            # Add the transaction to the entity data
                            sell_trade.entity.last_amount_traded[product] += sell_trade.quantity
                            # Return the excess money to the buyer
                            ## trade.entity.money = round(trade.entity.money + (trade.price * sell_trade.quantity) - (sell_trade.price * sell_trade.quantity),2)
                            trade.entity.add_money((trade.price * sell_trade.quantity) - (sell_trade.price * sell_trade.quantity))
                            # Rest the quantity of the sell trade
                            trade.quantity = round(trade.quantity - sell_trade.quantity,2)
                            # Fullfill the sell trade
                            ## sell_trade.entity.money = round(sell_trade.entity.money + (sell_trade.price * sell_trade.quantity),2)
                            sell_trade.entity.add_money(sell_trade.price * sell_trade.quantity)
                            # Change the sell trade future price
                            sell_trade.entity.items_price[sell_trade.product] = round(sell_trade.price + (sell_trade.price * 0.3),2) # Antes 0.1

                            # Remove the sell trade
                            sell_trade.quantity = 0
                        # If the sell quantity is higher than the buy quantity
                        elif sell_trade.quantity > 0:
                            # Sell the quantity of the buy trade
                            
                            trade.entity.items[product] = round(trade.entity.items[product] + trade.quantity,2)
                            # Add transaction to the database
                            self.database.add_transaction(product, sell_trade.price, trade.quantity)
                            # Add the transaction to the entity data
                            sell_trade.entity.last_amount_traded[product] += trade.quantity
                            # Return the excess money to the buyer
                            ## trade.entity.money = round(trade.entity.money + (trade.price * trade.quantity) - (sell_trade.price * trade.quantity),2)
                            trade.entity.add_money((trade.price * trade.quantity) - (sell_trade.price * trade.quantity))
                            # Rest the quantity of the buy trade
                            sell_trade.quantity = round(sell_trade.quantity - trade.quantity,2)
                            # Fullfill the buy trade
                            ## sell_trade.entity.money = round(sell_trade.entity.money + (sell_trade.price * trade.quantity),2) 
                            sell_trade.entity.add_money(sell_trade.price * trade.quantity)
                            # Change the buy trade future price
                            """
                            if not price_up:
                                if round(trade.price - (trade.price * 0.05)) != 0:
                                    # print("Precio antes era ", trade.entity.items_price[trade.product])
                                    trade.entity.items_price[trade.product] = round(trade.price - (trade.price * 0.05),2) # antes 0.05
                                    # print("Pecio ahora es ", trade.entity.items_price[trade.product])
                                price_up = True
                            # Remove the buy trade
                            """
                            trade.quantity = 0
                            """
                            # If the sell trade quantity left is 0 change the sell trade price
                            if sell_trade.quantity == 0:
                                sell_trade.entity.items_price[sell_trade.product] = round(sell_trade.price + (sell_trade.price * 0.3),2) # Antes 0.1
                            # Go to next buy trade (break)
                            """
                            
                            break

                        if trade.quantity == 0:
                            break
                        # Else
                            # Buy the quantity of the sell trade
                            # Rest the quantity of the sell trade
                            # Fullfill the sell trade
                            # Change the sell trade future price
                            # Remove the sell trade
                            # FUllfill the buy trade
                            # Change the buy trade future price
                            # Remove the buy trade
                            # Go to next buy trade (break)
                    # If the sell price is higher than the buy price
                        # Check next sell trade
                
        self.clean_market()
        self.database.add_last_average_price()
        return free_comerce_data
                        
                

        
    
    def print_prices(self):
        for product in self.products:
            print(product, self.products[product])
                
            






    
