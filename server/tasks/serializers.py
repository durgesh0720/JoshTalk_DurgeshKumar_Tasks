from rest_framework import serializers
from .models import UserModel, TaskModel

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'name', 'mobile', 'role']

class TaskModelSerializer(serializers.ModelSerializer):
    assigned_users = UserModelSerializer(many=True, read_only=True)
    assigned_user_ids = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), many=True, write_only=True, source='assigned_users'
    )

    class Meta:
        model = TaskModel
        fields = [
            'id', 'name', 'description', 'created_at', 'completed_at', 
            'status', 'task_type', 'priority', 'due_date', 
            'assigned_users', 'assigned_user_ids'
        ]


# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ['user', 'mobile', 'role']

#     def create(self, validated_data):
#         """
#         Create and return a new `UserModel` instance, given the validated data.
#         """
#         return UserModel.objects.create(**validated_data)