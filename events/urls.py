from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('events/<int:event_id>/', views.events_detail, name='events_detail'),
    path('events/<int:event_id>/attend/', views.attend_event, name='attend'),
    path('events/<int:event_id>/cancel_attend/', views.cancel_attend_event, name='cancel_attend'),
    path('search/', views.search_view, name='search'),
    path('notifications/', views.notifications, name='notifications'),
    path('events/<int:event_id>/invite/', views.invite_friends, name='invite_friends'),
    path('friend/<int:friend_id>/add/', views.add_friend, name='add_friend'),
    path('friend/<int:friend_id>/remove/', views.remove_friend, name='remove_friend'),
]