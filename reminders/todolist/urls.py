from django.urls import path

from . import views


urlpatterns = [
    path("", views.ToDoListView.as_view(), name="todo-list"),
    path('create/', views.ToDoCreateView.as_view(), name='todo-create'),
    path('<int:pk>/update/', views.ToDoUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/delete/', views.ToDoDeleteView.as_view(), name='todo-delete'),
]
