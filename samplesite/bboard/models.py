from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import timedelta
from django.utils import timezone
class ReadingQuerySet(models.QuerySet):
    def by_reader(self, reader):
        return self.filter(reader=reader)

    def order_by_date(self):
        return self.order_by('start_date')


class SpecialReadingEventManager(models.Manager):
    def recent_events(self):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return self.get_queryset().filter(date__gte=thirty_days_ago)
class Reading(models.Model):
    reader = models.ForeignKey('Reader', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    start_date = models.DateField()

    objects = ReadingQuerySet.as_manager()

class SpecialReadingEvent(models.Model):
    description = models.TextField()
    date = models.DateField()
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    extra_notes = models.TextField(null=True, blank=True)

    objects = SpecialReadingEventManager()


class Event(models.Model):
    description = models.CharField(max_length=255)
    date = models.DateField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date']

    def __str__(self):
        return f"{self.description} on {self.date}"



class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']

    def __str__(self):
        return self.title

class Reader(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, through='Reading', related_name='readers')

    class Meta:
        verbose_name = 'Reader'
        verbose_name_plural = 'Readers'
        ordering = ['name']

    def __str__(self):
        return self.name


