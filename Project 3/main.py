import runScript
from math import ceil
import fileinput


def getData():

    L=[]
    for line in fileinput.input():
        L.append(line.replace("\n",""))

    totalRunners = int(L[0])
    totalProducts = int(L[1])

    runnersPos = []
    for i in L[2].split(" "):
        runnersPos += [int(i)]

    movTime = []
    for i in range(totalProducts):
        order = []
        for j in L[3+i].split(" "):
            order += [int(j)]
        movTime.append(order)

    movTimeConv = list(map(int, L[3+totalProducts].split(" ")))


    totalOrders = int(''.join(L[4+totalProducts:5+totalProducts]))

    products = []
    for i in range(totalOrders):
        product = []
        for j in L[5+totalProducts+i].split(" "):
            product += [int(j)]
        products.append(product)

    return totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products





if __name__ == '__main__':

    prodHandled=[]
    prodConv=[]

    totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products = getData()
    
    #EXAMPLE enunciado1.wps
    #totalRunners = 2
    #runnersPos = [1,1]
    #movtime = [[1, 5, 3, 3], [5, 1, 3, 2], [3, 3, 1, 2], [3, 2, 2, 1]]
    #movTimeConv = [3, 1, 3, 2]
    #products = [[3, 1, 2, 3], [2, 4, 1]]


    lowerBound=2
    upperBound=60
    meanTime=ceil((lowerBound+upperBound)/2)
    realTime = 0
    minList=[]
    nothing=[]
    lastMinList = []


    sat=True
    while(meanTime!=upperBound):
        sat, prodHandled, prodConv,endTime, nothing = runScript.runScript(meanTime,totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products, nothing)

        if (sat == True):
            upperBound = meanTime
            realTime = endTime
        else:
            lowerBound = meanTime

        meanTime=ceil((lowerBound+upperBound)/2)
        

    sat, prodHandled, prodConv, endTime, minList = runScript.runScript(realTime,totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products, minList)
    
    while(sat == True):
        sat, prodHandled, prodConv,endTime, minList = runScript.runScript(meanTime,totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products, minList)
        if(sat == True):
            lastMinList = minList


    sat, prodHandled, prodConv,endTime, minList = runScript.runScript(meanTime,totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products, lastMinList[:-1])


    if (sat == True):
        print(realTime)
        for list in prodHandled:
           print(*list)
        for list in prodConv:
            print(*list)

    else:
        print("UNSAT")
        
