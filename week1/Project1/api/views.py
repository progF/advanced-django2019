from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import Review, Product
from api.serializers import ReviewSerializer

@api_view(['GET', 'POST'])
def get_user_reviews(request):
    if request.method == 'GET':
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            reviews = Review.objects.for_user(request.user)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
            
@api_view(['GET'])
def get_reviews(request, pk):
    try:
        product = Product.objects.get(id=pk)
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'DELETE', 'PUT'])
def users_review_detail(request, pk):
    if request.user.is_anonymous:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            review = Review.objects.for_user(request.user).get(id=pk)
        except Review.DoesNotExist as e:
            return Response({'error': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def createReview(request, pk):
    if request.user.is_anonymous==False:
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.get(id=pk)
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    
    

    

