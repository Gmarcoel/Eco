
class New():
    object = None
    city = None
    market = None
    job_market = None
    business_market = None

    def __init__(self, object, city, market, job_market, business_market = None):
        self.object = object
        self.city = city
        self.market = market
        self.job_market = job_market
        self.business_market = business_market