#views.py in the Message app.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Conversation, Message
from cars.models import Car
from .forms import MessageForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from designpatterns.observer import ConcreteObserver, NotificationSystem

#method to show all convos based on user type
@login_required
def inbox(request):
    if request.user.is_superuser: 
        conversations = Conversation.objects.filter(owner=request.user).order_by("-last_updated")
    else: 
        conversations = Conversation.objects.filter(renter=request.user).order_by("-last_updated")

    return render(request, "message/inbox.html", {"conversations": conversations})


#method to delete a conversation
@login_required
def delete_conversation(request, conversation_id):
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, id=conversation_id)

       
        if request.user == conversation.owner or request.user == conversation.renter:
            conversation.delete()
            messages.success(request, "Conversation deleted successfully!")
        else:
            messages.error(request, "You are not authorized to delete this conversation.")
    
    return redirect("inbox")

#method to create message
@login_required
def chat_room(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user != conversation.renter and request.user != conversation.owner:
        return HttpResponse("Unauthorized", status=403)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['text']
            receiver = conversation.owner if request.user == conversation.renter else conversation.renter

            #create the message
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                receiver=receiver,
                text=message_text
            )

            #create the notification system (subject)
            notification_system = NotificationSystem()

            #create a concrete observer for the receiver (car owner or renter)
            observer = ConcreteObserver(receiver)
            
            #register the observer
            notification_system.register_observer(observer)

            #notify all observers (send notifications)
            notification_system.notify_observers(f"You have a new message from {request.user.username}.")

            #update the conversation with the latest message
            conversation.last_message = message.text

            conversation.save()

            return JsonResponse({
                "sender": message.sender.username,
                "text": message.text,
                "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    else:
        form = MessageForm()

    messages = Message.objects.filter(conversation=conversation).order_by("timestamp")

    return render(request, "message/chat.html", {
        "conversation": conversation,
        "messages": messages,
        "form": form,
    })

#method to begin a convo (car renter first time new convo)
@login_required
def start_conversation(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    owner = car.owner  


    conversation, created = Conversation.objects.get_or_create(
        renter=request.user,
        owner=owner,
        car=car
    )
    return redirect("chat_room", conversation_id=conversation.id)


