from app.models import Product
from app.extensions import db
from app.errors.exceptions import InvalidSortFieldError

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


    query = Product.query

    if search:
        query = query.filter(
            Product.name.like(f"%{search}%")
        )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if min_stock is not None:
        query = query.filter(Product.stock >= min_stock)

    if max_stock is not None:
        query = query.filter(Product.stock <= max_stock)

    sort_fields = {
        "id": Product.id,
        "name": Product.name,
        "price": Product.price,
        "stock": Product.stock
    }

    descending = sort.startswith("-")
    field_name = sort[1:] if descending else sort


    if field_name not in sort_fields:
        raise InvalidSortFieldError("Invalid sort field")

    field = sort_fields[field_name]

    if descending:
        query = query.order_by(field.desc())
    else:
        query = query.order_by(field.asc())


    total = query.count()

    offset = (page - 1) * per_page

    products = (
        query
        .limit(per_page)
        .offset(offset)
        .all()
    )

    return products, total


def get_product(id):
    return db.session.get(Product, id)


def create_product(name, price, stock):
    new_product = Product(
        name=name,
        price=price,
        stock=stock
    )

    db.session.add(new_product)
    db.session.commit()

    return new_product



def update_product(product, name, price, stock):
    product.name = name
    product.price = price
    product.stock = stock

    db.session.commit()

    return product



def delete_product(product):
    db.session.delete(product)
    db.session.commit()



