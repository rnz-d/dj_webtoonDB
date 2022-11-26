from django.shortcuts import render
from .models import Webtoon

from bs4 import BeautifulSoup
import requests

# Create your views here.


def index(response):
    webtoon_list = Webtoon.objects.all()
    if response.method == "POST":
        title = response.POST.get("title")
        site = response.POST.get("site")
        finished_ch = response.POST.get("finished_ch")
        if Webtoon.objects.filter(title=title).exists():
            W = Webtoon.objects.get(title=title)
            W.site = site if site else "MR"
            W.finished_ch = finished_ch if finished_ch else 0
            W.save()
        else:
            W = Webtoon(
                title=title,
                site=site if site else "MR",
                finished_ch=finished_ch if finished_ch else 0,
            )
            W.save()
    return render(response, "main/index.html", {"webtoon_list": webtoon_list})


def scrape(response):
    webtoon_list = Webtoon.objects.all()

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

        for ar_webtoon in ar_webtoons:
            title = ar_webtoon.find(AR_TITLE_TYPE).text.strip()
            if Webtoon.objects.filter(title=title).exists():
                W = Webtoon.objects.get(title=title)
                if W.site == "AR":
                    url = ar_webtoon.find("a", class_=AR_URL_CLASS)["href"].strip()
                    list = ar_webtoon.find("li")
                    chapter = list.find("a").text.strip().partition("Chapter ")[2]
                    W.url = url
                    W.available_ch = float(chapter)
                    W.save()

    MR_PAGES = 6
    MR_GRID_TYPE = "ul"
    MR_GRID_CLASS = "novel-list grid col col2 chapters"
    MR_WEBTOON_TYPE = "li"
    MR_WEBTOON_CLASS = "novel-item"
    MR_TITLE_TYPE = "h4"
    MR_TITLE_CLASS = "novel-title text1row"
    MR_URL_CLASS = "list-body"
    MR_CHAPTER_TYPE = "h5"
    MR_CHAPTER_CLASS = "chapter-title text1row"

    mr_pages = MR_PAGES
    for page in range(1, mr_pages):
        mr_html_text = requests.get(
            f"https://www.mreader.co/jumbo/manga/?results={page}"
        ).text
        mr_soup = BeautifulSoup(mr_html_text, "lxml")
        mr_grid = mr_soup.find(MR_GRID_TYPE, class_=MR_GRID_CLASS)
        mr_webtoons = mr_grid.find_all(MR_WEBTOON_TYPE, class_=MR_WEBTOON_CLASS)

        for mr_webtoon in mr_webtoons:
            title = mr_webtoon.find(MR_TITLE_TYPE, class_=MR_TITLE_CLASS).text.strip()
            if Webtoon.objects.filter(title=title).exists():
                W = Webtoon.objects.get(title=title)
                if W.site == "MR":
                    url = mr_webtoon.find("a", class_=MR_URL_CLASS)["href"].strip()
                    chapter = (
                        mr_webtoon.find(MR_CHAPTER_TYPE, class_=MR_CHAPTER_CLASS)
                        .text.strip()
                        .partition("Chapter ")[2]
                    )
                    if "eng" in chapter:
                        chapter_parts = chapter.split("-")
                        if chapter_parts[1].isdigit():
                            chapter = f"{chapter_parts[0]}.{chapter_parts[1]}"
                        else:
                            chapter = chapter_parts[0]
                        W.url = url
                        W.available_ch = float(chapter)
                        W.save()

    return render(response, "main/index.html", {"webtoon_list": webtoon_list})
