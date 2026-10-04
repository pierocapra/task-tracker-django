from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Task
from .serializers import SignupSerializer, TaskSerializer


@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
        return Response(TaskSerializer(tasks, many=True).data)

    serializer = TaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)  # server sets the owner, not the client
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request, pk):
    # Filtering by user means someone else's task returns 404, not 403
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'GET':
        return Response(TaskSerializer(task).data)

    if request.method in ('PUT', 'PATCH'):
        serializer = TaskSerializer(task, data=request.data, partial=(request.method == 'PATCH'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"})

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]