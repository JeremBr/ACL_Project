import fileinput
import pycosat

#ATTENTION JAI MIS ACCENTS DANS LES COMMENTAIRES CA PEUT POSER SOUCIS (donc suppr les commentaires si bug UTF-8)



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





#CE QUI PERMET DE DEFINIR VARIABLES
#ATTENTION SI ON RAJOUTE UN PARAMETRE AUX VARIABLES IL FAUT MODIF PARTOUT DANS LE CODE
def p(r,t,p):
	return r*totalRunners + p*totalProducts +t + 1000
	#CEST PTET PAS LES BONS CALCULS DE POSSIBILITES

def v(p,tc):
	return p*totalProducts +tc






#OK------------
#CE QUI PERMET DE RECUP DATA DEPUIS LE FILE DONNE (python3 proj1.py < fichier.wps)
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





#CE QUI PERMET DE METTRE OUTPUT SOUS LE BON FORMAT POUR POUVOIR METTRE DANS FICHIER (python3 proj1.py < fichier.wps > solution.txt)
def outputData(exemple): 
#mettre en input de cette fonction, les values associes a ce quon obtient pour les mettres au bon format
	
	optTime=0
	orderRunners=[]
	timeConvProducts=[]

	#puis mettre sous le bon format d'output







def packaging_clauses(runnerList):
	'''
	Create the clauses, and return them as a list
	'''

	clausesList=[]


	#OK------------
	#orderList est la liste des orders avec chacun des products requis
	#on a donc orderList=[[1,2,3],[1,4]] par exemple
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
	#timeList est la liste des temps
	#on a donc timeList=[[1,5,3,3],[5,1,3,2],[3,3,1,2],[3,2,2,1]] par exemple
	timeList=[]
	for i in range(len(movTime)):
		time=movTime[i].replace(" ","")
		L=[]
		for j in range(len(time)):
			L.append(int(time[j]))

		timeList.append(L)
	#--------------


	#OK------------
	#temps maximal dans le pire des cas, pour avoir un intervalle, sachant que temps conveyor est forcement plus grand que temps runners
	maxTime=0
	timeConvList=[]
	for i in range(len(movTimeConv)):
		time=movTimeConv[i]
		timeConvList.append(int(time))


	for j in range(len(orderList)):
		for k in range(len(orderList[j])):
			maxTime+=timeConvList[k]

	maxTime = maxTime - (maxTime//4)
	#--------------









	# 1) On ecrit toutes les possib

	

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




			




	# x) runners toujours en mouvement
	# utiliser A -> B
	# R_T_P -> R_T+CT_p  avec p le new endroit, et CT le temps de P à p

	#JAI POSSIBLEMENT MAL FAIT CETTE IMPLEMENTATION PRSK IL FAIT SOMMEIL

	for i in range(totalRunners):
		L=[]
		for j in range(maxTime):
			for k in range(totalProducts):
				for l in range(totalProducts):
					if k!=l:
						L.append(p(i+1,j+(timeList[k][l]),l+1))

			L.append(-p(i+1,j,k+1))
		clausesList.append(L)






	#OK------------
	# x) runners peuvent pas etre au meme endroit au meme moment
	for i in range(1,totalRunners):
		for j in range(maxTime):
			for k in range(totalProducts):
				clausesList.append([-p(i,j,k),-p(i+1,j,k)])

	# n*t*m (pas fait expres decrire n-t-m MDR) (dans l'exemple 1 ca fait 1*9*4=36 clauses)
	#--------------




	


	# variable O_P_TC
	# Le product P de l'order O arrive sur le conveyor à l'instant TC


	#OK------------
	# x) pour toutes les commandes il faut sassurer que leurs produits sont bien recu au packaging area
	for i in range(len(orderList)):
		for j in range(len(orderList[i])):
			L=[]
			for k in range(maxTime):
				L.append(v(orderList[i][j],k+1))

			clausesList.append(L)

	# nombre de produit à package (exemple 1: 5 clauses)
	# PEUT ETRE RAJOUTER CE QUE JAI VU AVEC PROF
	#--------------



	#OK------------
	# x) Que ca n'arrive pas en meme temps au point de packaging area
	for i in range(len(orderList)):
		for j in range(1,len(orderList[i])):
			for k in range(maxTime):
				clausesList.append([-v(orderList[i][j-1],k+1),-v(orderList[i][j],k+1)])

	# nombre de produit à package * T (exemple 1 : (3-1 + 2-1)*9=27 clauses)
	#--------------


	print(len(clausesList))
	return clausesList,productList,maxTime



def solve():
	
	#create Runners
	runnerList=[]
	for i in range(totalRunners):
		runnerList.append(Runner(i+1,int(runnersPos[i])))



	clauses,productList,maxTime = packaging_clauses(runnerList)

	#rajouter clause en fonction de où sont les runners
	# for i in range(totalRunners):
	# 	clauses.append([p(i+1,0,int(runnersPos[i]))])

	sol = set(pycosat.solve(clauses))
	

	#Il va ptet falloir faire un test quand on a plusieurs product

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
	solve()