import requests
import json
import csv
from collections import defaultdict
from pprint import pprint
import datetime

def employee2github(employeeFile, ghUsername, ghToken, ldapResource):
    employeesInfo = {}

    while True:
        employee = employeeFile.readline()
        if employee != 0:
            print(f'Trying user {employee}')
            ldapsearch = f'{ldapResource}'
            res = requests.get(ldapsearch, auth=(ghUsername, ghToken))
            gitLogin = json.loads(res.text)
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
    for employee in employeesInfo.keys():
        if employeesInfo[employee] != '<NONE>':
            outputFile.write(f'{employee.strip()},{employeesInfo[employee]}\n')

    outputFile.close()

def getUserListfromCSV(csvfile):
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
    for repo in repos:
        filename = str(target+repo.strip()+'.zip')
        file = open(filename, 'wb')
        res = requests.get(f'https://github.com/{repo.strip()}/archive/refs/heads/master.zip', auth=(ghUsername, ghToken), stream=True)
        for chunk in res.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)
        file.close()


