from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(deleted__isnull=True, draft=True)

class Post(models.Model):
    title = models.CharField(max_length=120, blank=False, null=False)
    author = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    context = models.TextField(blank=False, null=False)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0, blank=True, null=False)
    draft = models.BooleanField(default=False, blank=True, null=False)
    published = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(upload_to="news/posts/%Y/%m/%d", null=True, blank=True,
                              height_field="height_field",
                              width_field="width_field")

    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')


    objects = PostManager()

    @property
    def is_deleted(self):
        if (self.deleted):
            return True
        return False

    @property
    def comments(self):
        instance = self
        comments = Comment.objects.filter_by_instance(instance).filter(parent=None, deleted__isnull=True)
        return comments

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def view_counter(self):
        self.views += 1
        self.save()

    def set_deleted(self):
        if not (self.deleted):
            self.deleted = timezone.now()
            self.save()

    def get_absolute_url(self):
        return reverse("news:post_detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("news:post_like", kwargs={"id": self.id})

    def get_like_api_url(self):
        return reverse("news:post_like_api", kwargs={"id": self.id})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)[:20]
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_resiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_resiver, sender=Post)
