import fileinput
from z3 import Solver, Bool, Or, And, Not, AtMost, AtLeast



#OK------------
# To get data from file : (python3 proj2.py < file.wps)
def getData():

    L=[]
    for line in fileinput.input():
        L.append(line.replace("\n",""))

    totalRunners = int(L[0])
    totalProducts = int(L[1])

    runnersPos = L[2].replace(" ","")

    movTime = L[3:3+totalProducts]
    movTimeConv = L[3+totalProducts:4+totalProducts][0].replace(" ","")

    totalOrders = int(''.join(L[4+totalProducts:5+totalProducts]))
    products = L[5+totalProducts:5+totalProducts+totalOrders]

    return totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products
#--------------


def solve():

    s = Solver()


    # VARIABLES :

    #JE CROIS QUI A UN PRB AVEC LE MAXTIME CA ON A PAS LA VALEURE 0 DU COUP
    #JE VIENS DE LIMPLEM DU COUP, ESTCE QUE C BON?
    #CA FAIT DE 0 JUSQUA MAXTIME COMPRIS

    # X__R_T_P
    X = [ [ [ Bool("x_%s_%s_%s" % (i+1, j, k+1)) for k in range(totalProducts)] for j in range(maxTime+1) ] for i in range(totalRunners) ] #TIME: [0,T] donc maxTime+1 values

    #A__R_T
    A = [ [ Bool("a_%s_%s" % (i+1, j)) for j in range(maxTime+1) ] for i in range(totalRunners) ] #TIME: [0,T] donc maxTime+1 values

    #Y__TC_P
    Y = [ [ Bool("y_%s_%s" % (i, j+1)) for j in range(totalProducts) ] for i in range(maxTime+1) ]  #TIME: [0,T] donc maxTime+1 values

    


    
    # (1): We have to make sure that two runners are not at the same position at time T.
    
    diffPos=[]
    for i in range(1,maxTime+1):
        for j in range(totalProducts):

            L=[]
            for k in range(totalRunners):
                L.append(X[k][i][j])


            L.append(1)
            diffPos.append(AtMost(L))



    # (2): Runner doesn't have a task between two tasks

    noTaskBetween=[]
    for i in range(totalRunners):
        for j in range(maxTime):
            for k in range(totalProducts):
                for l in range(totalProducts):
                    timeBetweenKandL=timeList[k][l]

                    if(j+timeBetweenKandL<maxTime): #to not get an "index out of range" # <=
                        for m in range(totalProducts):
                            for n in range(j+1,j+timeBetweenKandL):
                                noTaskBetween.append(Or(Not(X[i][j][k]),Not(X[i][j+timeBetweenKandL][l]),Not(X[i][n][m])))

    
    #peux etre que cest mal implem
    #et ptet prb au niveau TIME intervalle            
    #print(noTaskBetween)




    # (3): If a runner is at position p he can't be at position q at the same time t.
    onePos = []
    for i in range(maxTime+1): #[0,T]
        for j in range(totalRunners):
            L=[]
            for k in range(totalProducts):
                L.append(X[j][i][k])


            L.append(1)
            onePos.append(AtMost(L))

    




    # (x): If a runner is inactive at time t, then he is inactive at time k+1.
    inactive=[]
    for i in range(totalRunners):
        for j in range(maxTime):
            inactive.append(Or(A[i][j],Not(A[i][j+1])))

    

    # (x): If a runner is active at time t, then all others runners must be active at time t/2.

    activityRunner=[]
    for i in range(totalRunners):
        for j in range(1,maxTime):
            for k in range(totalRunners):
                if k!=i:
                    activityRunner.append(Or(Not(A[i][j]),A[k][j//2])) #ptet prb ici avec //2

    

    # (x): If a runner is at a given position, then then it must move to another position or he becomes inactive.

    noBreak=[]
    for i in range(totalRunners):
        for j in range(maxTime+1): # [0,T]
            for k in range(totalProducts):

                #if j+1 <= maxTime

                L=[Not(X[i][j][k]),Not(A[i][j])]

                for l in range(totalProducts):
                    if(j+timeBetweenKandL<maxTime):
                        timeBetweenKandL=timeList[k][l]
                        L.append(X[i][j+timeBetweenKandL][l])

                noBreak.append(Or(L))



    # (x): If a product p arrives at time t, then a runner must be at position p at time t-c_p.

    productOnConveyor=[]
    for i in range(totalProducts):
        for j in range(1,maxTime):

            conveyorTime=timeConvList[i]
            if((j-conveyorTime) > 0): # >=0
                L=[Not(Y[j][i])]

                for k in range(totalRunners):
                    L.append(X[k][j-conveyorTime][i])


                productOnConveyor.append(Or(L))

    #peux etre que cest mal implem            
    #print(productOnConveyor)


    # (x): All products must arrive at the packaging area
    for i in range(len(orderList)):
        order=orderList[i]
        count=len(order)
        L=[]
        
        for j in range(1,maxTime+1):
            for k in range(len(order)):
                L.append(Y[j][order[k]-1])

        L.append(count)

        s.add(AtMost(L))
        s.add(AtLeast(L))




    ############### FAIRE FAIRE FAIRE FAIRE : REGARDER PHOTOS POUR VOIR LES INTERVALLES (TIME SURTOUT) QUE CE SOIT BON POUR TOUTES LES FONCTIONS AVEC LES BOUCLES FOR ETC




    # INITIALIZATIONS

    for i in range(totalRunners):
        s.add(X[i][0][int(runnersPos[i])-1] == True)





    
    s.add(diffPos + noTaskBetween + inactive + activityRunner + productOnConveyor + noBreak + onePos)
    print(s.check())
    print(s.model())






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
    
