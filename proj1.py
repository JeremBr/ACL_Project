import fileinput
import pycosat

#ATTENTION JAI MIS ACCENTS DANS LES COMMENTAIRES CA PEUT POSER SOUCIS (donc suppr les commentaires si bug UTF-8)


#je sais pas si utilité au final, mais ya moy que ca soit utile
class Runner:
	def __init__(self,runner,initPos):
		self.set_runner(runner)
		self.set_time(0)
		self.set_pos(initPos)
		self.set_cost(0)

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

	def get_cost(self):
		return self.__cost

	def set_cost(self,cost):
		self.__cost=cost


#CE QUI PERMET DE DEFINIR VARIABLES
#ATTENTION SI ON RAJOUTE UN PARAMETRE AUX VARIABLES IL FAUT MODIF PARTOUT DANS LE CODE
def p(r,t,p):
	return totalRunners*r + t + p*totalProducts 
	#CEST PAS LES BONS CALCULS DE POSSIBILITES, car on va avoir croisement 
	# => ON PEUT RAJOUTER UNE VALEUR ARBITRAIRE POUR CELA, genre +1000 COMME CA ON EST SUR OKLM, ca changera pas le nombre de VARIABLES, FAUDRA JUSTE SOUSTRAIRE QUAND RECUP

def v(o,p,tc):
	return o*totalOrders+p*totalProducts + tc #CEST PAS LES BONS CALCULS DE POSSIBILITES, mais dans l'idee






#CE QUI PERMET DE RECUP DATA DEPUIS LE FILE DONNE (python3 proj1.py < fichier.wps)
def getData():

	L=[]
	for line in fileinput.input():
		L.append(line.replace("\n",""))

	totalRunners=int(L[0])
	totalProducts=int(L[1])
	runnersPos=L[2].replace(" ","")
	movTime=L[3:3+totalProducts]
	movTimeConv=L[3+totalProducts:4+totalProducts].replace(" ","")
	totalOrders=int(''.join(L[4+totalProducts:5+totalProducts]))
	products=L[5+totalProducts:5+totalProducts+totalOrders]

	return totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products





#CE QUI PERMET DE METTRE OUTPUT SOUS LE BON FORMAT POUR POUVOIR METTRE DANS FICHIER (python3 proj1.py < fichier.wps > solution.txt)
def outputData(exemple): 
#mettre en input de cette fonction, les values associes a ce quon obtient pour les mettres au bon format
	
	optTime=0
	orderRunners=[]
	timeConvProducts=[]

	#puis mettre sous le bon format d'output







def packaging_clauses():
	'''
	Create the clauses, and return them as a list
	'''

	clausesList=[]


	#orderList est la liste des orders avec chacun des products requis
	#on a donc orderList=[[1,2,3],[1,4]] par exemple
	orderList=[]
	for i in range(len(products)):
		order=products[i].replace(" ","")
		L=[]
		for j in range(1,len(order)):
			L.append(int(order[j]))

		orderList.append(L)


	#timeList est la liste des temps
	#on a donc timeList=[[1,5,3,3],[5,1,3,2],[3,3,1,2],[3,2,2,1]] par exemple
	timeList=[]
	for i in range(len(movTime)):
		time=movTime[i].replace(" ","")
		L=[]
		for j in range(len(time)):
			L.append(int(time[j]))

		timeList.append(L)



	#temps maximal dans le pire des cas, pour avoir un intervalle, sachant que temps conveyor est forcement plus grand que temps runners
	maxTime=0
	timeConvList=[]
	for i in range(len(movTimeConv)):
		time=movTimeConv[i]
		timeConvList.append(int(time))


	for j in range(len(orderList)):
		for k in range(len(orderList[j])):
			maxTime+=(timeConvList[k]*orderList[j][k])

	maxTime = maxTime - (maxTime//4)








	# 1) On test toutes les possibilites pour runner 1

	# on prend le runner 1 et on le fait choisir d'aller a un des endroits parmis les products a livrer
	# donc 1_1_1 ou 1_5_2 ou 1_3_3 ou 1_3_4 par exemple
	# il faut donc calculer T quand il aura mis le product sur le conveyor
	# T = T_prec + Ti,j



	
	firstR=runnerList[0]
	present=[]

	for j in range(len(orderList)):
		for k in range(len(orderList[j])):
			product=orderList[j][k]

			if product not in present:
				L=orderList
				del L[j][k]
				present.append(product)
				last_pos=firstR.get_pos()
				time=firstR.get_time()

				clausesList.append([-p(firstR.get_runner(),(firstR.get_time()+timeList[last_pos][product]),product),v(j,product,(time+timeConvList[product-1]))])

			#FINIR CA






		













	# x) runners toujours en mouvement
	# utiliser A -> B
	# R_T_P -> R_T+CT_p  avec p le new endroit, et CT le temps de P à p








	# x) runners peuvent pas etre au meme endroit au meme moment
	#CA C BON NE PAS TOUCHER
	for i in range(1,totalRunners):
		for j in range(maxTime):
			for k in range(totalProducts):
				clausesList.append([-p(i,j,k),-p(i+1,j,k)])

	# n*t*m (pas fait expres decrire n-t-m MDR) (dans l'exemple 1 ca fait 2*9*4=64 clauses)




	


	# variable O_P_TC
	# Le product P de l'order O arrive sur le conveyor à l'instant TC


	# x) pour toutes les commandes il faut sassurer que leurs produits sont bien recu au packaging area
	for i in range(len(orderList)):
		for j in range(len(orderList[i])):
			for k in range(maxTime): #mettre valeure plus grande?
				L=[]
				L.append(v(i+1,orderList[i][j],k))

			clausesList.append(L)

	# nombre de produit à package (exemple 1: 6 clauses)


	# x) Que ca n'arrive pas en meme temps au point de packaging
	for i in range(len(orderList)):
		for j in range(len(1,orderList[i])):
			for k in range(maxTime): #mettre valeure plus grande?
				clausesList.append([-v(i+1,orderList[i][j-1],k),-v(i+1,orderList[i][j],k)])

	# nombre de produit à package * T (exemple 1 : 6*9=54 clauses)







	return clausesList



def solve():
	
	#create Runners
	runnerList=[]
	for i in range(totalRunners):
		runnerList.append(Runner(i+1,runnersPos[i]))



	clauses = packaging_clauses()


	#rajouter clause en fonction de où sont les runners
	#for i in range(totalRunners):
		#clauses.append([p(i+1,0,runnersPos[i],0)])



	#sol = set(pycosat.solve(clauses))


	#def read_jsp():


	



    



if __name__ == '__main__':
	totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products=getData()
	solve()