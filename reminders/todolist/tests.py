from django.core.exceptions import ObjectDoesNotExist
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
        self.update_url = reverse("todo-update", args=[1])
        self.delete_url = reverse("todo-delete", args=[2])
        self.complete_url = reverse("todo-complete", args=[3])
        self.clear_url = reverse("todo-clear")

        ToDoItem.objects.create(description="Get groceries")
        ToDoItem.objects.create(description="Write unit tests", completed=True)
        ToDoItem.objects.create(description="Clean the flat")
        ToDoItem.objects.create(description="Learn guitar")

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

    def test_view_crud_todo_item_get(self):
        """
        Test that the create and update / delete views each return a 200 response, use the correct template and contain
        the right form
        """

        for url in (self.create_url, self.update_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "todolist/todo_form.html")
            self.assertIsInstance(response.context["form"], ToDoItemModelForm)

    def test_view_create_todo_item_post(self):
        """
        Test inserting a new ToDoItem through the create view
        """
        response = self.client.post(
            self.create_url, {"description": "Deploy a Django app"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ToDoItem.objects.count(), 5)

    def test_view_update_todo_item_post(self):
        """
        Test that the update view changes a ToDoItem correctly and redirects
        """
        updated_desc = "Pay bills"
        response = self.client.post(self.update_url, {"description": updated_desc, "priority": True, "completed": True})
        item = ToDoItem.objects.get(pk=1)
        item.refresh_from_db()
        self.assertEqual(item.description, updated_desc)
        self.assertTrue(item.priority)
        self.assertFalse(item.completed, "This form should not modify the 'completed' attribute")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)

    def test_view_delete_todo_item_post(self):
        """
        Test that the delete view removes a ToDoItem correctly and redirects
        """
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(ObjectDoesNotExist):
            ToDoItem.objects.get(pk=2)

        self.assertRedirects(response, self.list_url)

    def test_complete_task_post(self):
        """
        Test that the complete task view completes a ToDoItem and redirects
        """
        item = ToDoItem.objects.get(pk=3)
        self.assertFalse(item.completed)
        response = self.client.post(self.complete_url, {"completed": "true"})
        item.refresh_from_db()
        self.assertTrue(item.completed)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)

    def test_clear_completed_tasks_post(self):
        """
        Test that the clear completed task view successfully clears all completed tasks
        """
        all_items = ToDoItem.objects.all()
        init_completed_count = all_items.filter(completed=True).count()
        self.assertGreater(init_completed_count, 0, "There should be at least 1 completed item for this test to work")
        response = self.client.post(self.clear_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        final_completed_count = all_items.filter(completed=True).count()
        self.assertGreater(init_completed_count, final_completed_count)
