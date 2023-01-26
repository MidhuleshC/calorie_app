from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import FoodSerializer,RegisterSerializer,RecordFoodConsumptionSerializer,ActivityToBurnoutSerializer,ActivityRecordSerializer
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from foodapp.models import FoodList,ActivityToBurnout,ActivityRecord,FoodConsumed
import datetime


#view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = RegisterSerializer
  
#food view
class FoodView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = FoodList.objects.all()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data) 
    
    
    def create(self, request):
        serializer = RecordFoodConsumptionSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
                data = serializer.save() 
                return Response(status=status.HTTP_201_CREATED,data={
                    'status': status.HTTP_201_CREATED,
                    'data': serializer.data
                    })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data= serializer.errors)
        
#activity view
class ActivitView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = ActivityToBurnout.objects.filter(is_approved=True,is_global=True)
        serializer = ActivityToBurnoutSerializer(queryset, many=True)
        return Response(serializer.data) 
    
    
    def create(self, request):
        validated_data = ActivityToBurnoutSerializer(data=request.data,context={'request': request})
        if validated_data.is_valid():
            data = validated_data.save() 
            return Response(status=status.HTTP_201_CREATED,data={
                    'status': status.HTTP_201_CREATED,
                    'data': validated_data.data
                    })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data= validated_data.errors)
        
        
#record activity
class RecordActivityView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = ActivityRecord.objects.filter(user=request.user)
        serializer = ActivityRecordSerializer(queryset, many=True)
        return Response(serializer.data) 
    
    
    def create(self, request):
        validated_data = ActivityRecordSerializer(data=request.data,context={'request': request})
        if validated_data.is_valid():
            data = validated_data.save() 
            return Response(status=status.HTTP_201_CREATED,data={
                    'status': status.HTTP_201_CREATED,
                    'data': validated_data.data
                    })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data= validated_data.errors)
        
#total food food consumption
class FoodConsumptionStatsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        filter_type = self.request.query_params.get('filter_type')
        if (filter_type in (None, '')):
            raise ValidationError({"status": "Error", "message": "Invalid parameter, filter_type should have value"})
        start = datetime.date.today()
        if filter_type == 'day':
           
            end = start + datetime.timedelta(days=1)
            data = FoodConsumed.objects.filter(created_at__range=(start, end),user=request.user).aggregate(Sum('amount_consumed'))
            return Response(status=status.HTTP_200_OK,data={
                    'status': status.HTTP_200_OK,
                    'data': data
                    })
        elif filter_type == 'week':
            end = start + datetime.timedelta(days=7)
            data = FoodConsumed.objects.filter(created_at__range=(start, end),user=request.user).aggregate(Sum('amount_consumed'))
            return Response(status=status.HTTP_200_OK,data={
                    'status': status.HTTP_200_OK,
                    'data': data
                    })
        elif filter_type == 'month':
            end = start + datetime.timedelta(days=30)
            data = FoodConsumed.objects.filter(created_at__range=(start, end),user=request.user).aggregate(Sum('amount_consumed'))
            return Response(status=status.HTTP_200_OK,data={
                    'status': status.HTTP_200_OK,
                    'data': data
                    })
        
  #total burn out
class CalorieBurnOutStatsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        filter_type = self.request.query_params.get('filter_type')
        if (filter_type in (None, '')):
            raise ValidationError({"status": "Error", "message": "Invalid parameter, filter_type should have value"})
        start = datetime.date.today()
        if filter_type == 'day':
           
            end = start + datetime.timedelta(days=1)
            data = ActivityRecord.objects.filter(created_at__range=(start, end),user=request.user).aggregate(Sum('calorie_burned'))
            return Response(status=status.HTTP_200_OK,data={
                    'status': status.HTTP_200_OK,
                    'data': data
                    })
        elif filter_type == 'week':
            end = start + datetime.timedelta(days=7)
            data = ActivityRecord.objects.filter(created_at__range=(start, end),user=request.user).aggregate(Sum('calorie_burned'))
            return Response(status=status.HTTP_200_OK,data={
                    'status': status.HTTP_200_OK,
                    'data': data
                    })
        elif filter_type == 'month':
            end = start + datetime.timedelta(days=30)
            data = ActivityRecord.objects.filter(created_at__range=(start, end),user=request.user).aggregate(Sum('calorie_burned'))
            return Response(status=status.HTTP_200_OK,data={
                    'status': status.HTTP_200_OK,
                    'data': data
                    })
        
  