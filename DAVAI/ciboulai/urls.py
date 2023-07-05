from django.urls import path
from django.contrib import admin
  
from . import views

urlpatterns = [
    path('', views.Front, name='Front'),
    path('allTasks', views.AllTasks, name='AllTasks'),
    path('lastTaskInstances', views.LastTaskInstances, name='LastTaskInstances'),
    path('lightView/<int:cid>', views.CiboulexpLightView, name='CiboulexpLightView'),
    path('taskView/<int:tid>', views.TaskView, name='TaskView'),
    path('notesview/', views.NotesView, name='NotesView'),
    path('getSummary/', views.getSummary, name='getSummary'),
    path('addNote/', views.addNote, name='addNote'),
    path('api/', views.api, name='api'),
    path('ajaxLoadModal/', views.ajaxLoadModal, name='ajaxLoadModal'),       
    path('ajaxXpids/', views.ajaxXpids, name='ajaxXpids'),       
    path('admin/', admin.site.urls)
]

