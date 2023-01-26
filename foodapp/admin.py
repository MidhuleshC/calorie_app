from django.contrib import admin
from .models import FoodLabel,FoodList,ActivityToBurnout,FoodConsumed,ActivityRecord
# Register your models here.
class FoodLabelAdmin(admin.ModelAdmin):
    list_display = ('id','label','created_at','updated_at',)
   
    search_fields = ('id','label',)
    ordering = ('-created_at',)
    
    # def get_form(self, request, obj=None, **kwargs):
    #     """Override the get_form and extend the 'exclude' keyword arg"""
    #     if obj:
    #         kwargs.update({
    #             'exclude': getattr(kwargs, 'exclude', tuple()) + ('created_at',),
    #         })
    #     return super(CartMasterAdmin, self).get_form(request, obj, **kwargs)
    
    
class FoodListAdmin(admin.ModelAdmin):
    list_display = ('id','food_name','calorie','get_label','created_at','updated_at',)
    
  
   
    search_fields = ('id','food_name',)
    ordering = ('-created_at',)
    
class FoodActivityAdmin(admin.ModelAdmin):
    list_display = ('id','activity','duration','removes_calorie','created_at','updated_at',)
   
    search_fields = ('id','activity',)
    ordering = ('-created_at',)
    
class FoodConsumedAdmin(admin.ModelAdmin):
    list_display = ('food_id','amount_consumed','user_id','created_at')
   
    search_fields = ('id','user_id',)
    ordering = ('-created_at',)
    
class ActivityRecordAdmin(admin.ModelAdmin):
    list_display = ('activity','time_spent','user','created_at')
   
    search_fields = ('id','user',)
    ordering = ('-created_at',)
 
    
admin.site.register(FoodLabel,FoodLabelAdmin)
admin.site.register(FoodList,FoodListAdmin)
admin.site.register(ActivityToBurnout,FoodActivityAdmin)
admin.site.register(FoodConsumed,FoodConsumedAdmin)
admin.site.register(ActivityRecord,ActivityRecordAdmin)