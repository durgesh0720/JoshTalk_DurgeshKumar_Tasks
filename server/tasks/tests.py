from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserModel, TaskModel
from datetime import datetime
import pytz

class TaskAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up test data: create users and link them to UserModel instances.
        This runs before every test.
        """
        self.client = APIClient()

        # Create Django User instances
        self.user1 = User.objects.create_user(username='alice', password='password123')
        self.user2 = User.objects.create_user(username='bob', password='password123')
        self.user3 = User.objects.create_user(username='charlie', password='password123')

        # Create UserModel instances linked to Django Users
        self.usermodel1 = UserModel.objects.create(
            user=self.user1, name='Alice', mobile='1234567890', role='developer'
        )
        self.usermodel2 = UserModel.objects.create(
            user=self.user2, name='Bob', mobile='0987654321', role='tester'
        )
        self.usermodel3 = UserModel.objects.create(
            user=self.user3, name='Charlie', mobile='1122334455', role='manager'
        )

    def test_create_task(self):
        """
        Test the task creation API endpoint.
        """
        url = '/api/tasks/create/'
        data = {
            'name': 'Fix Login Bug',
            'description': 'Resolve authentication issue',
            'task_type': 'bug',
            'priority': 'high',
            'due_date': '2025-03-30T12:00:00Z',
            'assigned_user_ids': [self.usermodel1.id, self.usermodel2.id]
        }
        response = self.client.post(url, data, format='json')

        # Check response status and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Fix Login Bug')
        self.assertEqual(response.data['task_type'], 'bug')
        self.assertEqual(len(response.data['assigned_users']), 2)
        self.assertEqual(response.data['assigned_users'][0]['name'], 'Alice')

        # Verify task exists in the database
        task = TaskModel.objects.get(name='Fix Login Bug')
        self.assertEqual(task.assigned_users.count(), 2)

    def test_assign_task(self):
        """
        Test the task assignment API endpoint.
        """
        # Create a task first
        task = TaskModel.objects.create(
            name='Improve UI',
            description='Enhance user interface',
            task_type='improvement',
            priority='medium'
        )
        task.assigned_users.add(self.usermodel1)  # Initially assign to Alice

        # Assign task to Bob and Charlie
        url = f'/api/tasks/{task.id}/assign/'
        data = {
            'assigned_user_ids': [self.usermodel2.id, self.usermodel3.id]
        }
        response = self.client.patch(url, data, format='json')

        # Check response status and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['assigned_users']), 2)
        self.assertEqual(response.data['assigned_users'][0]['name'], 'Bob')
        self.assertEqual(response.data['assigned_users'][1]['name'], 'Charlie')

        # Verify task assignment in the database
        task.refresh_from_db()
        self.assertEqual(task.assigned_users.count(), 2)
        self.assertTrue(self.usermodel2 in task.assigned_users.all())
        self.assertFalse(self.usermodel1 in task.assigned_users.all())  # Alice removed

    def test_get_user_tasks(self):
        """
        Test the retrieval of tasks for a specific user.
        """
        # Create tasks and assign them
        task1 = TaskModel.objects.create(
            name='Task 1', description='First task', task_type='feature', priority='low'
        )
        task2 = TaskModel.objects.create(
            name='Task 2', description='Second task', task_type='bug', priority='high'
        )
        task1.assigned_users.add(self.usermodel1)
        task2.assigned_users.add(self.usermodel1, self.usermodel2)

        # Get tasks for Alice (usermodel1)
        url = f'/api/users/{self.usermodel1.id}/tasks/'
        response = self.client.get(url)

        # Check response status and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Alice has 2 tasks
        task_names = [task['name'] for task in response.data]
        self.assertIn('Task 1', task_names)
        self.assertIn('Task 2', task_names)

        # Get tasks for Bob (usermodel2)
        url = f'/api/users/{self.usermodel2.id}/tasks/'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)  # Bob has 1 task
        self.assertEqual(response.data[0]['name'], 'Task 2')