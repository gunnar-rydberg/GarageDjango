from django.conf.urls import url
from . import views
from . views import VehicleListView, VehicleDetailView

urlpatterns = [
    url(r'^$', VehicleListView.as_view(), name='vehicle_list'),
    url(r'^vehicle/(?P<pk>\d+)/$', VehicleDetailView.as_view(), name='vehicle_detail'),
    url(r'^vehicle/new/$', views.VehicleParkView.as_view(), name='vehicle_park'),
    url(r'^vehicle/(?P<pk>\d+)/edit/$', views.VehicleEditView.as_view(), name='vehicle_edit'),
    url(r'^vehicle/(?P<pk>\d+)/checkout/$', views.VehicleCheckoutView.as_view(), name='vehicle_checkout'),
    
    url(r'^(?P<regno>\d+)/$', VehicleListView.as_view(), name='vehicle_list'),

    url(r'^member/new/$', views.GarageMemberCreate.as_view(), name='member_create')

]
