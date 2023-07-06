from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices
from django.conf import settings

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)

class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
    def test_create_product(self):
        response = self.client.post(reverse("shopapp:product_create"),
        {"name": self.product_name, "price": "123.45", "description": "new table", "discount": "10"})
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())

class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(reverse("shopapp:product_details", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_chack_content(self):
        response = self.client.get(reverse("shopapp:product_details", kwargs={"pk": self.product.pk}))
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):
    fixtures = [
        "products-fixtures.json",
    ]
    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')

class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="user_test", password="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.LOGIN_URL, response.url)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user_test", password="qwerty")
        perm_view_order = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(perm_view_order)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="ul Vishnevaya, d 12",
            promocode="SALE555",
            user=self.user,
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_details", kwargs={"pk": self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["order"].pk, self.order.pk)

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "products-fixtures.json",
        "user-fixtures.json",
        "groups-fixtures.json",
    ]
    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products_export"))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data)

class OrdersExportTestCase(TestCase):
    fixtures = [
        "orders-fixtures.json",
        "products-fixtures.json",
        "user-fixtures.json",
        "groups-fixtures.json",
    ]
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user_test", password="qwerty", is_staff=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_export"))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "id": order.id,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": {
                    "id": order.user.pk,
                    "username": order.user.username,
                    "is_staff": order.user.is_staff,
                },
                "products": [
                    {
                        "id": product.pk,
                        "name": product.name,
                        "price": str(product.price),
                        "archived": product.archived,
                    }
                    for product in order.products.all()
                ],
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data["orders"], expected_data)
