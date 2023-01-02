from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render, redirect

from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.generics import *                   # ListCreateAPIView, Retrieve
from rest_framework import filters

from rest_framework.permissions import IsAuthenticated


# Create your views here.

# class TodoViewSet(ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated,]

#     def get_queryset(self):
#         return self.request.user.todos.all()

#     def create(self, request, *args, **kwargs):
#         serializer = TodoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoAPIView(APIView):
    def get(self, request):

        q = request.query_params.get('search')
        if q is None:
            todos = Todo.objects.all()
        else:
            todos = Todo.objects.annotate(similarity=TrigramSimilarity('heading', q)).filter(similarity__gt=0.2)
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


class TodosAPIView(ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['heading','details']                                # search_fields = '__all__'
    ordering_fields = ['heading', 'details', 'user', 'date']

# class TodoAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer