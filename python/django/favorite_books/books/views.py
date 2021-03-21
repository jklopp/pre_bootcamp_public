from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
# Create your views here.
def index(request):
    return render(request, 'index.html')

def delete_all(request):
    all = Book.objects.all()
    all.delete()
    return redirect("/success")

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'books': Book.objects.all()
    }
    return render(request, 'favorite_books.html', context)

def add_book(request):
    if request.method == "GET":
        return redirect('/success')
    errors = Book.objects.addBook(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/success')
    new_book = Book.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        uploaded_by = User.objects.get(id=request.session['user_id'])
    )
    return redirect('/success')