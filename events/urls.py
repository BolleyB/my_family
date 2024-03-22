from django.urls import path
from . import views
from .views import send_invitation

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('events/<int:event_id>/', views.events_detail, name='events_detail'),
    path('events/<int:event_id>/attend/', views.attend_event, name='attend'),
    path('events/<int:event_id>/cancel_attend/', views.cancel_attend_event, name='cancel_attend'),
    path('search/', views.search_view, name='search'),
    path('notifications/', views.notifications, name='notifications'),
    path('invitation/<str:invitation_id>/join/', views.join_event, name='join_event'),
    path('notifications/', views.notification_list, name='notification_list'),  # Include this line
    path('search/', views.search_users, name='search_users'),
    path('events/<int:event_id>/send_invitation/', views.send_invitation, name='send_invitation')

]