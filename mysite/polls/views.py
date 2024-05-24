from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db import connection, transaction
from .models import Message, SignupForm, LoginForm, MessageForm

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'message_list'

    def get_queryset(self):
        return Message.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Message
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Message.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Message
    template_name = 'polls/results.html'

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

def index(request):
    message_list = Message.objects.order_by('-pub_date')
    context = {'message_list': message_list}
    return render(request, 'polls/index.html', context)

def detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    return render(request, 'polls/detail.html', {'message': message})

def results(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    return render(request, 'polls/results.html', {'message': message})

def create_poll(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message_text']
            pub_date = form.cleaned_data['pub_date']

            print(message_text)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO polls_message (message_text, pub_date) VALUES (%s, %s)",
                    [message_text, pub_date]
                )
            print("success")
            transaction.commit()  
            return redirect('polls:index')
    else:
        form = MessageForm(initial={'pub_date': timezone.now()})
    return render(request, 'polls/create_poll.html', {'form': form})

def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        message.delete()
        return redirect('polls:index')  
    return redirect('polls:index')
