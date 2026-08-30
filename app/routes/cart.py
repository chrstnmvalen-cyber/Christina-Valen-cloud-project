from flask import Blueprint, request, jsonify, render_template

from flask_login import login_required, current_user

from app.models import db, Order

cart = Blueprint('cart', __name__)

@cart.route('/api/cart', methods=['GET'])

@login_required

def get_cart():

    cart_summary = Order.query.filter_by(user_id=current_user.id).all()

    order_total = round(sum(c.total for c in cart_summary),2)

    return jsonify({
       'info':[{

          'id': c.id,

          'user': c.user_id,

          'product_name': c.product_name,

          'price': c.price,

          'quantity': c.quantity,

          'total': c.total

       } for c in cart_summary], 'order_total' : order_total
})

@cart.route('/shopping_cart',methods=['GET'])

@login_required

def render_cart():

  return render_template('shopping_cart.html')
