# -*- coding: utf-8 -*-
from django.db import models


class University(models.Model):

    name = models.CharField(
        u'University Name',
        max_length=255
    )


class Author(models.Model):

    name = models.CharField(
        u'Author Name',
        max_length=255
    )

    university = models.ForeignKey(
        University,
        default=None
    )


class Book(models.Model):

    title = models.TextField(
        u'Book Title',
    )

    author = models.ForeignKey(
        Author,
        default=None
    )
