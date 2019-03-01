from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    objects = CommentManager()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.user.username)


    def children(self): # Replies
        return Comment.objects.filter(parent=self)

    def set_deleted(self):
        if (self.deleted == None):
            self.deleted = timezone.now()
            self.save()

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True