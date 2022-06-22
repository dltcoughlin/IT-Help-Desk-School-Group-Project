from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .ticket import Ticket

class Profile(models.Model):
    '''
    Choices for 'user_group' to identify users as 
    either your basic user or tech that accepts tickets
    '''
    USER_TYPE = [
        ('U', 'User'),
        ('T', 'Tech')
    ]

    '''
    Profile Model
    Extends Django's default user.model using one-to-one 
    Fields that are included:

    first_name: blank=true, 150 char
    last_name: blank=true, 150 char
    email: blank=true, email
    password: hashed password

    groups: many-to-many relations - ignore this
    user_permissions: many-to-many relations - ignore this
    is_staff: boolean to admin site access - set to false
    is_active: boolean to flag account - set to true
    is_superuser: boolean for all access - set to false

    last_login: datetime, auto generated last login
    date_joined: datetime, auto generated when created
    '''
    username = models.OneToOneField(User, on_delete=models.CASCADE)


    '''
    Custom fields for user.profile model in this app. 

    user_group: choice from USER_TYPE to identify if user is a User or Tech
    user_ticket: many-to-many, many 'users' can have many 'tickets'
                 A User creates a ticket under their name, then one or multiple
                 Techs can assign themselves to a single ticket.
                 Users/Tech should be able to see what tickets they have 
                 created/assigned to.
                 blank=true because a new user may not have any tickets yet
    '''
    user_group = models.CharField(max_length=1, choices=USER_TYPE)
    user_ticket = models.ManyToManyField(Ticket, blank=True)


    '''
    This updates default user model with our profile extention
    '''
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(username=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    '''
    Displays info in admin page
    '''
    def __str__(self) -> str:
        return '{username} - {user_type}'.format(username=self.username, user_type=self.user_group)