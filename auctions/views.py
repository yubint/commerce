from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Bid, Comment, Listing, Category
from . import utils

CATEGORY = [x.category for x in Category.objects.all()]

def index(request):
    listings = Listing.objects.filter(closed=False)
    return render(request, "auctions/index.html", {'listings' : listings})


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

@login_required(login_url='login')
def watchlist(request):
    user_watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })

@login_required(login_url='login')
def add_listing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title')
        price = request.POST.get('price')
        image = request.POST.get('image')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        if category_name not in CATEGORY and category_name != 'None':
            return render(request, "auctions/addlisting.html", {
                'message': 'The category is not available'
            })
        try:
            new_listing = Listing(title = title, price = float(price), image = image , description = description, user = user)
            if category_name == 'None':
                new_listing.save()
            else:
                new_listing.category= Category.objects.get(category=category_name)
                new_listing.save()
            return HttpResponseRedirect(reverse("my-listing"))
        except IntegrityError:
            return render(request, "auctions/addlisting.html", {
                'message' : 'Error While adding the Listing. Please try again.'
            })
    return render(request, "auctions/addlisting.html", {
        'categories': CATEGORY
    })


@login_required(login_url='login')
def my_listing(request):
    user = request.user
    listings = Listing.objects.filter(user=user)
    return render(request, "auctions/mylisting.html", {
        "listings": listings
    })

def listing_view(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    return render(request, "auctions/listing.html", {
        'listing': listing
    })

@login_required(login_url='login')
def bid(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        try:
            bid_value = int(request.POST.get('bid'))
        except TypeError:
            return utils.listing_error(request, listing, 'Error Bidding')
        if listing.highest_bid is None:
            if bid_value < listing.price:
                return utils.listing_error(request, listing, "Your bid value is lower than the price")
        else:
            if bid_value < listing.highest_bid.value:
                return utils.listing_error(request, listing, 'You bid value is lower than the highest value')
        try:
            new_bid = Bid(value=bid_value, listing=listing, user=user)
            new_bid.save()
            listing.highest_bid = new_bid
            listing.save()
        except IntegrityError:
            return utils.listing_error(request,listing, "Error Bidding")
        return HttpResponseRedirect(reverse('listing_view', args=[listing_id]))

@login_required(login_url='login')
def comment(request, listing_id):
    if request.method == 'POST':
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        comment_text = request.POST.get('comment') 
        if not comment_text:
            return utils.listing_error(request,listing, "Error Posting the comment")
        try:
            new_comment = Comment(comment=comment_text, listing=listing, user=user)
            new_comment.save()
        except IntegrityError:
            return utils.listing_error(request, listing, "Error Posting the comment")
        return HttpResponseRedirect(reverse('listing_view', args=[listing_id]))
    else:
        return HttpResponseRedirect(reverse('listing_view', args=[listing_id]))

@login_required(login_url='login')
def add_watchlist(request, listing_id):
    if request.method == 'POST':
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        listing.watchlisted_by.add(user)
    return HttpResponseRedirect(reverse('listing_view', args=[listing_id]))

@login_required(login_url='login')
def remove_watchlist(request, listing_id):
    if request.method == 'POST':
        user = request.user
        listing = Listing.objects.get(pk = listing_id)
        listing.watchlisted_by.remove(user)
    return HttpResponseRedirect(reverse('listing_view', args=[listing_id]))

def categories_view(request):
    return render(request, "auctions/categories_view.html", {
        'categories': CATEGORY, 
    })

def categories(request, category_name):
    category_listing = Category.objects.get(category=category_name).listing.all()
    return render(request, "auctions/categories.html", {
        'category': category_name,
        'category_listing': category_listing,
    })

@login_required(login_url='login')
def delete_listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    if listing.user != user:
        return utils.listing_error(request, listing, "You don't own this listing")
    try:
        listing.delete()
    except IntegrityError:
        return utils.listing_error(request,listing, "Error deleting this listing")
    return HttpResponseRedirect(reverse('my-listing'))

@login_required(login_url='login')
def my_bid(request):
    user = request.user
    bids = user.bids.all()
    # creating a list of tuples containing listing and bids for easy access of data
    listing_bid = []
    for bid in bids:
        listing = bid.listing
        listing_bid.append((listing, bid))
    print(listing_bid)
    return render(request, "auctions/mybid.html", {
        'listing_bid': listing_bid, 
    })

@login_required(login_url='login')
def close_listing(request, listing_id):
    if request.method == 'POST':
        print('hi')
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        if listing.user != user:
            return utils.listing_error(request, listing, "You don't own the listing")
        try:
            listing.closed = True
            listing.save()
        except IntegrityError:
            return utils.listing_error(request, listing, "Error closing the listing")
    
    return HttpResponseRedirect(reverse('my-listing'))

@login_required(login_url='login')
def won_bids(request):
    user = request.user
    # filters listing that are closed and the highest bidder is the user. '__' is used to get attribute of the user
    listings = Listing.objects.filter(closed= True).filter(highest_bid__user = user)
    return render(request, 'auctions/wonlostbids.html', {
        'listings': listings,
        'status': 'Won',
    })

@login_required(login_url='login')
def lost_bids(request):
    user = request.user
    listings = Listing.objects.filter(closed=True).exclude(highest_bid__user= user)
    return render(request, 'auctions/wonlostbids.html', {
        'listings':listings,
        'status': 'Lost',
    })
