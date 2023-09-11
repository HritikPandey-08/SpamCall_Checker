from django.urls import path
from .views import mark_number_as_spam, get_spam_numbers,search_users

urlpatterns = [
    path('api/spam/mark/', mark_number_as_spam, name='mark_number_as_spam'),
    path('api/spam/', get_spam_numbers, name='get_spam_numbers'),
    path('api/spam/search/', search_users, name='search_users'),
]