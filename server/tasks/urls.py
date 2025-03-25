from django.urls import path
from .views import CreateTaskView, AssignTaskView, UserTasksView

urlpatterns = [
    path('tasks/create/', CreateTaskView.as_view(), name='create-task'),
    path('tasks/<int:pk>/assign/', AssignTaskView.as_view(), name='assign-task'),
    path('users/<int:user_id>/tasks/', UserTasksView.as_view(), name='user-tasks'),
]