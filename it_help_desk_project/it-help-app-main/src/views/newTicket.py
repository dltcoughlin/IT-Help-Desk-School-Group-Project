from src.models import *
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date

@login_required(login_url='/login')
def as_view(request):
    if request.method =='POST':
        currentUser = Profile.objects.get(username_id=request.user)
        currentUserGroup = getattr(currentUser, 'user_group')
        newTicket = Ticket()
        newTicket.status = "O"
        newTicket.priority = request.POST["priority"]
        newTicket.description = request.POST['description']
        newTicket.title = request.POST["title"]

        if request.POST["priority"] == 'R':
            due_date = date.today() + timedelta(days=5)
        elif request.POST["priority"] == 'U':
            due_date = date.today() + timedelta(days=3)
        else:
            due_date = date.today() + timedelta(days=1)
        newTicket.due_date = due_date

        #Saves the ticket then add the new ticket to the user
        #If current user is a tech, it will save the ticket under
        #the user they selected.  If a normal user, the ticket will
        #be saved to themselves
        try:
            newTicket.save()
            if(currentUserGroup == 'T'):
                selectedUser = request.POST["users"]
                createdForUser = Profile.objects.get(username_id__username=selectedUser)
                createdForUser.user_ticket.add(newTicket)
            else:
                currentUser.user_ticket.add(newTicket)
                print('else')
        except:
            args = {}
            text = "Submission Failed"
            args['error'] = text
            return render(request, 'createNewTicket.html', args)
        return redirect('/home')

    #Allows techs to select a user to create a ticket, or themselves
    currentUser = Profile.objects.get(username_id=request.user)
    currentUserGroup = getattr(currentUser, 'user_group')
    users = {}
    if(currentUserGroup == 'T'):
        users = Profile.objects.filter(user_group='U') | Profile.objects.filter(username_id=request.user)
    return render(request, 'createNewTicket.html', {'currentUserGroup' : currentUserGroup, 'users' : users})
