from django.test import TestCase

# Create your tests here.
belong_domain = models.ForeignKey(Domain_Info, on_delete=models.CASCADE, verbose_name="所属领域")
