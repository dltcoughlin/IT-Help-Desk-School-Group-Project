from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

def as_view(request):
    if request.method =='POST':  # comes here when you are making a post request via submitting the form
        # Register user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            args = {}
            text = "Login Failed"
            args['error'] = text
            return render(request, 'login.html', args)
    return render(request, 'login.html')