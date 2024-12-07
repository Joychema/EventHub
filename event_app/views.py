import logging
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Sum
from event_management import settings
logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# from django.core.mail import send_email
from event_app.models import Event, Booking


# Create your views here.

def event_list(request):
    events = Event.objects.all() # Retrieve all events from the database
    return render(request,'event_list.html',{'events':events})

def event_detail(request,event_id):
    event = get_object_or_404(Event, pk=event_id) # Get the event by ID or return a 404 if not found

    # calculates the total booked tickets
    total_booked=event.bookings.aggregate(total=Sum('quantity'))['total'] or 0

    # calculates available_tickets
    available_tickets=event.total_tickets - total_booked

    # Calculate the max quantity that can be booked
    max_quantity=event.total_tickets - total_booked

    return render(request,'event_detail.html',{'event':event, 'total_booked':total_booked, 'available_tickets':available_tickets, 'max_quantity':max_quantity})

@login_required  # Ensure only authenticated users can book
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id) # Get the event by ID
    if request.method == 'POST':
        quantity=int(request.POST.get('quantity', 1))  # Get the quantity of tickets to book from the form
        if quantity < 1:
            messages.error(request, "Invalid quantity. Please select at least one ticket.")
            return redirect('event_detail', event_id=event.id)

        booking=Booking.objects.create(event=event, user=request.user, quantity=quantity)
        messages.success(request, f"You have successfully booked {quantity} ticket(s) for {event.name}! We have sent you a confirmation email, please check your email for more information.")

        # Send confirmation email
        send_mail(
            subject=f"Booking Confirmation: {event.name}",
            message=(
                f"Hello {request.user.username},\n\n"
                f"Thank you for booking {quantity} ticket(s) for the event '{event.name}'.\n"
                f"Event Details:\n"
                f"Date: {event.date}\n"
                f"Location: {event.location}\n\n"
                f"We look forward to seeing you there!"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        # send_email(subject, message)
        return redirect('event_list') # Redirect to the event list after booking
    return render(request,'book_event.html',{'event':event})

def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            logger.debug("User logged in successfully")

            fname=user.first_name
            return redirect('home')

            # return render(request,'event_list.html',{'fname':fname})
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, f"Account created for {username}😊")

        return redirect('login')
    return render(request,'register.html')


def logout1(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# def test_messages(request):
#     messages.success(request, "This is a success message!")
#     messages.error(request, "This is an error message!")
#     messages.warning(request, "This is a warning message!")
#     messages.info(request, "This is an info message!")
#     return render(request, 'base.html')

def debug_messages(request):
    storage = get_messages(request)
    for message in storage:
        print(f"Message: {message}")

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        # Add a friendly message for non-authenticated users
        if not request.user.is_authenticated:
            messages.info(request, "Please log in or register to book an event.")
        return super().dispatch(request, *args, **kwargs)

def home(request):
    return render(request,'home.html')