import uuid

from django.db import models
from django.utils import timezone


class BaseModel (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class UpdatedAtBaseModel (models.Model):
    # updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.updated_at = timezone.now()
        return super(UpdatedAtBaseModel, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class CreateAtBaseModel (models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class DateBaseModel(BaseModel, UpdatedAtBaseModel, CreateAtBaseModel):
    class Meta:
        abstract = True
