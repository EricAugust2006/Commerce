from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError

class User(AbstractUser):
    def __str__(self):
        return self.username

class Listings(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.ImageField(upload_to='listing/images', blank=True, null=True)  
    category = models.CharField(max_length=255, default='General')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title
     
class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids") 
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    
    def clean(self):
        if self.listing.created_by == self.user:
            raise ValidationError("You cannot bid on your own listing.")

        if self.amount <= self.listing.price:
            raise ValidationError("Your bid must be higher than the current price")
        
        if self.amount <= 0:
            raise ValidationError("Bid amount must be positive")
         
        if Bids.objects.filter(listing=self.listing, amount=self.amount).exists():
            raise ValidationError("This bid amount has already been placed. Please offer a higher amount.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"
    
    class Meta:
        unique_together = ("user", "listing")

class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"

