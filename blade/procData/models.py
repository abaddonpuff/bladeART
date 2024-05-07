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


#class results

#class query
class dbQueriedUsers(models.Model):
	user = models.CharField(max_length=100,unique=True)
	added = models.DateTimeField(auto_now_add=True)
	github_account = models.CharField(max_length=100,unique=True)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.user