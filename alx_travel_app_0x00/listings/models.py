import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email}"
    


class Listing(models.Model):
      id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      host = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='listings'
      )
      name = models.CharField(max_length=50, blank=True, null=True)
      description = models.TextField()
      location = models.CharField(max_length=255)
      price_per_unit = models.DecimalField(max_digits=10,decimal_places=2)
      created_at = models.TimeField(auto_now_add=True)
      updated_at = models.TimeField(auto_now=True)

      def __str__(self):
            return f"{self.name} - {self.location}"



class Booking(models.Model):
           id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
           listing = models.ForeignKey(
                 Listing,
                 on_delete=models.CASCADE,
                 related_name='bookings'
           )
           user = models.ForeignKey(
                 User,
                 on_delete=models.CASCADE,
                 related_name='bookings'
           )
           start_date = models.DateField()
           end_date = models.DateField()
           total_price = models.DecimalField(max_digits=10, decimal_places=2)
           status = models.CharField(
                 max_length=10,
                 choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'canceled')],
                 default='pending')
           created_at = models.TimeField()

           def __str__(self):
                 return f"Booking by {self.user.email} for {self.listing.name}"


class Review(models.Model):
      id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      listing = models.ForeignKey(
            Listing,
            on_delete=models.CASCADE,
            related_name="reviews"
      )
      user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='reviews'
      )
      rating = models.PositiveSmallIntegerField()
      comment = models.TextField(blank=True, null=True)
      created_at = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return f"Review {self.rating}/5 by {self.user.email}"
