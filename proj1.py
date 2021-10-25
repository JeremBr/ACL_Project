import fileinput



def getData():

	L=[]
	for line in fileinput.input():
		L.append(line.replace("\n",""))

	totalRunners=int(L[0])
	totalProducts=int(L[1])
	runnersPos=L[2]
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





def main():
	
	totalRunners,totalProducts,runnersPos,movTime,movTimeConv,totalOrders,products=getData()


	



    



if __name__ == '__main__':
	main()