from django.urls import path, include

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.message_delete, name='message_delete'),
]