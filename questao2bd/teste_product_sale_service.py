import unittest
import sqlite3

# Import fictício (TDD)
from product_sale_service import get_products_by_sale_id


class TestGetProductsBySaleId(unittest.TestCase):

    def setUp(self):
        # Arrange
        self.connection = sqlite3.connect(":memory:")
        self.create_tables()
        self.insert_mock_data()

    def tearDown(self):
        self.connection.close()

    # =========================
    # Setup do banco
    # =========================

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE Usuario (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                endereco TEXT,
                tipo_usuario TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE Produto (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                codigo TEXT,
                categoria TEXT,
                preco REAL,
                quantidade INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE Venda (
                id INTEGER PRIMARY KEY,
                id_responsavel INTEGER,
                total REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE Produto_venda (
                id INTEGER PRIMARY KEY,
                id_produto INTEGER,
                id_venda INTEGER,
                quantidade INTEGER
            )
        """)

        self.connection.commit()

    def insert_mock_data(self):
        cursor = self.connection.cursor()

        # Usuarios
        cursor.executemany("""
            INSERT INTO Usuario VALUES (?, ?, ?, ?)
        """, [
            (1, "João", "Rua A", "ADMIN"),
            (2, "Maria", "Rua B", "USER")
        ])

        # Produtos
        cursor.executemany("""
            INSERT INTO Produto VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (1, "Shampoo", "SH001", "Higiene", 10.0, 10),
            (2, "Condicionador", "CD001", "Higiene", 12.0, 10),
            (3, "Sabonete", "SB001", "Higiene", 5.0, 50),
            (4, "Notebook", "NT001", "Eletronicos", 2000.0, 5)
        ])

        # Vendas
        cursor.executemany("""
            INSERT INTO Venda VALUES (?, ?, ?)
        """, [
            (1, 1, 100.0),
            (2, 2, 200.0),
            (3, 1, 0.0)  # venda sem produtos
        ])

        # Produto_venda
        cursor.executemany("""
            INSERT INTO Produto_venda VALUES (?, ?, ?, ?)
        """, [
            (1, 1, 1, 2),  # Shampoo
            (2, 2, 1, 1),  # Condicionador
            (3, 3, 1, 1),  # Sabonete
            (4, 1, 1, 1),  # Shampoo repetido
            (5, 4, 2, 1),  # Notebook
            (6, 999, 1, 1) # FK inválida (produto inexistente)
        ])

        self.connection.commit()

    # =========================
    # ✅ SUCESSO
    # =========================

    def test_should_return_multiple_products(self):
        # Act
        result = get_products_by_sale_id(self.connection, 1)

        # Assert
        self.assertCountEqual(result, ["Shampoo", "Condicionador", "Sabonete"])

    def test_should_return_single_product(self):
        # Act
        result = get_products_by_sale_id(self.connection, 2)

        # Assert
        self.assertEqual(result, ["Notebook"])

    def test_should_not_return_duplicates(self):
        # Act
        result = get_products_by_sale_id(self.connection, 1)

        # Assert
        self.assertEqual(len(result), 3)

    def test_should_return_only_strings(self):
        # Act
        result = get_products_by_sale_id(self.connection, 1)

        # Assert
        for item in result:
            self.assertIsInstance(item, str)

    def test_should_return_empty_list_when_sale_has_no_products(self):
        # Act
        result = get_products_by_sale_id(self.connection, 3)

        # Assert
        self.assertEqual(result, [])

    def test_should_return_empty_list_when_sale_does_not_exist(self):
        # Act
        result = get_products_by_sale_id(self.connection, 999)

        # Assert
        self.assertEqual(result, [])

    # =========================
    # ❌ FALHAS
    # =========================

    def test_should_raise_type_error_when_sale_id_not_int(self):
        with self.assertRaises(TypeError):
            get_products_by_sale_id(self.connection, "1")

    def test_should_raise_value_error_when_sale_id_is_none(self):
        with self.assertRaises(ValueError):
            get_products_by_sale_id(self.connection, None)

    # =========================
    # ⚠️ EDGE CASES
    # =========================

    def test_should_ignore_invalid_foreign_keys(self):
        # Já existe FK inválida no mock (id_produto = 999)
        result = get_products_by_sale_id(self.connection, 1)

        self.assertCountEqual(result, ["Shampoo", "Condicionador", "Sabonete"])

    def test_should_work_with_empty_database(self):
        # Arrange
        self.connection.execute("DELETE FROM Produto_venda")
        self.connection.execute("DELETE FROM Produto")
        self.connection.execute("DELETE FROM Venda")

        # Act
        result = get_products_by_sale_id(self.connection, 1)

        # Assert
        self.assertEqual(result, [])

    def test_should_handle_large_dataset(self):
        # Arrange
        cursor = self.connection.cursor()

        many_products = [
            (100+i, f"Produto{i}", f"C{i}", "Cat", 10.0, 1)
            for i in range(500)
        ]
        cursor.executemany("INSERT INTO Produto VALUES (?, ?, ?, ?, ?, ?)", many_products)

        many_relations = [
            (1000+i, 100+i, 1, 1)
            for i in range(500)
        ]
        cursor.executemany("INSERT INTO Produto_venda VALUES (?, ?, ?, ?)", many_relations)

        self.connection.commit()

        # Act
        result = get_products_by_sale_id(self.connection, 1)

        # Assert
        self.assertTrue(len(result) >= 500)


if __name__ == "__main__":
    unittest.main()