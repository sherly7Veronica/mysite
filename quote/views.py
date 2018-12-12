# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

from music.pagination import DjangoPagination
from quote.models import Quote
from quote.serializers import QuoteSerializer


class QuoteListView(generics.ListAPIView):
    pagination_class = DjangoPagination
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()


class QuoteListCreateView(generics.ListCreateAPIView):
    pagination_class = DjangoPagination
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()


class QuoteRUDView(generics.RetrieveUpdateDestroyAPIView):
    pagination_class = DjangoPagination
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()


# class QuoteListDetailView(APIView):
#     serializer_class = QuoteSerializer
#     query = Quote.objects.all()