import pprint

#Dictionary to hold impact, severe impact and output data 
data=dict()
impactDict=dict()
severeImpactDict=dict()
estimate=dict()

keylist=["currentlyInfected","infectionsByRequestedTime","severeCasesByRequestedTime","hospitalBedsByRequestedTime",
		"casesForICUByRequestedTime","casesForVentilatorsByRequestedTime","dollarsInFlight"]

def estimator(x):
	# variables holding inputdata 
	
	period=x["periodType"]
	reportedCases=x['reportedCases']
	time=x["timeToElapse"]
	beds=x["totalHospitalBeds"]
	avgDailyIncome=x["region"]["avgDailyIncomeInUSD"]
	avgDailyPopulation=x["region"]["avgDailyIncomePopulation"]
	pop=x["population"]
	
	# check if reported cases key has a value
	if reportedCases == None:
		print("No value for reported Cases")


	# Days, weeks, months normalization to days
	if period == "weeks":
		days=time*7
	elif period == "months":
		days=time*30
	else:
		days=time


	factor= days/3
	factor=int(factor)

	number_of_days=pow(2,factor)
	
# Impact
	currently_infect=reportedCases *10
		

	infections_by_time=currently_infect* number_of_days
	infections_by_time=int(infections_by_time)


	severeCasesByRequestedTime=	0.15 * infections_by_time
	severeCasesByRequestedTime=int(severeCasesByRequestedTime)

	available_beds=0.35 * beds
	usable_beds=available_beds-severeCasesByRequestedTime
	usable_beds=int(usable_beds)

	casesForICUByRequestedTime=0.05 * infections_by_time
	casesForICUByRequestedTime=int(casesForICUByRequestedTime)
	
	casesForVentilatorsByRequestedTime=0.02 * infections_by_time
	casesForVentilatorsByRequestedTime=int(casesForVentilatorsByRequestedTime)

	dollars=(infections_by_time*avgDailyPopulation*avgDailyIncome)/time
	dollars=int(dollars)

	tlc=[currently_infect,infections_by_time,severeCasesByRequestedTime,usable_beds,
		casesForICUByRequestedTime,casesForVentilatorsByRequestedTime,dollars]

	impactDict=dict(zip(keylist,tlc))


# Severe impact
	scurrently_infect=reportedCases*50
	scurrently_infect=int(scurrently_infect)

	sinfections_by_time=scurrently_infect*number_of_days
	sinfections_by_time=int(sinfections_by_time)

	severeCasesByRequest=0.15 * sinfections_by_time
	severeCasesByRequest=int(severeCasesByRequest)

	free_beds=available_beds-severeCasesByRequest
	free_beds=int(free_beds)

	casesForICUByRequest=0.05 * sinfections_by_time
	casesForICUByRequest=int(casesForICUByRequest)
	
	casesForVentilatorsByRequest=0.02 * sinfections_by_time
	casesForVentilatorsByRequest=int(casesForVentilatorsByRequest)

	sdollars=(sinfections_by_time*avgDailyPopulation*avgDailyIncome)/time
	sdollars=int(sdollars)

	reekado=[scurrently_infect,sinfections_by_time,severeCasesByRequest,free_beds,casesForICUByRequest,
			casesForVentilatorsByRequest,sdollars]

	severeImpactDict=dict(zip(keylist,reekado))

# populating data dicts
	estimate["impact"]=impactDict
	estimate["severeImpact"]=severeImpactDict

	data["data"]=[x]
	data["estimated"]=estimate

	return data