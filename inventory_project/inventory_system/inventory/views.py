from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.core.cache import cache
from .models import Items
from .serializers import *
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Set up logging
logger = logging.getLogger(__name__)

class CreateItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        status, message, response = 200, "Item successfully created.", {}
        name = request.data.get('name', None)
        desc = request.data.get('description', None)
        
        logger.info(f"Creating item with name: {name}, description: {desc}")
        
        try:
            if not name or not desc:
                raise ValueError("Name and description are required.")

            query = Items.objects.filter(name=name)
            if query.exists():
                status, message = 400, "Item already exists."
            else:
                item = Items(name=name, description=desc)   
                item.save()
        except Exception as e:
            logger.error(f"Error creating item: {str(e)}")
            status, message = 500, "An error occurred while creating the item."
        
        response['status'] = status
        response['message'] = message
        print("response",response)
        return Response(response, status=status)   

class ReadItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id, *args, **kwargs):
        status, message, response, data = 200, "Item successfully retriviewed.", {}, {}
        
        logger.info(f"retriviewing item with ID: {id}")
        
        try:
            item = Items.objects.filter(pk=id).first()
            if item:
                data = ItemSerializer(item).data
            else:
                status, message = 404, "Item not found."
        except Exception as e:
            logger.error(f"Error retriviewing item with ID {id}: {str(e)}")
            status, message = 500, "An error occurred while retriviewing the item."

        response['data'] = data
        response['status'] = status
        response['message'] = message
        return Response(response, status=status)   

    def put(self, request, id, *args, **kwargs):
        status, message, response, data = 200, "Item successfully updated.", {}, {}
        
        logger.info(f"Updating item with ID: {id}")
        
        try:
            name = request.data.get('name', None)
            desc = request.data.get('description', None)

            if not name or not desc:
                raise ValueError("Name and description are required.")

            item = Items.objects.filter(pk=id).first()
            if item:
                item.name = name
                item.description = desc   
                item.save()
                data = {
                    "name": name,
                    "description": desc
                }
            else:
                status, message = 404, "Item not found."
        except Exception as e:
            logger.error(f"Error updating item with ID {id}: {str(e)}")
            status, message = 500, "An error occurred while updating the item."

        response['data'] = data
        response['status'] = status
        response['message'] = message
        return Response(response, status=status)   

    def delete(self, request, id, *args, **kwargs):
        status, message, response = 200, "Item successfully deleted", {}
        
        logger.info(f"Deleting item with ID: {id}")

        try:
            item = Items.objects.filter(pk=id).first()
            if item:
                item.delete()
            else:
                status, message = 404, "Item not found."
        except Exception as e:
            logger.error(f"Error deleting item with ID {id}: {str(e)}")
            status, message = 500, "An error occurred while deleting the item."

        response['status'] = status
        response['message'] = message
        print("response",response)
        return Response(response, status=status)   
