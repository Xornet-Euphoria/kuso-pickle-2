import pickle, io
import sys

def f(event, args):
    print(event, args)

sys.addaudithook(f)

with open("./chall.pkl", "rb") as f:
    pkl = f.read()

pickle.loads(pkl)
