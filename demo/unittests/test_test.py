import unittest
from io import StringIO
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPrintStatement(unittest.TestCase):
    """Unit tests for test.py"""

    def test_hello_world_print(self):
        """Test that 'Hello, World!' is printed"""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Import and execute the module
        import test as test_module
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Assert the output
        self.assertIn("Hello, World!", captured_output.getvalue())

    def test_output_is_string(self):
        """Test that output is a string"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Re-import to capture output
        if 'test' in sys.modules:
            del sys.modules['test']
        import test as test_module
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIsInstance(output, str)

    def test_output_ends_with_newline(self):
        """Test that output ends with newline"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Re-import to capture output
        if 'test' in sys.modules:
            del sys.modules['test']
        import test as test_module
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertTrue(output.endswith('\n'))


if __name__ == "__main__":
    unittest.main()
