import random
import string
import json
import datetime
import secrets
import hashlib


def generate_name():
    '''
    Generates random ldaps and returns a dictionary with the name of the person as a user_key
    '''
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
                   "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth",
                   "George", "Joshua", "Kevin", "Brian", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
                   "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
                  "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White",
                  "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall",
                  "Young", "Allen", "Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson"]
    desserts = ["Chocolate Cake", "Vanilla Ice Cream", "Apple Pie", "Lemon Tart", "Cheesecake", "Brownie", "Cupcake",
                "Donut", "Gelato", "Pavlova", "Macaron", "Mousse", "Tiramisu", "Panna Cotta", "Cannoli", "Baklava",
                "Eclair", "Sorbet", "Cobbler", "Strudel"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    dessert = random.choice(desserts)

    user_key = f"{first_name[0]}{last_name}"
    github_account = first_name.lower() + random.choice(last_names[:3]).lower()

    return {
        user_key: {
            "github_account": github_account,
            "passthrough_fields": dessert
        }
    }

def createEmployeeJson(employeeSize, filename):
    '''
    Generate a universe of test employees with the size of Employee Size and saves it to the filename path.
    '''
    employeeUniverse = {}
    while len(employeeUniverse.keys()) <= employeeSize:
        entry = generate_name()
        if list(entry.keys())[0] in employeeUniverse.keys():
            continue
        else:
            employeeUniverse.update(entry)

    with open(filename, 'w') as f:
        json.dump(employeeUniverse,f, indent=4)

    return

def generateEmployeesFromJSON(jsonFileName):
    '''
    Returns a list of logs from a created JSON file from generate_name
    input = generate_name dictionary as a JSON file
    output = listofNames
    '''
    jsonFile = open(jsonFileName, 'r')
    names = []
    testNames = json.load(jsonFile)
    for item in testNames.keys():
        names.append(item)

    jsonFile.close()
    return(names)

def employeeGithubUser(user, jsonFileName):
    '''
    Obtains the GithubAssociated user to an ldapName
    '''
    jsonFile = open(jsonFileName, 'r')
    namePool = json.load(jsonFile)
    githubUser = namePool[user]['github_account']
    jsonFile.close()
    return githubUser


def generateRandomLogsfromEmployees(startTime, endTime, orgname):
    '''
    Obtains random logs based on random information from the other functions.

    input = startTime, endTime (start and endtimes of the desired logs
    orgname = name of the organization for the json files
    '''

    #Define random pools
    myJSONFile = 'employeeUniverse.json'
    employees = generateEmployeesFromJSON(myJSONFile)
    idchars = string.ascii_letters + "_-"
    actions_target = ["org","team","repo"]
    actions_action = ["add_member","remove_member","invite_member","create","log_export","commit"]
    country_codes = ["US","GB","DE","MX","FR","CA"]
    operation_types = ["remove","create","remove_member"]
    testLogEmployees = random.sample(employees, 40)
    testuser = random.sample(employees, 2)
    ldapcreationStart = datetime.datetime(2020, 1, 1, 00, 00, 00, 00)
    ldapcreationEnd = datetime.datetime(2021, 12, 30, 23, 59, 59, 00)

    #Define possible values
    id = ''.join(secrets.choice(idchars) for i in range(22))
    unixTimestamp = random.randint(int(startTime.timestamp() * 1000), int(endTime.timestamp() * 1000))
    country_code = random.choice(country_codes)
    action = f'{random.choice(actions_target)}.{random.choice(actions_action)}'
    ldapCreation = random.randint(int(ldapcreationStart.timestamp() * 1000), int(ldapcreationEnd.timestamp() * 1000))
    hashed_token = secrets.token_urlsafe(32)+"=="
    actor = employeeGithubUser(random.choice(testLogEmployees), myJSONFile).lower()
    user = employeeGithubUser(random.choice(testuser), myJSONFile).lower()

    return{
        "@timestamp":unixTimestamp,
        "_document_id":id,
        "action":action,
        "actor":actor,
        "actor_location":{"country_code":country_code},
        "created_at":ldapCreation,
        "operation_type":random.choice(operation_types),
        "hashed_token":hashed_token,
        "org":orgname,
        "user":user
    }
def generate_testLog(orgName, startTime, endTime, logAmount):
    '''
    Generate a logFile on the simTests under the orgName folder and the specified starttime and endtime with (logAmount) numbers of logs
    '''
    with open(f'{orgName}_repo_github.log', 'w') as logFile:
        linesWritten = 0
        while linesWritten <= logAmount:
            json.dump(generateRandomLogsfromEmployees(startTime, endTime, orgName),logFile)
            logFile.write('\n')
            linesWritten += 1

    logFile.close()

def grabEmployeeSample(jsonFileName, employeeAmount):
    names=[]
    employeeCount = 0
    jsonFile = open(jsonFileName, 'r')
    namePool = json.load(jsonFile)
    while employeeCount <= employeeAmount:
        candidate = random.choice(list(namePool.keys()))
        if candidate not in names:
            names.append(candidate)
            employeeCount += 1
    jsonFile.close()
    return names

if __name__ == '__main__':
    # starttime = datetime.datetime(2023,12,12,00,00,00,00)
    # endtime = datetime.datetime(2024,4,12,23,59,59,00)
    # generate_testLog("leblanc", starttime, endtime, 150)
    myJSONFile = 'employeeUniverse.json'
    for employee in grabEmployeeSample(myJSONFile, 30):
        print(employee)