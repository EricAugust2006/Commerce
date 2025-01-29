from ast import Delete
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Listings, Bids, Comments

def index(request):
    listings = Listings.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        name_creator = request.POST.get("name_creator")
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        value = request.POST.get("value")
        image = request.FILES.get("image")
        
        try:
            user = User.objects.get(username = name_creator)
        except User.DoesNotExist:
            return render(request, 'auctions/create_listings.html', {
                "error_message": "User not found, Please check the name and try again"
            })
        
        new_listing = Listings(
            title = title,
            description = description, 
            category = category, 
            price = value,
            image_url = image,
            created_by = user
        )
        new_listing.save()
        redirect(reverse("index"))

    return render(request, "auctions/create_listing.html")
 
@login_required
def remove_listing(request, listing_id):
    listing = get_object_or_404(Listings, id = listing_id)

    if listing.created_by == request.user:
        listing.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/error.html', {
            "error_message": "Cannot remove this list"
        })

def listing_details(request, listing_id):
    try:
        listing = get_object_or_404(Listings, id=listing_id)
    except Listings.DoesNotExist:
        return render(request, 'auctions/error.html', {
            "message_error": "Listing not found!"
        })
    return render(request, 'auctions/listing_details.html', {
        "listing": listing
    })