
from managers.manager import Manager

class MarketManager(Manager):
    market = None
    def __init__(self, market, world):
        super().__init__(market)
        self.market = market
        self.world = world

        self.market.manager = self

    def do(self):
        self.market.free_commerce()