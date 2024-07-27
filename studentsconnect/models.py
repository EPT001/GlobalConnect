from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    picture = models.ImageField(upload_to='category_images', blank=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    country = models.ForeignKey(Country, null= True, blank=True, max_length=150, on_delete=models.SET_NULL)
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    university = models.ForeignKey(University, null= True, blank=True, max_length=150, on_delete=models.SET_NULL)


    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
        user_profile.follows.set([user_profile.id])
        user_profile.save()
        

post_save.connect(create_profile, sender=User)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
