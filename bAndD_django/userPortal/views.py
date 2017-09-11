""" views.py """
import json
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum, Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from userPortal.models import Child, UpdateEvent, DailyRequirementsReport
from userPortal.forms import UpdateBlocksForm, ScreentimePrereqsForm
from userPortal.forms import UpdateDollarsForm
from userPortal.signals.signals import child_logged_out, child_logged_in
from adminPortal.forms import StoreItemRequestForm
from adminPortal.models import Store_item

def logout(request):
    """ Send logout signal to userPortal.signals.handlers """
    child_logged_out.send(sender=request.user)
    return HttpResponseRedirect(reverse('userPortal:logout'))

def login(request):
    """ Send login signal to userPortal.signals.handlers """
    child_logged_in.send(sender=request.user)
    return HttpResponseRedirect(reverse('userPortal:users home'))

class Index(LoginRequiredMixin, View):
    template_name = 'userPortal/index.html' 

    def get(self, request):
        this_user = request.user
        this_child = this_user.child
        add_block_value = (this_child.blocks + 1) % 5
                            
        return render(request, self.template_name,
            context={'add_block_value': add_block_value})

class UpdateBlocksView(View):
    """ Handle Child blocks update """
    model = Child
    success_url = '/'

    def post(self, request, **kwargs):
        """ Handle blocks update """
        this_child = Child.objects.get(pk=kwargs['pk'])
        blocks_amount = int(self.request.POST.get('blocks', ''))
        update_event = UpdateEvent(
            user=request.user, 
            type=0, 
            amount=blocks_amount, 
            reason=self.request.POST.get('reason', 'because'))
        if blocks_amount:
            coin_amount = 0
            current_blocks_amount = this_child.blocks + blocks_amount
            if current_blocks_amount > 4:
                coin_amount = int(current_blocks_amount / 4)
                current_blocks_amount = current_blocks_amount % 5
            elif current_blocks_amount < 0:
                current_blocks_amount = 0
            this_child.blocks = current_blocks_amount
            if coin_amount > 0:
                this_child.coins = F('coins') + coin_amount
            this_child.save()
            update_event.save()
        return HttpResponseRedirect('/')

class UpdateDollarsView(UpdateView):
    """ Handle Child dollars update """
    
    def post(self, request, **kwargs):
        """ Handle dollars update """
        this_child = Child.objects.get(pk=kwargs['pk'])
        current_dollars_amount = float(this_child.dollars)
        dollars_amount = float(self.request.POST.get('dollars',''))
        result_amount = current_dollars_amount + dollars_amount
        
        # Save UpdateEvent
        update_event = UpdateEvent(
            user=request.user, 
            type=1, 
            amount=int(dollars_amount), 
            reason=self.request.POST.get('reason', 'because'))
        if result_amount > 0:
            this_child.dollars = F('dollars') + dollars_amount
            this_child.save()
        update_event.save()
        return HttpResponseRedirect('/')

class UpdateMinutesView(UpdateView):
    """ Handle Child minutes_left update """

    def post(self, request, **kwargs):
        """ Handle minutes_left update """

        this_child = Child.objects.get(pk=kwargs['pk'])
        new_minutes = int(self.request.POST.get('minutes_left', '-1'))
        screentime_is_on = False
        if self.request.POST.get('screentime_is_on', '') == "True":
            screentime_is_on = True
        current_minutes = this_child.minutes_left
        
        if new_minutes > 0:
        
            if new_minutes > current_minutes:
                current_minutes = current_minutes - 1
            else:
                current_minutes = new_minutes

        # Create UpdateEvent every 10 minutes of screentime
        if current_minutes % 10 == 0:
            # Save UpdateEvent
            update_event = UpdateEvent(
                user=request.user, 
                type=2, 
                amount=-10, 
                reason='Screentime timer running')
            update_event.save()
                
        this_child.minutes_left = current_minutes
        this_child.screentime_is_on = screentime_is_on;
        this_child.save()
        return HttpResponse(json.dumps(
            {
                'minutes_left': current_minutes,
                'screentime_is_on': screentime_is_on,
            }))

