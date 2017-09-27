# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from models import *

# Create your views here.
def index(request):
	return render(request, "belt_exam/index.html")

def register(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
          for tag, error in errors.iteritems():
              messages.error(request, error, extra_tags=tag)
          return redirect("/")
	else:
		name = request.POST['name']
		username = request.POST['username']
		emailaddress = request.POST['email']
		hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		password = hashedpw
		User.objects.create(name = name, username = username, email= emailaddress, password = password)
		return redirect("/")	

def login(request):
	email = request.POST['email']
	password = request.POST['password']
	u = User.objects.filter(email = email)
	print u
	if len(u) != 0:
		if bcrypt.checkpw(password.encode(), u[0].password.encode()):
			user = u[0]
			request.session['userid'] = user.id
			print request.session['userid']
			return redirect("/travels")
		else:
			messages.warning(request, "invalid Password!")
			return redirect("/")
	else:
		messages.warning(request, "Invalid E-mail!")
		return redirect("/")

def logoff(request):
	request.session.clear()
	return redirect('/')

def travels(request):
	loggedinuser = User.objects.get(id = request.session['userid'])
	context = {
		"loggedinuser": User.objects.get(id = request.session['userid']),
		"trips": Trip.objects.filter(user_planned = loggedinuser),
		"users": User.objects.all().exclude(id=loggedinuser.id),
		"plannedtrips": Trip.objects.all()
	}
	return render(request, "belt_exam/travels.html", context)

def add(request):
	context = {
		"loggedinuser": User.objects.get(id = request.session['userid'])
	}
	return render(request, "belt_exam/add.html", context)

def addtrip(request):
	errors = Trip.objects.basic_validator(request.POST)
	if len(errors):
          for tag, error in errors.iteritems():
              messages.error(request, error, extra_tags=tag)
          return redirect("travels/add")
	else:
		destination = request.POST['destination']
		description = request.POST['desc']
		tripstart = request.POST['trip_start']
		tripend = request.POST['trip_end']
		userid = request.POST['user']
		userplanned = User.objects.get(id = userid)
		print userplanned
		Trip.objects.create(destination = destination, desc = description, user_planned = userplanned, trip_start = tripstart, trip_end = tripend)
		return redirect("/travels")


def showtrip(request, id):
	id = id
	loggedinuser = User.objects.get(id = request.session['userid'])
	context = {
		"trips": Trip.objects.filter(id = id),
		"joinedusers": User.objects.filter(joined_trips = id)

	}
	return render(request, "belt_exam/showtrip.html", context)

def join(request):
	userid = request.POST['id']
	tripid = request.POST['tripid']
	t = Trip.objects.get(id = tripid)
	t.users_joined.add(userid)
	t.save()
	return redirect('/travels/destination/' + tripid)