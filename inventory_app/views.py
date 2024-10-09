import logging
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from .models import Item_details
from .serializers import ItemSerializer
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

class CreateItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        try:
            if Item_details.objects.filter(name=request.data.get('name')).exists():
                logger.warning(f'Attempted to create an item that already exists: {request.data.get("name")}')
                return Response({'error': 'Item already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                logger.info(f'Item created successfully: {serializer.data}')
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.error(f'Item creation failed due to validation errors: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception('An unexpected error occurred during item creation.')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrieveItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cache_key = f'item_{pk}'
        item = cache.get(cache_key)

        if not item:
            try:
                item = Item_details.objects.get(pk=pk)
                cache.set(cache_key, item, timeout=60 * 15)  # Cache for 15 minutes
            except Item_details.DoesNotExist:
                logger.warning(f'Attempted to retrieve a non-existing item with id: {pk}')
                return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item)
        logger.info(f'Item retrieved successfully: {serializer.data}')
        return Response(serializer.data)


class UpdateItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            item = get_object_or_404(Item_details, pk=pk)  # Simplified retrieval
            serializer = ItemSerializer(item, data=request.data)

            if serializer.is_valid():
                serializer.save()
                cache.delete(f'item_{pk}')
                logger.info(f'Item updated successfully: {serializer.data}')
                return Response(serializer.data)

            logger.error(f'Item update failed due to validation errors: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception('An unexpected error occurred during item update.')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = get_object_or_404(Item_details, pk=pk)  # Simplified retrieval
            item.delete()
            cache.delete(f'item_{pk}')
            logger.info(f'Item deleted successfully: {pk}')
            return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception('An unexpected error occurred during item deletion.')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
