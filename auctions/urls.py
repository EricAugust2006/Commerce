from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("listing/delete/<int:listing_id>/", views.remove_listing, name="remove_listing"),
    path("listing/details/<int:listing_id>/", views.listing_details, name="listing_details"),
    path('listing/edit/<int:listing_id>/', views.edit_list, name="edit_list"),
    path("place_bid/<int:listing_id>/", views.place_bid, name="place_bid"),
    path('add_watchlist/<int:listing_id>/', views.add_watchlist, name='add_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('watchlist/remove/<int:listing_id>/', views.remove_watchlist, name="remove_watchlist" ),
]

