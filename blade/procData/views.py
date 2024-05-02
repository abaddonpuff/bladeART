from django.shortcuts import render, get_object_or_404
from procData.models import breachStructure

# Create your views here.
def breachStructure_list(request):
	breachStructures = breachStructure.objects.all()


	return render(request,
		'breachStructure/list.html',
		{'breachStructures':breachStructures})


def breachStructure_detail(request, email):
	breachStruct = get_object_or_404(breachStructure, email=email)


	return render(request,
		'breachStructure/detail.html',
		{'breachStructures':breachStruct})
