from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for, session

from flask_cors import CORS

#import oracledb

import pandas as pd



app = Flask(__name__)
app.secret_key = "pollution_project"
users = {}

CORS(app)

#db = mysql.connector.connect(
 #   host="localhost",
  #  user="root",
   # password="aditri_1428",
    #database="pollution_db"
#=)
db=None


@app.route("/")
def home():
    return redirect(url_for("login"))
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")




@app.route("/data", methods=["POST"])

def receive_data():



    try:



        mq2 = int(request.form.get("mq2", 0))

        mq3 = int(request.form.get("mq3", 0))

        mq135 = int(request.form.get("mq135", 0))



        avg_sensor = (mq2 + mq3 + mq135) / 3

        aqi = int((avg_sensor / 4095.0) * 500)



        if aqi <= 50:

            status = "Good"

        elif aqi <= 100:

            status = "Satisfactory"

        elif aqi <= 200:

            status = "Moderate"

        elif aqi <= 300:

            status = "Poor"

        elif aqi <= 400:

            status = "Very Poor"

        else:

            status = "Severe"



        print("===================================")

        print("MQ2 :", mq2)

        print("MQ3 :", mq3)

        print("MQ135 :", mq135)

        print("AQI :", aqi)

        print("STATUS :", status)

        print("===================================")



        #cursor = db.cursor()



        #sql = """

        I#NSERT INTO sensor_data

        #(mq2, mq3, mq135, aqi_status)

        #VALUES (%s, %s, %s, %s)

        #"""



        #cursor.execute(

         #   sql,

          #  (mq2, mq3, mq135, status)

        #)



        #db.commit()



        return jsonify({

            "message": "Stored",

            "aqi": aqi,

            "status": status

        })



    except Exception as e:



        print("ERROR:", e)



        return jsonify({

            "error": str(e)

        }), 500




@app.route("/latest")
def latest():
    return {
        "mq2": 200,
        "mq3": 150,
        "mq135": 250,
        "aqi": 95,
        "status": "Satisfactory"
    }





@app.route("/history")

def history():



    try:



        cursor = db.cursor()



        cursor.execute("""

        SELECT *

        FROM sensor_data

        ORDER BY id DESC

        LIMIT 100

        """)



        rows = cursor.fetchall()



        result = []



        for row in rows:



            avg_sensor = (

                row[2] +

                row[3] +

                row[4]

            ) / 3



            aqi = int(

                (avg_sensor / 4095.0) * 500

            )



            result.append({



                "id": row[0],

                "time": str(row[1]),

                "mq2": row[2],

                "mq3": row[3],

                "mq135": row[4],

                "aqi": aqi,

                "status": row[5]



            })



        return jsonify(result)



    except Exception as e:



        return jsonify({

            "error": str(e)

        })





@app.route("/download_csv")

def download_csv():



    query = """

    SELECT *

    FROM sensor_data

    """



    df = pd.read_sql(

        query,

        db

    )



    csv_file = "sensor_data.csv"



    df.to_csv(

        csv_file,

        index=False

    )



    return send_file(

        csv_file,

        as_attachment=True

    )
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        session["user"] = email

        return redirect(url_for("dashboard"))

    return render_template("login.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        users[email] = password

        return redirect(url_for("login"))

    return render_template("signup.html")




if __name__ == "__main__":



    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )