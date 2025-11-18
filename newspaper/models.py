from django.db import models

# Create your models here.
# title
#content,description
#author
# published date
# views_count
# Tags
# image
# category
# comments


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)
    description = models.models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["Name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

class Tag(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("activate", "Active"),
        ("in_active", "Inactive"),
    ]
    title =models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    is_breaking_news = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title