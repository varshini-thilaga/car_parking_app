import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_parking.settings')
django.setup()
from django.urls import reverse, resolve
print('LOGIN URL', reverse('login'))
print('DASHBOARD URL', reverse('dashboard'))
print('RESOLVE LOGIN', resolve('/accounts/login/').view_name)
print('RESOLVE DASHBOARD', resolve('/dashboard/').view_name)
