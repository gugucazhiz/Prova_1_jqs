def calculate_total_revenue(sales):
    # valida tipo da entrada
    if not isinstance(sales, list):
        raise TypeError("Sales must be a list")

    total = 0.0

    for item in sales:
        # valida item
        if item is None:
            raise ValueError("Sales list cannot contain None")

        if not isinstance(item, tuple):
            raise ValueError("Each item must be a tuple")

        if len(item) != 2:
            raise ValueError("Each item must be (id_venda, valor_total)")

        sale_id, value = item

        # valida id
        if not isinstance(sale_id, int):
            raise TypeError("Sale ID must be an integer")

        # valida valor
        if value is None:
            raise TypeError("Value cannot be None")

        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric (int or float)")

        if value < 0:
            raise ValueError("Value cannot be negative")

        total += float(value)

    return total