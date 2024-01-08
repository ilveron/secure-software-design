from django.core.exceptions import ValidationError


def validate_title(value: str) -> None:
    if len(value) == 0:
        raise ValidationError('Title must not be empty')
    if not value[0].isupper():
        raise ValidationError('Title must be capitalized')
