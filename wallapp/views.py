from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt


# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to render home page
# -----------------------------------------------------------------------------------------------------------------------

def index(request):
    return render(request, "index.html")

# ----------------------------------------------------------------------------
# Route to validate, register user and redirect to user page
# ----------------------------------------------------------------------------


def register(request):
    errors = User.objects.basic_validations(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)

        return redirect('/')

    else:
        if request.method == "POST":
            print("begin creation")
            hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            hash1 = hash1.decode()
            request.session["log_status"] = True
            new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash1)
            request.session['first_name'] = new_user.first_name
            request.session['userid'] = new_user.id
            return redirect('/wall')

# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to login
# -----------------------------------------------------------------------------------------------------------------------

def login(request):
    errors = User.objects.login_validations(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')

    else:
        user = User.objects.get(email=request.POST['email2'])

        request.session["log_status"] = True
        request.session['userid'] = user.id
        request.session['first_name'] = user.first_name

        if bcrypt.checkpw(request.POST['password2'].encode(), user.password.encode()):
            print("password match")
       
            return redirect('/wall')
        else:
       
            print("failed password")
            return redirect('/')

# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to show user profile and wall
# -----------------------------------------------------------------------------------------------------------------------


def wall(request):

    if "userid" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "messages": Message.objects.all(),
        "comments": Comment.objects.all(),
    }
    return render(request, "show.html", context)


# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to logout of profile
# -----------------------------------------------------------------------------------------------------------------------


def logout(request):
    request.session.flush()
    return redirect('/')

# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to post comment and message
# -----------------------------------------------------------------------------------------------------------------------

def post_message(request):
    print('*'*100)
    print('creating message...')
    if request.method == 'POST':
        new_message = Message.objects.create(
            message = request.POST['msg'],
            user = User.objects.get(id = request.session['userid'])
        )
        new_message.save()
    return redirect('/wall')

def post_comment(request, msg_id):
    print('*'*100)
    print('posting comment...')
    if request.method == 'POST':
        new_comment = Comment.objects.create(
            comment = request.POST['cmnt'],
            user = User.objects.get(id = request.session['userid']),
            message = Message.objects.get(id = msg_id)
        )
        new_comment.save()
    return redirect('/wall')


# -----------------------------------------------------------------------------------------------------------------------
# ROUTE to delete comment and message
# -----------------------------------------------------------------------------------------------------------------------
def delete(request, msg_id):
    message = Message.objects.get(id=msg_id)
    message.delete()
    return redirect('/wall')