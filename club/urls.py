# -*- coding:utf-8 -*
#
# Copyright 2016,2017
# - Skia <skia@libskia.so>
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

from club.views import *

urlpatterns = [
    re_path(r"^$", ClubListView.as_view(), name="club_list"),
    re_path(r"^new$", ClubCreateView.as_view(), name="club_new"),
    re_path(r"^stats$", ClubStatView.as_view(), name="club_stats"),
    re_path(r"^(?P<club_id>[0-9]+)/$", ClubView.as_view(), name="club_view"),
    re_path(
        r"^(?P<club_id>[0-9]+)/rev/(?P<rev_id>[0-9]+)/$",
        ClubRevView.as_view(),
        name="club_view_rev",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/hist$", ClubPageHistView.as_view(), name="club_hist"
    ),
    re_path(r"^(?P<club_id>[0-9]+)/edit$", ClubEditView.as_view(), name="club_edit"),
    re_path(
        r"^(?P<club_id>[0-9]+)/edit/page$",
        ClubPageEditView.as_view(),
        name="club_edit_page",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/members$", ClubMembersView.as_view(), name="club_members"
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/elderlies$",
        ClubOldMembersView.as_view(),
        name="club_old_members",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/sellings$",
        ClubSellingView.as_view(),
        name="club_sellings",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/sellings/csv$",
        ClubSellingCSVView.as_view(),
        name="sellings_csv",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/prop$", ClubEditPropView.as_view(), name="club_prop"
    ),
    re_path(r"^(?P<club_id>[0-9]+)/tools$", ClubToolsView.as_view(), name="tools"),
    re_path(
        r"^(?P<club_id>[0-9]+)/mailing$", ClubMailingView.as_view(), name="mailing"
    ),
    re_path(
        r"^(?P<mailing_id>[0-9]+)/mailing/generate$",
        MailingAutoGenerationView.as_view(),
        name="mailing_generate",
    ),
    re_path(
        r"^(?P<mailing_id>[0-9]+)/mailing/delete$",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    re_path(
        r"^(?P<mailing_subscription_id>[0-9]+)/mailing/delete/subscription$",
        MailingSubscriptionDeleteView.as_view(),
        name="mailing_subscription_delete",
    ),
    re_path(
        r"^membership/(?P<membership_id>[0-9]+)/set_old$",
        MembershipSetOldView.as_view(),
        name="membership_set_old",
    ),
    re_path(
        r"^membership/(?P<membership_id>[0-9]+)/delete$",
        MembershipDeleteView.as_view(),
        name="membership_delete",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/poster$", PosterListView.as_view(), name="poster_list"
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/poster/create$",
        PosterCreateView.as_view(),
        name="poster_create",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/poster/(?P<poster_id>[0-9]+)/edit$",
        PosterEditView.as_view(),
        name="poster_edit",
    ),
    re_path(
        r"^(?P<club_id>[0-9]+)/poster/(?P<poster_id>[0-9]+)/delete$",
        PosterDeleteView.as_view(),
        name="poster_delete",
    ),
]
