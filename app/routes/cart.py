from flask import Blueprint, request, jsonify, render_template

from flask_login import login_required, current_user

from app.models import db, Cart, User, Product

cart = Blueprint('cart', __name__)

@cart.route('/api/cart', methods=['GET'])

@login_required

def get_cart():

    cart = Cart.query.filter_by(user_id=current_user.id).all()

    cart_arr = []

    for c in cart:

       product = Product.query.filter_by(name=c.product_name).first()
        
       cart_arr.append({

          'id': c.id,

          'user': c.user_id,

          'product_name': c.product_name,

          'price': product.price,

          'quantity': c.quantity,

       })

    return jsonify({'info': cart_arr})

@cart.route('/shopping_cart',methods=['GET'])

@login_required

def render_cart():

    return render_template('shopping_cart.html')

@cart.route('/api/cart/<int:id>', methods=['DELETE'])

@login_required

def delete_item(id):

    try:
        
        product = Cart.query.get_or_404(id)

        db.session.delete(product)
    
        db.session.commit()

        return jsonify({'message': 'item deleted'})
    
    except:

        return jsonify({'error': 'item not deleted'})
