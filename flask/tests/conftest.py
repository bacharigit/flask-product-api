import pytest

from main import create_app
from config import TestingConfig
from models import db, Product


@pytest.fixture
def app():
    return create_app(TestingConfig)


@pytest.fixture
def client(app):
    return app.test_client()



@pytest.fixture
def product(app):
    with app.app_context():
        product=Product(
            name="Test Product",
            price=100,
            stock=10
        )

        db.session.add(product)
        db.session.commit()
        yield product



@pytest.fixture
def products(app):
    with app.app_context():
        products = [
            Product(name="Product 1", price=100, stock=10),
            Product(name="Product 2", price=200, stock=20),
            Product(name="Product 3", price=300, stock=30),
            Product(name="Product 4", price=400, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()

        return products


@pytest.fixture(autouse=True)
def clean_products(app):
   yield


   with app.app_context():
        Product.query.delete()
        db.session.commit()


