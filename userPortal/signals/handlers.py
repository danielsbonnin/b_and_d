""" userPortal/signals/handlers.py """
from datetime import date
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from userPortal.models import Child
from userPortal import childHelpers
from django.contrib.auth.models import User
from userPortal.signals.signals import child_logged_out, child_logged_in

def create_child(sender, instance, created, **kwargs):
    """ Create the Child user type on User creation """
    if created:
        new_child = Child(user=instance)
        new_child.save()

# Handle the signal generated on User creation

def logged_in_handler(sender, **kwargs):
    """ logged-in handler """
    
    this_child = sender.child
    print(this_child.user.username + ' logged into the userPortal')
    # Add 1/7 weekly allowance for all days since last login
    # Add a block every thursday

    this_last_login_day = this_child.child_last_login or date.today()

    # Monday - Sunday is 0-6
    FREE_BLOCK_DAY = 3 # Thursday
    free_blocks = childHelpers.calculate_free_blocks(this_last_login_day,
        FREE_BLOCK_DAY)

    # Calculate how many coins/blocks to award
    new_blocks, new_coins = childHelpers.calculate_coins(
        free_blocks, this_child.blocks, this_child.coins)

    # Calculate allowance for each day since last login
    allowance_to_add = childHelpers.calculate_allowance_to_add(
        this_last_login_day, this_child.weekly_allowance)

    # Add calculated allowance to this_child.dollars
    childHelpers.save_auto_dollars(this_child, this_child.dollars,
        allowance_to_add)

    # Save updated blocks amount
    childHelpers.save_auto_blocks(this_child, this_child.blocks, 
        new_blocks, free_blocks)

    # Save updated coins amount
    childHelpers.save_auto_coins(this_child, this_child.coins, new_coins)

    # Update last_login value
    this_child.child_last_login = date.today()

    # Check if child has been banned from screentime
    if this_child.no_screens_until \
        and this_child.no_screens_until > date.today():
        this_child.minutes_left = 0
    
    # Reset minutes_left on first daily login
    elif not this_child.most_recent_screentime or\
        this_child.most_recent_screentime < date.today():
        this_child.minutes_left = this_child.daily_minutes
        this_child.most_recent_screentime = date.today()
    
    if not this_child.most_recent_screentime_ready or\
        this_child.most_recent_screentime_ready < date.today():
        this_child.is_ready_for_screens = False;
    this_child.save()
    
def logged_out_handler(sender, **kwargs):
    """ logged-out handler """
    this_child = sender.child
    print(this_child.user.username + ' logged_out_handler dispatched')
    if this_child.screentime_is_on:
        this_child.screentime_is_on = False
        this_child.save()
        print('Blocks and Dad Dollars turned off screen time on logout')

post_save.connect(create_child, sender=User)
child_logged_in.connect(logged_in_handler)
child_logged_out.connect(logged_out_handler)