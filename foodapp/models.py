from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class FoodLabel(models.Model):
    label = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return self.label 
    
class FoodList(models.Model):
    food_name = models.CharField(max_length=200)
    label = models.ManyToManyField(FoodLabel,null=True,blank=True,related_name='food_label')
    calorie = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def get_label(self):
        return " , ".join([str(l) for l in self.label.all()])
    
    def __unicode__(self):
        return self.food_name + self.label + self.label
    
    
class ActivityToBurnout(models.Model):
    activity = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    removes_calorie = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=True)
    is_global = models.BooleanField(default=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return self.activity + self.duration + self.removes_calorie
    
    
class FoodConsumed(models.Model):
    food = models.ForeignKey(FoodList,on_delete=models.CASCADE,related_name='fd_consumed')
    amount_consumed = models.PositiveIntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __unicode__(self):
        return self.food + self.amount_consumed + self.user
    
class ActivityRecord(models.Model):
    activity = models.ForeignKey(ActivityToBurnout,on_delete=models.CASCADE,related_name='activity_spent')
    time_spent = models.PositiveIntegerField()
    calorie_burned = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __unicode__(self):
        return self.activity + self.time_spent + self.user