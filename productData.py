class ProductData(object):
    name=None
    rating=None
    distance=None
    imageUrl=None
    deals=None
    address=''
    lat=0.0
    lng=0.0

    def __init__(self, pName,rating,distance,iUrl, deals, address,lat,lng):
        self.name=pName
        self.rating=rating
        self.distance=distance
        self.imageUrl=iUrl
        self.deals=deals
        self.address=address
        self.lat=lat
        self.lng=lng

    def serialize(self):
        return {
            'name': self.name,
            'rating': self.rating,
            'distance': self.distance,
            'imageUrl': self.imageUrl,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng,
            'deals': self.deals,
        }


class Deals(ProductData):
    title=''
    descrip=''
    original_price=''
    new_price=''
    purchase_url=''


    def __init__(self, title, orginal_price, new_price, descrip):
        self.title=title
        self.original_price=orginal_price
        self.new_price=new_price
        self.descrip=descrip

    def serialize(self):
        return {
            'title': self.title,
            'original_price': self.original_price,
            'new_price': self.new_price,
            'descrip': self.descrip,
        }


