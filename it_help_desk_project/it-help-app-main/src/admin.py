from django.contrib import admin

from src.models import Ticket
from src.models import Comment
from src.models import Profile

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Profile)

