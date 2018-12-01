# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login, authenticate
# from django.shortcuts import render
# from django.shortcuts import render, redirect

from rest_framework import generics, filters
from .pagination import DjangoPagination
# from .filters import SongFilter
from serializers import PostSerializers
from models import Post


class BlogListView(generics.ListAPIView):
    queryset = Post.objects.all()
    pagination_class = DjangoPagination
    serializer_class = PostSerializers
