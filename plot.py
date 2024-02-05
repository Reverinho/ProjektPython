from matplotlib.pyplot import *
from numpy import linspace, sin
from Projekt_Py import *

def generatePlot(inputObject):
    x = linspace(0, IRR(inputObject), 10)
    y = []

    for element in x:
        y.append(calculate(inputObject, element))

    plot(x, y, color = "green", marker = "o")
    xlabel("Discount rate")
    ylabel("NPV")
    legend(["NPV"])
    show()