
# Create your models here.
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validations(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Not a valid email address"

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
            
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"

        if len(postData['password']) < 7:
            errors['password'] = "Password should be at least 8 characters"
            
        if not len(postData['password']) == len(postData['confirm_password']):
            errors['password'] = "Passwords don't match"
            
        email_exists= User.objects.filter(email=postData['email']).exists()
        if (email_exists):
            errors['email'] = "Email already exists"
        
        return errors
        
    def login_validations(self, postData):
        errors = {}
        
        if len(postData['email2']) == 0:
            errors['email2'] = "Email should be at least 8 characters"
    
        if len(postData['password2']) == 0:
            errors['password2'] = "Password should be at least 8 characters"
            
        email_exists= User.objects.filter(email=postData['email2']).exists()
        if not (email_exists):
            errors['email2'] = "failed to login"
            
            
            
        user_list = User.objects.filter(email=postData['email2'])
        print("***********************************")
        print(user_list)
        if len(user_list)== 0:
            errors['email2'] = "No user with that email found"
        else:
            user =user_list[0]
            if not bcrypt.checkpw(postData['password2'].encode(), user.password.encode()):
                errors['password2'] = "failed to login"
            
        
        return errors

class User(models.Model):
# One to Many
# put foreign key on the many side 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    #messages
    #comments
    #reference to manager

    def __repr__(self):
        return f"first_name: {self.first_name} last_name: {self.last_name} email: {self.email} password: {self.password}"


    
class Message(models.Model):
    #comments
    message = models.TextField()
    user = models.ForeignKey(User,related_name = "messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    
class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User,related_name = "comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message,related_name = "comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    
# if you delete the user - all the comment and messages gets deleted

    #{{comment.user.first_name}} this to get comment from user
    #{{comment.message.content}}
