from __future__ import unicode_literals

from django.db import models
from datetime import datetime, date, time

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Your name should be at least 3 characters!"
        if len(postData['username']) < 3:
           	errors["username"] = "Your username should be at least 3 characters!"
        if not(postData['email']):
            errors["email"] = "Email should not be left blank!" 
        if User.objects.filter(email = postData['email']).exists():
        	errors['emailexists'] = "Email already exists!" 
       	if not EMAIL_REGEX.match(postData['email']):
			errors["invalidemail"] = "Email format is not valid!"
       	if postData['password'] != postData['passwordconfirm']:
			errors["passwordsnotmatch"] = "Passwords don't match!"
       	if len(postData['password']) < 8:
			errors["smallpassword"] = "Passwords should be at least 8 characters!!"
        return errors;

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects= UserManager()



class TripManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors["destination"] = "Your destination can't be blank!"        
        if len(postData['desc']) < 1:
            errors["desc"] = "Your description can't be blank!"
        if not postData['trip_start']:
            errors["trip_start"] = "Please insert a start date!"
        if not postData['trip_end']:
        	errors['trip_end'] = "Please insert an end date!"
        if postData['trip_end'] and postData['trip_start']:
          if postData['trip_end'] < postData['trip_start']:
             	errors["invaliddate1"] = "You should start your trip before the date it ends!!"
          if datetime.now() >= datetime.strptime(postData['trip_start'], '%Y-%m-%d'):
    			    errors["invaliddate2"] = "You can't be starting something before than today!!"
        return errors;

class Trip(models.Model):
  destination = models.CharField(max_length=255)
  desc = models.TextField()
  user_planned = models.ForeignKey(User, related_name = "planned_trips")
  users_joined = models.ManyToManyField(User, related_name = "joined_trips")
  trip_start = models.DateTimeField()
  trip_end = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)            
  objects= TripManager()

