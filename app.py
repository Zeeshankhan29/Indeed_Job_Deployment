from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/Job',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        data = request.form.items()

        data = dict(data)
        position = str(data['position'])
        location = str(data['location'])
        No_of_pages = int(data['No_of_pages'])


        reviews = []

        for i in range(1, No_of_pages + 1, 1):
            template = "https://in.indeed.com/jobs?q="+position+"&l="+location+"&start="+str(i)+"0&vjk=6cad8762e70bc5c1"
            url = template
            page = requests.get(url)
            indeed_html = bs(page.text, 'html.parser')
            boxes = indeed_html.findAll('div', 'job_seen_beacon')

            for i in range(30):
                try:
                    Job_title = boxes[i].find('h2', "jobTitle").text
                except:
                    Job_title = 'No Title Name'
                try:
                    Company_name = boxes[i].find('span', {'class': "companyName"}).text
                except:
                    Company_name = 'No Company Name'
                try:
                    Job_location = boxes[i].find('div', {'class': "companyLocation"}).text
                except:
                    Job_location = 'No location Name'
                try:
                    Job_description = boxes[i].find('div', {'class': "job-snippet"}).text.strip()
                except:
                    Job_description = "No description"
                try:
                    Job_posted_date = boxes[i].find('span', {'class': "date"}).text
                except:
                    Job_posted_date = 'No date'

                mydict = ({"JOB_TITLE": Job_title, "COMPANY_NAME": Company_name,'JOB_LOCATION': Job_location, 'JOB_DESCRIPTION': Job_description,
                           "JOB_POSTED_DATE": Job_posted_date})
                reviews.append(mydict)
                # print(reviews)

        df = pd.DataFrame(reviews)
        columns = ['JOB_TITLE', 'COMPANY_NAME', 'JOB_LOCATION', 'JOB_DESCRIPTION', 'JOB_POSTED_DATE']
        reviews1 = [[df.loc[i, col] for col in df.columns] for i in range(len(df))]
        return render_template('results.html', titles=columns, rows=reviews1)

        # except Exception as e:
        #     print('The Exception message is: ',e)
        #     return 'something is wrong'

    else:
        return render_template('index.html')

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)
