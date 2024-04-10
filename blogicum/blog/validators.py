import difflib

from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import truncatechars

from blog.constants import Config


class ForbiddenWord(models.Model):
    """A ForbiddenWord model is used to store forbidden words."""

    word = models.CharField('Запретное слово', max_length=256)

    class Meta:
        """A meta class that configures additional parameters of the model."""

        verbose_name = 'слово'
        verbose_name_plural = 'Слова'

    def __str__(self):
        return truncatechars(self.word, Config.TRUNCATION_LENGTH)


def forbidden_words(value: str) -> None:
    """Validate that a word is forbidden."""
    words = set(map(str.lower, value.split()))
    forbidden = set(
        map(
            str.lower,
            ForbiddenWord.objects.all().values_list('word', flat=True)
        )
    )
    restricted_words = tuple(
        item for item in forbidden
        if difflib.get_close_matches(item, words, n=1, cutoff=0.6)
    )
    if restricted_words:
        raise ValidationError(
            f'{", ".join(restricted_words)} запрещено использовать!'
        )
