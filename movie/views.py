from django.utils import timezone
from django.shortcuts import render, HttpResponse, redirect
import requests
from bs4 import BeautifulSoup as bs

from .models import SearchResult, Movie

# Create your views here.
def search_move(request, keyword=None):

    if request.method == "POST":
        keyword = request.POST["keyword"]

        if not keyword:
            return redirect("search")

        results = SearchResult.objects.filter(keyword=keyword).order_by('-search_date')

        if results:
            recent = results[0]
            if recent.search_date - timezone.now() > timezone.timedelta(days=1):
                return redirect("search-result", keyword=keyword)

        i = 1

        search_result = SearchResult.objects.create(
            keyword=keyword
        )

        while True:

            print("크롤링 시작")

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
        return redirect("search-result", keyword=keyword)

    if keyword:
        result = SearchResult.objects.filter(keyword=keyword).order_by('-search_date')

        if result[0].movie_set.all():
            return render(request, "search.html", {'result': result[0]})
        else:
            return render(request, "search.html", {'result': False})

    return render(request, "search.html")