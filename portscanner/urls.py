"""
URL configuration for portscanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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


# portscanner/urls.py
import logging
from django.contrib import admin
from django.urls import path
from portscanner_app.views import home_view, scan_view
import sys

logger = logging.getLogger(__name__)

logger.info(sys.path)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('scan/', scan_view, name='scan'),
]


"""# portscanner/urls.py
from django.contrib import admin
from django.urls import path
from portscanner_app.views import scan_view, home_view

import sys
print(sys.path)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('scan/', scan_view, name='scan'),
]"""


"""from django.urls import path, include
from django.contrib import admin
from portscanner_app.views import scan_view, home_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('scan/', scan_view, name='scan'),
]"""
