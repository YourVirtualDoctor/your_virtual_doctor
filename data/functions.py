from urllib2 import urlopen
import json
from googlemaps.client import Client
from googlemaps.places import places_nearby 
from googlemaps.distance_matrix import distance_matrix
import wikipedia
import pandas as pd
from random import randint
sd=pd.ExcelFile("sym_dis_matrix.xlsx")
df=sd.parse(sd.sheet_names[0])
d=df.columns[1:]
symtoms=[]
diseases=[]
sdmatrix=[]
for i in range(109):
	diseases.append(d[i])
sdmatrix=df.reset_index()[df.columns].values.tolist()
for i in range(len(sdmatrix)):
	symtoms.append(sdmatrix[i].pop(0))
sd=pd.ExcelFile("dia_3.xlsx")
df=sd.parse(sd.sheet_names[0])
ids=df["_id"]
text=df["diagnose"]
diseasenames=[]
for i in range(109):
	n=" ".join(text[i].split("\x0b"))
	diseasenames.append(n.lower())
print len(diseasenames)
sd=pd.ExcelFile("sym_3.xlsx")
df=sd.parse(sd.sheet_names[0])
ids=df["_id"]
text=df["symptom"]
symptomnames=[]
for i in range(131):
	symptomnames.append(text[i].lower())
#print diseasenames
#print symptomnames
for i in range(len(sdmatrix)):
	for j in range(len(sdmatrix[i])):
		if(sdmatrix[i][j]==0):
			sdmatrix[i][j]=1
		else:
			sdmatrix[i][j]*=sdmatrix[i][j]
#print sdmatrix
sdmatrix=sdmatrix[:109]
def find_nextquestion(questions):
	prevquestions=[]
	regectedquestions=[]
	for key in questions.keys():
		if questions[key]=="yes":
			prevquestions.append(symptomnames.index(key))
		else:
			regectedquestions.append(symptomnames.index(key))
	values=[]
	indexes=[]
	for i in range(len(sdmatrix)):
		if(i not in prevquestions and i not in regectedquestions):
			indexes.append(i)
	for i in range(len(indexes)):
		values.append(0.0)
	prevalues=range(len(prevquestions))
	for i in range(len(prevquestions)):
		prevalues[i]=0.0
	for i in range(len(sdmatrix)):
		for j in range(len(prevalues)):
			prevalues[j]+=sdmatrix[i][prevquestions[j]]
	#print prevalues
	for i in range(len(prevalues)):
		prevalues[i]=prevalues[i]/(len(sdmatrix))
	minvalue=min(prevalues)
	#print "minvalue",minvalue
	if(minvalue<1.0):
		return -1
	else:
		for i in range(len(sdmatrix)):
			#print check_row(prevquestions,minvalue,sdmatrix[i]),"check"
			if(check_row(prevquestions,minvalue,sdmatrix[i])==len(prevquestions)):
				for j  in range(len(indexes)):
					#print i,j
					values[j]+=sdmatrix[i][indexes[j]]
	maxvalue=max(values)
	#print values
	#print indexes
	return symptomnames[indexes[values.index(maxvalue)]]
def check_row(prevquestions,minvalue,row):
	val=0
	for i in range(len(prevquestions)):
		if(row[prevquestions[i]]>=minvalue):
			val+=1
	return val
def find_disease(questions):
	symptoms=[]
	for key in questions.keys():
		if(questions[key]=="yes"):
			symptoms.append(symptomnames.index(key))
	values=[]
	for row in sdmatrix:
		val=1
		for j in symptoms:
			val=val*row[j]
		values.append(val)
	#print values
	return diseasenames[values.index(max(values))]
#send_email("madadi.8@wright.edu","Sindhu94","sindhu.bhargavi009@gail.com","Nothing","body")
def survey():
	print "Answer the following questions"
	print "1:yes 0:No"
	regectedquestions=[]
	prevquestions=[randint(0,100)]
	while len(prevquestions)<4:
		nextquestion= find_nextquestion(prevquestions,regectedquestions)
		#print nextquestion
		#print len(symptomnames)
		print symptomnames[nextquestion]
		c=input()
		if(c==1):
			prevquestions.append(nextquestion)
		else:
			regectedquestions.append(nextquestion)
			continue
	disease=find_disease(prevquestions)
	print "The diagised disease based on the questions is ",diseasenames[disease]
def summary(disease):
	return wikipedia.summary(disease,sentences=3)
def getlocation():
	url = 'http://ipinfo.io/json'
	response = urlopen(url)
	data = json.load(response)
	return map(float,data['loc'].split(','))
client=Client(key='AIzaSyCI3v6QCJQGStSjCIsIntZht_9gfSdism4')
client2=Client(key="AIzaSyA33TOQQggSGj--2pKHiEK2X996VyjG8h8")
def gethospitals():
	places=places_nearby(client,getlocation(),keyword="Hospitals near me",open_now=True,rank_by='distance',type="hospital")
	hospitals=[]
	for hospital in places['results']:
		name=hospital['name']
		if not 'Vetenary' in name:
			if not "Critical" in name:
				if not "Neuro" in name:

					hospitals.append(name)
	#return hospitals
	hospitaldistances={}
	for name in hospitals:
		hospitaldistances[name]=distance_matrix(client2,[tuple(getlocation())],name)['rows'][0]['elements'][0]['distance']['text']
	return hospitaldistances
#survey()
