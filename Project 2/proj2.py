import fileinput
from z3 import Solver, Bool







#OK------------
# To get data from file : (python3 proj2.py < fichier.wps)
def getData():

    L=[]
    for line in fileinput.input():
        L.append(line.replace("\n",""))

    totalRunners=int(L[0])
    totalProducts=int(L[1])
    runnersPos=L[2].replace(" ","")
    movTime=L[3:3+totalProducts]
    movTimeConv=L[3+totalProducts:4+totalProducts][0].replace(" ","")
    totalOrders=int(''.join(L[4+totalProducts:5+totalProducts]))
    products=L[5+totalProducts:5+totalProducts+totalOrders]

    return totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products
#--------------


def solve():

                 




if __name__ == '__main__':
    totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products=getData()



    #OK------------
    #orderList is the order list with all products required
    #example 1: orderList=[[1,2,3],[1,4]]
    orderList=[]
    for i in range(len(products)):
        order=products[i].replace(" ","")
        L=[]
        for j in range(1,len(order)):
            L.append(int(order[j]))

        orderList.append(L)

    productList=[]
    for i in range(len(orderList)):
        for j in range(len(orderList[i])):
            productList.append(orderList[i][j])
    #--------------


    #OK------------
    #timeList is the time list to move from one point to another
    #example 1: timeList=[[1,5,3,3],[5,1,3,2],[3,3,1,2],[3,2,2,1]]
    timeList=[]
    for i in range(len(movTime)):
        time=movTime[i].replace(" ","")
        L=[]
        for j in range(len(time)):
            L.append(int(time[j]))

        timeList.append(L)
    #--------------


    #OK------------
    maxTime=0
    timeConvList=[]
    for i in range(len(movTimeConv)):
        time=movTimeConv[i]
        timeConvList.append(int(time))


    for j in range(len(orderList)):
        for k in range(len(orderList[j])):
            maxTime+=timeConvList[k]

    maxTime = maxTime - (maxTime//3)
    #--------------


    solve()
    
