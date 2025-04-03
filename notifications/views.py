from datetime import date
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from notifications.models import Notification
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from cars.models import Car, Booking
from django.http import HttpResponse
from django.utils import timezone



@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notifications.html', {'notifications': user_notifications})


@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    if notification.user == request.user:
        notification.delete()
        messages.success(request, "Notification deleted successfully!")
    else:
        messages.error(request, "You are not authorized to delete this notification.")
    
    return redirect('notifications')

@login_required
def submit_review(request, booking_id):
    # Fetch the booking by its ID
    booking = get_object_or_404(Booking, id=booking_id, renter=request.user)

    # Check if the booking has ended (end_date is before today's date)
    if booking.end_date > date.today():
        return HttpResponse("You cannot leave a review until the booking has ended.", status=400)

    # Prevent duplicate reviews for the same booking
    existing_review = Review.objects.filter(booking=booking).exists()
    if existing_review:
        messages.error(request, "You have already left a review for this booking.")
        return redirect('my_bookings')
    
    # Ensure the logged-in user is the renter of the booking
    if booking.renter != request.user:
        return HttpResponse("You can only review your own bookings.", status=400)

    # Process the form submission if it's a POST request
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        reviewed_user = booking.car.owner
        car = booking.car
         # Create the review
        review = Review.objects.create(
            booking=booking,  # Link the review to the booking
            reviewer=request.user,  # The user leaving the review
            reviewed_user=reviewed_user,  # The user being reviewed (the car owner in this case)
            car = car,
            rating=rating,
            comment=comment
        )
        review.save()

        # Redirect to the car detail page after review submission
        return redirect('my_bookings')

    # Render the review submission form
    return render(request, "notifications/submit_review.html", {"booking": booking})

@login_required
def extra(request):
    
    return render(request, 'notifications/extra.html')

