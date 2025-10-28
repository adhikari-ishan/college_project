from store.models import Product

class Cart():
    def __init__(self,request):
        self.session = request.session

        #getting current session if exists
        cart = self.session.get('session_key')

        # new user than there is no session key 
        if 'session_key' not in request.session:
            cart = self.session ['session_key'] = { }

        self.cart = cart #making available in all pages

    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)    

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
    
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #getting ids from cart 
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities 
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        #updating cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True