import os
import tkinter as tk
from tkinter import messagebox
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY", "7dc804bc349c86896464935c40f556f2")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city):
    complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(complete_url)
        weather_data = response.json()
        if weather_data.get("cod") != 200:
            return None, weather_data.get("message", "City not found or invalid API key.")
        main = weather_data['main']
        sys = weather_data['sys']
        weather = weather_data['weather'][0]
        temperature_celsius = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        city_name = weather_data['name']
        country = sys['country']
        weather_description = weather['description']
        info = {
            "city": city_name,
            "country": country,
            "temperature": f"{temperature_celsius}°C",
            "pressure": f"{pressure} hPa",
            "humidity": f"{humidity}%",
            "description": weather_description.title()
        }
        return info, None
    except requests.exceptions.RequestException:
        return None, "Network Error: Check your internet connection or API URL."
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

def search_weather():
    city_name = city_input.get()
    if not city_name:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return
    weather_info, error = get_weather(city_name)
    if weather_info:
        location_label.config(text=f"Location: {weather_info['city']}, {weather_info['country']}")
        temp_label.config(text=f"Temperature: {weather_info['temperature']}")
        desc_label.config(text=f"Condition: {weather_info['description']}")
        humidity_label.config(text=f"Humidity: {weather_info['humidity']}")
        pressure_label.config(text=f"Pressure: {weather_info['pressure']}")
    else:
        location_label.config(text="Location: ---")
        temp_label.config(text="Temperature: ---")
        desc_label.config(text="Condition: ---")
        humidity_label.config(text="Humidity: ---")
        pressure_label.config(text="Pressure: ---")
        messagebox.showerror("Weather Error", error)

root = tk.Tk()
root.title("Global Weather App 🌤")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(root, text="Enter City Name:", font=('Arial', 11)).pack(pady=10)
city_input = tk.Entry(root, width=30, font=('Arial', 10))
city_input.pack(pady=5)
tk.Button(root, text="Get Weather", command=search_weather, font=('Arial', 10, 'bold'), bg='#4CAF50', fg='white').pack(pady=10)

tk.Label(root, text="--- Current Weather ---", font=('Arial', 12, 'bold')).pack(pady=10)
location_label = tk.Label(root, text="Location: ---", font=('Arial', 10))
location_label.pack()
temp_label = tk.Label(root, text="Temperature: ---", font=('Arial', 10))
temp_label.pack()
desc_label = tk.Label(root, text="Condition: ---", font=('Arial', 10))
desc_label.pack()
humidity_label = tk.Label(root, text="Humidity: ---", font=('Arial', 10))
humidity_label.pack()
pressure_label = tk.Label(root, text="Pressure: ---", font=('Arial', 10))
pressure_label.pack()

root.mainloop()
