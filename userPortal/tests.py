from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Child

class UserProfileTest(TestCase):
    """ 
    Test the auto-creation of a Child
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', email='tester@tester.com', password='testpass')
    def check_child(self):
        this_child = self.user.child
        
# Create your tests here.
class ChildBlocksAddTest(TestCase):
    """
    Test adding blocks for all valid values
    """
    def test_smoke_test(self):
        self.assertIs(True, True)