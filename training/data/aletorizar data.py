import numpy as np
import pandas as pd

tabla = pd.read_csv('./simb_valido_test_santi.csv')
print(tabla)
tabla= tabla.sample(frac=1)
if not tabla.empty:
    tabla.to_csv("shuffle_simb_valido_test_santi.csv")
else:
    print("aaa")

