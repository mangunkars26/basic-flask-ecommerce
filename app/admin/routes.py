# app/admin/routes.py

from flask import render_template, redirect, url_for, flash, request
from app.admin import admin_bp
from app.admin.forms import ProductForm
from flask_login import login_required
from app import db  # Import db di sini
from app.models import Product  # Import Product di sini

# Menampilkan daftar produk
@admin_bp.route('/admin/products')
@login_required
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

# Tambah produk baru
@admin_bp.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data,
                          price=form.price.data, stock=form.stock.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.product_list'))
    return render_template('product_form.html', form=form)

# Edit produk
@admin_bp.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.product_list'))
    return render_template('product_form.html', form=form)

# Hapus produk
@admin_bp.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.product_list'))
