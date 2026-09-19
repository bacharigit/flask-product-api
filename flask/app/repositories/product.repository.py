from app.models import Product
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

