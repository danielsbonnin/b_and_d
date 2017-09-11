""" childHelpers.py """
from datetime import date
from .models import UpdateEvent, Child
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday']

def calculate_coins(blocks_to_add, current_blocks, current_coins):
    """ Calculate how many coins to add """
    total_blocks = blocks_to_add + current_blocks
    blocks_result = total_blocks % 5  # blocks value cannot exceed 4
    coins_result = total_blocks // 5  # 1 coin is awarded for every 5 blocks
    coins_result += current_coins
    return(blocks_result , coins_result)  # return a tuple (blocks, coins)

def calculate_free_blocks(last_login_date, free_block_day):
    """ Count how many free blocks days have passed since last login """

    last_login_weekday = last_login_date.weekday()
    today_weekday = date.today().weekday()
    num_days = (date.today() - last_login_date).days

    # Calculate days since most recent free block day
    days_since_free_block_day = ((today_weekday + 7) - free_block_day) % 7

    if num_days > days_since_free_block_day:
        blocks_to_add = 1 + (num_days - 1 - days_since_free_block_day) // 7
    else:
        blocks_to_add = 0

    print('Last login was {}, which was a {}.'
        .format(str(last_login_date),
            DAYS[last_login_weekday]))
    print('There were {} free block days since last login'.format(
        str(blocks_to_add)))

    return blocks_to_add

def calculate_allowance_to_add(last_login_date, weekly_allowance): 
    """ Calculate daily allowance * number of days """
    
    num_days = (date.today() - last_login_date).days
    daily_allowance = weekly_allowance / 7
    allowance_to_add = round(daily_allowance * num_days, 2)
    return allowance_to_add
    
def save_auto_dollars(child, old_dollars, dollars_to_add):
    """ Save new dollars and create UpdateEvent """
    new_dollars = old_dollars + dollars_to_add
    reason = 'automatic allowance deposit'
    update_event = UpdateEvent(user=child.user, type=1,
        amount=dollars_to_add, reason=reason)
    child.dollars = new_dollars
    child.save()
    update_event.save()

def save_auto_blocks(child, old_blocks, new_blocks, blocks_to_add):
    """ Save new blocks and create UpdateEvent """
 
    reason = 'automatic weekly block'
    update_event = UpdateEvent(user=child.user, type=0,
        amount=blocks_to_add, reason=reason)
    child.blocks = new_blocks
    child.save()
    update_event.save()
    
def save_auto_coins(child, old_coins, new_coins):
    """ Save new coins and create UpdateEvent """
 
    reason = 'automatic blocks increment'
    update_event = UpdateEvent(user=child.user, type=5,
        amount=new_coins - old_coins, reason=reason)
    child.coins = new_coins
    child.save()
    update_event.save()