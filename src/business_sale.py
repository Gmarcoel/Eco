# Business sale

class Sale: # Business
    entity = None
    price = 0
    sell = False
    business = None
    sector = "None"

    def __init__(self, entity, price, sell, business, sector):
        self.entity = entity
        self.price = price
        self.sell = sell
        self.business = business
        self.sector = sector
    
    def __str__(self):
        return f"Nombre: {self.entity.name} Precio {self.price} Venta:{self.sell} Sector: {self.sector}"
    

