from enum import unique
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)
  
 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Endpoint for deleting a record
@app.route("/", methods=["GET","POST"])
def home():
    return "API DANIELA"
# Endpoint to create a new product
@app.route('/product/add', methods=["POST"])
def add_product():
    name = request.json['name'] 
    price = request.json['price']

    record = Product(name,price) 

    db.session.add(record)
    db.session.commit()
 
    return jsonify(product_schema.dump(record)) 

# Endpoint to query all products
@app.route("/products", methods=["GET"])
def get_allproducts():
    all_products = Product.query.all()
    return jsonify(products_schema.dump(all_products))
 

# Endpoint for querying a single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

def read_product(id):
    try:
        product = db(id)
        if product != None:
            return jsonify({'product': product, 'Message': "Product found.", 'successful': True})
        else:
            return jsonify({'Message': "Product not found.", 'successful': False})
    except Exception as ex:
        return jsonify({'Message': "Error", 'successful': False})


# Endpoint for updating a guide
@app.route("/product/<id>", methods=["PUT"])
def product_update(id):
    product = Product.query.get(id)
    name = request.json['name']
    price = request.json['price']

    name = name
    product.price = price

    db.session.commit()
    return product_schema.jsonify(product)

 
# Endpoint for deleting a record
@app.route("/product/<id>", methods=["DELETE"])
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return "Product was successfully deleted"
  
'''
 we get email and password from the body
 we validate that the email and password match in the database
 if it is correct to return in a json to the name of the user and his id
 if it is not correct return a credential error 
'''
  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(50), nullable=False)
    carts = db.relationship('Cart', backref='user', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password 
 
class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Endpoint query login
@app.route('/login', methods=["POST"])
def read_user():
    email = request.json['email'] 
    query = "SELECT * FROM user WHERE email = '{0}' ".format(email)
    results = db.session.execute(query)

   
    if results :
        return  jsonify({"user_data":users_schema.dump(results)}) 

    else :
        return jsonify({'Message': "User not found.", 'successful': False})

 
# Endpoint to create a new user
@app.route('/user/add', methods=["POST"])
def add_user():
    name = request.json['name'] 
    email = request.json['email'] 
    password = request.json['password']

    record = User(name,email,password) 

    db.session.add(record)
    db.session.commit()
 
    return jsonify(user_schema.dump(record)) 

# Endpoint to create a new user
@app.route('/user', methods=["GET"])
def user():
    all=User.query.all()
    return jsonify(users_schema.dump(all)) 
 

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
@app.route('/cart/add', methods=["POST"])
def add_cart():
    quantity = request.json['quantity']
    taxes = request.json['taxes']
    subtotal = request.json['subtotal']
    total = request.json['total']

    new_cart = Cart(quantity,taxes,subtotal, total)

    db.session.add(new_cart)
    db.session.commit()
 
    return jsonify(cart_schema.dump(new_cart)) 
 
 
def read_cart(id):
    try:
        cart = db(id)
        if cart != None:
            return jsonify({'cart': cart, 'Message': "Cart found.", 'successful': True})
        else:
            return jsonify({'Message': "Cart not found.", 'successful': False})
    except Exception as ex:
        return jsonify({'Message': "Error", 'successful': False})

# Endpoint for updating a product
@app.route("/cart/update/<id>", methods=["PUT"])
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
@app.route("/cart/delete/<id>", methods=["DELETE"])
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

