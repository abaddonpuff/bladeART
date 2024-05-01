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

def generateEmployeesFromJSON(jsonFile):
    '''
    Returns a list of logs from a created JSON file from generate_name
    input = generate_name dictionary as a JSON file
    output = listpfNames
    '''
    names = []
    testNames = json.load(jsonFile)
    for item in testNames['employee']:
        names.append(list(item.keys())[0].lower())

    return(names)

def generateRandomLogsfromEmployees(startTime, endTime, orgname):
    '''
    Obtains random logs based on random information from the other functions.

    input = startTime, endTime (start and endtimes of the desired logs
    orgname = name of the organization for the json files
    '''

    #Define random pools
    myTestFile = open('employee2githubSIM.json', 'r')
    employees = generateEmployeesFromJSON(myTestFile)
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

    return{
        "@timestamp":unixTimestamp,
        "_document_id":id,
        "action":action,
        "actor":random.choice(testLogEmployees),
        "actor_location":{"country_code":country_code},
        "created_at":ldapCreation,
        "operation_type":random.choice(operation_types),
        "hashed_token":hashed_token,
        "org":orgname,
        "user":random.choice(testuser),
    }


if __name__ == '__main__':
    starttime = datetime.datetime(2023,12,12,00,00,00,00)
    endtime = datetime.datetime(2024,4,12,23,59,59,00)
    for i in list(range(20)):
        print(generateRandomLogsfromEmployees(starttime, endtime, "myOrg"))
