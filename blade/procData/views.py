from django.shortcuts import render, get_object_or_404, redirect
from procData.models import breachStructure, dbQueriedUsers
from procData.forms import uploadCSV
from csv import DictReader
from Scripts.githubLogParser import employee_to_github_test

LDAP_SIMULATED = './Scripts/simulatedResults/employeeUniverse.json'

# Create your views here.
def breachStructure_list(request):
    breachStructures = breachStructure.objects.all()

    return render(
        request, "breachStructure/list.html", {"breachStructures": breachStructures}
    )


def breachStructure_detail(request, email):
    breachStruct = get_object_or_404(breachStructure, email=email)

    return render(
        request, "breachStructure/detail.html", {"breachStructures": breachStruct}
    )


def upload_csv(request):
    if request.method == "POST":
        form = uploadCSV(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]

            reader = DictReader(csv_file.read().decode("utf-8").splitlines())
            for row in reader:
                github_associated = employee_to_github_test(row['Names'],LDAP_SIMULATED)
                user, created = dbQueriedUsers.objects.get_or_create(user=row['Names'].lower(),github_account=github_associated)
                if not created:
                    print(f"Skip, user {user} already exists")

            return redirect("success_url")

    else:
        form = uploadCSV()

    return render(request, "csvUpload/csvUpload.html", {"form": form})


def success_url(request):
    return render(request, "csvUpload/success_url.html")


def show_allusers(request):
    githubQueried = dbQueriedUsers.objects.all()

    return render(
        request, "csvUpload/list_users.html", {"dbQueriedUsers": githubQueried}
    )