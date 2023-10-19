from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import ToDoItem
from .forms import ToDoItemModelForm


class ListTaskView(ListView):
    template_name = "todolist/todo_list.html"
    context_object_name = "todos"
    model = ToDoItem


class CreateTaskView(CreateView):
    model = ToDoItem
    form_class = ToDoItemModelForm
    template_name = "todolist/todo_form.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create a new task"
        return context


class UpdateTaskView(UpdateView):
    model = ToDoItem
    form_class = ToDoItemModelForm
    template_name = "todolist/todo_form.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")
    success_message = "Task was successfully updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit task"
        return context


class DeleteTaskView(DeleteView):
    model = ToDoItem
    template_name = "todolist/todo_confirm_delete.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")
    success_message = "Task was successfully deleted."


class ClearCompletedTasksView(View):
    success_url = reverse_lazy("todo-list")

    def post(self, request, *args, **kwargs):
        completed_tasks = ToDoItem.objects.filter(completed=True)
        completed_tasks.delete()
        return HttpResponseRedirect(self.success_url)
