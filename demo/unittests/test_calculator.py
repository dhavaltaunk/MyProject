import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import calculator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calculator import CalculatorApp


class TestCalculatorApp(unittest.TestCase):
    """Unit tests for CalculatorApp class"""

    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.app = CalculatorApp(self.root)

    def tearDown(self):
        """Clean up after tests"""
        try:
            self.root.destroy()
        except:
            pass

    def test_initialization(self):
        """Test that CalculatorApp initializes correctly"""
        self.assertEqual(self.app.total_expression, "")
        self.assertEqual(self.app.current_expression, "")
        self.assertIsNotNone(self.app.display_frame)
        self.assertIsNotNone(self.app.button_frame)

    def test_digits_dictionary(self):
        """Test that digits are configured correctly"""
        self.assertIn(0, self.app.digits)
        self.assertIn(9, self.app.digits)
        self.assertIn(".", self.app.digits)
        self.assertEqual(len(self.app.digits), 11)  # 0-9 plus decimal point

    def test_operations_dictionary(self):
        """Test that operations are configured correctly"""
        self.assertIn("+", self.app.operations)
        self.assertIn("-", self.app.operations)
        self.assertIn("*", self.app.operations)
        self.assertIn("/", self.app.operations)
        self.assertEqual(len(self.app.operations), 4)

    def test_add_to_expression(self):
        """Test adding digits to expression"""
        self.app.add_to_expression("5")
        self.assertEqual(self.app.current_expression, "5")
        
        self.app.add_to_expression("3")
        self.assertEqual(self.app.current_expression, "53")

    def test_append_operator(self):
        """Test appending operators"""
        self.app.add_to_expression("5")
        self.app.append_operator("+")
        self.assertIn("+", self.app.total_expression)

    def test_clear_last(self):
        """Test clearing the last digit"""
        self.app.add_to_expression("5")
        self.app.add_to_expression("3")
        self.app.clear_last()
        self.assertEqual(self.app.current_expression, "5")

    def test_clear(self):
        """Test clearing all expressions"""
        self.app.add_to_expression("5")
        self.app.append_operator("+")
        self.app.add_to_expression("3")
        self.app.clear()
        self.assertEqual(self.app.current_expression, "")
        self.assertEqual(self.app.total_expression, "")

    def test_decimal_point(self):
        """Test decimal point handling"""
        self.app.add_to_expression("5")
        self.app.add_to_expression(".")
        self.app.add_to_expression("5")
        self.assertEqual(self.app.current_expression, "5.5")

    def test_window_properties(self):
        """Test window properties are set correctly"""
        self.assertEqual(self.app.root.title(), "Modern Calculator")
        self.assertFalse(self.app.root.resizable()[0])


if __name__ == "__main__":
    unittest.main()
