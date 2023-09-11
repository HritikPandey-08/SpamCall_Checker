from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Spam
from .serializers import SpamSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from user_app.models import UserData

@api_view(['POST']) 
@permission_classes([IsAuthenticated])  # Requires authentication

def mark_number_as_spam(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')

        #check is user entered number or not
        if not phone_number:
            return Response({'error': 'Please provide a phone number to mark as spam'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            existing_mark = Spam.objects.get(phone_number=phone_number)

            if user in existing_mark.marked_by.all():
                existing_mark.marked_by.remove(user)  # Unmark the number if the user already marked it
                existing_mark.spam_count -= 1
                existing_mark.save()
                return Response({'message': 'Number unmarked successfully'}, status=status.HTTP_200_OK)
            else:
                existing_mark.marked_by.add(user)
                existing_mark.spam_count += 1
                existing_mark.save()
                return Response({'message': 'Number is already marked as spam by another user'}, status=status.HTTP_400_BAD_REQUEST)
        except Spam.DoesNotExist:
            # Mark the number as spam
            spam = Spam.objects.create(phone_number=phone_number)
            spam.marked_by.set([user])
            return Response({'message': 'Number marked as spam successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_spam_numbers(request):
    if request.method == 'GET':
        spam_numbers = Spam.objects.all()
        serializer = SpamSerializer(spam_numbers, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    search_query = request.GET.get('query')
    if not search_query:
        return Response({'error': 'Please provide a search query'})
    
    user = request.user
    user_phone_number = user.phone_number
    
    # Check if the search query is a phone number
    is_phone_number = search_query.isdigit()
    
    if is_phone_number:
    # Check if there is a registered user with the provided phone number
        registered_user = UserData.objects.filter(phone_number=search_query).first()
        if registered_user:
            result = {
                'name': registered_user.name,
                'phone_number': registered_user.phone_number,
                'spam_likelihood': 0,  # No need to calculate spam likelihood for registered user
            }
            # Check if the searching user is in the person's contact list
            if user_phone_number == search_query:
                result['email'] = registered_user.email_address

            return Response(result)
        else:
            # Show all results matching the phone number
            users = UserData.objects.filter(phone_number=search_query)
            results = [
                {
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'spam_likelihood': 0,  # No need to calculate spam likelihood
                }
                for user in users
            ]
            return Response(results)
    else:
        # If no registered user with the provided phone number, show all matching results
        users = UserData.objects.filter(phone_number=search_query)

        # Get search results
        users = UserData.objects.filter(
            Q(name__istartswith=search_query) | Q(name__icontains=search_query)
        )

        # Calculate spam likelihood for each user based on spam reports
        total_reports_count = Spam.objects.count()
        for user in users:
            spam_reports_count = Spam.objects.filter(marked_by=user).count()
            user.spam_likelihood = spam_reports_count / total_reports_count if total_reports_count > 0 else 0

        # Sort results based on spam likelihood
        sorted_users = sorted(users, key=lambda user: user.spam_likelihood, reverse=True)

        # Return search results
        results = [
            {
                'name': user.name,
                'phone_number': user.phone_number,
                'spam_likelihood': user.spam_likelihood
            }
            for user in sorted_users
        ]
    
    return Response(results)