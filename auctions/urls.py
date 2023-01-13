from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add-listing", views.add_listing, name="add-listing"),
    path("my-listing", views.my_listing, name="my-listing"),
    path("<int:listing_id>", views.listing_view, name="listing_view"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("add-watchlist/<int:listing_id>", views.add_watchlist, name="add-watchlist"),
    path("remove-watchlist/<int:listing_id>", views.remove_watchlist, name="remove-watchlist"),
    path("categories", views.categories_view, name="categories-view"),
    path("categories/<str:category_name>", views.categories, name="categories"),
    path("delete-listing/<int:listing_id>", views.delete_listing, name="delete-listing"),
    path("my-bid", views.my_bid, name="my-bid"),
]
