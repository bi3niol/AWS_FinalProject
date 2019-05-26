PROP1 = "property_1"
PROP2 = "property_2"

obj = {
    PROP1:"value1",
    PROP2: "value2"
    }

print(obj)
print("test" in obj)
obj["test"] = 1
print("test" in obj)

def test(obj):
    obj["test"]="val"

tt = {}

test(tt)
print(tt)