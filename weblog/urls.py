from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from webno.sitemaps import PostSitemap

sitemaps = {
'posts': PostSitemap,
}


urlpatterns = [
    # Examples:
    # url(r'^$', 'weblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^' , include('webno.urls',namespace='webno')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
name='django.contrib.sitemaps.views.sitemap'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)