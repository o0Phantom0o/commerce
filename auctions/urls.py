from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("listings/<str:entry_id>", views.entry, name="entry"),
    path("category/<str:category_id>", views.category, name="category"),
    path("newbid", views.newbid, name="newbid"),
    path("comment", views.comment, name="comment"),
    path("close", views.close, name="close")
]
