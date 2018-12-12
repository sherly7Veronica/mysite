# -*- coding: utf-8 -*-

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from utils.helpers import random_string
from utils.models import DateBaseModel


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An email based user model
    """
    name = models.CharField(_('company name'), max_length=128, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    # def __str__(self):
    #     return str(self.name.encode('utf8', 'ignore'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.email

    def save(self, *args, **kwargs):
        """
        Always save the email as lowercase. Helps identifying unique email
        addresses.

        The de jure standard is that the local component of email addresses is
        case sensitive however the de facto standard is that they are not. In
        practice what happens is user confusion over why an email address
        entered with camel casing one day does not match an email address
        entered in different casing another day.
        """
        self.email = self.email.lower()
        return super(MyUser, self).save(*args, **kwargs)

    def get_username(self):
        """
        Returns the email address

        Satisifies API needs of other libraries.
        """
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def get_full_name(self):
        return self.email

    def get_short_name ( self ):
        return self.email


def generate_token():
    return random_string(size=256)


class ChangePasswordToken(DateBaseModel):
    user = models.ForeignKey(MyUser)
    token = models.CharField(max_length=256, default=generate_token)

    def change_password(self, password):
        self.user.change_password(password)
        self.delete()
