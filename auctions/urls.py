from . import views
from django.contrib import admin 
from django.urls import path 



urlpatterns=[
    path("", views.index, name="index"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name= "logout"),
    path("listingpage/<int:listing_id>", views.listingpage, name= "listingpage"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("createbid/<int:listing_id>", views.createbid, name="createbid"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlistitems", views.watchlistitems, name="watchlistitems"),
    path("closelisting/<int:listing_id>", views.closelisting, name="closelisting"),
    path("categories/<str:category>", views.category, name='category'),
    path("categories", views.categories, name="categories")
]