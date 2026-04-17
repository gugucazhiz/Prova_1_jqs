import unittest
import sqlite3

# TDD: função ainda NÃO implementada
from sales_service import get_sales_by_responsible


class TestGetSalesByResponsible(unittest.TestCase):

    def setUp(self):
        # Arrange
        self.conn = sqlite3.connect(":memory:")
        self._create_tables()
        self._insert_mock_data()

    def tearDown(self):
        self.conn.close()

    # =========================
    # 🔧 Setup do banco
    # =========================

    def _create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE Usuario (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                endereco TEXT,
                tipo_usuario TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE Venda (
                id INTEGER PRIMARY KEY,
                id_responsavel INTEGER,
                total REAL
            )
        """)

        self.conn.commit()

    def _insert_mock_data(self):
        cursor = self.conn.cursor()

        # Usuários (incluindo nomes duplicados)
        usuarios = [
            (1, "João", "Rua A", "ADMIN"),
            (2, "Maria", "Rua B", "USER"),
            (3, "joão", "Rua C", "USER"),  # mesmo nome (case diferente)
            (4, "Carlos", "Rua D", "USER"),
            (5, "João", "Rua E", "USER")   # mesmo nome (ID diferente)
        ]

        cursor.executemany("""
            INSERT INTO Usuario VALUES (?, ?, ?, ?)
        """, usuarios)

        # Vendas
        vendas = [
            (1, 1, 100.0),
            (2, 1, 200.0),
            (3, 2, 150.0),
            (4, 3, 300.0),
            (5, 5, 50.0)
        ]

        cursor.executemany("""
            INSERT INTO Venda VALUES (?, ?, ?)
        """, vendas)

        self.conn.commit()

    # =========================
    # ✅ SUCESSO
    # =========================

    def test_should_return_multiple_sales_for_user(self):
        # Act
        result = get_sales_by_responsible(self.conn, "João")

        # Assert
        self.assertCountEqual(result, [1, 2, 4, 5])

    def test_should_return_single_sale(self):
        # Act
        result = get_sales_by_responsible(self.conn, "Maria")

        # Assert
        self.assertEqual(result, [3])

    def test_should_return_empty_when_user_has_no_sales(self):
        # Arrange
        self.conn.execute("""
            INSERT INTO Usuario VALUES (10, 'Ana', 'Rua X', 'USER')
        """)

        # Act
        result = get_sales_by_responsible(self.conn, "Ana")

        # Assert
        self.assertEqual(result, [])

    def test_should_be_case_insensitive(self):
        # Act
        result = get_sales_by_responsible(self.conn, "joÃO")

        # Assert
        self.assertCountEqual(result, [1, 2, 4, 5])

    def test_should_trim_spaces_in_name(self):
        # Act
        result = get_sales_by_responsible(self.conn, "  João  ")

        # Assert
        self.assertCountEqual(result, [1, 2, 4, 5])

    def test_should_return_only_integers(self):
        # Act
        result = get_sales_by_responsible(self.conn, "João")

        # Assert
        for item in result:
            self.assertIsInstance(item, int)

    def test_should_return_empty_when_user_not_found(self):
        # Act
        result = get_sales_by_responsible(self.conn, "Inexistente")

        # Assert
        self.assertEqual(result, [])

    # =========================
    # ❌ FALHAS
    # =========================

    def test_should_raise_value_error_when_name_is_none(self):
        with self.assertRaises(ValueError):
            get_sales_by_responsible(self.conn, None)

    def test_should_raise_value_error_when_name_is_empty(self):
        with self.assertRaises(ValueError):
            get_sales_by_responsible(self.conn, "")

    def test_should_raise_value_error_when_name_is_blank(self):
        with self.assertRaises(ValueError):
            get_sales_by_responsible(self.conn, "   ")

    def test_should_raise_type_error_when_name_not_string(self):
        with self.assertRaises(TypeError):
            get_sales_by_responsible(self.conn, 123)

    # =========================
    # ⚠️ EDGE CASES
    # =========================

    def test_should_work_with_empty_database(self):
        # Arrange
        self.conn.execute("DELETE FROM Venda")
        self.conn.execute("DELETE FROM Usuario")

        # Act
        result = get_sales_by_responsible(self.conn, "João")

        # Assert
        self.assertEqual(result, [])

    def test_should_handle_large_dataset(self):
        # Arrange
        cursor = self.conn.cursor()

        users = [(100+i, "Teste", "Rua", "USER") for i in range(200)]
        sales = [(1000+i, 100+i, 10.0) for i in range(200)]

        cursor.executemany("INSERT INTO Usuario VALUES (?, ?, ?, ?)", users)
        cursor.executemany("INSERT INTO Venda VALUES (?, ?, ?)", sales)

        self.conn.commit()

        # Act
        result = get_sales_by_responsible(self.conn, "Teste")

        # Assert
        self.assertTrue(len(result) >= 200)


if __name__ == "__main__":
    unittest.main()