from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from Vendor_management.views import index, VendorViewset, PurchaseOrderViewset, HistoricalPerformanceViewset, VendorPerformanceViewset

router = routers.DefaultRouter()
router.register(r'Vendor', VendorViewset)
router.register(r'PurchaseOrder', PurchaseOrderViewset)
router.register(r'HistoricalPerformance', HistoricalPerformanceViewset)
router.register(r'vendor-performance', VendorPerformanceViewset,basename='vendor-performance')

urlpatterns = [
    path('',index,name='index'),
    path('index/', include(router.urls)),
]
