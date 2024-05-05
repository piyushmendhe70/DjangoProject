from django.db import models
from django.db.models import Count, Avg
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField() 
    address = models.TextField()
    vendor_code = models.CharField(max_length=50)

    def calculate_performance_metrics(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        if completed_pos.exists():
            self.on_time_delivery_rate = completed_pos.filter(delivery_date__lte=timezone.now()).count() / completed_pos.count()
            self.quality_rating_avg = completed_pos.exclude(quality_rating__isnull=True).aggregate(Avg('quality_rating'))['quality_rating__avg']
            self.average_response_time = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(Avg(models.F('acknowledgment_date') - models.F('issue_date')))['acknowledgment_date__avg'].total_seconds() / 3600
            self.fulfillment_rate = completed_pos.filter(status='completed', issue_date__isnull=False, acknowledgment_date__isnull=False).count() / self.purchaseorder_set.count()
        else:
            self.on_time_delivery_rate = 0
            self.quality_rating_avg = None
            self.average_response_time = None
            self.fulfillment_rate = 0

        # Update HistoricalPerformance
        HistoricalPerformance.objects.create(
            vendor=self,
            date=timezone.now(),
            on_time_delivery_rate=self.on_time_delivery_rate,
            quality_rating_avg=self.quality_rating_avg,
            average_response_time=self.average_response_time,
            fulfillment_rate=self.fulfillment_rate
        )

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.status == 'completed':
            self.vendor.calculate_performance_metrics()
        super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()