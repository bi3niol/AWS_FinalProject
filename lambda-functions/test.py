import datetime

print(datetime.date.min)
items = []
lastResult = max(items, key=lambda x: x[CI_CREATEDON_KEY])
print(lastResult)