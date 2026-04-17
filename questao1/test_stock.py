import unittest
from stock import count_low_stock_products


class TestCountLowStockProducts(unittest.TestCase):

    def test_one_product_below_limit(self):
        products = [('Shampoo', 10), ('Condicionador', 5), ('Sabonete', 2)]
        result = count_low_stock_products(products)
        self.assertEqual(result, 1)

    def test_multiple_products_below_limit(self):
        products = [('A', 1), ('B', 2), ('C', 10)]
        result = count_low_stock_products(products)
        self.assertEqual(result, 2)

    def test_no_products_below_limit(self):
        products = [('A', 5), ('B', 10)]
        result = count_low_stock_products(products)
        self.assertEqual(result, 0)

    def test_empty_list(self):
        result = count_low_stock_products([])
        self.assertEqual(result, 0)

    def test_negative_quantity_should_raise_error(self):
        products = [('A', -1)]
        with self.assertRaises(ValueError):
            count_low_stock_products(products)

    def test_invalid_tuple_format(self):
        products = [('A', 1, 2)]
        with self.assertRaises(ValueError):
            count_low_stock_products(products)

    def test_invalid_type_quantity(self):
        products = [('A', 'invalid')]
        with self.assertRaises(TypeError):
            count_low_stock_products(products)


if __name__ == '__main__':
    unittest.main()