class BuyMinutesView(UpdateView):
    """ Handle Child minutes purchase """
    
    MINUTES_RATE = 30

    def post(self, request, **kwargs):
        """ Handle minutes purchase request """

        this_child = Child.objects.get(pk=kwargs['pk'])
        current_minutes = this_child.minutes_left
        current_dollars = this_child.dollars
        if self.request.POST.get('buy', '') == "True"\
            and current_dollars >= 1.00:
            current_minutes += self.MINUTES_RATE
            current_dollars = current_dollars - 1

            # Save UpdateEvent
            update_event = UpdateEvent(
                user=request.user, 
                type=6, 
                amount=1.00, 
                reason='Buy Screentime button')
            update_event.save()

        this_child.minutes_left = current_minutes
        this_child.dollars = current_dollars;
        this_child.save()
        return HttpResponse(json.dumps(
            {
                'minutes_left': current_minutes,
                'dollars': float(current_dollars)
            }))

class ChildDetailView(DetailView):
    """ Display Child Details """
    
    model = Child

class DailyReportDetailView(DetailView):
    """ Daily Report Details """
   
    model = DailyRequirementsReport
    
class ScreentimePrereqsView(CreateView):
    """ Display ScreentimePrereqsForm """
    form_class = ScreentimePrereqsForm
    template_name = 'screentimePrereqs.html'
    
    def form_valid(self, form):
        new_report = form.save(commit=False)
        this_user = self.request.user
        this_child = this_user.child

        new_report.user = this_user
        new_report.save()
        this_child.most_recent_screentime_ready = new_report.timestamp
        this_child.is_ready_for_screens = True
        this_child.save()
        return HttpResponseRedirect('/')

