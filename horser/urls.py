"""horser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from horsequick.views import horser_index,horser_help,interface_add,interface_detail,\
    interface_depot,domain_manage,domain_add,horser_login,select_domain,edit_domain,\
    edit_category,delete_category,category_add,interface_webtest_detail,interface_webtest,\
    webtest_go


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', horser_index, name='horser_index'),
    url(r'^login/$', horser_login, name='horser_login'),
    url(r'^horser_help/$', horser_help, name='horser_help'),
    url(r'^interface_webtest/$', interface_webtest, name='interface_webtest'),
    url(r'^interface_webtest_detail/(\w+)$', interface_webtest_detail, name='interface_webtest_detail'),
    url(r'^interface_add/$', interface_add, name='interface_add'),
    url(r'^domain_add/$', domain_add, name='domain_add'),
    url(r'^interface_depot/$', interface_depot, name='interface_depot'),
    url(r'^domain_manage/$', domain_manage, name='domain_manage'),
    url(r'^select_domain/$', select_domain, name='select_domain'),
    url(r'^edit_domain/$', edit_domain, name='edit_domain'),
    url(r'^edit_category/$', edit_category, name='edit_category'),
    url(r'^category_add/$', category_add, name='category_add'),
    url(r'^delete_category/$', delete_category, name='delete_category'),
    url(r'^webtest_go/$', webtest_go, name='webtest_go'),
    url(r'^interface_detail/(\w+)$', interface_detail, name='interface_detail'),

    ]
