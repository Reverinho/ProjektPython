
def test(inputObject):

    if not all(isinstance(value, (float, int)) for value in inputObject.values()):
        return [False, "Some data hasn't been inserted yet"]

    if inputObject["equity"] > 100 or inputObject["equity"] < 0:
        return [False, "Equity stake can only range from 0 to 100%"]

    if any(value < 0 for value in inputObject.values()):
        return [False, "Only positive values are allowed"]

    if (inputObject["duration"] % 1 != 0 or inputObject["amortizationDur"] % 1 != 0):
        return [False, "Lifespan has to be in full years"]

    if inputObject["equityCost"] > 200 or inputObject["borrowedCapCost"] > 200:
        return [False, "Cost of the capital is over 200%! Project not approved"]

    if inputObject["duration"]>100:
        return [False, "Lifetime of the project has to be within a single century"]
    
    if inputObject["amortizationDur"]> 50:
        return [False, "Period of amortization shouldn't be longer than 50 years"]
    
    if max(inputObject["reveFirst"], inputObject["constCosts"], inputObject["investment"]) > 999999999:
        return [False, "Proposed figures are too large"]

    if max(inputObject["ccIncrease"], inputObject["reveIncrease"], inputObject["PercentageVarCosts"]) > 300:
        return [False, "Proposed % increases are unreasonable"]


    return [True]

    