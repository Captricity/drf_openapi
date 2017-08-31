"""
Extensions to django rest framework schema generation to support additional
features.
"""
from collections import OrderedDict
from django.utils.encoding import force_text
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.compat import coreschema


URL_REGEX = \
    r'^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$'


def field_to_schema(field):
    """
    Adapted from rest_framework:
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/schemas.py

    Extended to include support for length and pattern operators, as well as
    defining schemas directly on the field (as opposed to with introspection).
    """
    if hasattr(field, 'schema'):
        return field.schema

    title = force_text(field.label) if field.label else ''
    description = force_text(field.help_text) if field.help_text else ''

    if isinstance(field, (serializers.ListSerializer, serializers.ListField)):
        child_schema = field_to_schema(field.child)
        return coreschema.Array(
            items=child_schema,
            title=title,
            description=description
        )
    elif isinstance(field, serializers.Serializer):
        return coreschema.Object(
            properties=OrderedDict([
                (key, field_to_schema(value))
                for key, value
                in field.fields.items()
            ]),
            title=title,
            description=description
        )
    elif isinstance(field, serializers.ManyRelatedField):
        return coreschema.Array(
            items=coreschema.String(),
            title=title,
            description=description
        )
    elif isinstance(field, serializers.RelatedField):
        return coreschema.String(title=title, description=description)
    elif isinstance(field, serializers.MultipleChoiceField):
        return coreschema.Array(
            items=coreschema.Enum(enum=list(field.choices.keys())),
            title=title,
            description=description
        )
    elif isinstance(field, serializers.ChoiceField):
        return coreschema.Enum(
            enum=list(field.choices.keys()),
            title=title,
            description=description
        )
    elif isinstance(field, serializers.BooleanField):
        return coreschema.Boolean(title=title, description=description)
    elif isinstance(field, (serializers.DecimalField, serializers.FloatField)):
        return coreschema.Number(
            title=title,
            description=description,
            minimum=field.min_value,
            maximum=field.max_value)
    elif isinstance(field, serializers.IntegerField):
        return coreschema.Integer(
            title=title,
            description=description,
            minimum=field.min_value,
            maximum=field.max_value)
    elif isinstance(field, serializers.UUIDField):
        if field.uuid_format == 'hex_verbose':
            pattern = \
                r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        elif field.uuid_format == 'hex':
            pattern = r'^[0-9a-f]{32}$'
        elif field.uuid_format == 'urn':
            pattern = \
                r'^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        else:
            pattern = None
        return coreschema.String(
            title=title,
            description=description,
            pattern=pattern)
    elif isinstance(field, serializers.RegexField):
        regex_validator = \
            [validator for validator in field.validators
             if isinstance(validator, RegexValidator)]
        if regex_validator:
            pattern = regex_validator[0].regex.pattern
        else:
            pattern = None
        return coreschema.String(
            title=title,
            description=description,
            pattern=pattern,
            max_length=field.max_length,
            min_length=field.min_length)
    elif isinstance(field, serializers.URLField):
        return coreschema.String(
            title=title,
            description=description,
            pattern=URL_REGEX,
            max_length=field.max_length,
            min_length=field.min_length)
    elif isinstance(field, serializers.JSONField):
        return coreschema.Object(
            title=title,
            description=description)

    create_args = {'title': title, 'description': description}
    if hasattr(field, 'min_length'):
        create_args['min_length'] = field.min_length
    if hasattr(field, 'max_length'):
        create_args['max_length'] = field.max_length

    if field.style.get('base_template') == 'textarea.html':
        create_args['format'] = 'textarea'
    return coreschema.String(**create_args)
