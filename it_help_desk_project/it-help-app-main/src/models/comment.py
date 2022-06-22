from django.db import models
from .ticket import Ticket
from django.contrib.auth.models import User

class Comment(models.Model):
    '''
    Comment Model

    message: text field for user/tech to attach to ticket
    date_entered: auto generated, shows date/time comment is created
    user: one-to-many, one 'user' can have many 'comments' accross many 'tickets'
          shows who wrote the comment
    ticketNum: one-to-many, one 'ticket' can have many 'comments'
               Tickets should be able to list which comments are under it       
    '''
    message = models.TextField()
    date_entered = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    ticketNum = models.ForeignKey(Ticket, on_delete=models.PROTECT)

    '''
    Displays info in admin page
    '''
    def __str__(self) -> str:
        return '{ticketNum} | {message} - {user}'.format(ticketNum=self.ticketNum, message=self.message, user=self.user)
