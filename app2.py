import flask
import pandas as pd
import pickle
#import joblib
from flask import render_template
from flask_mysqldb import MySQL


#model = joblib.load(model, 'RandomForestRegressor.pkl')
#with open(f'RandomForestRegressor.joblib', 'rb') as f:
#   model = load(f)

app = flask.Flask(__name__, template_folder='templates')
model = pickle.load(open('RandomForestRegressor1.pkl','rb'))


# FLASK - MySQL DB connection
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'student_recruitment_system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)




#Saving data in CSV
def s_csv(TENTH,TWELTH,CGPA,GENDER,PROB,FULL_NAME,WORK_EXP):
        # Creating the first Dataframe using dictionary 
    df1 = pd.read_csv("walk_in_candidates2.csv")

        # Creating the Second Dataframe using dictionary 

    df2 = pd.DataFrame({"FULL_NAME":[FULL_NAME],
    "TENTH":[TENTH], 
    "TWELTH":[TWELTH], 
    "CGPA":[CGPA],
    "WORK_EXP":[WORK_EXP], 
    "GENDER":[GENDER],
    "Placement_Probability":[PROB]}) 
    
    dff2 = df1.append(df2, ignore_index = True)
    dff2.to_csv(r"walk_in_candidates2.csv", index = False)



@app.route('/', methods=['GET', 'POST'])
@app.route('/predictor2', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return (flask.render_template('predictor2.html'))

    if flask.request.method == 'POST':
        TENTH = flask.request.form['SSC']
        TWELTH = flask.request.form['HSC']
        CGPA = flask.request.form['CGPA']
        GENDER = flask.request.form['GENDER']
        FULL_NAME = flask.request.form['FULL_NAME']
        WORK_EXP = flask.request.form['WORK_EXP']


        input_variables = pd.DataFrame([[TENTH, TWELTH, CGPA, GENDER]],
                                       columns=['TENTH', 'TWELTH', 'CGPA', 'GENDER'],
                                       dtype='float',
                                       index=['input'])

        predictions = model.predict(input_variables)[0]
        print(predictions)

        PROB = predictions
        s_csv(TENTH,TWELTH,CGPA,GENDER,PROB,FULL_NAME,WORK_EXP)

        return flask.render_template('predictor2.html', original_input={'SSC marks': TENTH, 'HSC marks': TWELTH, 'CGPA': CGPA, 'GENDER': GENDER},
                                     result=predictions)



@app.route('/register', methods=['GET', 'POST'])
def register():

    cur  = mysql.connection.cursor()

    if flask.request.method == 'GET':
        return (flask.render_template('register.html'))

    if flask.request.method == 'POST':
        NAME1 = flask.request.form['FULL_NAME1']
        TENTH1 = flask.request.form['SSC1']
        TWELTH1 = flask.request.form['HSC1']
        CGPA1 = flask.request.form['CGPA1']
        GENDER1 = flask.request.form['GENDER1']
        WORK_EXP1 = flask.request.form['WORK_EXP1']
        DEPARTMENT1 = flask.request.form['DEPARTMENT1']
        SKILLS1 = flask.request.form['SKILLS1']

        #Insert into DB
        cur.execute('''INSERT INTO student_records VALUES ("'''+NAME1+'''", '''+TENTH1+''', '''+TWELTH1+''', '''+CGPA1+''', '''+GENDER1+''', "'''+DEPARTMENT1+'''", "'''+SKILLS1+'''")''')
        mysql.connection.commit()

        return flask.render_template('register.html', result1="Record added to Database")



@app.route('/static_predictor', methods=['GET', 'POST'])
def static_predictor():

    cur  = mysql.connection.cursor()

    if flask.request.method == 'GET':
        return (flask.render_template('static_predictor.html'))

    if flask.request.method == 'POST':
        DEPARTMENT = flask.request.form['DEPARTMENT']
        SKILLS = flask.request.form['SKILLS']

        print(DEPARTMENT , SKILLS)

        if (DEPARTMENT!='ALL' and SKILLS=='any'):
            cur.execute('''SELECT * FROM student_records WHERE DEPARTMENT LIKE "%'''+DEPARTMENT+'''%"''')
            results = cur.fetchall()
            print(results[0])

        elif (DEPARTMENT=='ALL' and SKILLS!='any'):
            cur.execute('''SELECT * FROM student_records WHERE SKILLS LIKE "%'''+SKILLS+'''%"''')
            results = cur.fetchall()
            print(results[0])

        elif (DEPARTMENT!='ALL' and SKILLS!='any'):
            cur.execute('''SELECT * FROM student_records WHERE SKILLS LIKE "%'''+SKILLS+'''%" AND DEPARTMENT LIKE "%'''+DEPARTMENT+'''%"''')
            results = cur.fetchall()
            print(results[0])

        else:
            cur.execute('''SELECT * FROM student_records''')
            results = cur.fetchall()
            print(results[0] , results[1])
    
        rdf = pd.DataFrame(results)
        rdf_pred = model.predict(rdf.drop(['NAME','DEPARTMENT','SKILLS'], axis=1))
        print(rdf_pred[0])
        rdf['PLACEMENT_PROBABILITY'] = rdf_pred
        rdf = rdf.sort_values(by = 'PLACEMENT_PROBABILITY' , ascending = False)
        rdf.reset_index(drop=True , inplace=True )
        print(rdf.head(5))


        return render_template('static_result.html',  tables=[rdf.to_html(classes='data')], titles=rdf.columns.values)
#        return render_template('static_result.html',  tables=[rdf.to_html(classes='data')], headers=rdf.columns.values)        

if __name__ == '__main__':
    app.run(debug=True)

