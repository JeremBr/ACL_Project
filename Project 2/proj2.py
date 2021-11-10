import fileinput

from z3 import Solver, Bool, Or, And, Not, AtMost, AtLeast, Then, With, is_true, sat



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

    #s = Solver()
    s=Then(With('simplify', arith_lhs=True, som=True), 'normalize-bounds', 'lia2pb', 'pb2bv', 'bit-blast', 'sat').solver()
    
    

    # VARIABLES :


    # X__R_T_P
    X = [ [ [ Bool("x_%s_%s_%s" % (i+1, j, k+1)) for k in range(totalProducts)] for j in range(maxTime+1) ] for i in range(totalRunners) ] #TIME: [0,T]

    #A__R_T
    A = [ [ Bool("a_%s_%s" % (i+1, j)) for j in range(maxTime+1) ] for i in range(totalRunners) ] #TIME: [0,T] donc maxTime+1

    #Y__TC_P
    Y = [ [ Bool("y_%s_%s" % (i, j+1)) for j in range(totalProducts) ] for i in range(maxTime+1) ]  #TIME: [1,T]

    


    
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
        for j in range(1,maxTime+1):
            for k in range(totalProducts):
                for l in range(totalProducts):
                    timeBetweenKandL=timeList[k][l]

                    if(j+timeBetweenKandL<=maxTime): #attention
                        for m in range(totalProducts):
                            for n in range(j+1,j+timeBetweenKandL):
                                noTaskBetween.append(Or(Not(X[i][j][k]),Not(X[i][j+timeBetweenKandL][l]),Not(X[i][n][m])))




    # (3): If a runner is at position p he can't be at position q at the same time t.
    onePos = []
    for i in range(maxTime+1): #[0,T]
        for j in range(totalRunners):
            L=[]
            for k in range(totalProducts):
                L.append(X[j][i][k])


            L.append(1)
            onePos.append(AtMost(L))

    

    # (4): We have to make sure that every runners stay active without taking any pauses. It means that a runner must move to another position or he becomes inactive.

    noBreak=[]
    for r in range(totalRunners):
        for t in range(maxTime+1): # [0,T]
            for p in range(totalProducts):

                if(t+1 <= maxTime):
                    L=[Not(X[r][t][p]),Not(A[r][t+1])]

                    for l in range(totalProducts):
                        timeBetweenPandL=timeList[p][l]

                        if(t+timeBetweenPandL<=maxTime):
                            L.append(X[r][t+timeBetweenPandL][l])

                    noBreak.append(Or(L))



    # (5): If we have a runner inactive at time t it implies that he is inactive at t+1.
    inactive=[]
    for i in range(totalRunners):
        for j in range(1,maxTime+1):
            if(j+1 <= maxTime):
                inactive.append(Or(A[i][j],Not(A[i][j+1])))

    

    # (6): All runners must have a timespan of at least 50% of the maximum. So, for a runner active at time t, all others runners must be active at t/2.

    activityRunner=[]
    for i in range(totalRunners):
        for j in range(1,maxTime+1):
            for k in range(totalRunners):
                if k!=i:
                    activityRunner.append(Or(Not(A[i][j]),A[k][j//2])) #ptet prb ici avec //2

    



    # (7): We have to check that a runner was at position p at time t-c_p when a product p arrives at the packaging area at time t.

    productOnConveyor=[]
    for i in range(totalProducts):
        for j in range(1,maxTime+1):

            conveyorTime=timeConvList[i]
            if((j-conveyorTime) > 0): # >=0
                L=[Not(Y[j][i])]

                for k in range(totalRunners):
                    L.append(X[k][j-conveyorTime][i])


                productOnConveyor.append(Or(L))
          


    # (8): All products must arrive at the packaging area.
    # for i in range(len(orderList)):
    #     order=orderList[i]
    #     count=len(order)
    #     L=[]
        
    #     for j in range(1,maxTime+1):
    #         for k in range(count):
    #             L.append(Y[j][order[k]-1])

    #     L.append(count)

    #     s.add(And(AtMost(L),AtLeast(L)))

    # (8): All products must arrive at the packaging area.
    for i in range(1,totalProducts+1):
        L=[]

        count=0
        for j in range(len(productList)):
            if productList[j]==i:
                count+=1

        for t in range(1,maxTime+1):
            L.append(Y[t][i-1])
            

        L.append(count)
        s.add(And(AtMost(L),AtLeast(L)))



    

    # for i in range(1,totalProducts+1):
    #     L=[]

    #     count=0
    #     for j in range(len(productList)):
    #         if productList[j]==i:
    #             count+=1


    #     for r in range(totalRunners):
    #         for t in range(maxTime+1):

    #             L.append(X[r][t][i-1])

    #     L.append(count)
    #     s.add(And(AtMost(L),AtLeast(L)))





    # INITIALIZATIONS

    #Runner Positions
    for i in range(totalRunners):
        s.add(X[i][0][int(runnersPos[i])-1] == True)

    #Runner Activities
    for i in range(totalRunners):
        s.add(A[i][0]==True)





    
    s.add(diffPos + noTaskBetween + inactive + activityRunner + productOnConveyor + noBreak + onePos)
    # if s.check() == sat:
    #     m = s.model()
    #     for x in m:
    #         if is_true(m[x]):
    #             print(x())

    s.check()
    m = s.model()
    formalize(s)
    
def formalize(s):
    
    m = s.model()
    conveyortime=[]
    if str(s.check()) == "sat":
        maxTime = 0
        for e in m:
            if m[e] == True:
                if int(str(e)[2]) > maxTime and str(e)[0 == "y"]:
                    maxTime = int(str(e)[2])
        print(maxTime)
        for r in range(totalRunners):
            counter = 0
            tempList =[]
            for e in m:
                if m[e] == True:
                    if str(e)[0] == "x" and int(str(e)[2]) == r+1:
                        counter +=1
                        tempList.append(str(e)[6])
            print(counter, end = " ")
            print(*tempList, sep = " ")            
            
             
        for r in range(len(orderList)):
            tempListProduct = []
            templistTime= []
            print(len(orderList[r]), end =" ")
            for e in m:
                if m[e] == True:
                    if str(e)[0] == "y":
                        for j in range(len(orderList[r])):
                            if int(str(e)[2]) == orderList[r][j]:
                                tempListProduct.append(int(str(e)[4]))
                                templistTime.append(int(str(e)[2]) - timeConvList[int(str(e)[4])-1])
            for i in range(len(tempListProduct)):
                print(tempListProduct[i], end=":")
                print(templistTime[i], end = " ") 
            print("")
    else:
        print("UNSAT")





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
    
