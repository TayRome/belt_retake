from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *



# Create your views here.
def preindex(request):
    return redirect("/main")

def index(request):
    return render(request, "travel/index.html")

def register(request):
    response = User.objects.register(
        request.POST["name"],
        request.POST["username"],
        request.POST["password"],
        request.POST["password_confirm"]
    )
    print (response)
    if response["valid"]:
        request.session["user_id"] = response["user"].id
        return redirect("/travel")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/main")

def login(request):
    response = User.objects.login(
        request.POST["username"],
        request.POST["password"]
    )
    if response["valid"]:
        request.session["user_id"] = response["user"].id
        return redirect("/travel")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/main")

def travel(request):
    if "user_id" not in request.session:
        return redirect("/main")

    context = {
        "user": User.objects.get(id = request.session["user_id"]),
        "users": User.objects.all().exclude(id = request.session["user_id"]),
        "my_travels": Travel.objects.all().filter(joined_users = User.objects.get(id = request.session["user_id"])),
        "all_travels": Travel.objects.all().exclude(joined_users = User.objects.get(id = request.session["user_id"]))
    }
    return render(request, "travel/travels.html", context)

def logout(request):
    request.session.clear()
    return redirect("/main")

def join(request, id):
    print ("Joining trip id {}".format(id))
    response = Travel.objects.joinTravel(id, request.session["user_id"])
    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, "You've successfully joined the trip!")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
    return redirect("/travel")

def add(request):
    return render(request, "travel/add.html")

def addTrip(request):
    response = Travel.objects.addTrip(
        request.POST.get("destination"),
        request.POST["description"],
        request.POST["date_from"],
        request.POST["date_to"],
        request.session["user_id"]
        )

    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, "Your trip has been added!")
        return redirect("/travel")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("travel/add")

def destination(request, id):
    print("In destination")
    context = {
        "travel": Travel.objects.get(id = id),
        "joined": Travel.objects.get(id = id).joined_users.all().exclude(id = Travel.objects.get(id = id).planned_by.id)
    }
    return render(request, "travel/destination.html", context)
