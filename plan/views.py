from django.shortcuts import render, redirect

from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated

# Create your views here.

# class TodoViewSet(ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated,]

#     def get_queryset(self):
#         return self.request.user.todos.all()

#     def create(self, request, *args, **kwargs):
#         todo = request.data
#         serializer = TodoSerializer(data=todo)

#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        user_todos = Todo.objects.filter(user=request.user)
        todo = Todo.objects.get(id=pk)
        if todo in user_todos:
            todo.delete()
            return Response({"delete_message": "Deleted successfully!"})
        return Response({"delete_message": "No such todo exists."})

    def put(self, request, pk):
        user_todos = Todo.objects.filter(user=request.user)
        todo = Todo.objects.get(id=pk)
        if todo in user_todos:
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"updated_data": serializer.data})
            return Response({"error_message": "PUT data has some errors!"})
        return Response({"put_message": "No such todo exists."}) 