import fileinput
import pycosat



def p(r,t,p,c):
	return totalRunners*r + t + p*totalProducts + c #c*max(movTime) ou c*nombrepossib(movTime)

	
def getData():

	L=[]
	for line in fileinput.input():
		L.append(line.replace("\n",""))

	totalRunners=int(L[0])
	totalProducts=int(L[1])
	runnersPos=L[2].replace(" ","")
	movTime=L[3:3+totalProducts]
	movTimeConv=L[3+totalProducts:4+totalProducts]
	totalOrders=int(''.join(L[4+totalProducts:5+totalProducts]))
	products=L[5+totalProducts:5+totalProducts+totalOrders]

	return totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products




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

	for i in range(1,totalRunners):
		clausesList.append([p(i,), p(i+1,)])



	return clausesList



def solve():
	
	

	clauses = packaging_clauses()


	#rajouter clause en fonction de où sont les runners
	for i in range(totalRunners):
		clauses.append([p(i+1,0,runnersPos[i],0)])



	sol = set(pycosat.solve(clauses))


	def read_jsp():


	



    



if __name__ == '__main__':
	totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products=getData()
	solve()