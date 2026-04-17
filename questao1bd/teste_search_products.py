import unittest
import sqlite3

from product_service import search_products


class TestSearchProducts(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.create_table()
        self.insert_mock_data()

    def tearDown(self):
        self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
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
        self.connection.commit()

    def insert_mock_data(self):
        cursor = self.connection.cursor()
        produtos = [
            (1, "Shampoo", "SH001", "Higiene", 10.50, 20),
            (2, "Condicionador", "CD001", "Higiene", 12.00, 15),
            (3, "Sabonete", "SB001", "Higiene", 5.00, 50),
            (4, "Notebook", "NT001", "Eletronicos", 2500.00, 5),
            (5, "Mouse", "MS001", "Eletronicos", 50.00, 30),
            (6, "Shampoo Premium", "SH002", "Higiene", 20.00, 10),
            (7, None, "XX001", "Outros", 1.00, 1)
        ]
        cursor.executemany("""
            INSERT INTO Produto VALUES (?, ?, ?, ?, ?, ?)
        """, produtos)
        self.connection.commit()

    # ✅ SUCESSO

    def test_search_by_name(self):
        result = search_products(self.connection, "shamp")
        self.assertEqual(len(result), 2)

    def test_search_by_code(self):
        result = search_products(self.connection, "SH00")
        self.assertEqual(len(result), 2)

    def test_search_by_category(self):
        result = search_products(self.connection, "eletron")
        self.assertEqual(len(result), 2)

    def test_case_insensitive(self):
        result = search_products(self.connection, "SHAMPOO")
        self.assertEqual(len(result), 2)

    def test_multiple_results(self):
        result = search_products(self.connection, "higiene")
        self.assertTrue(len(result) >= 3)

    def test_no_results(self):
        result = search_products(self.connection, "xyz")
        self.assertEqual(result, [])

    def test_null_field(self):
        result = search_products(self.connection, "XX001")
        self.assertEqual(len(result), 1)

    def test_empty_database(self):
        self.connection.execute("DELETE FROM Produto")
        result = search_products(self.connection, "shampoo")
        self.assertEqual(result, [])

    # ❌ ERROS

    def test_none_search_term(self):
        with self.assertRaises(ValueError):
            search_products(self.connection, None)

    def test_empty_search_term(self):
        with self.assertRaises(ValueError):
            search_products(self.connection, "")

    def test_blank_search_term(self):
        with self.assertRaises(ValueError):
            search_products(self.connection, "   ")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            search_products(self.connection, 123)

    # ⚠️ EDGE

    def test_large_dataset(self):
        cursor = self.connection.cursor()
        data = [(100+i, f"Produto{i}", f"C{i}", "Cat", 10.0, 1) for i in range(500)]
        cursor.executemany("INSERT INTO Produto VALUES (?, ?, ?, ?, ?, ?)", data)
        self.connection.commit()

        result = search_products(self.connection, "Produto")
        self.assertTrue(len(result) >= 500)


if __name__ == "__main__":
    unittest.main()