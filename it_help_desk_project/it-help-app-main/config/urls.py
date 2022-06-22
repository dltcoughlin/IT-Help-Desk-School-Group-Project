"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from src.views import index, home, login, newComment, newTicket, searchticket, getticketinfo, newComment, techOptions, logout

urlpatterns = [
    path('', home.as_view, name='home'),
    path('app/', include('src.urls')),
    path('admin/', admin.site.urls),
    path('home/', home.as_view, name='home'),
    path('login/', login.as_view, name='login'),
    path('newticket/', newTicket.as_view, name='newticket'),
    path('searchticket/', searchticket.as_view, name='searchticket'),
    path('getticket/', getticketinfo.as_view, name='getticket'),
    path('newcomment/', newComment.as_view, name='newcomment'),
    path('assign/', techOptions.assign, name='assign'),
    path('unassign/', techOptions.unassign, name='unassign'),
    path('close/', techOptions.close, name='close'),
    path('open/', techOptions.open, name='open'),
    path('logout/', logout.as_view, name='logout')
]
