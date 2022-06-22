from src.models import *
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.utils import timezone

@login_required(login_url='/login')
def as_view(request):
    if request.method =='GET':
        currentTicket = Ticket.objects.get(ticketNum=request.GET["ticketNum"])
        ticketTitle = currentTicket.title

    if request.method =='POST':
       
        currentTicket = Ticket.objects.get(ticketNum=request.POST["ticketNum"])

        newComment = Comment()
        newComment.message = request.POST["message"]
        newComment.date_entered = timezone.now
        newComment.user = request.user
        newComment.ticketNum = currentTicket

        try:
            newComment.save()
        except:
            args = {}
            text = "Submission Failed"
            args['error'] = text
            return render(request, 'addNewComment.html', args)
        return redirect('/home')

    return render(request, 'addNewComment.html', {'ticketTitle': ticketTitle})
