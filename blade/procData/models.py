from django.db import models

# Create your models here.

class breachStructure(models.Model):
	email = models.EmailField(max_length=100,unique=True)
	handle = models.CharField(max_length=100,unique=True)
	userId = models.BigIntegerField(default=0,blank=True)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.email