from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.db import connection, transaction
from .models import Message, SignupForm, LoginForm, MessageForm

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'message_list'

    def get_queryset(self):
        return Message.objects.order_by('-pub_date')
    
    # Flaw 3: Cross-Site Scripting (XSS)
    # Fix to Cross-Site Scripting (XSS) is removing the method "get_context_data"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for message in context['message_list']:
            message.message_text = mark_safe(message.message_text)
        return context

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:login')
    else:
        form = SignupForm()
    return render(request, 'polls/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('polls:index')
    else:
        form = LoginForm()
    return render(request, 'polls/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('polls:login')

def create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message_text']
            pub_date = form.cleaned_data['pub_date']
            
            with connection.cursor() as cursor:

            # FLAW 1: SQL Injection
                cursor.execute(f"INSERT INTO polls_message (message_text, pub_date) VALUES ('{message_text}','{pub_date}')")

            # Fix for SQL Injection:
            #   cursor.execute(
            #   "INSERT INTO polls_message (message_text, pub_date) VALUES (%s, %s)",
            #   [message_text, pub_date]
            #   )

                transaction.commit()
                return redirect('polls:index')
    else:
        form = MessageForm(initial={'pub_date': timezone.now()})
    return render(request, 'polls/create.html', {'form': form})

def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)

# FLAW 2: Broken Access Control:
    if request.method == "POST":
            message.delete()
            return redirect('polls:index')  
    return redirect('polls:index')

    # Fix for broken access control:

    # if request.user.is_superuser:
    #     if request.method == "POST":
    #         message.delete()
    #         return redirect('polls:index')  
    #     return redirect('polls:index')
    # else:
    #     return redirect('polls:index') 
