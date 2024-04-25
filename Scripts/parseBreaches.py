import re
import string

validChars = string.ascii_lowercase+string.ascii_uppercase+string.digits

def extractUniqueValues(breachFile):
    count = 0
    handles=[]
    emails=[]

    while True:
        line = breachFile.readline().strip()
        count+=1
        if count == 41036812:
            break
        if '@' in (list(line)):
            print(f'{count}: Working on {line} - Email')
            emails.append(line)
        else:
            print(f'{count}: Working on {line} - Handle')

    dedup_handles = set(handles)
    dedup_emails = set(emails)
    handles = list(dedup_handles)
    emails = list(dedup_emails)

    print(f'Unique handles: {len(handles)}')
    print(f'Unique emails: {len(emails)}')

def write_toFile(file, myList):
    for item in myList:
        file.write(f'{item}\n')

def extract_Source(handle_file, email_file):
    emailCounter = 1
    handleCounter = 1
    myRegex = '(.*):(.*)'

    count=0
    handles=[]
    emails=[]
    dump = open('twitter.txt','r', encoding="utf-8", errors='replace')

    myDump = dump.readlines()
    for item in myDump:
        count+=1
        print(f'{count}: Trying entry {item}')
        matches = re.findall(myRegex, item)
        if '@' in matches[0][0]:
            email_file.write(f'{matches[0][0]}\t{matches[0][1]}\n')
            if email_file.tell() > 250000000:
                email_file.close()
                emailCounter +=1
                email_file = open(f'emailMatch_{emailCounter}.csv', 'w')
        else:
            if len(set(matches[0][0]).difference(validChars)) == 0:
                handle_file.write(f'{matches[0][0]}\t{matches[0][1]}\n')
                if handle_file.tell() > 250000000:
                    handle_file.close()
                    handleCounter +=1
                    handle_file = open(f'handleMatch_{handleCounter}.csv','w')
    email_file.close()
    handle_file.close()
