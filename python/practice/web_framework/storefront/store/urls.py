from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'product/(?P<id>[0-9]+)', views.product, name='product'),
]
