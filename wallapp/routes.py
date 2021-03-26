from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('message', views.post_message),
    path('comment/<int:msg_id>', views.post_comment),
    path('delete/<int:msg_id>', views.delete),
    path('logout', views.logout),

]