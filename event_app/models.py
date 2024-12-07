import datetime

from django.db.models import Sum
from django.utils.timezone import make_aware
from django.db import models
from django.contrib.auth.models import User

# Create a naive datetime
# naive_datetime = datetime(2024, 1, 12, 19, 0, 0)

# Convert to aware datetime
# aware_datetime = make_aware(naive_datetime)

# Save the Event
# event = Event.objects.create(name="Concert", date=aware_datetime)

# Create your models here.

# Event Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    available_seats = models.PositiveIntegerField()
    image = models.ImageField(max_length=255, default='images/', blank=True, null=True)
    image_path=models.ImageField(max_length=255, default='images/default.jpg')
    total_tickets = models.PositiveIntegerField()

    def tickets_booked(self):
        # Aggregate the total quantity of booked tickets
        return self.bookings.aggregate(total=Sum('quantity'))['total'] or 0

    def tickets_available(self):
        # Calculate remaining tickets
        return self.total_tickets - self.tickets_booked()

    def __str__(self):
        return self.name


# Booking Model
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.event.name} - {self.quantity} tickets"

    # Ensure available seats are reduced during booking
    def save(self, *args, **kwargs):
        if not self.pk:  # New booking
            if self.quantity > self.event.available_seats:
                raise ValueError("Not enough seats available!")
            self.event.available_seats -= self.quantity
            self.event.save()
        super().save(*args, **kwargs)


# User Profile Model (Optional)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

