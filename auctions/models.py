from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField(null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='listings')
    highest_bid = models.ForeignKey('Bid', on_delete = models.PROTECT, null=True, related_name= 'highest_of')
    category = models.ForeignKey('Category', on_delete= models.PROTECT, related_name='listing', null=True)
    watchlisted_by = models.ManyToManyField(User, related_name='watchlist')

class Bid(models.Model):
    value = models.FloatField()
    made_on = models.DateTimeField(auto_now_add= True)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'bids')
class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete= models.SET_DEFAULT, related_name='comments', default='delete')
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name='comments')
    
class Category(models.Model):
    category = models.CharField(max_length=30)
