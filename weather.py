import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import json

api_key = ""
celcious_sign = "°C"
file_name = "api_key.json"

def main():
    json_data=[]
    if os.path.exists(f"{file_name}"):
        try:
            with open(f"{file_name}", "r") as j:
                loaded_data = json.load(j)
                
            if isinstance(loaded_data, list):
                json_data = loaded_data
            else:
                print(f"Warning: File {file_name} contains invalid data format. Initializing an empty list.")
                
        except json.JSONDecodeError:
            print(f"Warning: File {file_name} contains invalid data format. Initializing an empty list.")
    else:
        with open(f"{file_name}", "w") as j:
            json.dump([], j, indent=2)
    print(f"File '{file_name}' not found, created new empty JSON file.")
    ask_for_api(json_data,)

def ask_for_api(json_data):
    if json_data:
        api_key_ask = json_data[0]
        print(f"Using saved API key: {api_key_ask}")
        question_to_user(json_data, api_key_ask)
    else:
        api_key_ask = input("Type your OpenWeather API 32-character key: ")
        ask_for_save(api_key_ask, json_data)


def question_to_user(json_data,api_key_ask):
    get_data(api_key_ask)


def get_data(api_key_ask):
    city = input("Name of city to show weather forecast: ")
    api_key = api_key_ask
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    data_to_show = weather_data.json()
    show_weather(data_to_show)

def show_weather(data_to_show):
    data_main = "main"
    city_name = data_to_show["name"]
    country = data_to_show["sys"]["country"]
    for sky_data in data_to_show["weather"]:
        sky=(f"Sky is: {sky_data["description"]} .")
    temperture_min = data_to_show[data_main]["temp_min"]
    temperture_max = data_to_show[data_main]["temp_max"]
    feels_like = data_to_show[data_main]["feels_like"]
    humidinity = data_to_show[data_main]["humidity"]
    pressure = data_to_show[data_main]["pressure"]
    wind_speed = data_to_show["wind"]["speed"]
    to_show =  (f"\nCity name:  {city_name} \nThe country is:   {country}\n {sky} \n Mininal temperatue:  {temperture_min}{celcious_sign}, Maximal temperture:    {temperture_max}{celcious_sign} \n Feels like:  {feels_like}{celcious_sign} \n Humidinty is:   {humidinity}% and pressure is:   {pressure} hPa\n Wind speed is:   {wind_speed} km/h")
    print(to_show)
    ask_loop()
    
    
def ask_for_save(api_key_ask,json_data):
    ask_save = input("Do you want to save your API key to api_key.json? yes/no:  ")
    while ask_save in ["yes","y","no","n"]:
        if ask_save in ["yes","y"]:
            json_data.append(api_key_ask)
            with open("api_key.json","w") as api:
                json.dump(json_data,api, indent=2)
            print(f"Saved your API key: {api_key_ask}")
            get_data(api_key_ask)
            break
        else:
            get_data(api_key_ask)
    else:
        ask_save = input("Do you want to save your API key to api_key.json? yes/no:  ")
        
def exit_program():
    sys.exit()

def ask_loop():
    ask_for_reboot = input("Do you want to restart program? yes/no  ")
    while ask_for_reboot not in ["yes","y","no","n"]:
        ask_for_reboot = input("Do you want to restart program? yes/no  ")
    else:
        if ask_for_reboot in ["yes","y"]:
            main()
        else:
            exit_program()
    
main()
