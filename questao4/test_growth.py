import unittest

# TDD: função ainda não implementada
from growth import calculate_monthly_growth_percentage


class TestCalculateMonthlyGrowthPercentage(unittest.TestCase):

    # =========================
    # ✅ CENÁRIOS DE SUCESSO
    # =========================

    def test_should_calculate_positive_growth(self):
        # Arrange
        sales = [('1/22', 400.50), ('2/22', 1000.00)]

        # Act
        result = calculate_monthly_growth_percentage(sales, '2/22')

        # Assert
        self.assertAlmostEqual(result, 1.4969, places=4)

    def test_should_calculate_negative_growth(self):
        sales = [('1/22', 400.50), ('2/22', 1000.00), ('3/22', 10.50)]

        result = calculate_monthly_growth_percentage(sales, '3/22')

        self.assertAlmostEqual(result, -0.9895, places=4)

    def test_should_calculate_zero_growth(self):
        sales = [('1/22', 100.0), ('2/22', 100.0)]

        result = calculate_monthly_growth_percentage(sales, '2/22')

        self.assertEqual(result, 0.0)

    def test_should_work_with_unsorted_list(self):
        sales = [('2/22', 1000.00), ('1/22', 400.50)]

        result = calculate_monthly_growth_percentage(sales, '2/22')

        self.assertAlmostEqual(result, 1.4969, places=4)

    def test_should_work_with_only_two_months(self):
        sales = [('1/22', 100), ('2/22', 200)]

        result = calculate_monthly_growth_percentage(sales, '2/22')

        self.assertEqual(result, 1.0)

    def test_should_handle_decimal_values(self):
        sales = [('1/22', 10.5), ('2/22', 21.0)]

        result = calculate_monthly_growth_percentage(sales, '2/22')

        self.assertEqual(result, 1.0)

    def test_should_handle_mixed_int_and_float(self):
        sales = [('1/22', 10), ('2/22', 20.0)]

        result = calculate_monthly_growth_percentage(sales, '2/22')

        self.assertEqual(result, 1.0)

    def test_should_handle_year_transition(self):
        sales = [('12/22', 100), ('1/23', 200)]

        result = calculate_monthly_growth_percentage(sales, '1/23')

        self.assertEqual(result, 1.0)

    # =========================
    # ❌ DADOS INVÁLIDOS
    # =========================

    def test_should_raise_error_when_item_not_tuple(self):
        sales = ['invalid']

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_error_when_tuple_invalid_size(self):
        sales = [('1/22', 100, 200)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_error_when_list_contains_none(self):
        sales = [('1/22', 100), None]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_error_when_tuple_contains_none(self):
        sales = [('1/22', None)]

        with self.assertRaises(TypeError):
            calculate_monthly_growth_percentage(sales, '1/22')

    # =========================
    # ❌ TIPOS INVÁLIDOS
    # =========================

    def test_should_raise_error_when_month_not_string(self):
        sales = [(1, 100)]

        with self.assertRaises(TypeError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_error_when_value_not_numeric(self):
        sales = [('1/22', '100.50')]

        with self.assertRaises(TypeError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_error_when_invalid_month_format(self):
        sales = [('2022-01', 100)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '2022-01')

    def test_should_raise_error_when_invalid_month_number(self):
        sales = [('13/22', 100)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '13/22')

    # =========================
    # ❌ REGRAS DE NEGÓCIO
    # =========================

    def test_should_raise_error_when_value_negative(self):
        sales = [('1/22', -100)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_error_when_target_month_not_found(self):
        sales = [('1/22', 100)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '2/22')

    def test_should_raise_error_when_previous_month_not_found(self):
        sales = [('1/22', 100)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_error_when_duplicate_months(self):
        sales = [('1/22', 100), ('1/22', 200)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_raise_zero_division_when_previous_is_zero(self):
        sales = [('1/22', 0), ('2/22', 100)]

        with self.assertRaises(ZeroDivisionError):
            calculate_monthly_growth_percentage(sales, '2/22')

    # =========================
    # ⚠️ EDGE CASES
    # =========================

    def test_should_raise_error_for_empty_list(self):
        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage([], '1/22')

    def test_should_raise_error_for_single_month(self):
        sales = [('1/22', 100)]

        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '1/22')

    def test_should_handle_large_dataset(self):
        sales = [(f"{i%12+1}/22", float(i)) for i in range(1, 50)]

        # pode gerar duplicado → esperamos erro
        with self.assertRaises(ValueError):
            calculate_monthly_growth_percentage(sales, '2/22')


if __name__ == "__main__":
    unittest.main()