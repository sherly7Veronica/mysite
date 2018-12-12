# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from mysite import settings
from users.models import MyUser


class Stakeholder(models.Model):
    SHIPPER = 0
    TRANSPORTER = 1
    FORWARDER = 2

    STAKEHOLDER_CHOICES = (
        (SHIPPER, 'SHIPPER'),
        (TRANSPORTER, 'TRANSPORTER'),
        (FORWARDER, 'FORWARDER'),
    )
    user = models.OneToOneField(MyUser)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    mobile_verified = models.BooleanField(default=False)
    # dynamic_table = models.ForeignKey('cp_eav.DynamicTable', blank=True, null=True)
    dynamic_table = models.IntegerField(choices=STAKEHOLDER_CHOICES, blank=True, null=True)

    # def __str__(self):
    #     f_name = ''
    #     if self.first_name:
    #         f_name = self.first_name.encode('utf8', 'ignore')
    #
    #     l_name = ''
    #     if self.last_name:
    #         l_name = self.last_name.encode('utf8', 'ignore')
    #
    #     return "{}{}".format(l_name, f_name)

    # def get_stakeholder_type(self):
    #     return self.dynamic_table.table_name
    #
    # def is_customer(self):
    #     return settings.STAKEHOLDER_TYPE[self.get_stakeholder_type()] == settings.STAKEHOLDER_TYPE_CUSTOMER
    #
    # def get_stakeholder_info(self):
    #     return self.stakeholderinfo

