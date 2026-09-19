
from app.repositories.product_repository import (
    get_products as repository_get_products,
    get_product as repository_get_product,
    create_product as repository_create_product,
    update_product as repository_update_product,
    delete_product as repository_delete_product

    )

def get_product(id):
    return repository_get_product(id)


def create_product(name, price, stock):
    return repository_create_product(
        name=name,
        price=price,
        stock=stock
    )

def update_product(product, name, price, stock):
    return repository_update_product(product, name, price, stock)


def delete_product(product):
    return repository_delete_product(product)

def get_products(
    search=None,
    sort="id",
    min_price=None,
    max_price=None,
    min_stock=None,
    max_stock=None,
    page=1,
    per_page=10
    ):

    return repository_get_products(
        search=search,
        sort=sort,
        min_price=min_price,
        max_price=max_price,
        min_stock=min_stock,
        max_stock=max_stock,
        page=page,
        per_page=per_page
    )

