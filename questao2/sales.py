def calculate_product_sales_percentage(sales, all_products):
    if not isinstance(sales, list):
        raise TypeError("Sales must be a list")

    if not isinstance(all_products, list):
        raise TypeError("All products must be a list")

    product_totals = {pid: 0 for pid in all_products}
    total_quantity = 0

    for item in sales:
        if not isinstance(item, tuple) or len(item) != 3:
            raise ValueError("Each item must be (sale_id, product_id, quantity)")

        sale_id, product_id, quantity = item

        if not isinstance(product_id, int) or not isinstance(quantity, int):
            raise TypeError("Product ID and quantity must be integers")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        if product_id not in product_totals:
            product_totals[product_id] = 0  # opcional: aceita produto fora da lista

        product_totals[product_id] += quantity
        total_quantity += quantity

    # evita divisão por zero
    if total_quantity == 0:
        return [(pid, 0.0) for pid in all_products]

    result = []

    for product_id in product_totals:
        qty = product_totals[product_id]
        percentage = round(qty / total_quantity, 4)
        result.append((product_id, percentage))

    # ordena por percentual desc
    result.sort(key=lambda x: x[1], reverse=True)

    return result