from django.urls import path
  
from . import views

urlpatterns = [
    path('', views.Front, name='Front'),
    path('allTasks', views.AllTasks, name='AllTasks'),
    path('lastTaskInstances', views.LastTaskInstances, name='LastTaskInstances'),
    path('view/<int:cid>', views.CiboulexpView, name='CiboulexpView'),
    path('lightView/<int:cid>', views.CiboulexpLightView, name='CiboulexpLightView'),
    path('taskView/<int:tid>', views.TaskView, name='TaskView'),
    path('notesview/', views.NotesView, name='NotesView'),
    path('getSummary/', views.getSummary, name='getSummary'),
    path('addNote/', views.addNote, name='addNote'),
    path('importFile/', views.importFile, name='importFile'),
    path('api/', views.api, name='api'),
    path('ajaxLoadModal/', views.ajaxLoadModal, name='ajaxLoadModal'),
]

