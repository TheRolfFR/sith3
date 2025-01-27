# -*- coding:utf-8 -*
#
# Copyright 2019
# - Sli <antoine@bartuccio.fr>
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

from django.urls import re_path

from pedagogy.views import *

urlpatterns = [
    # Urls displaying the actual application for visitors
    re_path(r"^$", UVListView.as_view(), name="guide"),
    re_path(r"^uv/(?P<uv_id>[0-9]+)$", UVDetailFormView.as_view(), name="uv_detail"),
    re_path(
        r"^comment/(?P<comment_id>[0-9]+)/edit$",
        UVCommentUpdateView.as_view(),
        name="comment_update",
    ),
    re_path(
        r"^comment/(?P<comment_id>[0-9]+)/delete$",
        UVCommentDeleteView.as_view(),
        name="comment_delete",
    ),
    re_path(
        r"^comment/(?P<comment_id>[0-9]+)/report$",
        UVCommentReportCreateView.as_view(),
        name="comment_report",
    ),
    # Moderation
    re_path(r"^moderation$", UVModerationFormView.as_view(), name="moderation"),
    # Administration : Create Update Delete Edit
    re_path(r"^uv/create$", UVCreateView.as_view(), name="uv_create"),
    re_path(r"^uv/(?P<uv_id>[0-9]+)/delete$", UVDeleteView.as_view(), name="uv_delete"),
    re_path(r"^uv/(?P<uv_id>[0-9]+)/edit$", UVUpdateView.as_view(), name="uv_update"),
]
