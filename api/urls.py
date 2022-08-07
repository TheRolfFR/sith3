# -*- coding:utf-8 -*
#
# Copyright 2016,2017
# - Skia <skia@libskia.so>
#
# Ce fichier fait partie du site de l'Association des Étudiants de l'UTBM,
# http://ae.utbm.fr.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License a published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Sofware Foundation, Inc., 59 Temple
# Place - Suite 330, Boston, MA 02111-1307, USA.
#
#

from django.urls import re_path, path, include

from api.views import *
from rest_framework import routers

# Router config
router = routers.DefaultRouter()
router.register(r"counter", CounterViewSet, basename="api_counter")
router.register(r"user", UserViewSet, basename="api_user")
router.register(r"club", ClubViewSet, basename="api_club")
router.register(r"group", GroupViewSet, basename="api_group")

# Launderette
router.register(
    r"launderette/place", LaunderettePlaceViewSet, basename="api_launderette_place"
)
router.register(
    r"launderette/machine",
    LaunderetteMachineViewSet,
    basename="api_launderette_machine",
)
router.register(
    r"launderette/token", LaunderetteTokenViewSet, basename="api_launderette_token"
)

urlpatterns = [
    # API
    re_path(r"^", include(router.urls)),
    re_path(r"^login/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r"^markdown$", RenderMarkdown, name="api_markdown"),
    re_path(r"^mailings$", FetchMailingLists, name="mailings_fetch"),
    re_path(r"^uv$", uv_endpoint, name="uv_endpoint"),
    path("sas/<int:user>", all_pictures_of_user_endpoint, name="all_pictures_of_user"),
]
