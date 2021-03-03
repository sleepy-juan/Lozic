from Parser import RawExpression
from Visualization import Table
from Expression import *

eq = RawExpression.raw(input(">> "))
raw = input(">> ")
while raw != "solve":
    _eq = RawExpression.raw(raw)
    eq = AND(eq, _eq)
    raw = input(">> ")

vars = eq.variables()

table_data = [vars + [eq]]
def generateRow(arr, idx):
    if idx == len(vars):
        values = dict(zip(vars, arr))
        table_data.append(arr + [eq.solve(values)])
        return
    generateRow(arr + [True], idx+1)
    generateRow(arr + [False], idx+1)
generateRow([], 0)

table = Table(table_data)
table.show({eq: True})