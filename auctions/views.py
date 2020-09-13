from django.shortcuts import render
from .models import Listings, User, Bid, Comment, Category
from .forms import ListingsForm, BidForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listings.objects.filter(closed=False)
    })


@login_required
def createlisting(request):
    if request.method == "POST":
        form = ListingsForm(request.POST, request.FILES)
        try:
            newitem = form.save(commit=False)
            assert request.user.is_authenticated
            newitem.owner = request.user
            newitem.save()
            messages.success(request, "Your item is live now")
            return HttpResponseRedirect(reverse("index"))

        except ValueError:
            pass

    else:
        form = ListingsForm()
    return render(request, "auctions/createListing.html", {
        "form": form
    })


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


def listingpage(request, listing_id, bidform=None):
    
    listing = Listings.objects.get(pk=listing_id)
    print(listing.closed)
    if request.user.is_authenticated:
        is_watch_list = request.user.watchlist.filter(pk=listing_id).exists()
        if not bidform:
            bidform = BidForm()

        owner = listing.owner == request.user
    else:
        is_watch_list = None
        bidform = None
        owner = None

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'is_watchlist': is_watch_list,
        'form': bidform,
        'owner': owner
    })

@login_required
def createbid(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        bid = Bid(user=request.user, listing=listing)
        bidform = BidForm(request.POST, instance=bid)
        if bidform.is_valid():
            bidform.save()
            messages.success(request, "Your Bid is live now ")
        else:
            return listingpage(request, listing_id, bidform=bidform)

    return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))


@login_required
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        comment_content = request.POST['comment']
        comment = Comment(author=request.user, post=listing, body=comment_content)
        comment.save()
    return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))


@login_required
def watchlist(request, listing_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        user = request.user
        listing = Listings.objects.get(pk=listing_id)
        if user.watchlist.filter(pk=listing_id).exists():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))

@login_required
def watchlistitems(request):
    assert request.user.is_authenticated
    return render(request, "auctions/index.html", {
        'listings': request.user.watchlist.all(),
        'title': "Watchlist Items"
    })

@login_required
def closelisting(request, listing_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        listing = Listings.objects.get(pk=listing_id)
        print(request.user)
        print(listing.owner)
        print(listing.owner == request.user)
        if request.user == listing.owner:
            listing.closed = True
            listing.save()
    return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))

def category(request, category):
    listings= Listings.objects.filter(closed=False, category=category)
    return render(request, "auctions/index.html", {
        'category': category,
        'listings': listings
    })

def categories(request):
    categories = list(set([listing.category for listing in Listings.objects.all() if listing.category]))
    print(categories)
    return render(request, "auctions/categories.html", {
        'categories': categories
    })