import datetime
from bs4 import BeautifulSoup
import requests


def get_users_date():
    date = input("Which date do you want to travel back to? Type in YYYY-MM-DD format:\n")
    return date


def get_billboard_100(this_date):
    print(f"Date being searched: {this_date}")
    billboard_100_response = requests.get(f"https://www.billboard.com/charts/hot-100/{this_date}/")
    billboard_100_response.raise_for_status()
    billboard_100_page = BeautifulSoup(billboard_100_response.text, "html.parser")
    print(billboard_100_page)


chosen_date = input("Which date do you want to travel back to? Type in YYYY-MM-DD format:\n")

while True:
    try:
        datetime.datetime.strptime(chosen_date, '%Y-%m-%d')
    except ValueError:
        chosen_date = input("Wrong date format. Type in YYYY-MM-DD format:\n")
    else:
        break

get_billboard_100(this_date=chosen_date)
