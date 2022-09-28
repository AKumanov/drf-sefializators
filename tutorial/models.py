from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments import highlight
from pygments.formatters.html import HtmlFormatter

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


# Create your models here.
class Snippet(models.Model):
    MAX_LENGTH = 100

    created = models.DateTimeField(
        auto_now_add=True,
    )
    title = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        default=''
    )
    code = models.TextField()
    linenos = models.BooleanField(
        default=False
    )
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default='python',
        max_length=MAX_LENGTH
    )
    style = models.CharField(
        choices=STYLE_CHOICES,
        default='friendly',
        max_length=MAX_LENGTH
    )
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the 'pygments' library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {
            'title': self.title
        } if self.title else {}
        formatter = HtmlFormatter(
            style=self.style,
            linenos=linenos,
            full=True,
            **options
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created']


class Package(models.Model):
    _PACKAGE_NAME_MAX_LENGTH = 255
    _PACKAGE_DEFAULT = 0
    prod_name = models.CharField(
        max_length=_PACKAGE_NAME_MAX_LENGTH,
        default=_PACKAGE_DEFAULT
    )
    quantity = models.IntegerField(
        default=_PACKAGE_DEFAULT
    )
    unit_price = models.IntegerField(
        default=_PACKAGE_DEFAULT
    )

    def __str__(self):
        return str(self.prod_name)


class Orders(models.Model):
    _ORDERS_MAX_NAME_LENGTH = 255
    _ORDERS_DEFAULT_VALUE = 0
    order_id = models.CharField(
        max_length=_ORDERS_MAX_NAME_LENGTH,
        default=_ORDERS_DEFAULT_VALUE
    )
    package = models.ManyToManyField(Package)
    is_cod = models.BooleanField(
        default=False
    )

    def __str__(self):
        return str(self.order_id)
