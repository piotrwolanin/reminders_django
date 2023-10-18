from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import ToDoItem


class ToDoListView(ListView):
    template_name = "todolist/todo_list.html"
    model = ToDoItem


class ToDoCreateView(CreateView):
    model = ToDoItem
    fields = ['description']
    template_name = 'todolist/todo_form.html'
    context_object_name = 'todo'
    success_url = reverse_lazy('todo-list')


class ToDoUpdateView(UpdateView):
    model = ToDoItem
    fields = ['description']
    template_name = 'todolist/todo_form.html'
    context_object_name = 'todo'
    success_url = reverse_lazy('todo-list')


class ToDoDeleteView(DeleteView):
    model = ToDoItem
    template_name = 'todolist/todo_confirm_delete.html'
    context_object_name = 'todo'
    success_url = reverse_lazy('todo-list')
