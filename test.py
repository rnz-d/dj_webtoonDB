from bs4 import BeautifulSoup
import requests

AR_PAGES = 3
AR_GRID_TYPE = "div"
AR_GRID_CLASS = "listupd"
AR_WEBTOON_TYPE = "div"
AR_WEBTOON_CLASS = "utao styletwo"
AR_TITLE_TYPE = "h4"
AR_URL_CLASS = "series"

ar_pages = AR_PAGES
for page in range(1, ar_pages):
    ar_html_text = requests.get(f"https://asura.gg/page/{page}/").text
    ar_soup = BeautifulSoup(ar_html_text, "lxml")
    ar_grid = ar_soup.find_all(AR_GRID_TYPE, class_=AR_GRID_CLASS)[1]
    ar_webtoons = ar_grid.find_all(AR_WEBTOON_TYPE, class_=AR_WEBTOON_CLASS)
    print(ar_webtoons)

    for ar_webtoon in ar_webtoons:
        title = ar_webtoon.find(AR_TITLE_TYPE).text.strip()
        url = ar_webtoon.find("a", class_=AR_URL_CLASS)["href"].strip()
        list = ar_webtoon.find("li")
        chapter = list.find("a").text.strip().partition("Chapter ")[2]
        print(title)
