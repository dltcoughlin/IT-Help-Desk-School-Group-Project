from src.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def ticketStatusKey(key):
    return 0 if key.status == "O" else 1

def ticketPriorityKey(key):
    return 0 if key.priority == "E" else 1 if key.priority == "U" else 2

# tickets are sorted by the following order:
# 1. ticket status (Open tickets before closed tickets)
# 2. ticket priority (Emergency is first; Routine i last)
# 3. date created (most recent is last)
def sort(tickets):
    tickets.sort(key=lambda key: key.date_created)
    tickets.sort(key=ticketPriorityKey)
    tickets.sort(key=ticketStatusKey)

@login_required(login_url='/login')
def as_view(request):

    #check to see who is logged in
    currentUser = Profile.objects.get(username_id=request.user)
    currentUserGroup = getattr(currentUser, 'user_group')

    #If current user is 'User' then only shows own tickets
    #Also hides 'All Ticket' link on home page
    if (currentUserGroup == 'U') :
        ticketQuery = Ticket.objects.filter(profile__username_id=request.user)
        noshow = "noshow"
    else:
        ticketQuery = Ticket.objects.all()
        noshow = "show"

    tickets = [ticket for ticket in ticketQuery]
    sort(tickets)
    return render(request, 'home.html', {'tickets': tickets, 'noshow':noshow})
