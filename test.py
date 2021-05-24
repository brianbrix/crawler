import pandas as pd

ptest = pd.DataFrame([['a', 1,3], ['a', 2, 5], ['b', 3, 5]], columns=['id', 'value', 'valu3'])
d= area_dict = dict(zip(ptest.id, ptest.value))
print(d)