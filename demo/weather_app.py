import json
import urllib.error
import urllib.parse
import urllib.request
import tkinter as tk
from tkinter import messagebox


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        self.root.configure(bg="#f2f2f2")

        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(
            self.root,
            text="Current Weather",
            bg="#4a90e2",
            fg="white",
            font=("Segoe UI", 18, "bold"),
            pady=12,
        )
        header.pack(fill="x")

        input_frame = tk.Frame(self.root, bg="#f2f2f2", pady=16)
        input_frame.pack(fill="x")

        city_label = tk.Label(
            input_frame,
            text="City:",
            bg="#f2f2f2",
            fg="#333333",
            font=("Segoe UI", 12),
        )
        city_label.grid(row=0, column=0, padx=(16, 8), pady=4, sticky="w")

        self.city_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            width=24,
            bd=2,
            relief="groove",
        )
        self.city_entry.grid(row=0, column=1, padx=(0, 16), pady=4, sticky="w")
        self.city_entry.bind("<Return>", lambda event: self.fetch_weather())

        get_button = tk.Button(
            input_frame,
            text="Get Weather",
            command=self.fetch_weather,
            font=("Segoe UI", 11, "bold"),
            bg="#4a90e2",
            fg="white",
            activebackground="#357ab7",
            activeforeground="white",
            padx=10,
            pady=6,
            bd=0,
        )
        get_button.grid(row=0, column=2, padx=(0, 16), pady=4)

        separator = tk.Frame(self.root, height=1, bg="#d9d9d9")
        separator.pack(fill="x", padx=16, pady=(0, 16))

        self.result_text = tk.Text(
            self.root,
            wrap="word",
            bg="white",
            fg="#1c1c1c",
            font=("Segoe UI", 12),
            bd=2,
            relief="groove",
            height=10,
        )
        self.result_text.pack(fill="both", padx=16, pady=(0, 16), expand=True)
        self.result_text.configure(state="disabled")

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input required", "Please enter a city name.")
            return

        self.set_result("Fetching weather for {}...".format(city))
        try:
            weather = self.get_weather_for_city(city)
            self.display_weather(city, weather)
        except ValueError as error:
            messagebox.showerror("Weather error", str(error))
            self.set_result("")
        except urllib.error.URLError as error:
            messagebox.showerror(
                "Network error",
                "Unable to reach the weather service. Please check your internet connection.",
            )
            self.set_result("")

    def get_weather_for_city(self, city):
        encoded_city = urllib.parse.quote(city)
        url = f"https://wttr.in/{encoded_city}?format=j1"
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        with urllib.request.urlopen(request, timeout=10) as response:
            raw_data = response.read().decode("utf-8")

        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            raise ValueError("Received an invalid response from the weather service.")

        if not data or "current_condition" not in data:
            raise ValueError("Weather data is not available for this city.")

        current = data["current_condition"][0]
        description = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        temperature_c = current.get("temp_C", "?")
        feels_like_c = current.get("FeelsLikeC", "?")
        humidity = current.get("humidity", "?")
        wind_kph = current.get("windspeedKmph", "?")
        wind_dir = current.get("winddir16Point", "?")

        return {
            "description": description,
            "temperature_c": temperature_c,
            "feels_like_c": feels_like_c,
            "humidity": humidity,
            "wind_kph": wind_kph,
            "wind_dir": wind_dir,
        }

    def display_weather(self, city, weather):
        message = (
            f"Weather for {city}\n"
            f"-----------------------------\n"
            f"Description: {weather['description']}\n"
            f"Temperature: {weather['temperature_c']}°C\n"
            f"Feels like: {weather['feels_like_c']}°C\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Wind: {weather['wind_kph']} km/h {weather['wind_dir']}\n"
        )
        self.set_result(message)

    def set_result(self, text):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")


def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
