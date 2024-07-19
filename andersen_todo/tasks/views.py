from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TaskSerializer

def is_owner(user, task):
    if task.user_id == user:
        return True
    else: 
        return False

class Registration(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    def post(self, request):
        required_fields = ('first_name', 'username', 'password')
        missed_fields = []
        for field in required_fields:
            if field not in request.data.keys() or len(request.data[field]) == 0:
                missed_fields.append(field)
        if len(missed_fields) != 0:
            return Response(f'Missed required field(s): {missed_fields}', 
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=request.data['username']).exists():
            u = request.data['username']
            return Response(f'Username {u} is already registered.', 
                            status=status.HTTP_400_BAD_REQUEST)
        if len(request.data['password']) < 6:
            return Response(f'Password must be at least 6 characters long', 
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=request.data['username'], 
                                        password=request.data['password'])
        try:
            l_name = request.data['last_name']
            if len(l_name) != 0:
                user.last_name = l_name
        except KeyError:
            pass
        user.save()
        return Response(f'User successfully created!', 
                        status=status.HTTP_201_CREATED)        

class TasksView(APIView):
    # permission_classes = [permissions.IsAuthenticated] #УБРАТЬ пере релизом
    qs = Task.objects.all()
    serializer = TaskSerializer(qs, many=True)
    def get(self, request):
        # serializer = self.serializer
        return Response(self.serializer.data, status=status.HTTP_200_OK)
    
class TaskView(APIView):
    # permission_classes = [permissions.AllowAny] #УБРАТЬ пере релизом
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if is_owner(request.user, task):
            serializer = TaskSerializer(instance=task, 
                                    data=request.data, 
                                    partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response('The task was successfully modified', 
                                status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You can modify only own tasks", 
            status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if is_owner(request.user, task):
            task.delete()
            return Response('The task status was successfully deleted', 
                                status=status.HTTP_200_OK)
        else:
            return Response("You can delete only own tasks", 
            status=status.HTTP_403_FORBIDDEN)        

class TasksView(APIView):
    qs = Task.objects.all()
    serializer = TaskSerializer(qs, many=True)
    def get(self, request):
        return Response(self.serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        pass
        # return Response('The task status was successfully created', 
        #                 status=status.HTTP_201_CREATED)
    
class CompleteTaskView(APIView):
    def patch(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if is_owner(request.user, task):
            data = {'status': 'Completed'}
            serializer = TaskSerializer(instance=task, 
                                    data=data, 
                                    partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response('The task status was successfully set as Completed', 
                                status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You can modify only own tasks", 
            status=status.HTTP_403_FORBIDDEN)