class IXLReportView(View):
    """ 
    Displays Child IXL statistics from their submitted
    DailyRequirementsReports
    """
    
    template_name = 'userPortal/ixl_report.html'
    
    def get(self, request, *args, **kwargs):
        """ Display report """

        this_child = Child.objects.get(pk=kwargs['pk'])
        this_user = this_child.user
        start_date = this_user.date_joined.date()
        one_year_ago = date.today() - timedelta(days=365)
        one_month_ago = date.today() - timedelta(days=30)
        one_week_ago = date.today() - timedelta(days=6)
        this_sunday = date.today() - timedelta(days=(date.today().weekday() + 1) % 8)
        print('this_sunday date: {}'.format(this_sunday))
        print('one_week_ago date: {}'.format(one_week_ago))
        reports_year = DailyRequirementsReport.objects.filter(user=this_user).\
            filter(timestamp__range=(one_year_ago, date.today())).\
            order_by('timestamp').only('ixl_math_completed', 'ixl_language_arts_completed', 'timestamp')
        reports_month = reports_year.\
            filter(timestamp__range=(one_month_ago, date.today())).\
            order_by('timestamp')
        reports_week = reports_month.\
            filter(timestamp__range=(one_week_ago, date.today())).\
            order_by('timestamp')
        reports_since_sunday = reports_week.\
            filter(timestamp__range=(this_sunday, date.today())).\
            order_by('timestamp')

        # Yearly ixl data
        if start_date < one_year_ago:
            start_date = one_year_ago
        reports_this_year = reports_year.count()
        date_of_first_yearly_report = reports_year.earliest('timestamp').timestamp
        yearly_data = reports_year.\
            aggregate(num_math = Sum('ixl_math_completed'), 
                num_la = Sum('ixl_language_arts_completed'))
     
        math_this_year = yearly_data['num_math']
        la_this_year = yearly_data['num_la']
        math_avg_this_year = math_this_year / ((date.today() - start_date).days + 1)
        la_avg_this_year = la_this_year / ((date.today() - start_date).days + 1)
        
        # Monthly ixl data
        if start_date < one_month_ago:
            start_date = one_month_ago
        reports_this_month = reports_month.count()
        date_of_first_monthly_report = reports_month.earliest('timestamp').timestamp
        monthly_data = reports_month.\
            aggregate(num_math = Sum('ixl_math_completed'),
                num_la = Sum('ixl_language_arts_completed'))
                
        math_this_month = monthly_data['num_math']
        la_this_month = monthly_data['num_la']
        math_avg_this_month = math_this_month / ((date.today() - start_date).days + 1)
        la_avg_this_month = la_this_month / ((date.today() - start_date).days + 1)
        
        # Weekly ixl data
        if start_date < one_week_ago:
            start_date = one_week_ago
        reports_this_week = reports_week.count()
        date_of_first_weekly_report = reports_week.earliest('timestamp').timestamp
        weekly_data = reports_week.\
            aggregate(num_math = Sum('ixl_math_completed'),
                num_la = Sum('ixl_language_arts_completed'))
        math_this_week = weekly_data['num_math']
        la_this_week = weekly_data['num_la']
        math_avg_this_week = math_this_week / ((date.today() - start_date).days + 1)
        la_avg_this_week = la_this_week / ((date.today() - start_date).days + 1)
        print('number of days this week: {}'.format(str((date.today() - start_date).days)))

        # Since Sunday ixl data
        if start_date < this_sunday:
            start_date = this_sunday
        print('start date: {}'.format(this_sunday))
        
        if start_date < this_sunday:
            start_date = this_sunday
        reports_this_since_sunday = reports_since_sunday.count()
        date_of_first_report_since_sunday = reports_since_sunday.earliest('timestamp').timestamp
        since_sunday_data = reports_since_sunday.\
            aggregate(num_math = Sum('ixl_math_completed'),
                num_la = Sum('ixl_language_arts_completed'))
                
        math_since_sunday = since_sunday_data['num_math']
        la_since_sunday = since_sunday_data['num_la']
        math_avg_since_sunday = math_since_sunday / ((date.today() - start_date).days + 1)
        la_avg_since_sunday = la_since_sunday / ((date.today() - start_date).days + 1)
        context = {
                'yearly_count': reports_this_year,
                'math_this_year': math_this_year,
                'la_this_year': la_this_year,
                'math_avg_this_year': round(math_avg_this_year, 2),
                'la_avg_this_year': round(la_avg_this_year, 2),
                'monthly_count': reports_this_month,
                'math_this_month': math_this_month,
                'la_this_month': la_this_month,
                'math_avg_this_month': round(math_avg_this_month, 2),
                'la_avg_this_month': round(la_avg_this_month, 2),
                'weekly_count': reports_this_week,
                'math_this_week': math_this_week,
                'la_this_week': la_this_week,
                'math_avg_this_week': round(math_avg_this_week, 2),
                'la_avg_this_week': round(la_avg_this_week, 2),
                'since_sunday_count': reports_this_since_sunday,
                'math_since_sunday': math_since_sunday,
                'la_since_sunday': la_since_sunday,
                'math_avg_since_sunday': round(math_avg_since_sunday, 2),
                'la_avg_since_sunday': round(la_avg_since_sunday, 2),
            }
        return render(request, template_name=self.template_name, context=context)

class CoinStoreView(LoginRequiredMixin, View):
    template_name = 'userPortal/coin_store.html'
    
    def get(self, request, *args, **kwargs):
        store_items = Store_item.objects.all()
        context = {'store_items': store_items }
        
        return render(request, template_name=self.template_name, context=context)
        
class CoinItemRequestView(LoginRequiredMixin, CreateView):
    """ Coin Item Request Form """
    template_name = 'storeItemRequestForm.html'
    form_class = StoreItemRequestForm
    success_url = '/'
    def form_valid(self, form):
        this_request = form.save(commit=False)
        this_request.child = self.request.user
        return super(CoinItemRequestView, self).form_valid(form)
    