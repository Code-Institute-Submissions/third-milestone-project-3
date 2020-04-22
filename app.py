import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "appointment_scheduler"
app.config[
    "MONGO_URI"] = "mongodb+srv://philiph80:delrod123@myfirstcluster-yuvii.mongodb.net/appointment_scheduler?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
def index():
    today = datetime.now().strftime("%d/%m/%Y")
    doctor = "5e8f51b51c9d440000598471"
    appointments = mongo.db.appointments.find({"date": today})
    new_appointments = []
    for appointment in appointments:
        if len(appointment["appointment_list"]) != 0:
            test = next((item for item in appointment["appointment_list"] if item["doctor_id"] == doctor), None)
            if test != None:
                patient = mongo.db.patients.find_one({"_id": ObjectId(test["patient_id"])})
                new_appointments.append(
                    {"id": appointment["_id"], "time": appointment["time"], "patient": patient, "empty": False})
            else:
                new_appointments.append({"id": appointment["_id"], "time": appointment["time"], "empty": True})
        else:
            new_appointments.append({"id": appointment["_id"], "time": appointment["time"], "empty": True})

    return render_template("index.html", slots=new_appointments)


@app.route('/addAppointment/<appointmentId>/<time>', methods=["POST", "GET"])
def addAppointment(time, appointmentId):
    doctor = "5e8f51b51c9d440000598471"
    patients = mongo.db.patients.find({"doctor_id": doctor})
    return render_template("addAppointment.html", time=time, appointmentId=appointmentId, patients=patients)


@app.route("/updateAppointment")
def update_appointment():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
