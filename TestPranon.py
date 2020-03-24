dic = {
    'pranon':170041014,
    'hirok':170041034,
    'masum':170041050
}

print(dic['pranon'])

try:
    x = dic['zadid']
except KeyError:
    x = 'not found'
print(x)
