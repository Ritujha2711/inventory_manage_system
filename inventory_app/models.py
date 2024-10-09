from django.db import models

class Item_details(models.Model):
    item_name = models.CharField(max_length=300, blank=False, db_column="item_name")
    item_description = models.TextField()

    def __str__(self):
        return self.item_name
