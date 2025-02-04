from xxlimited import new
from  src.entity import Entity
from  src.business_sale import Sale
import random

class BusinessMarket(Entity):
    name = "sale Market"
    business = []
    people = []
    owner = None
    money = 0
    tax_rate = 0.1
    sales = {}
    sectors = {} # Esto aún hay que implementarlo
    # database = MarketDatabase()
    total_sales_price = 0
    total_sales_amount = 0
    average_sales_price = 1

    def __init__(self, name, owner, money, tax_rate):
        self.name = name
        self.owner = owner
        self.money = money
        self.tax_rate = tax_rate
        self.sales = {}
        self.sectors = {}

    def __str__(self):
        return f"{self.name} has {len(self.business)} businesses and {len(self.people)} people"

    def add_business(self, business):
        self.business.append(business)

    def add_person(self, person):
        self.people.append(person)

    # Sin uso
    # def add_sector(self, sector):
    #     self.sectors[sector.name] = sector.value

    def add_sale(self, sale):
        if not sale:
            return 0
        if not sale.sector in self.sales:
            self.sales[sale.sector] = []
        self.sales[sale.sector].append(sale)

    def sort_sale(self, sale):
        return sale.price

    def clean_market(self):
        """
        for sector in self.sales:
            for sale in self.sales[sector]:
                if sale.sell:
                    sale.entity.sales_price[sector] = round(sale.entity.sales_price[sector] + sale.entity.sales_price[sector]* 0.1,2)
                else:
                    if not "food" in sale.entity.items_price:
                        sale.entity.items_price["food"] = 1
                    if sale.entity.sales_price[sector] >= 2 * sale.entity.items_price["food"]:
                        sale.entity.sales_price[sector] = round(sale.entity.sales_price[sector] - sale.entity.sales_price[sector]* 0.1,2)
        """
        self.sales = {}


    def sort_sale(self, sale):
        return sale.price

    # Function to make all sales on a free market
    def free_commerce(self):
        self.total_sales_price = 0
        self.total_sales_amount = 0

        # For each sector on market
        for sector in self.sales:
            # Get all buy sales on market
            sell_sales = []
            for sale in self.sales[sector]:
                if sale.sell:
                    sell_sales.append(sale)
            # Get all sell sales on market
            buy_sales = []
            for sale in self.sales[sector]:
                if not sale.sell:
                    buy_sales.append(sale)
            # If more sells than buys, buys decide the price
            if len(sell_sales) > len(buy_sales):
                sell_sales.sort(key=self.sort_sale, reverse=True)
                random.shuffle(buy_sales)
            # If more buys than sells sells decide the price
            elif len(buy_sales) > len(sell_sales):
                # Shuffle order of sales
                random.shuffle(sell_sales)
                # random.shuffle(buy_sales)
                buy_sales.sort(key=self.sort_sale)
            # If same number of sells and buys
            else:
                # Shuffle order of sales
                random.shuffle(sell_sales)
                random.shuffle(buy_sales)
            
            # Print
            """
            print(f"Sector: {sector}")
            print("     Sell: ")
            for s in sell_sales:
                print(f"        {s.entity.name} vende {s.business.name} a {s.price}")
                print("     ////")
            print("     Buy: ")
            for s in buy_sales:
                print(f"        {s.entity.name} compra {s.sector} a {s.price}")
            print("______________________________")
            """

            # Loop trough all the buy sales
            for sale in sell_sales:
                # Loop through all the sell sales
                for buy_sale in buy_sales:
                    found = False

                    # If the buy money is higher or equal than the sell money
                    if sale.price >= buy_sale.price and buy_sale.price != 0:
                        """
                        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                        print("Sale: ", sale)
                        """

                        # Fill database data
                        self.total_sales_price += sale.price
                        self.total_sales_amount += 1

                        # Change ownership
                        old_owner = sale.business.owner
                        new_owner = buy_sale.entity
                        sale.business.owner = new_owner
                        if old_owner != None:
                            old_owner.businesses.remove(sale.business)
                        new_owner.businesses.append(sale.business)

                        # Open and add investment
                        sale.business.status = "open"
                        sale.business.active = True
                        old_owner.add_money(sale.business.money)
                        # print("LEGADO : ", sale.business.money)
                        sale.business.money = new_owner.investment_pool
                        # print("NUEVO: ", new_owner.investment_pool)
                        new_owner.investment_pool = 0
                        

                        # Set sale to 0 so it doesn't show again
                        sale.price = 0
                        buy_sale.price = 0

                        # Remove the sale from the market
                        self.sales[sector].remove(sale)
                        self.sales[sector].remove(buy_sale)

                        # Change sale price 
                        # sale.entity.sales_price[sector] = round(sale.entity.sales_price[sector] - sale.entity.sales_price[sector]* 0.05,2)
                        # buy_sale.entity.sales_price[sector] = round(buy_sale.entity.sales_price[sector] + buy_sale.entity.sales_price[sector]* 0.05,2)
                        break


                        
        
        if self.total_sales_amount != 0:
            self.average_sales_price = round(self.total_sales_price / self.total_sales_amount,2)
        self.clean_market()

