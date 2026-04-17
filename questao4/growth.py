import re


def calculate_monthly_growth_percentage(sales, target_month):
    # =========================
    # VALIDAÇÃO INICIAL
    # =========================
    if not isinstance(sales, list):
        raise TypeError("Sales must be a list")

    if not sales:
        raise ValueError("Sales list cannot be empty")

    # regex para validar formato M/YY
    pattern = r"^\d{1,2}/\d{2}$"

    parsed_sales = {}

    # =========================
    # VALIDAÇÃO E PARSE
    # =========================
    for item in sales:
        if item is None:
            raise ValueError("Sales list cannot contain None")

        if not isinstance(item, tuple):
            raise ValueError("Each item must be a tuple")

        if len(item) != 2:
            raise ValueError("Each item must be (month, value)")

        month, value = item

        # valida mês
        if not isinstance(month, str):
            raise TypeError("Month must be string")

        month = month.strip()

        if not re.match(pattern, month):
            raise ValueError("Invalid month format")

        m, y = month.split("/")
        m = int(m)

        if m < 1 or m > 12:
            raise ValueError("Invalid month number")

        # valida valor
        if value is None:
            raise TypeError("Value cannot be None")

        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric")

        if value < 0:
            raise ValueError("Value cannot be negative")

        # verifica duplicidade
        if month in parsed_sales:
            raise ValueError("Duplicate month found")

        parsed_sales[month] = float(value)

    # =========================
    # VALIDA TARGET
    # =========================
    if not isinstance(target_month, str):
        raise TypeError("Target month must be string")

    target_month = target_month.strip()

    if target_month not in parsed_sales:
        raise ValueError("Target month not found")

    # =========================
    # FUNÇÃO AUXILIAR (mês anterior)
    # =========================
    def get_previous_month(month_str):
        m, y = month_str.split("/")
        m = int(m)
        y = int(y)

        if m == 1:
            return f"12/{str(y - 1).zfill(2)}"
        else:
            return f"{m - 1}/{str(y).zfill(2)}"

    previous_month = get_previous_month(target_month)

    if previous_month not in parsed_sales:
        raise ValueError("Previous month not found")

    current_value = parsed_sales[target_month]
    previous_value = parsed_sales[previous_month]

    # =========================
    # REGRA DE NEGÓCIO
    # =========================
    if previous_value == 0:
        raise ZeroDivisionError("Previous month value is zero")

    growth = (current_value - previous_value) / previous_value

    return round(growth, 4)