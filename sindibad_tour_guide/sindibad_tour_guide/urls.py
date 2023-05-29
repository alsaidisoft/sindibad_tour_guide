"""
URL configuration for sindibad_tour_guide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='index'),
    path('home', views.homepage, name='index'),
    path('login/log', views.loginpage, name='log'),
    path('index', views.indexpage, name='index'),
    path('result', views.result, name='result'),
    path('about', views.about, name='about'),
    path('page/<int:id>', views.page, name='page'),
    path('countries/show', views.showcountries, name='show'),
    path('cities/show', views.showcities, name='show'),
    path('users/show', views.showusers, name='show'),
    path('categories/show', views.showcategories, name='show'),
    path('sub_cat/show', views.showsubcat, name='show'),
    path('login/index', views.logout, name='log'),
    path('login/singin', views.singin, name='singin'),
    path('login/log', views.singin, name='singin'),
    path('countries/add', views.addcountry, name='addcountry'),
    path('users/add', views.adduser, name='adduser'),
    path('cities/add', views.addcity, name='addcity'),
    path('categories/add', views.addcategory, name='addcategory'),
    path('sub_cat/add', views.addsubcat, name='addsubcat'),
    path('countries/edit/<int:id>', views.editcountry, name='editcountry'),
    path('users/edit/<int:id>', views.edituser, name='edituser'),
    path('cities/edit/<int:id>', views.editcity, name='editcity'),
    path('categories/edit/<int:id>', views.editcategory, name='editcategory'),
    path('sub_cat/edit/<int:id>', views.editsubcat, name='editsubcat'),
    path('countries/updatecountry/<int:id>', views.updatecountry, name='updatecountry'),
    path('users/updateuser/<int:id>', views.updateuser, name='updateuser'),
    path('cities/updatecity/<int:id>', views.updatecity, name='updatecity'),
    path('categories/updatecategory/<int:id>', views.updatecategory, name='updatecategory'),
    path('sub_cat/updatesubcat/<int:id>', views.updatesubcat, name='updatesubcat'),
    path('countries/deletecountry/<int:id>', views.deletecountry, name='deletecountry'),
    path('cities/deletecity/<int:id>', views.deletecity, name='deletecity'),
    path('categories/deletecategory/<int:id>', views.deletecategory, name='deletecategory'),
    path('sub_cat/deletesubcat/<int:id>', views.deletesubcat, name='deletesubcat'),
    path('users/deleteuser/<int:id>', views.deleteuser, name='deleteuser'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
