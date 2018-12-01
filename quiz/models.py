# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from djangogirls.mysite.music.models import Songs
from music.models import Songs


class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, blank=True, null=True)
    music = models.ForeignKey(Songs, blank=True, null=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


