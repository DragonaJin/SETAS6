from django.conf.urls import include, url
from django.contrib import admin
from webapp import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.index, {"template_name": "index.html"}, name="index"),
    url(r'^search/paper/$', views.goto, {"template_name": "search_paper.html"}, name="to_search_paper"),
    url(r'^paper/content/$', views.goto, {"template_name": "paper_content.html"}, name="to_paper_content"),
    url(r'^keyword/history/$', views.goto, {"template_name": "keyword_history.html"}, name="to_keyword_history"),
    url(r'^keyword/search/$', views.goto, {"template_name": "search_keyword.html"}, name="to_keyword_search"),
    url(r'^auther/search/$', views.goto, {"template_name": "search_auther.html"}, name="to_search_auther"),
    url(r'^auther/content/$', views.goto, {"template_name": "auther_content.html"}, name="to_auther_content"),
    url(r'^keyword/trend/$', views.goto, {"template_name": "keyword_trend.html"}, name="keyword_trend"),

]
