import pickle

with open("CrashDump.dump", "rb") as f: dump = pickle.load(f)
for i in range(dump["nItems"]):
    for field in dump[i]["locals"]:
        dump[i]["locals"][field] = pickle.loads(dump[i]["locals"][field])

    for field in dump[i]["globals"]:
        dump[i]["globals"][field] = pickle.loads(dump[i]["globals"][field])


import pprint
pprint.pprint(dump)

input()
