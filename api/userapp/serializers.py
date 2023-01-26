from rest_framework import serializers
from django.contrib.auth.models import User
from foodapp.models import FoodList,FoodLabel,FoodConsumed,ActivityToBurnout,ActivityRecord
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class FoodLabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodLabel
        fields = ('id','label',)


#Serializer to Get User Details using Django Token Authentication
class FoodSerializer(serializers.ModelSerializer):
  label = FoodLabelSerializer(many=True, read_only=True)
  class Meta:
    model = FoodList
    fields = ('id', 'food_name','calorie','label',)
    

#Serializer to add consumption
class RecordFoodConsumptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = FoodConsumed
    fields = ('food', 'amount_consumed',)
    
  def validate(self, validated_data):
     request = self.context['request']
     validated_data['user'] = request.user
     return validated_data
    
#Serializer to  ActivityToBurnout
class ActivityToBurnoutSerializer(serializers.ModelSerializer):
  class Meta:
    model = ActivityToBurnout
    fields = ['id','activity', 'duration','removes_calorie']

  def validate(self, validated_data):
     request = self.context['request']
     validated_data['added_by'] = request.user
     validated_data['is_approved'] = False
     validated_data['is_global'] = False
     return validated_data
  
#Serializer to  ActivityToBurnout
class ActivityRecordSerializer(serializers.ModelSerializer):
  activity_name = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = ActivityRecord
    fields = ['activity','time_spent','activity_name','calorie_burned']
    
    
  def get_activity_name(self,object):
    try:
      data = ActivityToBurnout.objects.only('activity').filter(pk = object.activity.id).first()
      return data.activity
    except Exception as e:
      pass
    
  def validate(self, validated_data):
     request = self.context['request']
     validated_data['user'] = request.user
     return validated_data
   
#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
      required=True,
      validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
      write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
      model = User
      fields = ('username', 'password', 'password2',
           'email', 'first_name', 'last_name')
      extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
      }
      
    def validate(self, attrs):
      if attrs['password'] != attrs['password2']:
        raise serializers.ValidationError(
          {"password": "Password fields didn't match."})
      return attrs
  
    def create(self, validated_data):
      user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
      )
      
      user.set_password(validated_data['password'])
      user.save()
      return user