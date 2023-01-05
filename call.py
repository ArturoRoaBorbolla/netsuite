import connect


suite = connect.SuiteSql()
results = suite.execute("Select * from Currency")
print(results)
for item in results["items"]:
    print(item)