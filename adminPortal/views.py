from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from django.urls import reverse_lazy, reverse
from userPortal.models import Child, DailyRequirementsReport
from .models import Store_item_request
# Create your views here.
#TemplateView.as_view(template_name="adminPortal/index.html")
class Index(LoginRequiredMixin, View):
    """ Admin home page """
    template_name = "adminPortal/index.html"
    def get(self, request):
        """ Handle GET requests """
        
        this_user = request.user
        
        context = {'children': Child.objects.filter(parent=this_user)}

        return render(request, self.template_name)

class ChildrenListView(ListView):
    """ Data about this Admin's children """
    
    model = Child
    template_name = 'adminPortal/child_list.html'

    def this_day(self):
        """ Return today's date """
        return date.today()
    
    def get_queryset(self):
        self.parent = get_object_or_404(User, id=self.kwargs['pid'])
        queryset = Child.objects.filter(parent=self.parent)
        
        return queryset

class DailyRequirementsReportDetail(DetailView):
    """ Data from a Child user's Screentime Requirements submission """
    
    model = DailyRequirementsReport
    template_name = 'adminPortal/dailyRequirementsReport_detail.html'

class CoinStoreReview(LoginRequiredMixin, ListView):
    """ View for reviewing coin store item requests """
    model = Store_item_request
    template_name = 'adminPortal/coin_store_review.html'
    
    def get_queryset(self):
        return Store_item_request.objects.filter(child__child__parent = self.request.user.id)
