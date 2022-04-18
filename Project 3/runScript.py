import os

def generateFile(time,totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products, minList):
    f = open("script.lp", "w")

    # Constances
    runnersConst= "#const r = "+str(totalRunners)+"."
    timeConst="#const t = "+str(time)+"."
    productConst="#const p = "+str(totalProducts)+"."
    f.write(runnersConst+"\n")
    f.write(timeConst+"\n")
    f.write(productConst+"\n")

    f.write("\n")

    for i in range(len(products)):
        for j in range(1,len(products[i])):
            f.write("order("+str(i+1)+","+str(products[i][j])+").\n")


    f.write("\n")
    f.write("runner(1..r).\n")
    f.write("time(1..t).\n")
    f.write("product(1..p).\n")


    f.write("\n")
    for i in range(totalRunners):
        f.write("task("+str(i+1)+",0,"+str(runnersPos[i])+",0).\n")

    f.write("\n")

    for i in range(len(movTime)):
        for j in range(len(movTime[i])):
            f.write("travel_time("+str(i+1)+","+str(j+1)+","+str(movTime[i][j])+").\n")
        f.write("\n")


    f.write("\n")
    for i in range(len(movTimeConv)):
        f.write("conveyor_time("+str(i+1)+","+str(movTimeConv[i])+").\n")

    f.write("\n")
    f.write("\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("%(0): Products MUST be achieved\n")
    f.write("1{task(R,T,P,O):time(T),T>0,runner(R)}1 :- order(O,P).\n")
    f.write("%------------------------------\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("%(1): We have to make sure that two runners are not at the same position at time t.\n")
    f.write(":- task(R1,T,P,_), task(R2,T,P,_), R1!=R2, T>0.\n")
    f.write("%------------------------------\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("%(2): no task between two tasks/positions\n")
    f.write(":- task(R,T1,P1,_), task(R,T2,P2,_), T2=TT+T1, travel_time(P1,P2,TT), task(R,T3,_,_), T1<T3, T3<T2.\n")
    f.write("%------------------------------\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("% (3): If a runner is at position p he can't be at position q at the same time t.\n")
    f.write(":- task(R,T,P,_), task(R,T,Q,_), P!=Q.\n")
    f.write(":- task(R,T,P,O), task(R,T,P,M), M!=O.\n")
    f.write("%------------------------------\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("% (4): We have to make sure that every runners stay active without taking any pauses. It means that a runner must move to another position or he becomes inactive.\n")
    f.write("activity(R,T):- task(R,T,P,_).\n")
    f.write("-activity(R,T):- not activity(R,T), runner(R), time(T).\n")
    f.write("valid_pos(R,T2,Q):- task(R,T1,P,O), travel_time(P,Q,TT),T2=TT+T1.\n")
    f.write("-task(R,T,P,O) :- not valid_pos(R,T,P), order(O,P), runner(R), time(T).\n")
    f.write("%------------------------------\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("%(5): runner active at T, must be active before\n")
    f.write("activity(R,T-1) :- activity(R,T), T>1.\n")
    f.write("%------------------------------\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("%(6): All runners must have a timespan of at least 50% of the maximum. So, for a runner active at time t, all others runners must be active at t/2.\n")
    f.write(":- activity(R1,T1), -activity(R2,T2), T2<T1/2, R1!=R2.\n")
    f.write("%------------------------------\n")
    f.write("\n")

    f.write("%------------------------------\n")
    f.write("%(7): two products doesnt arrive at the same time at the packaging area.\n")
    f.write("arrive(P,T+C) :- task(R,T,P,O), conveyor_time(P,C), T>0.\n")
    f.write(":- arrive(P1,T), arrive(P2,T), P1!=P2.\n")
    f.write("%------------------------------\n")
    f.write("\n")

    for i in range(len(minList)):
        f.write("-arrive(P,"+str(minList[i])+") :- product(P).\n")

    f.write("#show task/4.\n")
    f.write("#show arrive/2.")

    f.close()



def runScript(time,totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products, minList):
    
    generateFile(time,totalRunners, totalProducts, runnersPos, movTime, movTimeConv, totalOrders, products, minList)

    result = os.popen('clingo script.lp').read()
    #print(result)
    

    sat=False
    prodHandled = []
    prodConv=[]
    endTime=0


    if not "UNSATISFIABLE" in result:
        sat=True

        for _ in range(totalRunners):
            prodHandled += [[0]]

        for _ in range(len(products)):
            prodConv += [[0]]


        delivered_list = []
        for r in range(totalRunners):
            for t in range(1,time+1):
                for p in range(totalProducts):
                    for o in range(len(products)):
                        task = ("task("+str(r+1)+","+str(t)+","+str(p+1)+","+str(o+1)+")")
                        if(task in result):
                            delivered_list += [task]

                            prodHandled[r] += [p + 1]
                            prodHandled[r][0] += 1

                            prodConv[o] += [str(p+1)+":"+str(t)]
                            prodConv[o][0]+=1

                            break

        maxTimeConv=0
        for i in range(len(movTimeConv)):
            if movTimeConv[i]>maxTimeConv:
                maxTimeConv=movTimeConv[i]
        maxTime = time + maxTimeConv

        if(maxTime in minList):
            sat=False
        else:
            minList.append(maxTime)

        for t in range(1,maxTime):
            for p in range(totalProducts):
                arrive = "arrive("+str(p)+","+str(t)+")"
                if arrive in result:
                    if t>endTime:
                        endTime=t





    return sat, prodHandled, prodConv, endTime, minList