"""it1901 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as loginviews
from webapp import views


urlpatterns = [
    # index
    url(r'^$', loginviews.login, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^teknikker', views.tech_view, name = 'teknikker'),
    url(r'^arrangoer/riggeliste/',views.arrangoer_mainpage,name='webapp/riggeliste'),
    url(r'^arrangoer/sceneoversikt/', views.oversiktsview_konserter, name='webapp/sceneoversikt'),
    url(r'^login/$', loginviews.login, name='login'),
    url(r'^logout/$', loginviews.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^redir/',views.redirect_login,name='redirect'),
    url(r'^arrangoer',views.arrangoer,name='arrangoer'),

]
