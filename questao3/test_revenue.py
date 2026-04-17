import unittest

# Import fictício (TDD: ainda não implementado)
from revenue import calculate_total_revenue


class TestCalculateTotalRevenue(unittest.TestCase):

    # =========================
    # ✅ CENÁRIOS DE SUCESSO
    # =========================

    def test_should_calculate_total_with_multiple_sales(self):
        # Arrange
        sales = [(1, 50.50), (2, 200.95), (3, 20.95), (4, 100.40)]

        # Act
        result = calculate_total_revenue(sales)

        # Assert
        self.assertAlmostEqual(result, 372.80, places=2)

    def test_should_calculate_total_with_single_sale(self):
        sales = [(1, 100.00)]

        result = calculate_total_revenue(sales)

        self.assertEqual(result, 100.0)

    def test_should_return_zero_for_empty_list(self):
        result = calculate_total_revenue([])

        self.assertEqual(result, 0.0)

    def test_should_handle_decimal_values(self):
        sales = [(1, 10.25), (2, 20.75)]

        result = calculate_total_revenue(sales)

        self.assertAlmostEqual(result, 31.0, places=2)

    def test_should_handle_zero_values(self):
        sales = [(1, 0), (2, 0.0)]

        result = calculate_total_revenue(sales)

        self.assertEqual(result, 0.0)

    def test_should_handle_mixed_int_and_float(self):
        sales = [(1, 10), (2, 20.5), (3, 30)]

        result = calculate_total_revenue(sales)

        self.assertAlmostEqual(result, 60.5, places=2)

    def test_should_handle_large_values(self):
        sales = [(1, 1_000_000), (2, 2_500_000.75)]

        result = calculate_total_revenue(sales)

        self.assertAlmostEqual(result, 3_500_000.75, places=2)

    # =========================
    # ❌ DADOS INVÁLIDOS
    # =========================

    def test_should_raise_error_when_item_is_not_tuple(self):
        sales = [123]

        with self.assertRaises(ValueError):
            calculate_total_revenue(sales)

    def test_should_raise_error_when_tuple_has_invalid_size(self):
        sales = [(1, 100, 200)]

        with self.assertRaises(ValueError):
            calculate_total_revenue(sales)

    def test_should_raise_error_when_list_contains_invalid_element(self):
        sales = [(1, 100), "invalid"]

        with self.assertRaises(ValueError):
            calculate_total_revenue(sales)

    def test_should_raise_error_when_list_contains_none(self):
        sales = [(1, 100), None]

        with self.assertRaises(ValueError):
            calculate_total_revenue(sales)

    def test_should_raise_error_when_tuple_contains_none(self):
        sales = [(1, None)]

        with self.assertRaises(TypeError):
            calculate_total_revenue(sales)

    # =========================
    # ❌ TIPOS INVÁLIDOS
    # =========================

    def test_should_raise_error_when_id_is_not_int(self):
        sales = [("1", 100)]

        with self.assertRaises(TypeError):
            calculate_total_revenue(sales)

    def test_should_raise_error_when_value_is_not_numeric(self):
        sales = [(1, "100.50")]

        with self.assertRaises(TypeError):
            calculate_total_revenue(sales)

    def test_should_raise_error_when_value_is_invalid_type(self):
        sales = [(1, [100])]

        with self.assertRaises(TypeError):
            calculate_total_revenue(sales)

    # =========================
    # ❌ REGRAS DE NEGÓCIO
    # =========================

    def test_should_raise_error_when_value_is_negative(self):
        sales = [(1, -50.0)]

        with self.assertRaises(ValueError):
            calculate_total_revenue(sales)

    # =========================
    # ⚠️ EDGE CASES
    # =========================

    def test_should_handle_total_equal_zero(self):
        sales = [(1, 0), (2, 0)]

        result = calculate_total_revenue(sales)

        self.assertEqual(result, 0.0)

    def test_should_handle_very_large_list(self):
        sales = [(i, 1.0) for i in range(10000)]

        result = calculate_total_revenue(sales)

        self.assertEqual(result, 10000.0)


if __name__ == "__main__":
    unittest.main()