
from managers.manager import Manager

class BusinessMarketManager(Manager):
    business_market = None
    def __init__(self, business_market, world):
        super().__init__(business_market)
        self.business_market = business_market
        self.world = world

        self.business_market.manager = self

    def do(self):
        self.business_market.free_commerce()