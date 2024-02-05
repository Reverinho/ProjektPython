from tkinter import *
from tkinter import ttk
from data import dataObject
from window import *
from Test import test
from Projekt_Py import *
from plot import generatePlot

myTreeObject = {}
def plotClick():
    generatePlot(inputObject)

def infoClick():
    text.configure(padx = 0, text = 
                   "Project is approved. NPV equals: {}\n Acceptable discount rates range from 0 to {}%"
                   .format(round(result[0], 2), 100*round(result[3], 2)))

def inputClick():
    string = ""
    for i in range(11): string += myTree.item(i, "text") + ": " + myTree.item(i, "value")[0] + "\n"
    text.configure(text = string, padx = 100)
def createTheGoodEnding():
    global text
    textFrame.grid(row = 0, column = 1, padx = 60)
    buttonFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
    infoButton = Button(buttonFrame, text = "Project info", bg = LGRAY, fg = "white", borderwidth = 10, padx = 40, pady = 5, command = infoClick, highlightthickness = 0, bd = 0)
    inputButton = Button(buttonFrame, text = "Inputs info", bg = LGRAY, fg = "white", borderwidth = 10, padx = 40, pady = 5, command = inputClick, highlightthickness = 0, bd = 0)
    plotButton = Button(buttonFrame, text = "Generate plot", bg = LGRAY, fg = "white", borderwidth = 10, padx = 40, pady = 5, command = plotClick, highlightthickness = 0, bd = 0)
    infoButton.pack(fill = X)
    inputButton.pack(pady = 70, fill = X)
    plotButton.pack(fill = X)
    text = Label(textFrame, pady = 10, bg = DGRAY, fg = "white", 
                 text = "Project is approved. NPV equals: {}\n Acceptable discount rates range from 0 to {}%"
                 .format(round(result[0], 2), 100*round(result[3], 2)))
    text.pack()
def submitInfo(result):
    global info, textFrame, buttonFrame
    try: info.destroy()
    except: pass
    info = Toplevel(window)
    info.focus()
    info.title("Result")
    x = (screen_width / 2) - (700 / 2)
    y = (screen_height / 2) - (300 / 2)
    info.geometry(f"{700}x{300}+{int(x)}+{int(y)- 100}")
    infoFrame = Frame(info, bg = DGRAY)
    infoFrame.pack(expand = True, fill = BOTH)
    textFrame = Frame(infoFrame, bg = DGRAY)
    buttonFrame = Frame(infoFrame, bg = DGRAY)
    if result[1]: createTheGoodEnding()
    else:
        textFrame.pack(fill = BOTH, expand = True)
        if result[3] < 0: Label(textFrame, bg = DGRAY, fg = "white",pady = 10, 
                                text = "Project cannot be approved due to NPV being equal to {}\n There are no acceptable discount rates for this project\n Try inputting different set of data"
                                .format(round(result[0], 2), round(result[3], 2))).pack(anchor = CENTER)
        else: 
            if result[3] < result[2]: Label(textFrame, bg = DGRAY, fg = "white", pady = 10, 
                    text = "Project cannot be approved due to NPV being equal to {}\n Acceptable discount rates range from 0 to {}%\n Try inputting different set of data\nYour current discount rate is {}%"
                    .format(round(result[0], 2), 100*round(result[3], 2), 100*round(result[2], 2) )).pack(anchor = CENTER)
            else: Label(textFrame, bg = DGRAY, fg = "white",pady = 10, 
                                text = "Project cannot be approved due to NPV being equal to {}\n There are no acceptable discount rates for this project\n Try inputting different set of data"
                                .format(round(result[0], 2), round(result[3], 2))).pack(anchor = CENTER)
    def destroy(event):
        info.destroy()
    info.bind("<Return>", destroy)
    info.mainloop()

def submitFunc():
    global inputObject
    inputObject = {
    "equity": 0,
    "equityCost": 0,
    "borrowedCapCost": 0,
    "duration": 0,
    "reveFirst": 0,
    "reveIncrease": 0,
    "PercentageVarCosts": 0, 
    "constCosts": 0, 
    "ccIncrease": 0, 
    "investment": 0, 
    "amortizationDur": 0,
}
    itemIndex = 0
    for element in inputObject:
        try: value = float(myTree.item(itemIndex, "value")[0])
        except: value = myTree.item(itemIndex, "value")[0]
        inputObject[element] = value
        itemIndex += 1
    if (test(inputObject))[0]: 
        inputObject["duration"] = int(inputObject["duration"]); inputObject["amortizationDur"] = int(inputObject["amortizationDur"])
        inputObject["equity"] /= 100; inputObject["equityCost"] /= 100; inputObject["borrowedCapCost"] /= 100
        inputObject["ccIncrease"] /= 100; inputObject["PercentageVarCosts"] /= 100; inputObject["reveIncrease"] /= 100
        global result
        result = evaluate(inputObject)
        result.append(IRR(inputObject))
        submitInfo(result)
    else: errorFunc((test(inputObject))[1])

