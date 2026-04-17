def count_low_stock_products(products):
    if not isinstance(products, list):
        raise TypeError("Products must be a list")

    count = 0

    for item in products:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("Each item must be a tuple (name, quantity)")

        name, quantity = item

        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        if quantity < 5:
            count += 1

    return count