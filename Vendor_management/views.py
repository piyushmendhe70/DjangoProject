from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from Vendor_management.models import Vendor, PurchaseOrder, HistoricalPerformance
from Vendor_management.serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.utils import timezone
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

def index(request):
    return render(request,'index.html')

class VendorViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'], url_path='performance')
    def performance_metrics(self, request, pk=None):
        vendor = self.get_object()
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data)

class PurchaseOrderViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['post'], url_path='acknowledge')
    def acknowledge_po(self, request, pk=None):
        po = self.get_object()
        po.acknowledgment_date = timezone.now()
        po.save()
        # Recalculate average_response_time after acknowledgment_date update
        po.vendor.calculate_performance_metrics()
        return Response({"message": "Acknowledgment date updated successfully."})

class HistoricalPerformanceViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            return HistoricalPerformance.objects.filter(vendor_id=vendor_id)
        return super().get_queryset()

class VendorPerformanceViewset(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk=None):
        vendor = get_object_or_404(Vendor, pk=pk)
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data)

