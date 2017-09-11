from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Store_item(models.Model):
    """ Item that can be purchased with coins """
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    link = models.CharField(max_length=1000, null=True, blank=True)
    price = models.PositiveSmallIntegerField()
    date_added = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return ('{}'.format(self.name))

class Store_item_request(models.Model):
    """ Child's request for a coin price and listing in the coin store """
    child = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    link = models.CharField(max_length=1000, null=True, blank=True)
    date_of_request = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return ('{} from {}'.format(self.name, self.child.username)) 
