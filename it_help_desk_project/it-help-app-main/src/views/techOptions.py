from src.models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone



#Assignes current tech to ticket
@login_required(login_url='/login')
def assign(request):

    #Checks if tech is currently assigned to ticket
    if request.method =='GET':
        currentTicket = Ticket.objects.get(ticketNum=request.GET["ticketNum"])
        ticketTitle = currentTicket.title
        usersAssigned = Profile.objects.filter(user_ticket = currentTicket.ticketNum)
        userList = list(usersAssigned.values_list('username', flat=True))

        isAssigned = False
        for user in userList:
            if  user == request.user.pk:
                isAssigned = True

    #Assigns tech to ticket if 'Yes' is clicked            
    if request.method =='POST':
        currentTicket = Ticket.objects.get(ticketNum=request.POST["ticketNum"])
        currentUser = Profile.objects.get(username_id=request.user)

        if request.POST["submit"] == "Yes":
            currentUser.user_ticket.add(currentTicket)
            Ticket.objects.filter(ticketNum=request.POST["ticketNum"]).update(is_assigned=True)
            return redirect('/home')
        elif request.POST["submit"] == "No":
            print("not assigned")
            return redirect('/home')
        else:
            print("back")
            return redirect('/home')

    return render(request, 'assignTicket.html', {'isAssigned': isAssigned, 'ticketTitle': ticketTitle})

#Assignes current tech to ticket
@login_required(login_url='/login')
def unassign(request):

    #Checks if tech is currently assigned to ticket
    if request.method =='GET':
        currentTicket = Ticket.objects.get(ticketNum=request.GET["ticketNum"])
        ticketTitle = currentTicket.title
        usersAssigned = Profile.objects.filter(user_ticket = currentTicket.ticketNum)
        userList = list(usersAssigned.values_list('username', flat=True))

        isAssigned = False
        for user in userList:
            if  user == request.user.pk:
                isAssigned = True

    #Assigns tech to ticket if 'Yes' is clicked            
    if request.method =='POST':
        currentTicket = Ticket.objects.get(ticketNum=request.POST["ticketNum"])
        currentUser = Profile.objects.get(username_id=request.user)

        if request.POST["submit"] == "Yes":
            currentUser.user_ticket.remove(currentTicket)

            isStillAssigned = bool(Profile.objects.filter(user_ticket=request.POST["ticketNum"]).filter(user_group='T'))
            if not isStillAssigned:
                Ticket.objects.filter(ticketNum=request.POST["ticketNum"]).update(is_assigned=False)




            return redirect('/home')
        elif request.POST["submit"] == "No":
            print("not assigned")
            return redirect('/home')
        else:
            print("back")
            return redirect('/home')

    return render(request, 'unassignTicket.html', {'isAssigned': isAssigned, 'ticketTitle': ticketTitle})

#Closes current ticket
@login_required(login_url='/login')
def close(request):

    if request.method =='GET':
        currentTicket = Ticket.objects.get(ticketNum=request.GET["ticketNum"])
        ticketTitle = currentTicket.title

    if request.method =='POST':
        if request.POST["submit"] == "Yes":
            Ticket.objects.filter(ticketNum=request.POST["ticketNum"]).update(status='C')
            Ticket.objects.filter(ticketNum=request.POST["ticketNum"]).update(date_closed=timezone.now())
            return redirect('/home')
        else:
            return redirect('/home')
    return render(request, 'close.html', {'ticketTitle': ticketTitle})

#Re-opens current ticket
@login_required(login_url='/login')
def open(request):

    if request.method =='GET':
        currentTicket = Ticket.objects.get(ticketNum=request.GET["ticketNum"])
        ticketTitle = currentTicket.title

    if request.method =='POST':
        if request.POST["submit"] == "Yes":
            Ticket.objects.filter(ticketNum=request.POST["ticketNum"]).update(status='O')
            Ticket.objects.filter(ticketNum=request.POST["ticketNum"]).update(date_closed=None)
            return redirect('/home')
        else:
            return redirect('/home')
    return render(request, 'open.html', {'ticketTitle': ticketTitle})
