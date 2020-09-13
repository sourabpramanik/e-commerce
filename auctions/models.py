from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class User(AbstractUser):
  pass


class Category(models.Model):
    field= models.CharField(max_length= 64)

    def __str__(self):
        return self.field

    def get_absolute_url(self):
        return reverse('home')
    

class Listings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owneditems")
    product_name= models.CharField(max_length= 64)
    description= models.CharField(max_length=2048, default='')
    date_time= models.DateTimeField(auto_now=False, auto_now_add=True)
    image= models.CharField(max_length=2048, null=True, blank= True)
    price= models.DecimalField(max_digits= 10, decimal_places=2, default="")
    category = models.CharField(max_length=64, blank=False)
    closed = models.BooleanField(default=False)
    watchlistusers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def current_price(self):
        return max([bid.bid for bid in self.bids.all()]+[self.price])

    def no_of_bids(self):
        return len(self.bids.all())

    def current_winning_bidder(self):
        return self.bids.get(bid=self.current_price()).user if self.no_of_bids() > 0 else None

    def __str__(self):
        return f"{self.product_name} {self.description} {self.price} {self.date_time}"



class Bid(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")

    def clean(self):
        print(self.bid)
        print(self.listing.current_price())
        if self.bid and self.listing.current_price():
            if self.bid <= self.listing.current_price():
                raise ValidationError({'bid': ('Warning!! Your bidding value should be higher than the current price of the item!')})

    def __str__(self):
        return f"{self.user} last bid is ${self.bid} for the listing: {self.listing}"


class Comment(models.Model):
    post= models.ForeignKey(Listings, on_delete=models.CASCADE, related_name= "comments", null= True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body= models.TextField()
    post_time= models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.author} says {self.body} for listing: {self.post}"