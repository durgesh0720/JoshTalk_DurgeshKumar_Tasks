# Task Management API

A Django-based RESTful API for managing tasks and user assignments, built with Django and Django Rest Framework. This project allows users to create tasks, assign tasks to users, and retrieve tasks assigned to specific users.

## Features
- Create a new task with a name, description, and optional fields like task type, priority, and due date.
- Assign tasks to one or multiple users.
- Retrieve all tasks assigned to a specific user.
- Built with Django, including serializers, generic views, and comprehensive testing.

## Prerequisites
- Python 3.8+
- Virtualenv (recommended)
- Git (optional, for cloning the repository)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd JoshTalk_DurgeshKumar_Tasks
```
## 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
## 3. Install Dependencies
```bash

pip install -r requirements.txt
```
## 4. Apply Database Migrations
```bash

python manage.py migrate
```
## 5. Create a Superuser (Optional, for Admin Access)
```bash

python manage.py createsuperuser
```

### Alternatively, seed the database with sample data:

```bash
python manage.py shell
>>> from tasks import seed
>>> seed.run_seed()
```

## 6. Rename Environment File
### Rename .envENV to .env:
``` bash
mv .envENV .env
```

## 7. Run the Development Server
```bash

python manage.py runserver
```

### The API will be available at http://127.0.0.1:8000/api/.

# API Endpoints
## 1. Create a Task
### Endpoint: POST /api/tasks/create/

Description: Creates a new task with specified details and assigns it to users.
## Request:
### json
```
{
    "name": "Fix Login Bug",
    "description": "Resolve authentication issue",
    "task_type": "bug",
    "priority": "high",
    "due_date": "2025-03-30T12:00:00Z",
    "assigned_user_ids": [1, 2]
}

Response (201 Created):

```

### json
```
{
    "id": 1,
    "name": "Fix Login Bug",
    "description": "Resolve authentication issue",
    "created_at": "2025-03-25T10:00:00Z",
    "completed_at": null,
    "status": "pending",
    "task_type": "bug",
    "priority": "high",
    "due_date": "2025-03-30T12:00:00Z",
    "assigned_users": [
        {"id": 1, "name": "Alice", "mobile": "1234567890", "role": "developer"},
        {"id": 2, "name": "Bob", "mobile": "0987654321", "role": "tester"}
    ]
}
```
## 2. Assign a Task to Users

### Endpoint: PATCH /api/tasks/<task_id>/assign/
Description: Updates the list of users assigned to a specific task.
## Request (e.g., for task ID 1):
### json
```
{
    "assigned_user_ids": [1, 3]
}
Response (200 OK):
```

### json
```
{
    "id": 1,
    "name": "Fix Login Bug",
    "description": "Resolve authentication issue",
    "created_at": "2025-03-25T10:00:00Z",
    "completed_at": null,
    "status": "pending",
    "task_type": "bug",
    "priority": "high",
    "due_date": "2025-03-30T12:00:00Z",
    "assigned_users": [
        {"id": 1, "name": "Alice", "mobile": "1234567890", "role": "developer"},
        {"id": 3, "name": "Charlie", "mobile": "1122334455", "role": "manager"}
    ]
}
```

## 3. Get Tasks for a Specific User
### Endpoint: GET /api/users/<user_id>/tasks/
Description: Retrieves all tasks assigned to a specific user.

## Request (e.g., for user ID 1):

### GET /api/users/1/tasks/
#### Response (200 OK):
json
```
[
    {
        "id": 1,
        "name": "Fix Login Bug",
        "description": "Resolve authentication issue",
        "created_at": "2025-03-25T10:00:00Z",
        "completed_at": null,
        "status": "pending",
        "task_type": "bug",
        "priority": "high",
        "due_date": "2025-03-30T12:00:00Z",
        "assigned_users": [
            {"id": 1, "name": "Alice", "mobile": "1234567890", "role": "developer"},
            {"id": 3, "name": "Charlie", "mobile": "1122334455", "role": "manager"}
        ]
    }
]
``` 

#### Testing the Project
#### Run the automated tests to verify API functionality:
```
python manage.py test tasks
``` 
```
Expected Output: "Ran 3 tests in X.XXXs OK"
Tests cover task creation, assignment, and retrieval.
Test Credentials
For testing via the Django Admin or API:
```

Username: test
Password: test
Create additional users via the admin panel (/admin/) or use the seed.py script.

## Project Structure

server/
├── manage.py
├── requirements.txt
├── server/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── README.md