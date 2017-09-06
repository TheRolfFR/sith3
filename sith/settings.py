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

"""
Django settings for sith project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import binascii
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ['HTTPS'] = "off"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(4sjxvhz@m5$0a$j0_pqicnc$s!vbve)z+&++m%g%bjhlz4+g2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS = ['*']


# Application definition

SITE_ID = 4000

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_jinja',
    'rest_framework',
    'ajax_select',
    'haystack',
    'core',
    'club',
    'subscription',
    'accounting',
    'counter',
    'eboutic',
    'launderette',
    'api',
    'rootplace',
    'sas',
    'com',
    'election',
    'forum',
    'stock',
    'trombi',
    'matmat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'sith.urls'

TEMPLATES = [
    {
        "NAME": "jinja2",
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "app_dirname": "templates",
            "newstyle_gettext": True,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
            ],
            "filters": {
                "markdown": "core.templatetags.renderer.markdown",
            },
            "globals": {
                "can_edit_prop": "core.views.can_edit_prop",
                "can_edit": "core.views.can_edit",
                "can_view": "core.views.can_view",
                "settings": "sith.settings",
                "Launderette": "launderette.models.Launderette",
                "Counter": "counter.models.Counter",
                "ProductType": "counter.models.ProductType",
                "timezone": "django.utils.timezone",
                "get_sith": "com.views.sith",
                "scss": "core.templatetags.renderer.scss",
            },
            "bytecode_cache": {
                "name": "default",
                "backend": "django_jinja.cache.BytecodeCache",
                "enabled": False,
            },
            "autoescape": True,
            "auto_reload": True,
            "translation_engine": "django.utils.translation",
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'core.search_indexes.UserOnlySignalProcessor'

SASS_PRECISION = 8

WSGI_APPLICATION = 'sith.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

PHONENUMBER_DEFAULT_REGION = "FR"

# Medias
MEDIA_ROOT = './data/'
MEDIA_URL = '/data/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = './static/'

# Static files finders which allow to see static folder in all apps
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'core.scss.finder.ScssFinder',
]

# Auth configuration
AUTH_USER_MODEL = 'core.User'
AUTH_ANONYMOUS_MODEL = 'core.models.AnonymousUser'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'
DEFAULT_FROM_EMAIL = "bibou@git.an"
SITH_COM_EMAIL = "bibou_com@git.an"

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = "localhost"
EMAIL_PORT = 25

# Below this line, only Sith-specific variables are defined

IS_OLD_MYSQL_PRESENT = False
OLD_MYSQL_INFOS = {
    'host': 'ae-db',
    'user': "my_user",
    'passwd': "password",
    'db': "ae2-db",
    'charset': 'utf8',
    'use_unicode': True,
}


SITH_URL = "my.url.git.an"
SITH_NAME = "Sith website"

# AE configuration
SITH_MAIN_CLUB_ID = 1  # TODO: keep only that first setting, with the ID, and do the same for the other clubs
SITH_MAIN_CLUB = {
    'name': "AE",
    'unix_name': "ae",
    'address': "6 Boulevard Anatole France, 90000 Belfort"
}

# Bar managers
SITH_BAR_MANAGER = {
    'name': "BdF",
    'unix_name': "bdf",
    'address': "6 Boulevard Anatole France, 90000 Belfort"
}

# Launderette managers
SITH_LAUNDERETTE_MANAGER = {
    'name': "Laverie",
    'unix_name': "laverie",
    'address': "6 Boulevard Anatole France, 90000 Belfort"
}

# Define the date in the year serving as reference for the subscriptions calendar
# (month, day)
SITH_START_DATE = (8, 15)  # 15th August

# Used to determine the valid promos
SITH_SCHOOL_START_YEAR = 1999

SITH_GROUP_ROOT_ID = 1
SITH_GROUP_PUBLIC_ID = 2
SITH_GROUP_SUBSCRIBERS_ID = 3
SITH_GROUP_OLD_SUBSCRIBERS_ID = 4
SITH_GROUP_ACCOUNTING_ADMIN_ID = 5
SITH_GROUP_COM_ADMIN_ID = 6
SITH_GROUP_COUNTER_ADMIN_ID = 7
SITH_GROUP_BANNED_ALCOHOL_ID = 8
SITH_GROUP_BANNED_COUNTER_ID = 9
SITH_GROUP_BANNED_SUBSCRIPTION_ID = 10
SITH_GROUP_SAS_ADMIN_ID = 11
SITH_GROUP_FORUM_ADMIN_ID = 12


SITH_CLUB_REFOUND_ID = 89
SITH_COUNTER_REFOUND_ID = 38
SITH_PRODUCT_REFOUND_ID = 5

# Pages
SITH_CORE_PAGE_SYNTAX = "Aide_sur_la_syntaxe"

# Forum

SITH_FORUM_PAGE_LENGTH = 30

# SAS variables
SITH_SAS_ROOT_DIR_ID = 4

SITH_BOARD_SUFFIX = "-bureau"
SITH_MEMBER_SUFFIX = "-membres"

SITH_MAIN_BOARD_GROUP = SITH_MAIN_CLUB['unix_name'] + SITH_BOARD_SUFFIX
SITH_MAIN_MEMBERS_GROUP = SITH_MAIN_CLUB['unix_name'] + SITH_MEMBER_SUFFIX

SITH_PROFILE_DEPARTMENTS = [
    ("TC", _("TC")),
    ("IMSI", _("IMSI")),
    ("IMAP", _("IMAP")),
    ("INFO", _("INFO")),
    ("GI", _("GI")),
    ("E", _("E")),
    ("EE", _("EE")),
    ("GESC", _("GESC")),
    ("GMC", _("GMC")),
    ("MC", _("MC")),
    ("EDIM", _("EDIM")),
    ("HUMA", _("Humanities")),
    ("NA", _("N/A")),
]

SITH_ACCOUNTING_PAYMENT_METHOD = [
    ('CHECK', _('Check')),
    ('CASH', _('Cash')),
    ('TRANSFERT', _('Transfert')),
    ('CARD', _('Credit card')),
]

SITH_SUBSCRIPTION_PAYMENT_METHOD = [
    ('CHECK', _('Check')),
    ('CARD', _('Credit card')),
    ('CASH', _('Cash')),
    ('EBOUTIC', _('Eboutic')),
    ('OTHER', _('Other')),
]

SITH_SUBSCRIPTION_LOCATIONS = [
    ('BELFORT', _('Belfort')),
    ('SEVENANS', _('Sevenans')),
    ('MONTBELIARD', _('Montbéliard')),
    ('EBOUTIC', _('Eboutic')),
]

SITH_COUNTER_BARS = [
    (1, "MDE"),
    (2, "Foyer"),
    (35, "La Gommette"),
]

SITH_COUNTER_PAYMENT_METHOD = [
    ('CHECK', _('Check')),
    ('CASH', _('Cash')),
    ('CARD', _('Credit card')),
]

SITH_COUNTER_BANK = [
    ('OTHER', 'Autre'),
    ('SOCIETE-GENERALE', 'Société générale'),
    ('BANQUE-POPULAIRE', 'Banque populaire'),
    ('BNP', 'BNP'),
    ('CAISSE-EPARGNE', 'Caisse d\'épargne'),
    ('CIC', 'CIC'),
    ('CREDIT-AGRICOLE', 'Crédit Agricole'),
    ('CREDIT-MUTUEL', 'Credit Mutuel'),
    ('CREDIT-LYONNAIS', 'Credit Lyonnais'),
    ('LA-POSTE', 'La Poste'),
]

SITH_ECOCUP_CONS = 1152

SITH_ECOCUP_DECO = 1151

# The limit is the maximum difference between cons and deco possible for a customer
SITH_ECOCUP_LIMIT = 3

# Defines pagination for cash summary
SITH_COUNTER_CASH_SUMMARY_LENGTH = 50

# Defines which product type is the refilling type, and thus increases the account amount
SITH_COUNTER_PRODUCTTYPE_REFILLING = 3

# Defines which product is the one year subscription and which one is the six month subscription
SITH_PRODUCT_SUBSCRIPTION_ONE_SEMESTER = 1
SITH_PRODUCT_SUBSCRIPTION_TWO_SEMESTERS = 2
SITH_PRODUCTTYPE_SUBSCRIPTION = 2

SITH_CAN_CREATE_SUBSCRIPTIONS = [
    1,
]

# Subscription durations are in semestres
# Be careful, modifying this parameter will need a migration to be applied
SITH_SUBSCRIPTIONS = {
    'un-semestre': {
        'name': _('One semester'),
        'price': 15,
        'duration': 1,
    },
    'deux-semestres': {
        'name': _('Two semesters'),
        'price': 28,
        'duration': 2,
    },
    'cursus-tronc-commun': {
        'name': _('Common core cursus'),
        'price': 45,
        'duration': 4,
    },
    'cursus-branche': {
        'name': _('Branch cursus'),
        'price': 45,
        'duration': 6,
    },
    'cursus-alternant': {
        'name': _('Alternating cursus'),
        'price': 30,
        'duration': 6,
    },
    'membre-honoraire': {
        'name': _('Honorary member'),
        'price': 0,
        'duration': 666,
    },
    'assidu': {
        'name': _('Assidu member'),
        'price': 0,
        'duration': 2,
    },
    'amicale/doceo': {
        'name': _('Amicale/DOCEO member'),
        'price': 0,
        'duration': 2,
    },
    'reseau-ut': {
        'name': _('UT network member'),
        'price': 0,
        'duration': 1,
    },
    'crous': {
        'name': _('CROUS member'),
        'price': 0,
        'duration': 2,
    },
    'sbarro/esta': {
        'name': _('Sbarro/ESTA member'),
        'price': 15,
        'duration': 2,
    },
    'un-semestre-welcome': {
        'name': _('One semester Welcome Week'),
        'price': 0,
        'duration': 1,
    },
    'deux-mois-essai': {
        'name': _('Two month for free'),
        'price': 0,
        'duration': 0.33,
    }
    # To be completed....
}

SITH_CLUB_ROLES = {}

SITH_CLUB_ROLES_ID = {
    'President': 10,
    'Vice-President': 9,
    'Treasurer': 7,
    'Communication supervisor': 5,
    'Secretary': 4,
    'IT supervisor': 3,
    'Board member': 2,
    'Active member': 1,
    'Curious': 0,
}

SITH_CLUB_ROLES = {
    10: _('President'),
    9: _('Vice-President'),
    7: _('Treasurer'),
    5: _('Communication supervisor'),
    4: _('Secretary'),
    3: _('IT supervisor'),
    2: _('Board member'),
    1: _('Active member'),
    0: _('Curious'),
}

# This corresponds to the maximum role a user can freely subscribe to
# In this case, SITH_MAXIMUM_FREE_ROLE=1 means that a user can set himself as "Membre actif" or "Curieux", but not higher
SITH_MAXIMUM_FREE_ROLE = 1

# Minutes to timeout the logged barmen
SITH_BARMAN_TIMEOUT = 20

# Minutes to delete the last operations
SITH_LAST_OPERATIONS_LIMIT = 10

# Minutes for a counter to be inactive
SITH_COUNTER_MINUTE_INACTIVE = 10

# ET variables
SITH_EBOUTIC_CB_ENABLED = True
SITH_EBOUTIC_ET_URL = "https://preprod-tpeweb.e-transactions.fr/cgi/MYchoix_pagepaiement.cgi"
SITH_EBOUTIC_PBX_SITE = "4000666"
SITH_EBOUTIC_PBX_RANG = "42"
SITH_EBOUTIC_PBX_IDENTIFIANT = "123456789"
SITH_EBOUTIC_HMAC_KEY = binascii.unhexlify("0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF")
SITH_EBOUTIC_PUB_KEY = ""
with open('./sith/et_keys/pubkey.pem') as f:
    SITH_EBOUTIC_PUB_KEY = f.read()

# Launderette variables
SITH_LAUNDERETTE_MACHINE_TYPES = [('WASHING', _('Washing')), ('DRYING', _('Drying'))]
SITH_LAUNDERETTE_PRICES = {
    'WASHING': 1.0,
    'DRYING': 0.75,
}

SITH_NOTIFICATIONS = [
    ('MAILING_MODERATION', _("A new mailing list needs to be moderated")),
    ('NEWS_MODERATION', _("There are %s fresh news to be moderated")),
    ('FILE_MODERATION', _("New files to be moderated")),
    ('SAS_MODERATION', _("New pictures/album to be moderated in the SAS")),
    ('NEW_PICTURES', _("You've been identified on some pictures")),
    ('REFILLING', _("You just refilled of %s €")),
    ('SELLING', _("You just bought %s")),
    ('GENERIC', _("You have a notification")),
]

# The keys are the notification names as found in SITH_NOTIFICATIONS, and the
# values are the callback function to update the notifs.
# The callback must take the notif object as first and single argument.
SITH_PERMANENT_NOTIFICATIONS = {
    'NEWS_MODERATION': 'com.models.news_notification_callback',
}

SITH_QUICK_NOTIF = {
    'qn_success': _("Success!"),
    'qn_fail': _("Fail!"),
    'qn_weekmail_new_article': _("You successfully posted an article in the Weekmail"),
    'qn_weekmail_article_edit': _("You successfully edited an article in the Weekmail"),
    'qn_weekmail_send_success': _("You successfully sent the Weekmail"),
}

# Mailing related settings

SITH_MAILING_DOMAIN = 'utbm.fr'
SITH_MAILING_FETCH_KEY = 'IloveMails'

try:
    from .settings_custom import *
    print("Custom settings imported", file=sys.stderr)
except:
    print("Custom settings failed", file=sys.stderr)

if DEBUG:
    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'sith.toolbar_debug.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    SASS_INCLUDE_FOLDERS = [
        'core/static/',
    ]
