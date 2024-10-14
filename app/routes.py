from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for)
from flask_login import login_required, current_user
from .models import (Product,
                     Cart,
                     Order,
                     OrderItem)


main = Blueprint('main', __name__)

@main.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@main.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=current_user.id, product_id=product.id, quantity=1)
        db.session.add(new_cart_item)
    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/cart')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

@main.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return redirect(url_for('main.home'))
    order = Order(user_id=current_user.id, total=0)
    db.session.add(order)
    total_price = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, price=product.price)
        total_price += product.price * item.quantity
        db.session.add(order_item)
        db.session.delete(item)  # Remove item from cart after checkout
    order.total = total_price
    db.session.commit()
    return redirect(url_for('main.home'))
