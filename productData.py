class ProductData(object):
    productName=None
    storeName=None
    price=0
    description=None
    url=None
    imageUrl=None

    def __init__(self, pName,sName,prodPrice,descrip,prodUrl,iUrl):
        self.productName=pName
        self.storeName=sName
        self.price=prodPrice
        self.description=descrip
        self.url=prodUrl
        self.imageUrl=iUrl



