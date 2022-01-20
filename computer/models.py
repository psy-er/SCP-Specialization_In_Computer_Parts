from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
# Create your models here.

class Maker(models.Model):
    maker_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    maker_address = models.CharField(max_length=50)
    maker_contact = models.CharField(max_length=50)
    maker_certificate = models.CharField(max_length=50)
    maker_certificate_name = models.CharField(max_length=50)

    def __str__(self):
        return self.maker_name

    def get_absolute_url(self):
        return f'/blog/maker/{self.slug}'

class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

class Item(models.Model):
    item_name = models.CharField(max_length=50)
    explanation = MarkdownxField()
    item_price = models.CharField(max_length=50)

    maker = models.ForeignKey(Maker, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    head_image = models.ImageField(upload_to='computer/images/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    item_state = models.CharField(max_length=50)
    item_receipt = models.CharField(max_length=50)

    author = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] {self.item_name} :: {self.author}'

    def get_absolute_url(self):
        return f'/computer/{self.pk}/'

    def get_explanation_markdown(self):
        return markdown(self.explanation)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return 'https://doitdjango.com/avatar/id/367/f8b6bb3fdf643ed8/svg/{self.author.email}/'

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.item.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()

        else :
            return 'https://doitdjango.com/avatar/id/367/f8b6bb3fdf643ed8/svg/{self.author.email}/'
