def calculate(inputObject, wacc):
    equity, equityCost, borrowedCapCost, duration, reveFirst, reveIncrease, PercentageVarCosts, constCosts, ccIncrease, investment, amortizationDur = inputObject.values()  
    
    wsp = []
    for i in range(0, duration + 1): wsp.append(1 / ((1 + wacc) ** i)) ##tworzenie współczynnika dyskonta

    VarCosts = PercentageVarCosts * reveFirst

    earnings_aftertax = []
    earnings_aftertax.insert(0, (reveFirst - constCosts - VarCosts) * (0.81))

    workingCap = [0.15 * reveFirst]
    przychody = [reveFirst]

    for i in range(1, duration): #kalkulowanie zysku operacyjnego po opodatkowaniu 
        reveFirst = reveFirst * (reveIncrease+1)
        przychody.append(reveFirst)
        constCosts = constCosts * (ccIncrease + 1)
        VarCosts = 0.25 * reveFirst
        earnings_aftertax.append((reveFirst - constCosts - VarCosts) * (0.81))
        workingCap.append(0.15 * reveFirst - 0.15 * przychody[i-1])  
   
    amortyzacja = investment / amortizationDur 

    FCFF = [(-1) * investment] #Przepływy pieniężne 

    for i in range(0, duration): FCFF.append(earnings_aftertax[i] + amortyzacja - workingCap[i])
            
    #Liczenie NPV
    NPV = 0
    for i in range(0, duration + 1): NPV = NPV + FCFF[i] * wsp[i]
    return NPV

def evaluate(inputObject):
    equity, equityCost, borrowedCapCost = inputObject["equity"], inputObject["equityCost"], inputObject["borrowedCapCost"]
    borrowedCap = 1 - equity
    wacc = (equity * equityCost + borrowedCap * borrowedCapCost * (1 - 0.19))
    
    NPV = calculate(inputObject, wacc)
    
    if NPV > 0: result = [NPV, True, wacc]
    else: result = [NPV, False, wacc]

    return result

def IRR(inputObject):
    equity, equityCost, borrowedCapCost = inputObject["equity"], inputObject["equityCost"], inputObject["borrowedCapCost"]
    #Liczenie wewnętrznej stopy zwrotu
    borrowedCap = 1 - equity
    wacc = (equity * equityCost + borrowedCap * borrowedCapCost * (1-0.19))
    epsilon = 10 #Dokładność przybliżenia 
    
    #aproksymacja IRR - program będzie ponownie przeliczać NPV dla konkrentych irr
    NPV = 1 + epsilon
    while (abs(NPV) > epsilon):
        NPV = calculate(inputObject, wacc)
        dNPV = derivative(inputObject,wacc)
        new_wacc = wacc - (NPV/dNPV)
        wacc = new_wacc    
    return wacc

def derivative(inputObject, wacc):
    equity, equityCost, borrowedCapCost, duration, reveFirst, reveIncrease, PercentageVarCosts, constCosts, ccIncrease, investment, amortizationDur = inputObject.values()
    wsp = [1.0]
    for i in range(1, duration + 1): wsp.append((-i) / ((1 + wacc) ** (i+1)))

    VarCosts = PercentageVarCosts * reveFirst

    earnings_aftertax = []
    earnings_aftertax.insert(0, (reveFirst - constCosts - VarCosts) * (0.81))

    workingCap = [0.15 * reveFirst]
    przychody = [reveFirst]

    for i in range(1, duration): #kalkulowanie zysku operacyjnego po opodatkowaniu 
        reveFirst = reveFirst * (reveIncrease+1)
        przychody.append(reveFirst)
        constCosts = constCosts * (ccIncrease + 1)
        VarCosts = 0.25 * reveFirst
        earnings_aftertax.append((reveFirst - constCosts - VarCosts) * (0.81))
        workingCap.append(0.15 * reveFirst - 0.15 * przychody[i-1])  
   
    amortyzacja = investment / amortizationDur 

    FCFF = [(-1) * investment] #Przepływy pieniężne 

    for i in range(0, duration): FCFF.append(earnings_aftertax[i] + amortyzacja - workingCap[i])
            
    #Liczenie dNPV
    dNPV = 0
    for i in range(0, duration + 1): dNPV = dNPV + FCFF[i] * wsp[i]
    return dNPV