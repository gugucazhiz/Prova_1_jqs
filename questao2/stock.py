import unittest
from sales import calculate_product_sales_percentage


class TestCalculateProductSalesPercentage(unittest.TestCase):

    # =========================
    # ✅ CENÁRIOS DE SUCESSO
    # =========================

    def test_should_calculate_percentage_with_missing_products(self):
        # Arrange
        sales = [(1, 1, 4), (1, 2, 3), (1, 3, 1), (2, 1, 3)]
        all_products = [1, 2, 3, 4]

        # Act
        result = calculate_product_sales_percentage(sales, all_products)

        # Assert
        expected = [
            (1, 0.6364),
            (2, 0.2727),
            (3, 0.0909),
            (4, 0.0)
        ]
        self.assertEqual(result, expected)

    def test_should_return_all_zero_when_no_sales(self):
        sales = []
        all_products = [1, 2, 3]

        result = calculate_product_sales_percentage(sales, all_products)

        expected = [
            (1, 0.0),
            (2, 0.0),
            (3, 0.0)
        ]
        self.assertEqual(result, expected)

    def test_should_handle_single_product(self):
        sales = [(1, 1, 10)]
        all_products = [1]

        result = calculate_product_sales_percentage(sales, all_products)

        expected = [(1, 1.0)]
        self.assertEqual(result, expected)

    def test_should_aggregate_multiple_sales_same_product(self):
        sales = [(1, 1, 2), (2, 1, 3), (3, 1, 5)]
        all_products = [1]

        result = calculate_product_sales_percentage(sales, all_products)

        expected = [(1, 1.0)]
        self.assertEqual(result, expected)

    def test_should_return_sorted_desc(self):
        sales = [(1, 1, 1), (1, 2, 5), (1, 3, 3)]
        all_products = [1, 2, 3]

        result = calculate_product_sales_percentage(sales, all_products)

        expected = [
            (2, 0.5556),
            (3, 0.3333),
            (1, 0.1111)
        ]
        self.assertEqual(result, expected)

    # =========================
    # ❌ CENÁRIOS DE FALHA
    # =========================

    def test_should_raise_error_when_quantity_negative(self):
        sales = [(1, 1, -5)]
        all_products = [1]

        with self.assertRaises(ValueError):
            calculate_product_sales_percentage(sales, all_products)

    def test_should_raise_error_invalid_tuple(self):
        sales = [(1, 1)]  # inválido
        all_products = [1]

        with self.assertRaises(ValueError):
            calculate_product_sales_percentage(sales, all_products)

    def test_should_raise_error_invalid_type(self):
        sales = [(1, "produto", 5)]
        all_products = [1]

        with self.assertRaises(TypeError):
            calculate_product_sales_percentage(sales, all_products)

    def test_should_raise_error_quantity_not_int(self):
        sales = [(1, 1, "dez")]
        all_products = [1]

        with self.assertRaises(TypeError):
            calculate_product_sales_percentage(sales, all_products)


if __name__ == "__main__":
    unittest.main()