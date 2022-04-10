
class Trade:
    entity = None
    price = 0
    sell = False
    quantity = 0
    product = None

    def __init__(self, entity, price, sell, quantity, product):
        self.entity = entity
        self.price = price
        self.sell = sell
        self.quantity = quantity
        self.product = product
    
    def __str__(self):
        return f"Nombre: {self.entity.name} Precio {self.price} Venta:{self.sell} Cantidad:{self.quantity} Producto: {self.product}"
    
    def get_price(self):
        return self.price
    
    def get_quantity(self):
        return self.quantity
    
    def get_product(self):
        return self.product
    
    def get_entity(self):
        return self.entity
    
    def get_sell(self):
        return self.sell
    
    def cancel(self):
        if self.sell:
            self.entity.items[self.product] += self.quantity
        else:
            ## self.entity.money = round(self.entity.money + self.price * self.quantity ,2)
            self.entity.add_money(self.price * self.quantity)
        return True
