from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('events/<int:event_id>/', views.events_detail, name='events_detail'),
    path('events/<int:event_id>/attend/', views.attend_event, name='attend'),
    path('events/<int:event_id>/cancel_attend/', views.cancel_attend_event, name='cancel_attend')
]