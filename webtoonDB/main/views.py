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
    PAGES = 6
    webtoon_list = Webtoon.objects.all()
    pages = PAGES
    for page in range(1, pages):
        html_text = requests.get(
            f"https://www.mreader.co/jumbo/manga/?results={page}"
        ).text
        soup = BeautifulSoup(html_text, "lxml")
        grid = soup.find("ul", class_="novel-list grid col col2 chapters")
        webtoons = grid.find_all("li", class_="novel-item")

        for webtoon in webtoons:
            title = webtoon.find("h4", class_="novel-title text1row").text.strip()
            if Webtoon.objects.filter(title=title).exists():
                url = webtoon.find("a", class_="list-body")["href"].strip()
                chapter = (
                    webtoon.find("h5", class_="chapter-title text1row")
                    .text.strip()
                    .partition("Chapter ")[2]
                )
                if "eng" in chapter:
                    chapter_parts = chapter.split("-")
                    if chapter_parts[1].isdigit():
                        chapter = f"{chapter_parts[0]}.{chapter_parts[1]}"
                    else:
                        chapter = chapter_parts[0]
                    W = Webtoon.objects.get(title=title)
                    W.url = url
                    W.available_ch = float(chapter)
                    W.save()

    return render(response, "main/index.html", {"webtoon_list": webtoon_list})
