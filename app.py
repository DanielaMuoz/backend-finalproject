from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    idproduct = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(144), unique=False)
    price = db.Column(db.Integer)

    def __init__(self, product_name, description,price):
        self.product_name = product_name
        self.description = description
        self.price = price


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_name', 'description','price')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

 
# Endpoint to create a new product
@app.route('/product', methods=["POST"])
def add_product():
    product_name = request.json['product_name']
    description = request.json['description']

    new_product = Product(product_name, description)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.idproduct)
    return "product saved"


@app.route('/store-products', methods=["POST"])
def product():
    lista=[{"product_name": "lila","description": "purple","price":5},{"product_name": "water","description": "water","price":10},{"product_name": "soda","description": "sosa","price":10}]
    for product in lista:
        product_name=product['product_name']
        description = product['description']
        price = product['price']
        new_product = Product(product_name, description,price)
        db.session.add(new_product)
        db.session.commit()

    return "products saved"

# Endpoint to query all products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)


# Endpoint for querying a single product
@app.route("/product/<idproduct>", methods=["GET"])
def get_product(idproduct):
    product = Product.query.get(idproduct)
    return product_schema.jsonify(product)

def read_product(idproduct):
    try:
        product = db(idproduct)
        if product != None:
            return jsonify({'product': product, 'Message': "Product found.", 'successful': True})
        else:
            return jsonify({'Message': "Product not found.", 'successful': False})
    except Exception as ex:
        return jsonify({'Message': "Error", 'successful': False})

# Endpoint for updating a product
@app.route("/product/<idproduct>", methods=["PUT"])
def product_update(idproduct):
    product = Product.query.get(idproduct)
    product_name = request.json['product_name']
    description = request.json['description']
    price = request.json['price']


    product.product_name = product_name
    product.description = description
    price.description = price

    db.session.commit()
    return product_schema.jsonify(product)


# Endpoint for deleting a record
@app.route("/product/<idproduct>", methods=["DELETE"])
def product_delete(idproduct):
    product = Product.query.get(idproduct)
    db.session.delete(product)
    db.session.commit()

    return "Product was successfully deleted"
  

  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    carts = db.relationship('Cart', backref='user', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password 
 
class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

  



#obtenemos email y passsword del body 
#validamos que el email y password coincidadn en la base da tos
#si es correcto regresar en un json al nombre del usaurio y su id
#si no es corecta regresar un error de credenciales

#we get email and password from the body
# we validate that the email and password match in the database
#if it is correct to return in a json to the name of the user and his id
#if it is not correct return a credential error 
@app.route('/login', methods=["POST"])
def read_login_db(id):
    try:
        cursor = app.config.connection.cursor()
        sql = "SELECT id, email, password FROM user WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            user = {'id': data[0], 'email': data[1], 'password': data[2]}
            return user
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/login/<id>', methods=['POST'])
def read_login(id):
    try:
        user = read_login_db(id)
        if user != None:
            return jsonify({'user': product, 'Message': "User found.", 'successful': True})
        else:
            return jsonify({'Message': "User not found.", 'successful': False})
    except Exception as ex:
        return jsonify({'Message': "Error", 'successful': False})









# Endpoint to create a new user
@app.route('/user', methods=["POST"])
def add_user():
    email = request.json['email']
    password = request.json['password']

    new_user = User(email, password)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)
    return "user saved"


@app.route('/store-users', methods=["POST"])
def product():
    lista=[{"email": "hola@hotmail.com","password": "1234"}]
    for user in lista:
        email=user['email']
        password = user['password']
        
        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()

    return "users saved"

# Endpoint to query all products
@app.route("/user", methods=["GET"])
def get_products():
    all_products = User.query.all()
    result = users_schema.dump(all_products)
    return jsonify(result.data)


# Endpoint for querying a single product
@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

def read_user(id):
    try:
        user = db(id)
        if user != None:
            return jsonify({'user': user, 'Message': "Product found.", 'successful': True})
        else:
            return jsonify({'Message': "Product not found.", 'successful': False})
    except Exception as ex:
        return jsonify({'Message': "Error", 'successful': False})

# Endpoint for updating a product
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    email = request.json['email']
    password = request.json['password']

    user.email = email
    user.password = password

    db.session.commit()
    return user_schema.jsonify(user)


# Endpoint for deleting a record
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return "User was successfully deleted"
  
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    taxes = db.Column(db.Integer)
    subtotal = db.Column(db.Integer)
    total = db.Column(db.Integer)
    product= db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, quantity,taxes,subtotal,total):
            self.quantity = quantity 
            self.taxes = taxes 
            self.subtotal = subtotal
            self.total = total
 
class CartSchema(ma.Schema):
    class Meta:
        fields = ('quantity','taxes','subtotal','total')


cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

  
# Endpoint to create a new buy
@app.route('/cart', methods=["POST"])
def add_cart():
    quantity = request.json['quantity']
    taxes = request.json['taxes']
    subtotal = request.json['subtotal']
    total = request.json['total']

    new_cart = Cart(quantity,taxes,subtotal, total)

    db.session.add(new_cart)
    db.session.commit()

    cart = Cart.query.get(new_cart.id)
    return "cart saved"


@app.route('/store-cart', methods=["POST"])
def cart():
    lista=[{"quantity": "2","taxes": "0.50","subtotal": "10","total": "10.50"},{"quantity": "1","taxes": "0.50","subtotal": "10","total": "10.50"},{"quantity": "3","taxes": "1","subtotal": "30","total": "31"}]
    for cart in lista:
        quantity=cart['quantity']
        taxes = cart['taxes']
        subtotal = cart['subtotal']
        total = cart['total']
        
        new_cart = Cart(quantity, taxes, subtotal, total)
        db.session.add(new_cart)
        db.session.commit()

    return "cart saved"

# Endpoint to query all buyes
@app.route("/cart", methods=["GET"])
def get_carts():
    all_carts = Cart.query.all()
    result = carts_schema.dump(all_carts)
    return jsonify(result.data)


# Endpoint for querying a single cart
@app.route("/cart/<id>", methods=["GET"])
def get_cart(id):
    cart = Cart.query.get(id)
    return cart_schema.jsonify(cart)

def read_cart(id):
    try:
        cart = db(id)
        if cart != None:
            return jsonify({'user': cart, 'Message': "Product found.", 'successful': True})
        else:
            return jsonify({'Message': "Product not found.", 'successful': False})
    except Exception as ex:
        return jsonify({'Message': "Error", 'successful': False})

# Endpoint for updating a product
@app.route("/cart/<id>", methods=["PUT"])
def cart_update(id):
    cart = Cart.query.get(id)
    quantity = request.json['quantity']
    taxes = request.json['taxes']
    subtotal = request.json['subtotal']
    total = request.json['total']

    cart.quanity = quantity
    cart.taxes = taxes
    cart.subtotal = subtotal
    cart.total = total

    db.session.commit()
    return cart_schema.jsonify(cart)


# Endpoint for deleting a record
@app.route("/cart/<id>", methods=["DELETE"])
def cart_delete(id):
    cart = Cart.query.get(id)
    db.session.delete(cart)
    db.session.commit()

    return "Cart was successfully deleted"
 
def page_not_found():
    return "<h1>Page not found</h1>", 404
 
if __name__ == '__main__': 
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)

