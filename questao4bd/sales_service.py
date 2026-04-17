def get_sales_by_responsible(connection, user_name):
    # =========================
    # Validações
    # =========================
    if user_name is None:
        raise ValueError("user_name não pode ser None")

    if not isinstance(user_name, str):
        raise TypeError("user_name deve ser string")

    if user_name.strip() == "":
        raise ValueError("user_name não pode ser vazio")

    # =========================
    # Normalização
    # =========================
    user_name = user_name.strip().lower()

    cursor = connection.cursor()

    # =========================
    # Query
    # =========================
    query = """
        SELECT v.id
        FROM Venda v
        INNER JOIN Usuario u
            ON v.id_responsavel = u.id
        WHERE LOWER(u.nome) = ?
    """

    cursor.execute(query, (user_name,))
    rows = cursor.fetchall()

    # =========================
    # Tratamento do retorno
    # =========================
    # rows: [(1,), (2,), (4,), (5,)]
    result = [row[0] for row in rows]

    return result