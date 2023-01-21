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
    song_classes = [("c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet "
                     "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis "
                     "u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"),
                    ("c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet "
                     "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis "
                     "u-max-width-330 u-max-width-230@tablet-only")]
    song_element_list = billboard_100_page.find_all(name="h3", class_=song_classes)
    song_title_list = [song_el.text.replace('\n', '').replace('\t', '') for song_el in song_element_list]
    print(song_title_list)
    print(len(song_title_list))


chosen_date = input("Which date do you want to travel back to? Type in YYYY-MM-DD format:\n")

while True:
    try:
        datetime.datetime.strptime(chosen_date, '%Y-%m-%d')
    except ValueError:
        chosen_date = input("Wrong date format. Type in YYYY-MM-DD format:\n")
    else:
        break

get_billboard_100(this_date=chosen_date)
