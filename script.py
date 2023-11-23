





def main():
	Warpstation = {
			"Trimps" : 50000,
			"Increase" : 1.4,
			"Initial_Cost" : [0, 0, 1000000000000000,  1e14, 0]

	}


	for p in range(0,10):
		for l in range(0,12):

			base = 1
			trimps = 1


			cost = base * (pow(1.75,p)  * pow(1.4, l) / (trimps *pow(1.2,p)))
			if cost < 40:
				print("L : " + str(l) + " , P : " + str(p) + " Ratio : " + str(cost)) 


main()