from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Task, Category, Tag
from .permissions import IsOwner
from .serializers import TaskSerializer, CategorySerializer, TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Category.objects.none()

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Tag.objects.none()

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Task.objects.none()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'tags']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
