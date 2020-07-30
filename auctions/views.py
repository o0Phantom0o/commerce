from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import User, listing, bid, comments, watch


def index(request):
    bids = bid.objects.filter(listingId__status="a")

    return render(request, "auctions/index.html", {
        "bids": bids
        })

def entry(request, entry_id):
    entry = listing.objects.get(id=entry_id)
    bids = bid.objects.get(listingId=listing.objects.get(id=entry_id))
    allcomments = comments.objects.filter(listingId=entry)
    winner = bids.highestBidder

    watchlistcheck = watch.objects.filter(user=request.user, listingId=entry_id)
    if len(watchlistcheck) > 0:
        watchlistbutton = "Remove from Watchlist"

    else:
        watchlistbutton = "Add to Watchlist"

    if entry.status == "a":
        return render(request, "auctions/entry.html", {
            "entry": entry,
            "bid": bids,
            "comments": allcomments,
            "watchlist": watchlistbutton
            })
    
    else:
        return render(request, "auctions/closed.html", {
            "message": "This listing has been closed!",
            "winner": winner
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

@login_required(redirect_field_name="login_view")
def create(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["startingBid"]
        picUrl = request.POST["picUrl"]
        category = request.POST["category"]

        if title is not "" and description is not "" and startingBid is not "":

            newList = listing(title=title, category=category, picture=picUrl, description=description)

            newBid = bid(listingId=newList, startingBid=startingBid, currentPrice=startingBid)

            newList.save()
            newBid.save()

            return render(request, "auctions/create.html", {
                "message": "Listing Created!"
                })

        else:
            return render(request, "auctions/create.html", {
                "message": "Listing must include a title, description and a starting bid!"})

    else:
        return render(request, "auctions/create.html")


@login_required(redirect_field_name="login_view")
def watchlist(request):
    if request.method == "POST":
        user = request.user
        list = listing.objects.get(id=request.POST["listing"])
        bidid = bid.objects.get(listingId=list)
        
        check = watch.objects.filter(user=user, listingId=list)

        if len(check) > 0:
            instance = watch.objects.get(user=user, listingId=list)
            instance.delete()
            message = "Removed from watchlist"


        else:
            add = watch(user=user, listingId=list, bidId=bidid)
            add.save()
            message = "added to watchlist"

        return render(request, "auctions/watchlist.html", {
            "message": message
            })
    else:
        list = watch.objects.filter(user = request.user)

        return render(request, "auctions/watchlist.html", {
            "list": list,
            })

@login_required(redirect_field_name="login_view")
def categories(request):
    bids = bid.objects.all()
    list = listing.objects.order_by().values('category').distinct()
    return render(request, "auctions/categories.html", {
        "bids": bids,
        "list": list
        })

@login_required(redirect_field_name="login_view")
def category(request, category_id):
    list = bid.objects.filter(listingId__category=category_id)

    return render(request, "auctions/category.html", {
        "list": list
        })

@login_required(redirect_field_name="login_view")
def newbid(request):
    if request.method == 'POST':

        title = request.POST["title"]
        newbid = request.POST["newbid"]

        currentprice = request.POST["currentprice"]

        if newbid > currentprice:
            update = bid.objects.get(id=request.POST["bidid"])
            update.currentPrice = newbid
            update.highestBidder = request.user

            update.save()
            return render(request, "auctions/newbid.html", {
                "title": title,
                "message": "Your bid has been accepted as the highest bid"
                })

        else:
            return render(request, "auctions/newbid.html", {
                "title": title,
                "message": "Your bid is lower than the current price"
                })

        return render(request, "auctions/newbid.html", {
            "title": title,
            "message": currentPrice
            })

@login_required(redirect_field_name="login_view")
def comment(request):
    if request.method == 'POST':
        user = request.user
        newcomment = request.POST["newcomment"]
        listingid= request.POST["listingid"]

        item = listing.objects.get(id=listingid)

        new = comments(user=request.user, listingId=item, comment=newcomment)
        new.save()

        return HttpResponseRedirect(reverse("entry", kwargs= {
            "entry_id": listingid
            }))

@login_required(redirect_field_name="login_view")
def close(request):
    if request.method == 'POST':
        user = request.user.username
        creator = request.POST["creator"]
        listid = request.POST["listid"]
        winner = request.POST["winner"]

        list = listing.objects.get(id=request.POST["listid"])

        if creator == user:

            list.status = "d"
            list.save()

            return render(request, "auctions/closed.html", {
                "message": "This listing has been closed!",
                "winner": winner
                })
        else:
            return render(request, "auctions/closed.html", {
                "message": "You are not the creator of this listing!"
                })