def DownKey(event):
    item = label.cget("text")
    index = list(dataObject.values()).index(item) 
    entry.delete(0, END)
    try:
        label.configure(text = "{}".format(myTree.item(index + 1, "text")))
    except:
        label.configure(text = "{}".format(myTree.item(0, "text")))

def UpKey(event):
    item = label.cget("text")
    index = list(dataObject.values()).index(item)
    entry.delete(0, END)
    try:
        label.configure(text = "{}".format(myTree.item(index - 1, "text")))
    except:
        label.configure(text = "{}".format(myTree.item(len(dataObject) - 1, "text")))

def errorFunc(arg = 0):
    global error
    try: error.destroy()
    except: pass
    error = Toplevel(window)
    error.focus()
    error.title("Error")
    x = (screen_width / 2) - (300 / 2)
    y = (screen_height / 2) - (50 / 2)
    error.geometry(f"{300}x{50}+{int(x)}+{int(y)- 100 }")
    frame = Frame(error)
    frame.pack(expand = True)
    if arg == 0: Label(frame, text = "You entered wrong input\nTry again").pack()
    else: Label(frame, text = arg).pack()
    def destroy(event):
        error.destroy()
    error.bind("<Return>", destroy)
    error.mainloop()

def buttonClick(event = 0):
    item = label.cget("text")
    index = list(dataObject.values()).index(item)
    itemName = myTree.item(index, "text")
    try:
        value = list(entry.get())
        for i in range(len(value)):
            if value[i] == ",":
                value[i] = "."
        value = "".join(value)
        value = float(value)
        try: label.configure(text = "{}".format(myTree.item(index + 1, "text")))
        except: label.configure(text = "{}".format(myTree.item(0, "text")))
        myTreeObject[itemName] = value
        try: entry.delete(0, END)
        except: pass
        loadMyInterface()
    except ValueError:
        errorFunc()
        
def OnDoubleClick(event):
    item = myTree.selection()[0]
    itemName = myTree.item(item, "text")
    label.configure(text = "{}".format(itemName))
    loadMyInterface()

def loadMyInterface():
    global myTree, window, label, entry

    try: myTree.destroy()
    except: pass
    
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", background = LGRAY, 
                fieldbackground = LGRAY, foreground = "white")
    style.map("Treeview", background = [("selected", "#6495ED")])

    myTree = ttk.Treeview(firstFrame)

    myTree["columns"] = ("Value")

    myTree.configure(height = 11)

    myTree.column("#0", anchor = W, width = 300, minwidth = 25)
    myTree.column("Value", anchor = CENTER, width = 150)

    myTree.heading("#0", text = "Data", anchor = CENTER)
    myTree.heading("Value", text = "Value", anchor = CENTER)
    count = 0
    for i in dataObject.values():
        try:
            myTree.insert(parent = "", index = "end", iid = count, text = i, values = myTreeObject[i])
        except KeyError:
            myTree.insert(parent = "", index = "end", iid = count, text = i, values = "Enter")
            pass
        count += 1

    myTree.bind("<Double-1>", OnDoubleClick)

    myTree.grid(column = 0, row = 0, padx = 30, pady = 30)

firstFrame = Frame(window, bg = DGRAY, highlightthickness = 0)
entryFrame = Frame(firstFrame, bg = DGRAY, highlightthickness = 0)
entry = Entry(entryFrame, bg = LGRAY, highlightthickness = 0, fg = "white", width = 35, borderwidth = 10)
label = Label(entryFrame, bg = DGRAY, highlightthickness = 0, fg = "white", text = "{}".format(dataObject["data1"]))
inputButton = Button(entryFrame, text = "Enter", bg = LGRAY, fg = "white", borderwidth = 10, padx = 40, pady = 5, command = buttonClick, highlightthickness = 0, bd = 0)
submitButton = Button(window, text = "Submit", bg = LGRAY, fg = "white", borderwidth = 10, padx = 40, pady = 5, command = submitFunc, highlightthickness = 0, bd = 0)

firstFrame.pack()
entryFrame.grid(row = 0, column = 1, padx = 35)
Label(entryFrame, text = "Enter", bg = DGRAY, highlightthickness = 0, fg = "white").pack()
label.pack()
entry.pack()
inputButton.pack(padx = 40, pady = 5)
submitButton.pack()


loadMyInterface()
    
entry.bind('<Tab>', entry.after(1, lambda: window.focus_force()))
root.bind('<Up>', UpKey)
root.bind('<Down>', DownKey)
root.bind('<Return>', buttonClick)
def destroy(event):
    root.destroy()
root.bind('<Escape>', destroy)

root.mainloop()