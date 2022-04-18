# Timespan
# products handled, i th line = runner i : nb of products - product handled
# product arrives at conv belt, i th line = order i : nb of products - onConv:arrives

def output(sat,meanTime,prodHandled,prodConv):
	if(sat == True):
		print(meanTime)
		for list in prodHandled:
			print(*list)

		for list in prodConv:
			print(*list)

	else:
		print("UNSAT")