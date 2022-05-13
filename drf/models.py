from tabnanny import verbose
from turtle import title
from webbrowser import get
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class drf_Article(models.Model):
    STATUS_CHOICES = (
        ('p', _('Published')),
        ('d', _('Draft')),
    )

    title = models.CharField(max_length=128, verbose_name=_('Title (*)'), db_index=True)
    body = models.TextField(verbose_name=_('body'), blank=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(_('status(*)'),max_length=1, choices=STATUS_CHOICES, default='s', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=_('Create_Date'), auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-create_date']
        db_table = "drf_Article"
        verbose_name = "drf_Article"
        verbose_name = "drf_Article"