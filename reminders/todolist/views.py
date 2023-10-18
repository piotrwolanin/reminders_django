from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import ToDoItem
from .forms import ToDoItemModelForm


class ToDoListView(ListView):
    template_name = "todolist/todo_list.html"
    context_object_name = "todos"
    model = ToDoItem


class ToDoCreateView(CreateView):
    model = ToDoItem
    form_class = ToDoItemModelForm
    template_name = "todolist/todo_form.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")


class ToDoUpdateView(UpdateView):
    model = ToDoItem
    form_class = ToDoItemModelForm
    template_name = "todolist/todo_form.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")
    success_message = "Task was successfully updated."


class ToDoDeleteView(DeleteView):
    model = ToDoItem
    template_name = "todolist/todo_confirm_delete.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")
    success_message = "Task was successfully deleted."
