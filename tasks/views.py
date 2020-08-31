from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def create(request):
    Priorities = Priority.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        priority = Priority.objects.get(pk=int(request.POST["priority"]))
        creator = request.user
        newtask = Task(title = title, description = description, priority = priority, creator = creator)
        newtask.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tasks/create.html", {
            "priorities": Priorities
        })

def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(done = False, creator = request.user)
        return render(request, "tasks/index.html", {
            "tasks" : tasks
        })
    else:
        return render(request, "tasks/layout.html")

def viewcompleted(request):
    tasks = Task.objects.filter(done = True, creator = request.user)
    return render(request, "tasks/index.html", {
        "tasks" : tasks,
        "completed" : True
    })

def viewpriority(request, p_id):
    try:
        priority = Priority.objects.get(id=p_id)
    except Priority.DoesNotExist:
        raise Http404("Category not found.")
    return render(request, "tasks/index.html", {
        "tasks": Task.objects.filter(priority = priority, creator = request.user, done = False)
    })

def markdone(request, t_id):
    task = Task.objects.get(id = t_id)
    task.datecomp = datetime.datetime.now()
    task.done = True
    task.save()
    return HttpResponseRedirect(reverse("index"))

def changepriority(request, t_id):
    task = Task.objects.get(pk = t_id)
    if request.method == "POST":
        task.priority = Priority.objects.get(pk=int(request.POST["priority"]))
        task.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tasks/change.html", {
            "t": task,
            "priorities": Priority.objects.all()
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tasks/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tasks/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tasks/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tasks/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tasks/register.html")
