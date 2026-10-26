from flask import Blueprint, request, jsonify, render_template

from flask_login import login_required, current_user

from sqlalchemy import func

from app.models import db, Product, Cart

products = Blueprint('products', __name__)

@products.route('/api/products', methods=['GET'])

def get_products():

    all_products = Product.query.all()

    return jsonify([{

        'id': p.id,

        'name': p.name,

        'description': p.description,

        'price': f"{p.price:.2f}",

        'stock': p.stock,

        'image_url': p.image_url

    } for p in all_products])

@products.route('/products_display',methods=['GET'])
def render_products():
  return render_template('products.html')

@products.route('/products', methods=['POST'])
@login_required

def create_product():

    data = request.get_json()

    product = Product(

        name=data['name'],

        description=data['description'],

        price=data['price'],

        stock=data['stock'],

        image_url=data.get('image_url')

    )

    db.session.add(product)

    db.session.commit()

    return jsonify({'message': 'Product created'}), 201

@products.route('/products/<int:id>', methods=['PUT'])

@login_required

def update_product(id):
    
    product = Product.query.get_or_404(id)

    data = request.get_json()
   
    # check that price and stock are numbers before update

    for key, value in data.items():
        
        if value:

            if 'price' in data:

                price_val = data['price']

                # take out $ if in price
        
                if "$" in price_val: 
                    
                    price_val = price_val.split("$")[1]
       
                try:

                    product.price = round(float(price_val), 2)
                    
                    if product.price < 0:

                        return jsonify({'error': 'Negative Price Not Allowed'}), 401
                
                except:

                    return jsonify({'error': 'Invalid Price'}), 400

            if 'stock' in data:

                try:

                    product.stock = int(data['stock'])

                    if product.stock < 0:

                        return jsonify({'error': 'Negative Stock Not Allowed'}), 401

                except:

                    return jsonify({'error': 'Invalid Stock'}), 400

            setattr(product, key, value)
    
    db.session.commit()

    return jsonify({'message': 'Product updated'})

@products.route('/products/<int:id>', methods=['DELETE'])

@login_required

def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)

    db.session.commit()

    return jsonify({'message': 'Product deleted'})

@products.route('/carts', methods=['POST'])

@login_required

def new_product_order():
    
    data = request.get_json()

    product_id = data.get('product_id')

    quantity = int(data.get('quantity', 1))

    product = Product.query.get_or_404(product_id)

    # sum up amount of item already in user cart  and check that new order won't exceed stock before adding to cart

    cart_product_amount = db.session.query(func.sum(Cart.quantity)).filter_by(user_id = current_user.id, product_name = product.name).scalar() or 0;

    if cart_product_amount + quantity > product.stock:
    
        return jsonify({'error':'Items in cart exceed stock; not added'}), 401

    cart_item = Cart(

        user_id = current_user.id,
        
        product_name = product.name,
                
        price = product.price,
                
        quantity = quantity, 
    )
    
    db.session.add(cart_item)

    db.session.add(product)

    db.session.commit()

    # user only able to add to cart if signed-in

    if current_user.is_authenticated:
        return  jsonify({'id': cart_item.id,})
    else:
        return jsonify({'error':'Register or Sign-in first'}), 401
