from django.urls import path

from . import views


urlpatterns = [
    path("", views.ListTaskView.as_view(), name="todo-list"),
    path("create/", views.CreateTaskView.as_view(), name="todo-create"),
    path("<int:pk>/update/", views.UpdateTaskView.as_view(), name="todo-update"),
    path("<int:pk>/delete/", views.DeleteTaskView.as_view(), name="todo-delete"),
    path("<int:pk>/complete/", views.complete_task, name="todo-complete"),
    path("clear/", views.ClearCompletedTasksView.as_view(), name="todo-clear"),
]
