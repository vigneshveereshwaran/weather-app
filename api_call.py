import streamlit as st
import requests

st.title("🌦️ Weather App")

api_key = "3ced0f180200e383496b881267b46bc8"


city = st.text_input("Enter cities (comma separated):")


if st.button("Get Weather"):

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

                temp = data["main"]["temp"] - 273.15
                weather = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]

              
                st.subheader(f"📍 {data['name']}")
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