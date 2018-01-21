# -------------imports for flask------------------------------
from flask import Flask
from flask import redirect, flash, render_template, request, session, abort

# -------------imports for flask SQL------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from data.functions import *

engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)

# this is required to use sqllite database
app.secret_key = "sampath"


symptoms = {}
questions = []

# ----------------- Home Page ----------------------------------
'''
using sessions to remember whether a user is logged in or not. 
'''
@app.route('/')
@app.route('/index')
def index():
    '''
    input : This is the home page
    output: either directs to the login page or the main page
    functionality: if the user is not logged in, he will go to login page
		   else he goes to the main page
    '''
    if not session.get('logged_in'):
	# login_page
        return render_template('login.html') 
    else:
	# created a user dictionary to be used at html side
	 location = getlocation()
	 session['latitude'] = str(location[0])
	 session['longitude'] = str(location[1])
	 user  = {"name": session['name'], "email":session['email'], "birthday":session['birthday'], "latitude": session['latitude'], "longitude" : session['longitude']   }
	 hospitals = gethospitals()
         if questions and symptoms:
		 return render_template('profile.html' , user=user, questions=questions, symptoms = symptoms,hospitals = hospitals )
	 else:
	 	return render_template('profile.html' , user=user ,hospitals = hospitals) 

# ----------------- Logout Page ----------------------------------
@app.route("/logout")
def logout():
    '''
    input : logout url
    output: directs to the main page
    functionality: makes you logut of the page
    '''
    symptoms = {}
    session['logged_in'] = False
    return index()

# ----------------- After Login Page ----------------------------------
@app.route('/login', methods=['POST'])
def login():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.email.in_([request.form['email']]), User.password.in_([request.form['password']]) )
    result = query.first()
    if result:
	session['logged_in'] = True
    	session['name'] =  result.username
    	session['email'] =  result.email
    	session['birthday'] =  result.birthday
    	session['latitude'] = "42.7282084"
	session['longitude'] = "-84.48165440000001"
        return index()
	
    else:
        return signup_form() 


# ----------------- Signup Form ----------------------------------
@app.route('/signup_form')
def signup_form():
    # sign_up form
    return render_template('signup.html')

# ----------------- Signup Form ----------------------------------
@app.route('/signup' , methods=['POST'])
def signup():
    # sign_up form
    user = User(request.form['name'],request.form['birthday'],request.form['email'],request.form['password'] )
    Session = sessionmaker(bind=engine)
    s = Session()
    s.add(user)
    session['logged_in'] = True
    session['name'] =  result.username
    session['email'] =  result.email
    session['birthday'] =  result.birthday
    session['latitude'] = "42.7282084"
    session['longitude'] = "-84.48165440000001"
    s.commit()
    s.commit()
    return index()

# ----------------- Symptom Form ----------------------------------

def get_symptom_question(question):
       #words = question.split(" ")
       return question.strip("?")


@app.route('/symptom' , methods=['POST'])
def symptom():
   if not session.get('logged_in'):
	# login_page
        return render_template('login.html') 
   else:
	 questions = ["headache"]
         user  = {"name": session['name'], "email":session['email'], "birthday":session['birthday'], "latitude": session['latitude'], "longitude" : session['longitude']}
	 symptom = get_symptom_question(request.form['symptom'])
	 if (request.form['action'] == "Submit"):
		for i in symptomnames:
			if symptom in i:
				symptoms[i] = "yes"
				questions[0]=find_nextquestion(symptoms)
				break
	 elif (request.form['action'] == "Yes"):
	 	symptoms[symptom] = "yes"
		questions[0]=find_nextquestion(symptoms)

	 elif (request.form['action'] == "No"):
	 	symptoms[symptom] = "no"
		questions[0]=find_nextquestion(symptoms)
         else:
		pass
	 count = 0
	 disease = "null"
	 description = None
	 for each in symptoms:
		if symptoms[each] == "yes":
			count = count + 1
			if count >= 3:
				disease = find_disease(symptoms)
                                # wikipedia
				try:
	 				description = summary(disease.split(" ")[0])
				except:
					description = "Wikipedia Doesnt Have information on this"
				break
	 hospitals = gethospitals()
	 print hospitals
         return render_template('profile.html' , user=user, questions=questions, symptoms = symptoms, disease= disease, description = description, hospitals = hospitals) 



@app.route('/remove' , methods=['POST'])
def remove():
   if not session.get('logged_in'):
	# login_page
        return render_template('login.html') 
   else:

         user  = {"name": session['name'], "email":session['email'], "birthday":session['birthday'], "latitude": session['latitude'], "longitude" : session['longitude']}
	 symptom = get_symptom_question(request.form['action'])
	 symptoms[symptom] = "no"
	 questions[0]=find_nextquestion(symptoms)
         return render_template('profile.html' , user=user, questions=questions, symptoms = symptoms ) 

@app.route('/clear' , methods=['POST'])
def clear():
   if not session.get('logged_in'):
	# login_page
        return render_template('login.html') 
   else:
	 global questions
	 global symptoms
	 questions[:] = []
 	 symptoms = {}
         return index()

# --------------------- Testing the Database -------------------------------
@app.route('/test')
def test():
 
    POST_USERNAME = "python"
    POST_PASSWORD = "python"
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
	print(result.username)
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD




if __name__ == "__main__":
    app.run()
