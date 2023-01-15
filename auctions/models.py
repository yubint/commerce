from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender='auctions.Bid')
def delete_function_for_highest_bid(sender, **kwargs):
    bid = kwargs['instance']
    listing = bid.listing
    if listing.highest_bid == bid:
        try:
            new_highest_bid = listing.bids.all().order_by('-value')[1]
            listing.highest_bid = new_highest_bid
            listing.save()
        except IndexError:
            listing.highest_bid = None 
            listing.save()

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True, blank= True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='listings')
    highest_bid = models.ForeignKey('Bid', on_delete = models.DO_NOTHING, null=True, blank=True, related_name= 'highest_of')
    category = models.ForeignKey('Category', on_delete= models.PROTECT, related_name='listing', null=True, blank=True)
    watchlisted_by = models.ManyToManyField(User, related_name='watchlist', blank=True)
    closed = models.BooleanField(default=False)

class Bid(models.Model):
    value = models.FloatField()
    made_on = models.DateTimeField(auto_now_add= True)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'bids')
class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete= models.SET_DEFAULT, related_name='comments', default='deleted')
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name='comments')
    
class Category(models.Model):
    category = models.CharField(max_length=30)

