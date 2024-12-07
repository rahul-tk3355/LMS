from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from .models import User,Book,BorrowRequest
from .serializers import UserSerializer,BookSerializer,BorrowRequestSerializer
# Create your views here.

class UserRegistration(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListBooks(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BorrowBook(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        book = Book.objects.filter(id=data.get('book')).first()

        if not book:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        elif book.copies_available < 1:
            return Response({"error": "No available copies."}, status=status.HTTP_400_BAD_REQUEST)
        
        #Overlapping borrow dates
        overlapping_dates = BorrowRequest.objects.filter(
            book=book,
            end_date = data['start_date'],
            start_date = data['end_date'],
            status = 'Approved'
        ).exists()

        if overlapping_dates:
            return Response({'error': 'Book already borrowed on these dates.'}, status=status.HTTP_400_BAD_REQUEST)
        
        borrow_request = BorrowRequest.objects.create(
            user=user,
            book=book,
            start_date=data['start_date'],
            end_date = data['end_date'],
        )
        return Response(BorrowRequestSerializer(borrow_request).data, status=status.HTTP_201_CREATED)

class BorrowHistory(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        history = BorrowRequest.objects.filter(user=request.user)
        serializer = BorrowRequestSerializer(history, many=True)
        return Response(serializer.data)

    
class ManageBorrowRequests(APIView):
    permission_classes = [permissions.IsAdminUser]    
    
    def get(self, request):
        requests = BorrowRequest.objects.all()
        serializer = BorrowRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        borrow_request = BorrowRequest.objects.filter(id=pk).first()
        if not borrow_request:
            return Response({"error": "Borrow request not found."}, status=status.HTTP_404_NOT_FOUND)

        status_update = request.data.get('status')
        if status_update not in ['Approved', 'Denied']:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        if status_update == 'Approved':
            borrow_request.book.copies_available -= 1
            borrow_request.book.save()

        borrow_request.status = status_update
        borrow_request.save()
        return Response(BorrowRequestSerializer(borrow_request).data)
    