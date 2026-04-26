import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock, mock_open
import json
import sys
import os

# Add parent directory to path to import weather_app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from weather_app import WeatherApp


class TestWeatherApp(unittest.TestCase):
    """Unit tests for WeatherApp class"""

    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.app = WeatherApp(self.root)

    def tearDown(self):
        """Clean up after tests"""
        try:
            self.root.destroy()
        except:
            pass

    def test_initialization(self):
        """Test that WeatherApp initializes correctly"""
        self.assertEqual(self.app.root.title(), "Weather App")
        self.assertIsNotNone(self.app.city_entry)
        self.assertIsNotNone(self.app.result_text)

    def test_window_properties(self):
        """Test window properties are set correctly"""
        self.assertEqual(self.app.root.title(), "Weather App")
        # Verify window is not resizable
        resizable = self.app.root.resizable()
        self.assertFalse(resizable[0])  # width not resizable
        self.assertFalse(resizable[1])  # height not resizable

    def test_city_entry_widget_exists(self):
        """Test that city entry widget is created"""
        self.assertIsNotNone(self.app.city_entry)

    def test_result_text_widget_exists(self):
        """Test that result text widget is created"""
        self.assertIsNotNone(self.app.result_text)
        
    def test_set_result_empty_string(self):
        """Test setting result to empty string"""
        self.app.set_result("")
        result = self.app.result_text.get("1.0", tk.END).strip()
        self.assertEqual(result, "")

    def test_set_result_with_text(self):
        """Test setting result with text"""
        test_text = "Test weather data"
        self.app.set_result(test_text)
        result = self.app.result_text.get("1.0", tk.END).strip()
        self.assertEqual(result, test_text)

    def test_set_result_multiline(self):
        """Test setting result with multiline text"""
        test_text = "Line 1\nLine 2\nLine 3"
        self.app.set_result(test_text)
        result = self.app.result_text.get("1.0", tk.END).strip()
        self.assertEqual(result, test_text)

    def test_fetch_weather_empty_city(self):
        """Test fetch_weather with empty city name"""
        self.app.city_entry.delete(0, tk.END)
        self.app.city_entry.insert(0, "")
        
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            self.app.fetch_weather()
            mock_warning.assert_called_once()

    def test_display_weather(self):
        """Test displaying weather information"""
        city = "London"
        weather = {
            "description": "Rainy",
            "temperature_c": "15",
            "feels_like_c": "12",
            "humidity": "80",
            "wind_kph": "20",
            "wind_dir": "N",
        }
        
        self.app.display_weather(city, weather)
        result = self.app.result_text.get("1.0", tk.END)
        
        self.assertIn(city, result)
        self.assertIn("15", result)
        self.assertIn("Rainy", result)

    def test_get_weather_for_city_valid_data(self):
        """Test parsing valid weather data"""
        mock_response_data = {
            "current_condition": [
                {
                    "weatherDesc": [{"value": "Sunny"}],
                    "temp_C": "25",
                    "FeelsLikeC": "24",
                    "humidity": "60",
                    "windspeedKmph": "10",
                    "winddir16Point": "N",
                }
            ]
        }
        
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            result = self.app.get_weather_for_city("London")
            
            self.assertEqual(result["description"], "Sunny")
            self.assertEqual(result["temperature_c"], "25")
            self.assertEqual(result["humidity"], "60")

    def test_get_weather_for_city_invalid_json(self):
        """Test handling invalid JSON response"""
        mock_response = MagicMock()
        mock_response.read.return_value = b"Invalid JSON"
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            with self.assertRaises(ValueError):
                self.app.get_weather_for_city("London")

    def test_get_weather_for_city_missing_data(self):
        """Test handling missing weather data"""
        mock_response_data = {"no_condition": []}
        
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            with self.assertRaises(ValueError):
                self.app.get_weather_for_city("London")

    def test_city_entry_clear_on_new_fetch(self):
        """Test that city entry can be updated"""
        self.app.city_entry.delete(0, tk.END)
        self.app.city_entry.insert(0, "Paris")
        city = self.app.city_entry.get()
        self.assertEqual(city, "Paris")


if __name__ == "__main__":
    unittest.main()
