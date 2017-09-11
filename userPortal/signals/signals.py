""" userPortal/signals.py """
import django.dispatch

child_logged_out = django.dispatch.Signal()
child_logged_in = django.dispatch.Signal()