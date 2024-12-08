from django.urls import path
from . import views

urlpatterns = [

    path('login', views.loginPage, name="login"), #login_registration
    path('logout', views.logoutUser, name="logout"),

    path('home', views.home, name='home'),
    path('room/<str:pk>/', views.room, name="room"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    path('layout/', views.layout, name="layout"),
    path('about_us/', views.about_us, name="about_us"),
    path('contact_us/', views.contact_us, name="contact_us"),
    path('projects_landing/', views.projects_landing, name="projects_landing"),
    path('events/', views.events, name="events"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('login/', views.loginPage, name="login"),
    path('', views.landing_page, name="landing_page"), 

]
