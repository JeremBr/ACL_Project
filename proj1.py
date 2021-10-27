import fileinput
import pycosat


class Runner:
	def __init__(self,runner,initPos):
		self.set_runner(runner)
		self.set_time(0)
		self.set_pos(initPos)

	def get_runner(self):
		return self.__runner

	def set_runner(self,runner):
		self.__runner=runner

	def get_time(self):
		return self.__time

	def set_time(self,time):
		self.__time=time

	def get_pos(self):
		return self.__pos

	def set_pos(self,pos):
		self.__pos=pos



# Creating variables

def p(r,t,p):
	return r*totalRunners + p*totalProducts +t+1000 #+1000 to have different variable names

def v(p,tc):
	return p*totalProducts +tc



#OK------------
# To get data from file : (python3 proj1.py < fichier.wps)
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



# To get output in the required format (python3 proj1.py < fichier.wps > solution.txt)
def outputData(exemple): 
	
	optTime=0
	orderRunners=[]
	timeConvProducts=[]

	#Not done because we don't have a nice solver


def packaging_clauses(runnerList):
	'''
	Create the clauses, and return them as a list
	'''
	clausesList=[]

	# (1) Try all possibilities

	def allClausesProduct(index,product_list):

		actualRunner=runnerList[index]

		for j in range(len(product_list)):

			product=product_list[j]
			last_pos=actualRunner.get_pos()
			time=actualRunner.get_time()

			newTime=(time+timeList[last_pos-1][product-1])
			newPos=product
			if(newTime>maxTime):
				continue

			clausesList.append([-p(index+1,newTime,newPos),v(newPos,(newTime+timeConvList[product-1]))])
			
			actualRunner.set_time(newTime)
			actualRunner.set_pos(newPos)

			newProductList=product_list[:j]+product_list[j+1:len(product_list)]

			if(newProductList==[]):
				continue

			allClausesProduct(index,newProductList)


	for i in range(totalRunners):
		allClausesProduct(i,productList)




			
	#OK------------
	# (2)) Runners can't be at the same position P in a time T
	for i in range(1,totalRunners):
		for j in range(maxTime):
			for k in range(totalProducts):
				clausesList.append([-p(i,j+1,k),-p(i+1,j+1,k)])

	#--------------


	#OK------------
	# (3) Runners keep moving
	# R_T_P -> R_T+t_p

	for i in range(totalRunners):
		for j in range(maxTime):
			for k in range(totalProducts):
				for l in range(totalProducts):
						clausesList.append([-p(i+1,j,k+1),p(i+1,j+(timeList[k][l]),l+1)])

	#--------------




	# variable P_TC


	#OK------------
	# (4) Doesn't arrive in the same time at the packaging area
	for i in range(len(orderList)):
		for j in range(1,len(orderList[i])):
			for k in range(maxTime):
				clausesList.append([-v(orderList[i][j-1],k+1),-v(orderList[i][j],k+1)])

	# total product to package * T 
	# (example 1 : (3-1 + 2-1)*9=27 clauses)
	#--------------


	#OK------------
	# (5) for all orders, we have to check if all products arrived in the packaging area
	for i in range(len(orderList)):
		for j in range(len(orderList[i])):
			L=[]
			for k in range(maxTime):
				L.append(v(orderList[i][j],k+1))

			clausesList.append(L)

	# total product to package
	# (example 1: 5 clauses)
	#--------------


	print(len(clausesList))
	return clausesList,productList,maxTime



def solve():
	
	#create Runners
	runnerList=[]
	for i in range(totalRunners):
		runnerList.append(Runner(i+1,int(runnersPos[i])))

	clauses,productList,maxTime = packaging_clauses(runnerList)

	#add clauses where the runners start
	# for i in range(totalRunners):
	# 	clauses.append([p(i+1,0,int(runnersPos[i]))])

	sol = set(pycosat.solve(clauses))

	
	def read_product(i,j):
		for d in range(totalProducts):
			if (p(i,j,d+1)-1000) in sol:
				return d+1


	def read_conveyor(i):
		for t in range(maxTime):
			if (v(i,t)) in sol:
				return t




	runnersMov=[]
	for i in range(totalRunners):
		for j in range(maxTime):
			prd=read_product(i+1,j+1)

			if prd!=None:
			 	runnersMov.append([i+1,j,prd])


	conveyorMov=[]
	for i in range(len(productList)):
		conv=read_conveyor(i+1)
		if conv!=None:
			conveyorMov.append([i+1,conv])


	print(runnersMov)
	print(conveyorMov)



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
