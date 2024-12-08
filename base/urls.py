from django.urls import path
from . import views

urlpatterns = [
    
    # Authentication
    path('login/', views.loginPage, name="login"), #login_registration
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    
    # Home and Rooms
    path('home/', views.home, name='home'),
    #path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name="room"),
    
    #Profiles
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    
    #Room Management
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    #path('jobDetails/', views.jobDetails, name='job-details'),
    

    path('projects/', views.project_list, name='project-list'),
    path('add-project/', views.add_project, name='add-project'),


    path('events/', views.events_list, name="events-list"),
    path('create-event/', views.create_event, name="create-event"),

    ##added for job search.
    path('jobs/details/<str:pk>',views.job_description, name='job_description'),
    path('jobDetails/', views.job_search, name = 'job-details'),




    # path('layout/', views.layout, name="layout"),
    path('about_us/', views.about_us, name="about_us"),
    path('contact_us/', views.contact_us, name="contact_us"),
    #path('projects_landing/', views.projects_landing, name="projects_landing"),
    path('events/', views.events, name="events"),
    # path('sign_up/', views.sign_up, name="sign_up"),

    path('', views.landing_page, name="landing_page"), 

]