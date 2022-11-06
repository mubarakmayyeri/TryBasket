from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
# Create your views here.

def adminLogin(request):
  if 'email' in request.session:
    return redirect('dashboard')
  
  if request.method == 'POST':
    form = LoginForm(request.POST)
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
      if user.is_superadmin:
        request.session['email'] = email
        login(request, user)
        return redirect(adminLogin)
      else:
        messages.error(request, 'Not Authorized!!!')
        return redirect(adminLogin)
    else:
      messages.error(request, 'Invalid login credentials')
      return redirect(adminLogin)
    
  form = LoginForm
  return render(request, 'adminPanel/login.html', {'form':form})

def dashboard(request):
  if 'email' in request.session:
    return render(request, 'adminPanel/dashboard.html')
  
@login_required(login_url = 'adminLogin')
def adminLogout(request):
  if 'email' in request.session:
    request.session.flush()
  logout(request)
  messages.success(request, 'Logged out successfully.')
  return redirect(adminLogin)