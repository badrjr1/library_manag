import random
from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count , F
from .forms import RegistrationForm 
from .models import Books , Loans , Penalty 


def home(request):
    list_book=Books.objects.all()
    context={"liste_book":list_book}
    return render(request,"home.html",context)

def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.warning(request,'Remplir les champs corretement')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def logIn(request):
       if request.POST:
           username = request.POST.get('username')
           pwd= request.POST.get('password')
           user= authenticate(request,username=username,password=pwd)
           if user is not None:
               login(request,user)
               return redirect('home')
           else:
               messages.warning(request,'Mot de passe ou nom d\'utilisateur incorrect')
       return render(request, 'login.html')

def logOut(request):
    logout(request)
    return redirect('home')

def pagelivre(request, livre_id):
    livre = Books.objects.get(id=livre_id)
    context = {"livre": livre}
    if request.method == 'POST':
        if Loans.objects.filter(book=livre, member=request.user, returned=False).exists() or livre.nombre_de_copiess < 1 :
            messages.warning(request,'You have already reserved this book.')
        else:
            due_date = timezone.now().date() + timedelta(days=30)
            Loans.objects.create(
                book=livre,
                member=request.user,
                due_date=due_date,
                returned=False,
                reminder_sent=False
            )
            livre.nombre_de_copiess=livre.nombre_de_copiess-1
            livre.save()
            messages.success(request, 'Book reserved.')
            return redirect('profile')
    
    all_books = list(Books.objects.exclude(id=livre_id))
    random_books = random.sample(all_books, min(len(all_books), 10)) 
    context["random_books"] = random_books
    
    return render(request, "reserve_book.html", context)

@login_required
def profile_view(request):
    user = request.user
    loans = Loans.objects.filter(member=user.id)
    penalties = Penalty.objects.filter(loan__member=user.id)
    
    context = {
        'user': user,
        'loans': loans,
        'penalties': penalties,
    }
    return render(request, 'profil.html', context)

def book_search(request):
    query = request.GET.get('title')
    liste_book = []
    if query:
        liste_book = Books.objects.filter(title__icontains=query)
        if not liste_book :
            messages.warning(request,'livre n\'existe pas')
    else:
        liste_book=Books.objects.all()
    return render(request, 'home.html', {'query': query, 'liste_book': liste_book})

@login_required
def update_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('profile') 

    return render(request, 'profile.html') 
