from django.shortcuts import render, HttpResponse
import requests
from bs4 import BeautifulSoup as bs

from .models import SearchResult, Movie

# Create your views here.
def search_move(request):

    if request.method == "POST":
        keyword = request.POST["keyword"]

        print(keyword)
        i = 1

        search_result = SearchResult.objects.create(
            keyword=keyword
        )

        while True:
            url = "http://www.cgv.co.kr/search/movie.aspx?query={}&page={}".format(keyword, i)
            i += 1

            response = requests.get(url)

            result = bs(response.text, "html.parser")

            try:
                ul = result.find("div", {'class': 'sect-chart'}).ul

                if len(ul.findAll("li")) == 0:
                    break

                for li in ul.findAll("li"):

                    Movie.objects.create(
                        name=li.find("strong").text,
                        img_url=li.img['src'],
                        release_date="-".join(li.i.text.split(".")),
                        search_result=search_result
                    )

            except AttributeError as ex:
                print(ex)
                break


    return render(request, "search.html")