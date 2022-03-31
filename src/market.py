from math import prod
import random


from  src.entity import Entity
from  src.trade import Trade

class MarketDatabase():

    traded_goods = []

    # For each good, the ammount of money spent on buying and selling
    total_value = {}
    

    # For each good, the average price of buying and selling
    average_price = {}

    # For each good, the ammount of goods bought and sold
    ammount = {}

    def __init__(self):
        pass

    def add_transaction(self, good, price, quantity):
        if good not in self.traded_goods:
            self.traded_goods.append(good)
            self.average_price[good] = 0
            self.ammount[good] = 0
            self.total_value[good] = 0
        
        self.total_value[good] = round(self.total_value[good] + price * quantity,2)
        self.ammount[good] = round(self.ammount[good] +quantity,2)
        if self.ammount[good] != 0:
            self.average_price[good] = round(self.total_value[good] / self.ammount[good],2)
    
    def __srt__(self):
        return f"{self.traded_goods} value: {self.total_value} price: {self.average_price} ammount: {self.ammount}"
    
    def print_database(self):
        print(f"{self.traded_goods} value: {self.total_value} price: {self.average_price} ammount: {self.ammount}")



class Market():
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
                if t.quantity >0 and t.sell:
                    s += 1
                if t.quantity >0 and not t.sell:
                    
                    b += 1
            for trade in self.trades[product]:
                if trade.quantity > 0:
                    if trade.sell: # and b != 0 and round(trade.price - (trade.price * 0.05))!=0: # Solo baja si había más compradores
                        trade.entity.items_price[trade.product] = round(trade.price - (trade.price * 0.05),2)
                    elif trade.sell and s == 1: # Si es el único vendedor sube
                        trade.entity.items_price[trade.product] = round(trade.price + (trade.price * 0.05),2)
                    elif not trade.sell: # Solo sube si había más vendedores
                        trade.entity.items_price[trade.product] = round(trade.price + (trade.price * 0.05),2)

                trade.cancel()
            self.trades[product] = []


    # Function to make all trades on a free market
    def free_commerce(self):
        # For each product on market
        for product in self.trades:
            # Get all buy trades on market
            buy_trades = []
            for trade in self.trades[product]:
                if not trade.sell:
                    buy_trades.append(trade)
            # Get all sell trades on market
            sell_trades = []
            for trade in self.trades[product]:
                if trade.sell:
                    sell_trades.append(trade)
            print("RECURSO ", product)
            print("===========================")
            print("COMPRAS")
            print("-------")
            for t in buy_trades:
                print(t)
            print("VENTAS")
            print("------")
            for t in sell_trades:
                print(t)
            

            # Shuffle order of trades
            random.shuffle(buy_trades)
            random.shuffle(sell_trades)
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
                            # Return the excess money to the buyer
                            trade.entity.money = round(trade.entity.money + (trade.price * sell_trade.quantity) - (sell_trade.price * sell_trade.quantity),2)
                            # Rest the quantity of the sell trade
                            trade.quantity = round(trade.quantity - sell_trade.quantity,2)
                            # Fullfill the sell trade
                            sell_trade.entity.money = round(sell_trade.entity.money + (sell_trade.price * sell_trade.quantity),2)
                            # Change the sell trade future price
                            sell_trade.entity.items_price[sell_trade.product] = round(sell_trade.price + (sell_trade.price * 0.05),2)
                            # Remove the sell trade
                            sell_trade.quantity = 0
                        # If the sell quantity is higher than the buy quantity
                        elif sell_trade.quantity > 0:
                            # Sell the quantity of the buy trade
                            trade.entity.items[product] = round(trade.entity.items[product] + trade.quantity,2)
                            # Add transaction to the database
                            self.database.add_transaction(product, sell_trade.price, trade.quantity)
                            # Return the excess money to the buyer
                            trade.entity.money = round(trade.entity.money + (trade.price * trade.quantity) - (sell_trade.price * trade.quantity),2)
                            # Rest the quantity of the buy trade
                            sell_trade.quantity = round(sell_trade.quantity - trade.quantity,2)
                            # Fullfill the buy trade
                            sell_trade.entity.money = round(sell_trade.entity.money + (sell_trade.price * trade.quantity),2) 
                            # Change the buy trade future price
                            if not price_up:
                                if round(trade.price - (trade.price * 0.05)) != 0:
                                    # print("Precio antes era ", trade.entity.items_price[trade.product])
                                    trade.entity.items_price[trade.product] = round(trade.price - (trade.price * 0.05),2)
                                    # print("Pecio ahora es ", trade.entity.items_price[trade.product])
                                price_up = True
                            # Remove the buy trade
                            trade.quantity = 0
                            # If the sell trade quantity left is 0 change the sell trade price
                            if sell_trade.quantity == 0:
                                sell_trade.entity.items_price[sell_trade.product] = round(sell_trade.price + (sell_trade.price * 0.05),2)
                            # Go to next buy trade (break)
                            
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
                        
                

        
    
    def print_prices(self):
        for product in self.products:
            print(product, self.products[product])
                
            






    
