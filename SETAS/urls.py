from django.conf.urls import include, url
from django.contrib import admin
from webapp import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', views.quit,  name="logout"),
    url(r'^index/$', views.index, {"template_name": "index.html"}, name="index"),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^search/paper/$', views.search, {"template_name": "search_paper.html"}, name="to_search_paper"),
    url(r'^paper/detail/(?P<paperId>\w+)/$', views.detail, {"template_name": "paper_content.html"}, name="to_paper_content"),
    url(r'^auther/search/$', views.searchAuthor, {"template_name": "search_auther.html"}, name="to_search_auther"),
    url(r'^auther/content/(?P<authorId>\d+)/$', views.authorContent, {"template_name": "auther_content.html"}, name="to_auther_content"),

    url(r'^keyword/history/$', views.keyword_history, {"template_name": "keyword_history.html"}, name="to_keyword_history"),
    url(r'^search/keyword/$', views.search_keyword, {"template_name": "search_keyword.html"}, name="to_keyword_search"),
    url(r'^keyword/trend/(?P<keyword>\w+)/$', views.keyword_trend, {"template_name": "keyword_trend.html"}, name="keyword_trend"),
]
