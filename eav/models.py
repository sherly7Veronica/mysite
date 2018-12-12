# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Attribute(models.Model):
    '''
    Putting the **A** in *EAV*. This holds the attributes, or concepts.
    Examples of possible *Attributes*: color, height, weight,
    number of children, number of patients, has fever?, etc...

    Each attribute has a name, and a description, along with a slug that must
    be unique.  If you don't provide a slug, a default slug (derived from
    name), will be created.

    The *required* field is a boolean that indicates whether this EAV attribute
    is required for entities to which it applies. It defaults to *False*.

    .. warning::
       Just like a normal model field that is required, you will not be able
       to save or create any entity object for which this attribute applies,
       without first setting this EAV attribute.

    There are 7 possible values for datatype:

        * int (TYPE_INT)
        * float (TYPE_FLOAT)
        * text (TYPE_TEXT)
        * date (TYPE_DATE)
        * bool (TYPE_BOOLEAN)
        * object (TYPE_OBJECT)
        * enum (TYPE_ENUM)

    Examples:

    >>> Attribute.objects.create(name='Height', datatype=Attribute.TYPE_INT)
    <Attribute: Height (Integer)>

    >>> Attribute.objects.create(name='Color', datatype=Attribute.TYPE_TEXT)
    <Attribute: Color (Text)>

    >>> yes = EnumValue.objects.create(value='yes')
    >>> no = EnumValue.objects.create(value='no')
    >>> unkown = EnumValue.objects.create(value='unkown')
    >>> ynu = EnumGroup.objects.create(name='Yes / No / Unkown')
    >>> ynu.enums.add(yes, no, unkown)
    >>> Attribute.objects.create(name='Has Fever?',
    ...                          datatype=Attribute.TYPE_ENUM,
    ...                          enum_group=ynu)
    <Attribute: Has Fever? (Multiple Choice)>

    .. warning:: Once an Attribute has been used by an entity, you can not
                 change it's datatype.
    '''

    class Meta:
        ordering = ['content_type', 'name']
        unique_together = ('site', 'content_type', 'slug')

    TYPE_TEXT = 'text'
    TYPE_FLOAT = 'float'
    TYPE_INT = 'int'
    TYPE_DATE = 'date'
    TYPE_BOOLEAN = 'bool'
    TYPE_OBJECT = 'object'
    TYPE_ENUM = 'enum'

    DATATYPE_CHOICES = (
        (TYPE_TEXT, _(u"Text")),
        (TYPE_FLOAT, _(u"Float")),
        (TYPE_INT, _(u"Integer")),
        (TYPE_DATE, _(u"Date")),
        (TYPE_BOOLEAN, _(u"True / False")),
        (TYPE_OBJECT, _(u"Django Object")),
        (TYPE_ENUM, _(u"Multiple Choice")),
    )

    name = models.CharField(_(u"name"), max_length=100,
                            help_text=_(u"User-friendly attribute name"))

    content_type = models.ForeignKey(ContentType,
                                     blank=True, null=True,
                                     verbose_name=_(u"content type"))

    site = models.ForeignKey(Site, verbose_name=_(u"site"),
                             default=settings.SITE_ID)

    slug = EavSlugField(_(u"slug"), max_length=50, db_index=True,
                        help_text=_(u"Short unique attribute label"))

    description = models.CharField(_(u"description"), max_length=256,
                                   blank=True, null=True,
                                   help_text=_(u"Short description"))

    enum_group = models.ForeignKey(EnumGroup, verbose_name=_(u"choice group"),
                                   blank=True, null=True)

    type = models.CharField(_(u"type"), max_length=20, blank=True, null=True)

    @property
    def help_text(self):
        return self.description

    datatype = EavDatatypeField(_(u"data type"), max_length=6,
                                choices=DATATYPE_CHOICES)

    created = models.DateTimeField(_(u"created"), default=timezone.now,
                                   editable=False)

    modified = models.DateTimeField(_(u"modified"), auto_now=True)

    required = models.BooleanField(_(u"required"), default=False)

    display_order = models.PositiveIntegerField(_(u"display order"), default=1)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def get_validators(self):
        '''
        Returns the appropriate validator function from :mod:`~eav.validators`
        as a list (of length one) for the datatype.

        .. note::
           The reason it returns it as a list, is eventually we may want this
           method to look elsewhere for additional attribute specific
           validators to return as well as the default, built-in one.
        '''
        DATATYPE_VALIDATORS = {
            'text': validate_text,
            'float': validate_float,
            'int': validate_int,
            'date': validate_date,
            'bool': validate_bool,
            'object': validate_object,
            'enum': validate_enum,
        }

        validation_function = DATATYPE_VALIDATORS[self.datatype]
        return [validation_function]

    def validate_value(self, value):
        '''
        Check *value* against the validators returned by
        :meth:`get_validators` for this attribute.
        '''
        for validator in self.get_validators():
            validator(value)
        if self.datatype == self.TYPE_ENUM:
            if value not in self.enum_group.enums.all():
                raise ValidationError(_(u"%(enum)s is not a valid choice "
                                        u"for %(attr)s") % \
                                      {'enum': value, 'attr': self})

    def save(self, *args, **kwargs):
        '''
        Saves the Attribute and auto-generates a slug field if one wasn't
        provided.
        '''
        if not self.slug:
            self.slug = EavSlugField.create_slug_from_name(self.name)
        self.full_clean()
        super(Attribute, self).save(*args, **kwargs)

    def clean(self):
        '''
        Validates the attribute.  Will raise ``ValidationError`` if
        the attribute's datatype is *TYPE_ENUM* and enum_group is not set,
        or if the attribute is not *TYPE_ENUM* and the enum group is set.
        '''
        if self.datatype == self.TYPE_ENUM and not self.enum_group:
            raise ValidationError(_(
                u"You must set the choice group for multiple choice" \
                u"attributes"))

        if self.datatype != self.TYPE_ENUM and self.enum_group:
            raise ValidationError(_(
                u"You can only assign a choice group to multiple choice " \
                u"attributes"))

    def get_choices(self):
        '''
        Returns a query set of :class:`EnumValue` objects for this attribute.
        Returns None if the datatype of this attribute is not *TYPE_ENUM*.
        '''
        if not self.datatype == Attribute.TYPE_ENUM:
            return None
        return self.enum_group.enums.all()

    def save_value(self, entity, value):
        '''
        Called with *entity*, any django object registered with eav, and
        *value*, the :class:`Value` this attribute for *entity* should
        be set to.

        If a :class:`Value` object for this *entity* and attribute doesn't
        exist, one will be created.

        .. note::
           If *value* is None and a :class:`Value` object exists for this
            Attribute and *entity*, it will delete that :class:`Value` object.
        '''
        ct = ContentType.objects.get_for_model(entity)
        try:
            value_obj = self.value_set.get(entity_ct=ct,
                                           entity_id=entity.pk,
                                           attribute=self)
        except Value.DoesNotExist:
            if value == None or value == '':
                return
            value_obj = Value.objects.create(entity_ct=ct,
                                             entity_id=entity.pk,
                                             attribute=self)
        if value == None or value == '':
            value_obj.delete()
            return

        if value != value_obj.value:
            value_obj.value = value
            value_obj.save()

    def __unicode__(self):
        return u"%s.%s (%s)" % (self.content_type, self.name, self.get_datatype_display())