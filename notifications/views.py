from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from notifications.models import Notification
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from cars.models import Car, Booking
from django.http import HttpResponse
from django.utils.timezone import now


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
def submit_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Get the latest confirmed booking
    booking = Booking.objects.filter(car=car, is_confirmed=True).order_by("-end_date").first()

    if not booking:
        return HttpResponse("This car has no confirmed rental yet.", status=400)

    renter = booking.renter  
    reviewer = request.user  

    # Check if the booking is still ongoing or in the future
    if booking.end_date > now():
        return HttpResponse("You cannot leave a review until the booking has ended.", status=400)

    # Prevent duplicate reviews
    existing_review = Review.objects.filter(reviewer=reviewer, car=car).exists()
    if existing_review:
        return redirect("extra")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        review = Review.objects.create(
            car=car,
            reviewer=reviewer, 
            reviewed_user=renter, 
            rating=rating,
            comment=comment
        )
        review.save()

        return redirect('car_detail', pk=car.id)

    return render(request, "notifications/submit_review.html", {"car": car, "renter": renter})


@login_required
def extra(request):
    
    return render(request, 'notifications/extra.html')


