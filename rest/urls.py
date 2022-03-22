from django.urls import path
from . import views

urlpatterns = [
  path('time', views.current_datetime, name='time'),
  path('dbquery', views.db, name='db'),
  path('dbsave', views.dbSave, name='dbsave'),
  path('dbdelete', views.dbDelete, name='dbdelete'),
  path('get_highscores/<str:world>', views.get_highscores, name='get_highscores'),
  path('get_worlds', views.get_worlds, name='get_worlds'),
]