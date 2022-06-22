from django.db import models

class Ticket(models.Model):
    '''
    Choices for the current status of tickets on 'status'
    '''
    STATUS_TYPE = [
        ('O', 'Open'),
        ('C', 'Closed')
    ]

    '''
    Choices for the current priority of tickets on 'priority'
    '''
    PRIOIRTY_TYPE = [
        ('R', 'Routine'),
        ('U', 'Urgent'),
        ('E', 'Emergency')
    ]

    '''
    Ticket Model

    ticketNum: the id and primary key.  Auto generated as an integer
    is_assigned:  a boolean to identify if a tech has been assgined or not
                  default is False
    status: choice from STATUS_TYPE to identify if ticket is open or closed
            default is 'O' for Open
    priority: choice from PRIOIRTY_TYPE to identify the urgency of the ticket
    title: max length 50, short description of issue
    description: Longer text field to describe issue
    date_created: auto generated with current date/time
    last_checked: blank=true, shows when tech last reviewed
    due_date = blank=true, shows due date based off priority
    date_closed = blank=true, shows date/time when closed
    '''
    ticketNum = models.AutoField(auto_created=True, primary_key=True)
    is_assigned = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_TYPE, default='O')
    priority = models.CharField(max_length=1, choices=PRIOIRTY_TYPE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    date_closed = models.DateTimeField(null=True, blank=True)

    '''
    Displays info in admin page
    '''
    def __str__(self) -> str:
        return 'Ticket: {ticketNum} - {title}'.format(ticketNum=self.ticketNum, title=self.title)