from flask import Blueprint, request, jsonify, render_template

from flask_login import login_required, current_user

from app.models import db, Product, Order

products = Blueprint('products', __name__)

@products.route('/api/products', methods=['GET'])

def get_products():

    all_products = Product.query.all()

    return jsonify([{

        'id': p.id,

        'name': p.name,

        'description': p.description,

        'price': p.price,

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
   
    
    for key, value in data.items():

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

@products.route('/orders', methods=['POST'])

@login_required

def new_order():
    data = request.get_json()

    product_id = data.get('product_id')

    quantity = int(data.get('quantity', 1))

    product = Product.query.get_or_404(product_id)

    total = product.price*quantity
    
    order_item = Order(
        user_id = current_user.id,
        
        product_name = product.name,
                
        price = product.price,
                
        quantity = quantity, 
                
        total = total
    )
    
    db.session.add(order_item)

    db.session.add(product)

    db.session.commit()

    return jsonify(
    {
        'id': order_item.id,
        'total': total
    })
