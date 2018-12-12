# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics

from hubs.models import Hubs
from hubs.serializers import HubsSerializers
from music.pagination import DjangoPagination


class HubListView(generics.ListAPIView):
    pagination_class = DjangoPagination
    serializer_class = HubsSerializers
    queryset = Hubs.objects.all()


class HubListCreateView(generics.ListCreateAPIView):
    pagination_class = DjangoPagination
    serializer_class = HubsSerializers
    queryset = Hubs.objects.all()


class HubRUDView(generics.RetrieveUpdateDestroyAPIView):
    pagination_class = DjangoPagination
    serializer_class = HubsSerializers
    queryset = Hubs.objects.all()