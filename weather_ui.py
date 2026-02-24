import tkinter as tk
import requests
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

api_key = "627738f9dcc6193c3bb19d0ec7a7e2c4"

def get_weather():
    city = city_entry.get().strip()

    if city == "":
        result_label.config(text="City name cannot be empty.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            result_label.config(text="City not found.")
            return

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        weather_text = (
            f"Weather in {data['name']}\n\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Condition: {description}\n"
            f"Wind Speed: {wind} m/s"
        )

        result_label.config(text=weather_text)

    except:
        result_label.config(text="Network error.")

root = tk.Tk()
root.title("Weather Forecast App")
root.geometry("700x700")

title = tk.Label(root, text="🌦️ Weather Forecast App", font=("Arial", 16))
title.pack(pady=15)

city_label = tk.Label(root, text="Enter City Name:")
city_label.pack()

city_entry = tk.Entry(root, width=25)
city_entry.pack(pady=5)

get_button = tk.Button(root, text="Get Weather", command=get_weather)
get_button.pack(pady=10)

result_label = tk.Label(root, text="", justify="left", font=("Arial", 11))
result_label.pack(pady=20)

root.mainloop()
