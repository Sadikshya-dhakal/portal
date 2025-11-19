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
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

class Tag(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("in_active", "Inactive"),
    ]
    title =models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    is_breaking_news = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    




# Post - Author
# 1 user can add M post => M
# 1 post is associated to only 1 user =>1

# Post - category
# 1 category can have M post => M
# 1 post is associated to only 1 category => 1
# 1-M relationship => foreignkey() => can be used in multiple model

# Tag - Post
# 1 tag can have M post => M
# 1 post can have M tag => M
# M-M relationship => ManyToManyField() 

# 1-1 relation
# 1 user can have 1 profile => 1
# 1 profile is associated to 1 user => 1
# OneToOneField() => can be used in any model