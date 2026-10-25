from flask import Blueprint, request, jsonify, render_template, redirect, url_for

from flask_login import current_user, login_required

from prometheus_client import Summary

from app.models import db, User, Cart, Order, Product

orders = Blueprint('orders', __name__)

ELAPSED_TIME= Summary('task_duration_seconds', 'Time spent creating order')

@orders.route('/checkout', methods=['POST'])

@login_required

@ELAPSED_TIME.time()

def checkout():

    with ELAPSED_TIME.time():

        # Check that cart is not empty

        cart = Cart.query.filter_by(user_id = current_user.id).all()

        total = sum(product.price*product.quantity for product in cart)

        # create order if price

        if total > 0:

            order = Order(

                    user_id = current_user.id,

                    total = total

            )

            db.session.add(order)

            for product in cart:

                # check the product stock is at least 1 before continuing order, throw error if there aren't enough of an item
            
                product_query = Product.query.filter_by(name = product.product_name).first()
        
                if (product_query.stock < 1):

                    # undo previous actions

                    db.session.rollback()

                    db.session.delete(product)

                    db.session.commit()

                    return jsonify({'error': 'Items out of stock will be deleted from cart; Order not submitted.'}), 401
            
                else:

                    # if there is stock, decrement product stock and then delete from cart 

                    product_query.stock -= product.quantity

                    db.session.delete(product)

            db.session.commit()

        return jsonify({'message': 'Order Created'}), 201

@orders.route('/api/orders', methods=['GET'])

@login_required

def get_orders():
   
    if current_user.is_authenticated:

        orders = Order.query.filter_by(user_id=current_user.id).all()

        return jsonify([{

            'order_id': o.order_id,

            'total': o.total,

            'order_time': o.order_time,

        } for o in orders])
    
    else:

        return jsonify({'error': 'Did not fetch orders'}), 401

@orders.route('/orders', methods=['GET'])

@login_required

def render_orders():

    orders = Order.query.filter_by(user_id=current_user.id).all()

    # user can only access orders if they have orders

    if (len(orders) > 0 and current_user.is_authenticated):

        return render_template('orders.html')
    else:

        return jsonify({'error': 'No orders found.'}), 401
