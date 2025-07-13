class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'name': product.name,
                'price': float(product.price),    
                'image': product.image_url,
                'quantity': int(quantity),         
            }
        self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        return self.cart.items()

    def get_total(self):
        return sum(
            float(item['price']) * int(item['quantity']) for item in self.cart.values()
        )

    def get_count(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()
