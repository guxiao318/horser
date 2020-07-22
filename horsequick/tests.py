from django.test import TestCase

# Create your tests here.
belong_category = models.ForeignKey(Category_Info, on_delete=models.CASCADE, verbose_name="所属类别")
