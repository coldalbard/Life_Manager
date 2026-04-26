from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    # Audit поля
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='categories_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='categories_updated'
    )

    # Soft delete
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags')

    # Audit поля
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tags_created')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tags_updated')

    # Soft delete
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [('todo', 'To Do'),
                      ('in_progress', 'In Progress'),
                      ('done', 'Done'), ]
    PRIORITY_CHOICES = [('low', 'Low'),
                        ('medium', 'Medium'),
                        ('high', 'High')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    reminder_time = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='tasks_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='tasks_updated')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
