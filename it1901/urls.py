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
    url(r'^manager/tekniskebehov/', views.manager_mainpage, name='manager'),
    url(r'^tekniker', views.tech_view, name = 'tekniker'),
    url(r'^arrangoer/riggeliste/',views.arrangoer_mainpage,name='webapp/riggeliste'),
    url(r'^arrangoer/sceneoversikt/', views.oversiktsview_konserter, name='webapp/sceneoversikt'),
    url(r'^login/$', loginviews.login, name='login'),
    url(r'^logout/$', loginviews.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^redir/',views.redirect_login,name='redirect'),
    url(r'^arrangoer',views.arrangoer,name='arrangoer'),
    url(r'^bookingansvarlig/tidligere_konserter/$',views.bookingansvarlig_tidligere_konserter,name='webapp/bookingansvarlig_tidligere_konserter'),
    url(r'^bookingansvarlig/tekniske_behov/$',views.bookingansvarlig_tekniske_behov,name='webapp/bookingansvarlig_tekniske_behov'),
    url(r'^bookingansvarlig/$',views.bookingansvarlig,name="bookingansvarlig"),
    url(r'^bookingansvarlig/bestilling/$', views.bookingansvarlig_bestilling_view, name='webapp/bookingansvarlig_bestilling'),
    url(r'^bookingansvarlig/artister/$', views.bookingansvarlig_artister, name = 'webapp/bookingansvarlig_artister'),
    url(r'^bookingansvarlig/tidligere_artister/$', views.bookingansvarlig_tidligere_artister, name = 'webapp/bookingansvarlig_tidligere_artister'),
    url(r'^bookingsjef$',views.bookingsjef_prisgenerator,name="bookingsjef"),
    url(r'^bookingsjef/rapport/$',views.bookingsjef_rapport,name="webapp/bookingsjef_rapport"),
    url(r'^bookingsjef/bandtilbud/',views.bookingsjef_bandtilbud,name="webapp/bookingsjef_bandtilbud"),

    url(r'^bookingsjef/oversikt/$',views.bookingsjef_oversikt,name="webapp/bookingsjef_oversikt")
]
