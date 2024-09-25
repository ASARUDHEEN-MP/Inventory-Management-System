from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from rest_framework.exceptions import ValidationError,NotFound
import logging
import time

logger = logging.getLogger('items.view')

# Create your views here.
class Items(viewsets.ModelViewSet):
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Item.objects.all()


    # Function to create the item model 
    def create(self, request, *args, **kwargs):
        logger.info(f"POST request to /items/ from {request.META.get('REMOTE_ADDR')}")
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)  
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Override the getobject
    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'pk': self.kwargs.get('pk')}
        try:
            return queryset.get(**filter_kwargs)
        except queryset.model.DoesNotExist:
            raise NotFound(detail="Item not found with the specified ID.")
        
    def retrieve(self, request, *args, **kwargs):
            # CHECK THE API USAGE
            logger.info(f"GET request to /items/{kwargs.get('pk')} from {request.META.get('REMOTE_ADDR')}")
            # start time 
            start_time = time.time()
            # Get the item ID from the URL
            item_id = kwargs.get('pk')
            
            # Check if the item ID is valid
            if item_id is None:
                logger.error("Item ID is missing.")
                return Response({"error": "Item ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            cache_key = f'item_{item_id}'
            
            # Check if the item is in the cache
            item = cache.get(cache_key)


            if item is None:
                try:
                    # Retrieve the item from the database
                    item_instance = self.get_object()  # This should raise NotFound if the object is not found
                    serializer = self.get_serializer(item_instance)
                    
                    # Cache the item (ensure you're serializing it correctly)
                    cache.set(cache_key, serializer.data, timeout=60 * 5)  # Set a timeout of 5 minutes
                    end_time = time.time()
                    duration = end_time - start_time
                    logger.info(f"Request to {request.path} took {duration:.4f} seconds taken from db.")
                    return Response(serializer.data)
                except NotFound:
                    logger.error(f"Item with ID {item_id} not found.")
                    return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    logger.error(f"Error retrieving item with ID {item_id}: {str(e)}")
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # Item found in cache
                # Time taken to end this api call
                end_time = time.time()
                duration = end_time - start_time
                logger.info(f"Request to {request.path} took {duration:.4f} seconds take becouse of cache.")
            
                return Response(item)  # Return the cached data directly
            

    def update(self, request, *args, **kwargs):
        logger.info(f"UPDATE request to /items/ from {request.META.get('REMOTE_ADDR')}")
        try:
            item_instance = self.get_object()  
            serializer = self.get_serializer(item_instance, data=request.data)  
            serializer.is_valid(raise_exception=True)  
            serializer.save()
            # if this updating item in cache delete and update the cache
            cache.delete(f'item_{item_instance.id}')
            # refresh the cache 
            item_instance.refresh_from_db() 
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            logger.error(f"Item not found.")
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def destroy(self, request, *args, **kwargs):
        logger.info(f"DELETE request to /items/ from {request.META.get('REMOTE_ADDR')}")
        try:
            item = self.get_object()
            item_data = self.get_serializer(item).data
            self.perform_destroy(item)
            cache.delete(f'item_{item.id}')
            return Response({"message": "Item deleted successfully.", "item": item_data}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            logger.error("Item not found.")
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting item: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
