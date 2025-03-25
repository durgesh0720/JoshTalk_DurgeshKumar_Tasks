from rest_framework import generics, status
from rest_framework.response import Response
from .models import TaskModel, UserModel
from .serializers import TaskModelSerializer

# API to create a task
class CreateTaskView(generics.CreateAPIView):
    """
    CreateTaskView is a view that handles the creation of new TaskModel instances.

    Attributes:
        queryset (QuerySet): A queryset containing all TaskModel instances.
        serializer_class (Serializer): The serializer class used to validate and
            deserialize input, and to serialize output.
    """
    queryset = TaskModel.objects.all()
    serializer_class = TaskModelSerializer




# API to assign a task to users
class AssignTaskView(generics.UpdateAPIView):
    """
    AssignTaskView is a view that handles the updating of a task.

    This view inherits from generics.UpdateAPIView and provides the functionality
    to update an existing task in the database.

    Attributes:
        queryset (QuerySet): The queryset that retrieves all TaskModel instances.
        serializer_class (Serializer): The serializer class used to validate and
            deserialize input and serialize output.

    Methods:
        update(request, *args, **kwargs):
            Handles the HTTP PUT request to update a task. It retrieves the task
            object, validates the incoming data using the serializer, saves the
            updated task, and returns the serialized data with a 200 OK status.
    """
    queryset = TaskModel.objects.all()
    serializer_class = TaskModelSerializer

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)




# API to get tasks for a specific user
class UserTasksView(generics.ListAPIView):
    """
    UserTasksView is a view that provides a list of tasks assigned to a specific user.

    Attributes:
        serializer_class (TaskModelSerializer): The serializer class used to serialize the task data.

    Methods:
        get_queryset(self):
            Retrieves the queryset of tasks assigned to the user specified by the 'user_id' URL parameter.

            Returns:
                QuerySet: A queryset of TaskModel instances filtered by the assigned user's ID.
    """
    serializer_class = TaskModelSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return TaskModel.objects.filter(assigned_users__id=user_id)