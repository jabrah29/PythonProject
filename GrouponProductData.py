class GrouponProductData(object):
    shortAnnouncementTitle=''
    end_date=''
    sold_out=None
    store_name=''
    descrip=''
    discount_price=0.0
    price_string=''
    url=''
    lat=0.0
    lng=0.0


    def __init__(self, shortTitle,end_date,sold_out,store_name,descrip,lat,lng,discount_price,price_string,url):
        self.shortAnnouncementTitle=shortTitle
        self.end_date=end_date;
        self.sold_out=sold_out
        self.store_name=store_name
        self.descrip=descrip
        self.lat=lat
        self.lng=lng
        self.discount_price=discount_price
        self.price_string=price_string
        self.url=url
