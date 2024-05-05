from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from Vendor_management.models import Vendor, PurchaseOrder, HistoricalPerformance
import json

class VendorManagementTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='Contact 1', address='Address 1', vendor_code='V001')
        self.purchase_order1 = PurchaseOrder.objects.create(po_number='PO001', vendor=self.vendor1, order_date='2024-05-01T12:00:00Z', delivery_date='2024-05-10T12:00:00Z', items='["Item 1"]', quantity=10, status='pending', issue_date='2024-05-01T12:00:00Z')
        self.historical_performance1 = HistoricalPerformance.objects.create(vendor=self.vendor1, date='2024-05-01T12:00:00Z', on_time_delivery_rate=0, quality_rating_avg=0.0, average_response_time=0.0, fulfillment_rate=0)

    def test_vendor_creation(self):
        response = self.client.post(reverse('vendor-list'), {'name': 'Vendor 2', 'contact_details': 'Contact 2', 'address': 'Address 2', 'vendor_code': 'V002'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_purchase_order_creation(self):
        response = self.client.post(reverse('purchaseorder-list'), {'po_number': 'PO002', 'vendor': self.vendor1.id, 'order_date': '2024-05-02T12:00:00Z', 'delivery_date': '2024-05-15T12:00:00Z', 'items': '["Item 2"]', 'quantity': 20, 'status': 'pending', 'issue_date': '2024-05-02T12:00:00Z'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(PurchaseOrder.objects.count(), 1)

    def test_acknowledge_purchase_order(self):
        response = self.client.post(reverse('purchaseorder-acknowledge-po', kwargs={'pk': self.purchase_order1.id}))
        self.assertEqual(response.status_code, 401)
        self.purchase_order1.refresh_from_db()