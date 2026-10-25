from model.model import Model

mymdl=Model()
mymdl.creaGrafo("Road Bikes","2016-01-01","2018-12-28")
print(mymdl.getGraphDetails())