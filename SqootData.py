class SqootData(object):
    store_name=''
    store_address=''
    phone_number=''
    image_url=''
    discount_title=''
    expire_date=''
    orig_price=0
    discount_price=0
    fine_print=''
    main_url=''
    lat=0.0
    lng=0.0

    def __init__(self,store_name,store_add,phone_number,image_url,discount_title,expire_date,orig_price,discount_price,fine_print,main_url,lat,lng):
        self.store_name=store_name
        self.store_address=store_add
        self.phone_number=phone_number
        self.image_url=image_url
        self.discount_price=discount_price
        self.expire_date=expire_date
        self.discount_title=discount_title
        self.orig_price=orig_price
        self.fine_print=fine_print
        self.main_url=main_url
        self.lat=lat
        self.lng=lng
