from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
router = DefaultRouter()


router.register('list_food',views.FoodView, basename='list_food')
router.register('activity',views.ActivitView, basename='activity')
router.register('record_activity',views.RecordActivityView, basename='record_activity')
router.register('food_consumption_stats',views.FoodConsumptionStatsView, basename='food_consumption_stats')
router.register('calorie_burned_stats',views.CalorieBurnOutStatsView, basename='calorie_burned_stats')



# urlpatterns = router.urls
urlpatterns = [ 
    path('log_in/', TokenObtainPairView.as_view(), name='log_in'),
    path('register',views.RegisterUserAPIView.as_view()),
    path('', include(router.urls)),

]