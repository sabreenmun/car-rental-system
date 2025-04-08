from django.urls import path
from .views import *

#paths for navigation
urlpatterns = [
    path("inbox/", inbox, name="inbox"),
    path("chat/<int:conversation_id>/", chat_room, name="chat_room"),
    path("start-conversation/<int:car_id>/", start_conversation, name="start_conversation"),
    path("delete-conversation/<int:conversation_id>/", delete_conversation, name="delete_conversation"),
]
