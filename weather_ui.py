import tkinter as tk
import requests
import ctypes
from PIL import Image, ImageTk
ctypes.windll.shcore.SetProcessDpiAwareness(1)

from config import api_key
def detect_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        return data["city"]
    except:
        return None

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return None

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind": data["wind"]["speed"]
        }
    except:
        return None

def show_weather():
    if mode.get() == "auto":
        city = detect_location()
        if not city:
            result_label.config(text="Could not detect location")
            return
    else:
        city = city_entry.get().strip()
        if city == "":
            result_label.config(text="Enter a city name")
            return

    weather = get_weather(city)

    if not weather:
        result_label.config(text="Error fetching weather")
        return

    text = (
        f"📍 {weather['city']}\n\n"
        f"🌡 Temp: {weather['temperature']}°C\n"
        f"💧 Humidity: {weather['humidity']}%\n"
        f"🌥 {weather['description']}\n"
        f"💨 Wind: {weather['wind']} m/s\n\n"
        f"✨ Have a good day ahead ☀"
    )

    result_label.config(text=text)
    result_label.pack(pady=20)

def toggle_entry():
    if mode.get() == "manual":
        city_entry.pack(before=get_btn, pady=10)
    else:
        city_entry.pack_forget()

root = tk.Tk()
root.title("Weather App")
root.geometry("600x690")
bg_image = Image.open("bg4.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title = tk.Label(
    root,
    text="☁ How's the Weather?",
    font=("Arial", 20, "bold"),
    bg="#5CBFD0",
    fg="navy"
)
title.pack(pady=15)

mode = tk.StringVar(value="auto")

auto_btn = tk.Radiobutton(
    root, text="Auto Detect Location",
    variable=mode, value="auto",
    command=toggle_entry,
    bg="#ffffff", font=("Arial", 11)
)
auto_btn.pack(pady=5)

manual_btn = tk.Radiobutton(
    root, text="Enter City Manually",
    variable=mode, value="manual",
    command=toggle_entry,
    bg="#ffffff", font=("Arial", 11)
)
manual_btn.pack(pady=5)

city_entry = tk.Entry(root, width=25, font=("Arial", 12))
city_entry.pack_forget()

get_btn = tk.Button(
    root,
    text="Show Weather",
    command=show_weather,
    bg="#7ad0e8",
    fg="black",
    font=("Arial", 12, "bold"),
    padx=12,
    pady=6
)
get_btn.pack(pady=20)

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 12),
    bg="#ffffff",
    fg="black",
    justify="left"
)

exit_btn = tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    bg="#000000",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5
)
exit_btn.pack(side="bottom", pady=20)

root.mainloop()