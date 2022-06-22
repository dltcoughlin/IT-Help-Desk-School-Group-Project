from django.urls import path
from src.views import home, searchticket, newTicket, getticketinfo, newComment, techOptions, logout

urlpatterns = [
    path('', home.as_view, name='home'),
    path('', newTicket.as_view, name='newticket'),
    path('', searchticket.as_view, name='searchticket'),
    path('', getticketinfo.as_view, name='getticket'),
    path('', newComment.as_view, name='newcommnet'),
    path('', techOptions.assign, name='assign'),
    path('', techOptions.assign, name='unassign'),
    path('', techOptions.close, name='close'),
    path('', techOptions.open, name='open'),
    path('', logout.as_view, name='logout'),
]
