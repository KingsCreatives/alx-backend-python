from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User,pk=user_id)

    user_to_delete.delete()

    return redirect('home')