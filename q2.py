from undercut_procedure import undercut
import gspread

account = gspread.service_account("credentials.json")
# Open spreadsheet by name:
spreadsheet = account.open("input")
# read Input sheet
input = spreadsheet.worksheet('input')

data = input.get_all_values()
print(data)

Alice = {}
Bob = {}
items=[]


for index,item in enumerate(data[0]):
    if (index!=0):
        items.append(item)
    
for index,item in enumerate(data[0]):
    if (index!=0):
        Alice[item]=int(data[1][index])

for index,item in enumerate(data[0]):
    if (index!=0):
        Bob[item]=int(data[2][index])


allocation,allocation_alice,allocation_bob = undercut([(Alice),(Bob)],items)
print(allocation)

try:
    output = spreadsheet.worksheet('output')
    spreadsheet.del_worksheet(output)
except:
    pass
output = spreadsheet.add_worksheet("output", input.row_count, input.col_count)

output.insert_row(allocation_alice, index=1)
output.insert_row(allocation_bob, index=2)
