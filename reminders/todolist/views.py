from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .models import ToDoItem
from .forms import ToDoItemModelForm


class ListTaskView(ListView):
    template_name = "todolist/todo_list.html"
    context_object_name = "todos"
    model = ToDoItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_items"] = ToDoItem.objects.filter(completed=False)
        context["completed_items"] = ToDoItem.objects.filter(completed=True)
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit task"
        return context


class DeleteTaskView(DeleteView):
    model = ToDoItem
    template_name = "todolist/todo_confirm_delete.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")


@require_POST
def complete_task(request, pk):
    item = get_object_or_404(ToDoItem, pk=pk)
    item.completed = request.POST.get("completed") == "true"
    item.save()
    return redirect("todo-list")


class ClearCompletedTasksView(View):
    success_url = reverse_lazy("todo-list")

    def post(self, request, *args, **kwargs):
        completed_tasks = ToDoItem.objects.filter(completed=True)
        completed_tasks.delete()
        return HttpResponseRedirect(self.success_url)
