# -*- coding: utf-8 -*-
from django.db import models


class Author(models.Model):

    name = models.CharField(
        u'Author Name',
        max_length=255
    )


class Book(models.Model):

    title = models.TextField(
        u'Book Title',
    )

    author = models.ForeignKey(Author)
