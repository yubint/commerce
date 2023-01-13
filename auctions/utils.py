from django.shortcuts import render


def listing_error(request, listing, message):
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'message': message
    })