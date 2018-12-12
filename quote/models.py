# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from hubs.models import Hubs
from stakeholder.models import Stakeholder
from utils.models import DateBaseModel


class Quote(DateBaseModel):
    stakeholder = models.ForeignKey(Stakeholder, blank=True, null=True)
    source = models.ForeignKey(Hubs, related_name='sourceName')
    destination = models.ForeignKey(Hubs, related_name='destinationName')
    for_date = models.DateTimeField()
    rate = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    rate_currency = models.CharField(max_length=3, blank=True, null=True)