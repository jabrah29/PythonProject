class ProductData(object):
    name=None
    rating=None
    distance=None
    imageUrl=None
    deals=None
    address=''
    lat=0.0
    lng=0.0
    price_difference=None
    id=''



    def __init__(self, pName,rating,distance,iUrl, deals, address,lat,lng,id):
        self.name=pName
        self.rating=rating
        self.distance=distance
        self.imageUrl=iUrl
        self.price_difference=0
        self.deals=deals
        self.address=address
        self.id=id
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
            'id':self.id
        }

    def set_differences(self,result):
        self.price_difference=result


class Deals(object):
    title=''
    descrip=''
    original_price=''
    new_price=''
    purchase_url=''
    orig_price_calculation=0
    dis_price_calculation=0


    def __init__(self, title, orginal_price, new_price, descrip,o_p_c, d_p_c):
        self.title=title
        self.original_price=orginal_price
        self.new_price=new_price
        self.descrip=descrip
        self.orig_price_calculation=o_p_c
        self.dis_price_calculation=d_p_c

    def serialize(self):
        return {
            'title': self.title,
            'original_price': self.original_price,
            'new_price': self.new_price,
            'descrip': self.descrip,
        }





