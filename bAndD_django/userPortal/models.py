""" models.py """
from datetime import date
from django.db import models
from django.db.models import F
from django.conf import settings 
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.urls import reverse

def validate_blocks(value):
    """ Validate blocks value is 0-4 """
    if value < 0 or value > 4:
        raise ValidationError(
            'Blocks must be 0-4. The value %(value)s is out of range.', 
            params={'value': value},)

def validate_dollars(value):
    """ Validate dollars value is 0-999.99 """
    if value < 0 or value > 999.99:
        raise ValidationError(
        'Dollars must be $0-$999.99. The value %(value)s is out of range.',
        params={'value': value},)

def validate_minutes_left(value):
    """ Validate minutes_left value is 0-200 """
    if value < 0 or value > 200:
        raise ValidationError(
        'Minutes_left must be 0-200. The value %(value)s is out of range.',
        params={'value': value},)

def validate_coins(value):
    """ Validate coins value is 0-20 """
    if value < 0 or value > 20:
        raise ValidationError(
        'Minutes_left must be 0-20. The value %(value)s is out of range.',
        params={'value': value},)

class UpdateEvent(models.Model):
    """ A record of User Activity """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #{0:blocks, 1:dollars, 2:minutes, 3:did_read, 4:did_do_homework:, 5:coins,
    # 6:buy}
    type = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True,
        default=0.00)
    reason = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        types = ['blocks', 'dollars', 'minutes', 'did_read', 'did_do_homework',
            'coins', 'buy']
        return '{0} changed {1} by: {2}.'.format(
            self.user.username, types[self.type], str(self.amount))

class DailyRequirementsReport(models.Model):
    """ A record of daily objectives completion """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_reports')
    book_read = models.CharField(verbose_name='Today\'s book', max_length=50)
    last_page_read = models.IntegerField(help_text='# of last full page')
    reading_summary = models.CharField(verbose_name='Reading summary', max_length=300)
    had_schoolwork = models.BooleanField(verbose_name='Did assigned schoolwork')
    had_other_homework = models.BooleanField(verbose_name='Did self-directed study')
    homework_description = models.CharField(verbose_name='Homework summary', 
        max_length=300)
    ixl_math_completed = models.IntegerField(
        verbose_name='Number of IXL math skills today')
    ixl_language_arts_completed = models.IntegerField(
        verbose_name='Number of IXL language arts skills today')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.user.username, str(self.timestamp))

    def get_absolute_url(self):
        return reverse('daily-report-detail', kwargs={'pk': self.pk})
        
    class Meta:
        get_latest_by = "timestamp"

class Child(models.Model):
    """ Non admin user type """
    
    class Meta:
        verbose_name_plural = "children"

    user = models.OneToOneField(User, 
        on_delete=models.CASCADE)
    parent = models.ForeignKey(User, 
        on_delete=models.CASCADE, blank=True, null=True, related_name='parent')
    child_last_login = models.DateField(null=True, blank=True)
    blocks = models.PositiveSmallIntegerField(default=0, blank=True, 
        validators=[validate_blocks])
    coins = models.PositiveSmallIntegerField(default=0, 
        validators=[validate_coins])
    dollars = models.DecimalField(max_digits=6, decimal_places=2, blank=True,
        validators=[validate_dollars], default=0.00)
    minutes_left = models.PositiveSmallIntegerField(default=120, blank=True,
        validators=[validate_minutes_left])
    is_ready_for_screens = models.BooleanField(default=False)
    screentime_is_on = models.BooleanField(default=False)
    daily_minutes = models.PositiveSmallIntegerField(default=120, blank=True)
    weekly_allowance = models.DecimalField(max_digits=5, decimal_places=2,
        default=3.00)
    most_recent_screentime = models.DateField(null=True, blank=True)
    most_recent_screentime_ready = models.DateField(null=True, blank=True)
    no_screens_until = models.DateField(null=True, blank=True)

    def clean(self):
        """ 
        Override Child.clean() to set is_ready_for_screens and
        validate screentime_is_on.
        """
        super(Child, self).clean()
        
        # screentime_is_on requires is_ready_for_screens
        if not self.is_ready_for_screens:
            self.screentime_is_on = False
    
    def get_latest_report(self):
        return self.user.daily_reports.latest()

    def get_absolute_url(self):
        return reverse('child-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username


