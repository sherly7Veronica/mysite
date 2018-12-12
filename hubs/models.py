# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from stakeholder.models import Stakeholder
from utils.models import DateBaseModel


class Hubs(DateBaseModel):
    name = models.CharField(max_length=64)
    stakeholder = models.ForeignKey(Stakeholder, blank=True, null=True)
