
from managers.manager import Manager

class JobMarketManager(Manager):
    job_market = None
    def __init__(self, job_market, world):
        super().__init__(job_market)
        self.job_market = job_market
        self.world = world

    def do(self):
        self.job_market.free_commerce()