from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/delete/<int:listing_id>", views.remove_listing, name="remove_listing"),
    path("listing/details/<int:listing_id>", views.listing_details, name="listing_details")
]
