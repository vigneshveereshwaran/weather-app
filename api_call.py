import streamlit as st
import requests
from datetime import datetime
import geocoder

st.title("🌦️ Weather App")

api_key = "3ced0f180200e383496b881267b46bc8"
g = geocoder.ip('me')
current_city = g.city
st.write(f"📍 Detected Location: {current_city}")

city = st.text_input("Enter cities (comma separated):")


if st.button("Get Weather"):
    if not city:
        city = current_city
    if city:
        cities = city.split(",")

        for c in cities:
            c = c.strip()

            if c == "":
                continue

            url = f"https://api.openweathermap.org/data/2.5/weather?q={c}&appid={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                def get_icon(weather):
                    weather = weather.lower()    
                    if "rain" in weather:
                        return "🌧️ Rainy"
                    elif "cloud" in weather:
                        return "☁️ Cloudy"
                    elif "clear" in weather:
                        return "☀️ Clear"
                    elif "haze" in weather:
                        return "🌫️ Hazy"
                    else:
                        return "🌍 Unknown"
                temp = data["main"]["temp"] - 273.15
                weather = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]
                now = datetime.now()
                st.write(f"🕒 Date & Time: {now.strftime('%d-%m-%Y %H:%M:%S')}")
                st.subheader(f"📍 {data['name']}")
                icon = get_icon(weather)
                st.subheader(f" Climate: {icon} ")
                st.metric("🌡️ Temperature", f"{round(temp,2)} °C")
                st.write(f"🌦️ Condition: {weather}")
                st.write(f"💧 Humidity: {humidity}%")
                st.write(f"🌬️ Wind: {wind}")
                st.write("---")
                

                with open("history.txt", "a") as f:
                    f.write(f"{data['name']} - {round(temp,2)}°C\n")
            elif response.status_code == 404:
                st.error(f"{c} ❌ city not found")
            elif response.status_code == 401:
                st.error("Invalid API key ❌")
            else:
                st.error(f"{c} ❌ not found")

    else:
        st.warning("Please enter a city ⚠️")



if st.button("Show History"):
    try:
        with open("history.txt", "r") as f:
            st.text(f.read())
    except FileNotFoundError:
        
        st.warning("No history found yet 📂")