import sqlite3
from datetime import datetime
import xmltodict as xmltodict
import requests

if __name__ == '__main__':
    response = requests.get('https://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_BillHistoryInitiator()')
    # returns an XML file
    dataset = xmltodict.parse(response.content)
    db = sqlite3.connect('my_database.db') # creating database, connecting to database
    cursor = db.cursor() # Get a cursor
    cursor.execute(
        '''
        CREATE TABLE KNS_BillHistoryInitiator(
        BillHistoryInitiatorID integer primary key, BillID integer, PersonID integer, IsInitiator bit, StartDate datetime2,
        EndDate datetime2 , ReasonID integer, ReasonDesc varchar (125), LastUpdateDate datetime2
        )
        '''
    )
    for element in dataset['feed']['entry']: #extracting elements values
        entry = element['content']['m:properties']
        BillHistoryInitiatorID = int(entry['d:BillHistoryInitiatorID']['#text'])
        BillID = int(entry['d:BillID']['#text'])
        PersonID = int(entry['d:PersonID']['#text'])
        IsInitiator = entry['d:IsInitiator']['#text'] == 'true'
        StartDate = None if dict(entry['d:StartDate']).keys().__contains__('@m:null') else datetime.strptime(entry['d:StartDate']['#text'], '%Y-%m-%dT%H:%M:%S')
        EndDate = None if dict(entry['d:EndDate']).keys().__contains__('@m:null') else datetime.strptime(entry['d:EndDate']['#text'], '%Y-%m-%dT%H:%M:%S')
        ReasonID = int(entry['d:ReasonID']['#text'])
        ReasonDesc = str(entry['d:ReasonDesc'])
        LastUpdatedDate = None if dict(entry['d:LastUpdatedDate']).keys().__contains__('@m:null') else datetime.strptime(entry['d:LastUpdatedDate']['#text'], '%Y-%m-%dT%H:%M:%S')
        data = [BillHistoryInitiatorID, BillID, PersonID, IsInitiator, StartDate, EndDate, ReasonID, ReasonDesc,LastUpdatedDate]
        cursor.execute('''
            INSERT OR IGNORE INTO KNS_BillHistoryInitiator(BillHistoryInitiatorID, BillID, PersonID, IsInitiator, StartDate,
             EndDate, ReasonID, ReasonDesc, LastUpdateDate) VALUES (?,?,?,?,?,?,?,?,?)''',data)
    cursor.execute('''
                   SELECT * FROM KNS_BillHistoryInitiator
                   ''')
    for row in cursor:
        print(row)