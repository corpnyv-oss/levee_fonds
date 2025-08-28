from django.test import TestCase

class BasicTest(TestCase):
    def test_basic_addition(self):
        """Test basique pour vérifier que les tests fonctionnent"""
        self.assertEqual(1 + 1, 2)

    def test_database_connection(self):
        """Test de connexion à la base de données"""
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)
