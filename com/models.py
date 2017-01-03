from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings
from django.core.mail import EmailMessage

from core.models import User
from club.models import Club

class Sith(models.Model):
    """A one instance class storing all the modifiable infos"""
    alert_msg = models.TextField(_("alert message"), default="", blank=True)
    info_msg = models.TextField(_("info message"), default="", blank=True)
    index_page = models.TextField(_("index page"), default="", blank=True)
    weekmail_destinations = models.TextField(_("weekmail destinations"), default="")

    def is_owned_by(self, user):
        return user.is_in_group(settings.SITH_GROUP_COM_ADMIN_ID)

    def __str__(self):
        return "⛩ Sith ⛩"

NEWS_TYPES = [
        ('NOTICE', _('Notice')),
        ('EVENT', _('Event')),
        ('WEEKLY', _('Weekly')),
        ('CALL', _('Call')),
        ]

class News(models.Model):
    """The news class"""
    title = models.CharField(_("title"), max_length=64)
    summary = models.TextField(_("summary"))
    content = models.TextField(_("content"))
    type = models.CharField(_("type"), max_length=16, choices=NEWS_TYPES, default="EVENT")
    club = models.ForeignKey(Club, related_name="news", verbose_name=_("club"))
    author = models.ForeignKey(User, related_name="owned_news", verbose_name=_("author"))
    is_moderated = models.BooleanField(_("is moderated"), default=False)
    moderator = models.ForeignKey(User, related_name="moderated_news", verbose_name=_("moderator"), null=True)

    def is_owned_by(self, user):
        return user.is_in_group(settings.SITH_GROUP_COM_ADMIN_ID) or user == self.author

    def can_be_edited_by(self, user):
        return user.is_in_group(settings.SITH_GROUP_COM_ADMIN_ID)

    def can_be_viewed_by(self, user):
        return self.is_moderated or user.is_in_group(settings.SITH_GROUP_COM_ADMIN_ID)

    def get_absolute_url(self):
        return reverse('com:news_detail', kwargs={'news_id': self.id})

    def __str__(self):
        return "%s: %s" % (self.type, self.title)

class NewsDate(models.Model):
    """
    A date class, useful for weekly events, or for events that just have no date

    This class allows more flexibilty managing the dates related to a news, particularly when this news is weekly, since
    we don't have to make copies
    """
    news = models.ForeignKey(News, related_name="dates", verbose_name=_("news_date"))
    start_date = models.DateTimeField(_('start_date'), null=True, blank=True)
    end_date = models.DateTimeField(_('end_date'), null=True, blank=True)

    def __str__(self):
        return "%s: %s - %s" % (self.news.title, self.start_date, self.end_date)

class Weekmail(models.Model):
    """
    The weekmail class
    """
    title = models.CharField(_("title"), max_length=64, blank=True)
    intro = models.TextField(_("intro"), blank=True)
    joke = models.TextField(_("joke"), blank=True)
    protip = models.TextField(_("protip"), blank=True)
    conclusion = models.TextField(_("conclusion"), blank=True)
    sent = models.BooleanField(_("sent"), default=False)

    class Meta:
        ordering = ['-id']

    def send(self):
        with transaction.atomic():
            print("Sending weekmail n°" + str(self.id))
            email = EmailMessage(
                    subject=self.title,
                    body="\n\n".join([self.intro, self.joke, self.protip, self.conclusion]),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[],
                    bcc=Sith.objects.first().weekmail_destinations.split(' '),
                    )
            self.sent = True
            self.save()
            Weekmail().save()

class WeekmailArticle(models.Model):
    weekmail = models.ForeignKey(Weekmail, related_name="articles", verbose_name=_("weekmail"))
    title = models.CharField(_("title"), max_length=64)
    content = models.TextField(_("content"))
    author = models.ForeignKey(User, related_name="owned_weekmail_articles", verbose_name=_("author"))
    club = models.ForeignKey(Club, related_name="weekmail_articles", verbose_name=_("club"))
    rank = models.IntegerField(_('rank'), default=-1)

    def clean(self):
        super(WeekmailArticle, self).clean()
        if not self.weekmail:
            self.weekmail = Weekmail.objects.order_by('-id').first()
