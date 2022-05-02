from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    path('', views.index, name="index"),
    path('employees', views.home, name="home"),
    path('add_employee/',views.home, name="home"),
    path('employees', views.employees, name="employees"),
    path('search_employees', views.search_employees, name='search_employees'),
    path('searchposts/',views.searchposts, name='searchposts'),
    path('date_range/',views.filter_by_date, name='filter_by_date'),

    # path('dns_lookup', views.dns_lookup, name='dns_lookup'),
]
