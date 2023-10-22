from django.test import TestCase, Client
from django.urls import reverse

from .forms import ToDoItemModelForm
from .models import ToDoItem


class ToDoItemModelTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.desc = "Write unit tests"

    def setUp(self):
        ToDoItem.objects.create(description=self.desc, completed=False)

    def test_todo_creation(self):
        todo = ToDoItem.objects.get(description=self.desc)
        self.assertTrue(isinstance(todo, ToDoItem))
        self.assertEqual(str(todo), todo.description)

    def test_todo_default_completed(self):
        todo = ToDoItem.objects.get(description=self.desc)
        self.assertEqual(todo.completed, False)


class ToDoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("todo-list")
        self.create_url = reverse("todo-create")

        ToDoItem.objects.create(description="Pay bills")
        ToDoItem.objects.create(description="Write unit tests", completed=True)

    def test_view_list_todo_items(self):
        """
        Test that the list view returns a 200 response and uses the correct template
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todolist/todo_list.html")
        self.assertTrue("pending_items" in response.context)
        self.assertTrue("completed_items" in response.context)
        self.assertTrue(len(response.context["pending_items"]) > 0)
        self.assertTrue(len(response.context["completed_items"]) > 0)

    def test_view_create_todo_item_get(self):
        """
        Test that the create view returns a 200 response, uses the correct template and contains the form
        """
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todolist/todo_form.html')
        self.assertIsInstance(response.context['form'], ToDoItemModelForm)

    def test_view_create_todo_item_post(self):
        """
        Test creating a new todo item through the insert view
        """
        response = self.client.post(self.create_url, {"description": "Deploy a Django app"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ToDoItem.objects.count(), 3)
