def get_products_by_sale_id(connection, sale_id):
    # =========================
    # Validações
    # =========================
    if sale_id is None:
        raise ValueError("sale_id não pode ser None")

    if not isinstance(sale_id, int):
        raise TypeError("sale_id deve ser inteiro")

    # =========================
    # Query
    # =========================
    cursor = connection.cursor()

    query = """
        SELECT DISTINCT p.nome
        FROM Produto p
        INNER JOIN Produto_venda pv
            ON p.id = pv.id_produto
        WHERE pv.id_venda = ?
    """

    cursor.execute(query, (sale_id,))
    rows = cursor.fetchall()

    # =========================
    # Tratamento do retorno
    # =========================
    # rows: [('Shampoo',), ('Sabonete',)]
    result = [row[0] for row in rows if row[0] is not None]

    return result