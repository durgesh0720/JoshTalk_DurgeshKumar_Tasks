from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):

    """
    UserModel represents a user in the system.

    Attributes:
        id (IntegerField): The primary key for the user.
        name (CharField): The name of the user, with a maximum length of 100 characters.
        email (EmailField): The email address of the user.
        mobile (CharField): The mobile number of the user, with a maximum length of 15 characters. This field is optional.
        role (CharField): The role of the user, chosen from predefined roles. This field is optional.

    Methods:
        __str__(): Returns a string representation of the user in the format "name : role".
    """

    USER_ROLES = [
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('manager', 'Manager'),
        ('tester', 'Tester'),
        ('guest', 'Guest')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, blank=True)

    def __str__(self):
        return f"{self.name} : {self.role}"


class TaskModel(models.Model):

    """
    TaskModel represents a task in the system with various attributes such as name, description, status, type, and assigned users.

    Attributes:
        id (IntegerField): The primary key for the task.
        name (CharField): The name of the task, with a maximum length of 100 characters.
        description (TextField): A detailed description of the task.
        created_at (DateTimeField): The date and time when the task was created, automatically set on creation.
        completed_at (DateTimeField): The date and time when the task was completed, can be null or blank.
        status (CharField): The current status of the task, chosen from predefined statuses. Default is 'pending'.
        task_type (CharField): The type of task, chosen from predefined types. Default is 'feature'.
        priority (CharField): The priority level of the task, chosen from predefined levels. Default is 'medium'.
        due_date (DateTimeField): The date and time by which the task should be completed, can be null or blank.
        assigned_users (ManyToManyField): The users assigned to the task, related to the UserModel.

    Methods:
        __str__(): Returns the name of the task as its string representation.
    """

    TASK_STATUSES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled')
    ]

    TASK_TYPES = [
        ('bug', 'Bug Fix'),
        ('feature', 'Feature Development'),
        ('improvement', 'Improvement'),
        ('documentation', 'Documentation'),
        ('testing', 'Testing'),
        ('deployment', 'Deployment'),
        ('research', 'Research'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]

    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='pending')
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default='feature')
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    assigned_users = models.ManyToManyField(UserModel, related_name='tasks')

    def __str__(self):
        return self.name