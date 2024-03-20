from .models import Notification

def send_notification(recipient, message):
    Notification.objects.create(recipient=recipient, message=message)

# When an invite or friend request is received:
# send_notification(recipient=user, message="You have received a friend request.")
