# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from utils.models import DateBaseModel


class DynamicTable(DateBaseModel):
    table_name = models.CharField(max_length=200, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.table_name.encode('utf8', 'ignore')

    # def get_dynamic_attributes(self):
    #     return DynamicAttribute.objects.filter (dyn_table=self)


# class DynamicAttribute(DateBaseModel):
#     attribute = models.ForeignKey(Attribute)
#     is_unique = models.BooleanField(default=False)
#     is_required = models.BooleanField(default=False)
#     is_foreignkey = models.BooleanField(default=False)
#     foreign_dyn_table = models.ForeignKey(DynamicTable, related_name='related_attribute', on_delete=models.SET_NULL,
#                                           blank=True, null=True)
#     dyn_table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
