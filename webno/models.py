# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,verbose_name=_('creator'))
    title = models.CharField(max_length=80,verbose_name=_('post title'))
    slug = models.SlugField(max_length=250,unique_for_date='updatetime')
    content = RichTextUploadingField(_('post content'))
    createtime = models.DateTimeField(_('createtime'),auto_now=True,auto_now_add=False)
    updatetime = models.DateTimeField(_('updatetime'),auto_now=False,auto_now_add=True)
    tags = TaggableManager()
    
    class Meta:
        verbose_name= _('Post')
        verbose_name_plural =_('Posts')
        ordering = ('-createtime',)

    def __str__(self):
        return self.title 

    def __unicode__(self):
        return self.title 


    def get_absolute_url(self):
        return reverse('webno:detail', kwargs={'id': self.id})



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)