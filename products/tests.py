from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name="Test Phone",
            weight=0.500,
            price=50000.00,
            description="A test product description"
        )
        self.assertEqual(product.name, "Test Phone")
        # Verify it is stored in the correct database via the router
        self.assertEqual(product._state.db, 'products_db')
