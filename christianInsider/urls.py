from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap


sitemaps = {
'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/',include('blog.urls',namespace='blog')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap')]+static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
# +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)