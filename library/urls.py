from django.urls import path
from .views import UserRegistration, ListBooks, BorrowBook, BorrowHistory, ManageBorrowRequests

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('books/', ListBooks.as_view(), name='books'),
    path('borrow/', BorrowBook.as_view(), name='borrow'),
    path('history/', BorrowHistory.as_view(), name='history'),
    path('requests/', ManageBorrowRequests.as_view(), name='manage_requests'),
    path('requests/<int:pk>/', ManageBorrowRequests.as_view(), name='update_request'),
]
