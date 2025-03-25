import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from .models import UserModel, TaskModel

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

fake = Faker()

USER_ROLES = ['admin', 'developer', 'manager', 'tester', 'guest']
TASK_STATUSES = ['pending', 'in_progress', 'completed', 'on_hold', 'cancelled']
TASK_TYPES = ['bug', 'feature', 'improvement', 'documentation', 'testing', 'deployment', 'research']
PRIORITIES = ['low', 'medium', 'high', 'urgent']
task_list = [
    "Write report", "Fix bug", "Design logo", "Update database",
    "Deploy project", "Test API", "Optimize query", "Refactor code"
]

def create_users(n=5):
    """Create n random users in both User and UserModel"""
    users = []
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = "password123"

        # Create User in Django's built-in User model
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create associated UserModel
        user_model = UserModel.objects.create(
            user=user,
            mobile=fake.phone_number(),
            role=random.choice(USER_ROLES)
        )
        users.append(user_model)
    return users

def create_tasks(n=10, users=None):
    """Create n random tasks and assign them to users randomly"""
    if users is None:
        users = list(UserModel.objects.all())

    for _ in range(n):
        task = TaskModel.objects.create(
            name = random.choice(task_list),
            description=fake.paragraph(),
            status=random.choice(TASK_STATUSES),
            task_type=random.choice(TASK_TYPES),
            priority=random.choice(PRIORITIES),
            due_date=fake.future_datetime()
        )

        # Assign the task to 1 or more random users
        assigned_users = random.sample(users, random.randint(1, len(users)))
        task.assigned_users.set(assigned_users)

def run_seed():
    print("Seeding database with users and tasks...")
    users = create_users(5)  # Create 5 users
    create_tasks(10, users)   # Create 10 tasks and assign them randomly
    print("Seeding completed successfully!")

if __name__ == "__main__":
    run_seed()
