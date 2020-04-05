import pandas as pd 
a = pd.DataFrame({"a": [1,3], "b": [65,4]})
print(a["a"])
print(a.index)
a = a.set_index(a["a"])
print(a.index)
print(a["a"])