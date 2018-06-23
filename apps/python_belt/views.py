from __future__ import unicode_literals
from django.shortcuts import render, redirect
from apps.python_belt.models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def home(request):
    if "user_id" in request.session:
        return redirect ("/board")
    return render (request, "python_belt/home.html")

def create_user(request):
    errors = User.objects.registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/")
    else:
        User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode(),
        )
        messages.success(request, "Registration successful!")
        return redirect ("/")

def login(request):
    errors = User.objects.login(request.POST)
    if len(errors) > 0:
        messages.error(request, "Login failed.")
        return redirect ("/")
    else:
        request.session["user_id"] = User.objects.get(email=request.POST["email"]).id
        return redirect ("/board")

def logout(request):
    request.session.flush()
    return redirect ("/")

def board(request):
    if not "user_id" in request.session:
        return redirect ("/")
    context = {
        "current_user" : User.objects.get(id=request.session["user_id"]),
        "quotes" : Quote.objects.all(),
    }
    print(context)
    return render(request, "python_belt/board.html", context)

def add_quote(request):
    errors = Quote.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/board")
    else:
        Quote.objects.create(
            poster = User.objects.get(id=request.session["user_id"]),
            author = request.POST["author"],
            content = request.POST["content"],
        )
        messages.success(request, "Quote posted!")
        return redirect ("/board")

def user(request, number):
    if not "user_id" in request.session:
        return redirect ("/")
    context = {
        "current_user" : User.objects.get(id=request.session["user_id"]),
        "user_name" : User.objects.get(id=number).first_name,
        "quotes" : Quote.objects.filter(poster=User.objects.get(id=number)).all()
    }
    return render(request, "python_belt/user.html", context)

def edit(request):
    if not "user_id" in request.session:
        return redirect ("/")
    context = {
        "current_user" : User.objects.get(id=request.session["user_id"]),
    }
    return render(request, "python_belt/edit.html", context)

def editing_user(request):
    errors = User.objects.edit(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/edit")
    else:
        user = User.objects.get(id=request.session["user_id"])

        temp = user.email
        user.email = "blank"
        user.save()

        if User.objects.filter(email=request.POST["email"]).count() > 0:
            messages.error(request, "Email already registered.")
            user.email = temp
            user.save()
            return redirect ("/edit")

        else:
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.save()
            messages.success(request, "Edit successful!")
            return redirect ("/edit")

def delete_quote(request, number):
    ex_quote = Quote.objects.get(id=number)
    ex_quote.delete()
    messages.warning(request, "Quote deleted!")
    return redirect ("/board")

def like_quote(request, number):
    if Quote.objects.get(id=number).likes.filter(id=request.session["user_id"]).count() > 0:
        messages.warning(request, "Already liked!")
        return redirect ("/board")
    else:
        quote = Quote.objects.get(id=number)
        user = User.objects.get(id=request.session["user_id"])
        quote.likes.add(user)
        messages.info(request, "Quote liked!")
        return redirect ("/board")
