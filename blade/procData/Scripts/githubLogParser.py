import csv
import datetime
import json
from collections import defaultdict
from pprint import pprint
import requests
from csv import reader
'''
Order:
 Input: List of repos, list of ldap names, name of the organization.
 downloadReposfromList (Obtains all logs from org)
 employee2github (Process github from ldap)
 transformDict2CSV (Get a dictionary from the previous call)
 getUserListfromCSV (Process the dict information into a CSV)
 getOrgMembership (Process the list and determine repo membership)
 analyzeLog(Obtain the logs from the interesting subjects and stores into another csv)

'''
def employee_to_github_test(employee_name, ldapResource):
    '''
    Obtains github account name from an employee.

    Input: List of employees
    Output: Dictionary with the github account
    '''
    with open(ldapResource, 'r') as ldap_environment:
        print(f'Trying user {employee_name}')
        try:
            #Change to resolve through Actual LDAP Later
            ldapsearch = json.load(ldap_environment)
            gitLogin = ldapsearch[employee_name]
            return gitLogin['github_account'].lower()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")



def get_Github_dict_from_csv(employee_file_path, ldap_file_path):
    employeesInfo = {}

    with open(employee_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for employee in reader:
            name = employee[0]
            employeesInfo[name.lower()] = employee_to_github_test(name, ldap_file_path)

    return employeesInfo


def employee2github(employeeFile, ghUsername, ghToken, ldapResource):
    '''
    Obtains github account name from an employee list.

    Input: List of employees
    Output: Dictionary with the github account
    '''
    employeesInfo = {}

    while True:
        #Commenting to work on the test environment
        #employee = employeeFile.readline().strip()

        with open('./simTests/userTest.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                employee = row[0]
                if employee != '':
                    print(f'Trying user {employee}')

                    #Commenting to work on the test environment
                    #ldapsearch = f'{ldapResource}'
                    #res = requests.get(ldapsearch, auth=(ghUsername, ghToken))
                    #gitLogin = json.loads(res.text)

                    #Test
                    ldapsearch = json.load(ldapResource)
                    gitLogin = json.loads(ldapsearch[employee])
                    print(gitLogin)
                    #EndofTest

                    if 'github_account' in gitLogin.keys():
                        print(f'Found Github Account: {gitLogin["github_account"]}')
                        github = gitLogin['github_account']
                    else:
                        github = '<NONE>'
                    employeesInfo[employee] = github
                else:
                    break
    return employeesInfo

def transformDict2CSV(outputFile, employeesInfo):
    '''
    Uses Dictionary obtained from employee2github to return a file with github users as a CSV

    Input: Dictionary of github accounts and employees
    Output:
    '''
    for employee in employeesInfo.keys():
        if employeesInfo[employee] != '<NONE>':
            outputFile.write(f'{employee.strip()},{employeesInfo[employee]}\n')

    outputFile.close()

def getUserListfromCSV(csvfile):
    '''
    Gets a list of users from a CSV file processed by transferDict2CSV to grab the Github accounts

    Input: CSV File with ldapAccount and correlated github accounts
    Output: List of Github accounts from the associated list
    '''
    users=[]
    reader = csv.reader(csvfile)
    data = list(reader)
    count = 0
    for item in data:
        count +=1
        if item[1] != '<NONE>' and count !=1:
            users.append(item[1])

    print(f'Users in list: {len(users)}')
    csvfile.close()
    return users

def getOrgMembership(orgFile, users, ghUsername, ghToken):
    '''
    Gets the organization memberships associated to a github account using a list of organizations

    Input: List of organizations, list of users
    Output: List of organization memberships to a github account
    '''
    userInOrg = defaultdict(list)

    while True:
        org = orgFile.readline()
        if org != '':
            try:
                orgSearch = f'https://api.github.com/orgs/{org.strip()}/members'
                print(f'Trying URL {orgSearch}')
                res = requests.get(orgSearch, auth=(ghUsername, ghToken))
                orgJson = json.loads(res.text)
                for item in orgJson:
                    print(item.keys())
                    if item['login'] in users:
                        userInOrg[org.strip()].append(item['login'])
            except:
                print(f'Exception on {org.strip()}')
        else:
            break
    orgFile.close()
    return userInOrg

def analyzeLog(dateToCheck, logFileList, outputLogFile, outputAnalysisFile, userList):
    '''
    Check multiple log files for any hits from a github account list associated to an ldap as processed by
    employee2github and getUserListfromCSV/transformDict2CSV after a specific date. And check how many times somone
    appears on said logs

    Input: Date to check, List with all the log files, output filename for results, list of github accounts.
    Output: File log with all relevant logs and status about how many logs and results were processed.
    '''
    logsProcessed = 0
    userHits = 0
    logsAfterDate = 0
    for file in logFileList:
        with open(file, 'r') as logfile:
            logNum = 0
            while True:
                log_json = logfile.readline()
                logsProcessed +=1
                if log_json != '':
                    log = json.loads(log_json)
                    logNum +=1
                    print(f'Processing log {logNum} on file: {file}')
                    outputLogFile.write(f'Processing log {logNum} on file: {file} \n')
                    if 'actor' in log.keys() and log['actor'] in userList:
                        userHits += 1
                        if int(log['@timestamp']) / 1000 > dateToCheck:
                            logsAfterDate += 1
                            timestamp = datetime.datetime.fromtimestamp(int(log['@timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                            if 'repo' in log.keys():
                                outputAnalysisFile.write(f"{timestamp},{file},{log['actor']},{log['repo']}\n")
                            else:
                                outputAnalysisFile.write(f"{timestamp},{file},{log['actor']},{log['action']}\n")
                    else:
                        break
        logfile.close()
        print(f'Logs Processed: {logsProcessed} \nUser Hits: {userHits} \n Logs after Date: {logsAfterDate}')
        outputLogFile.write(f'Logs Processed: {logsProcessed} \nUser Hits: {userHits} \n Logs after Date: {logsAfterDate}')
        outputLogFile.close()
        return

def downloadReposfromList(repos, target, ghUsername, ghToken):
    '''
    From list of repo names, download all repo files from a github org.

    Input: list of repos in a github org, target github org name.
    Output: Downloaded log files from all repos in the list.
    '''
    for repo in repos:
        filename = str(target+repo.strip()+'.zip')
        file = open(filename, 'wb')
        res = requests.get(f'https://github.com/{repo.strip()}/archive/refs/heads/master.zip', auth=(ghUsername, ghToken), stream=True)
        for chunk in res.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)
        file.close()

def main():
    myCSV = './simTests/userTest.csv'
    myLDAP = './simulatedResults/employeeUniverse.json'
    print(get_Github_dict_from_csv(myCSV, myLDAP))

if __name__ == '__main__':
    main()
