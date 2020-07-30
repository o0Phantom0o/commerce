from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class listing(models.Model):
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100, null=True)
    picture = models.CharField(max_length=300, null=True)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STATUS = (
        ('a', 'active'),
        ('d', 'disabled'),
        )
    status = models.CharField(max_length=1, choices=STATUS, default="a")

    def __str__(self):
        return f"{self.id}: {self.title}"

class bid(models.Model):
    listingId = models.ForeignKey(listing, on_delete=models.CASCADE)
    startingBid = models.IntegerField()
    currentPrice = models.IntegerField()
    highestBidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.listingId.title} - {self.currentPrice}"

class comments(models.Model):
    listingId = models.ForeignKey(listing, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class watch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listingId = models.ForeignKey(listing, on_delete=models.CASCADE)
    bidId = models.ForeignKey(bid, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.listingId.title} - {self.user.username}"