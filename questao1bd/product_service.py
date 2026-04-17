def search_products(connection, search_term):
    # =========================
    # Validações
    # =========================
    if search_term is None:
        raise ValueError("search_term não pode ser None")

    if not isinstance(search_term, str):
        raise TypeError("search_term deve ser string")

    if search_term.strip() == "":
        raise ValueError("search_term não pode ser vazio")

    # =========================
    # Query segura
    # =========================
    search_term = search_term.strip().lower()
    like_term = f"%{search_term}%"

    cursor = connection.cursor()

    query = """
        SELECT id, nome, codigo, categoria, preco, quantidade
        FROM Produto
        WHERE
            LOWER(COALESCE(nome, '')) LIKE ?
            OR LOWER(COALESCE(codigo, '')) LIKE ?
            OR LOWER(COALESCE(categoria, '')) LIKE ?
    """

    cursor.execute(query, (like_term, like_term, like_term))

    results = cursor.fetchall()

    return results