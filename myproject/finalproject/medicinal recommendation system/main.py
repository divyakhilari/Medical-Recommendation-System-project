from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
import numpy as np
import pandas as pd
import pickle
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

# flask app
app = Flask(__name__)
app.secret_key = "your-secret-key"   # change to random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Example%402025%23@localhost/patientdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Link to recommendations
    recommendations = db.relationship("Recommendation", backref="patient", lazy=True, cascade="all, delete-orphan")


class Recommendation(db.Model):
    __tablename__ = "recommendation"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    disease = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # relationships to child tables
    description = db.relationship("Description", backref="recommendation", lazy=True, cascade="all, delete-orphan")
    precautions = db.relationship("Precaution", backref="recommendation", lazy=True, cascade="all, delete-orphan")
    medications = db.relationship("Medication", backref="recommendation", lazy=True, cascade="all, delete-orphan")
    workouts = db.relationship("Workout", backref="recommendation", lazy=True, cascade="all, delete-orphan")
    diets = db.relationship("Diet", backref="recommendation", lazy=True, cascade="all, delete-orphan")


class Description(db.Model):
    __tablename__ = "description"
    id = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey("recommendation.id"), nullable=False)
    # detail = db.Column(db.String(500), nullable=False)
    detail = db.Column(db.Text, nullable=False)


class Precaution(db.Model):
    __tablename__ = "precaution"
    id = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey("recommendation.id"), nullable=False)
    precaution = db.Column(db.Text, nullable=False)

    # precaution = db.Column(db.Text, nullable=False)


class Medication(db.Model):
    __tablename__ = "medication"
    id = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey("recommendation.id"), nullable=False)
    # detail = db.Column(db.String(200), nullable=False)
    medication = db.Column(db.Text, nullable=False)

    # medication = db.Column(db.Text, nullable=False)


class Workout(db.Model):
    __tablename__ = "workout"
    id = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey("recommendation.id"), nullable=False)
    # detail = db.Column(db.String(200), nullable=False)
    workout = db.Column(db.Text, nullable=False)

    # workout = db.Column(db.Text, nullable=False)


class Diet(db.Model):
    __tablename__ = "diet"
    id = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey("recommendation.id"), nullable=False)
    # detail = db.Column(db.String(200), nullable=False)
    diet = db.Column(db.Text, nullable=False)



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# load databasedataset===================================
sym_des = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv('datasets/medications.csv')
diets = pd.read_csv("datasets/diets.csv")


# load model===========================================
svc = pickle.load(open('models/svc.pkl','rb'))
#============================================================

with app.app_context():
    db.create_all()
# custome and helping functions
#==========================helper funtions ==takes the predicted disease as input and fetches all related recommendations ================
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis] ['workout']
    return desc,pre,med,die,wrkout

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

# ------------------------ ADDED: confidence computation ------------------------
def compute_confidence(patient_symptoms):
    """
    Returns confidence percentage (float) for the top prediction.
    Uses predict_proba if available; otherwise falls back to decision_function.
    """
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1

    # Preferred: probability from SVC if trained with probability=True
    if hasattr(svc, "predict_proba"):
        try:
            proba = svc.predict_proba([input_vector])[0]
            confidence = float(np.max(proba) * 100.0)
            return round(confidence, 1)
        except Exception:
            pass

    # Fallback: use decision_function -> softmax/sigmoid for confidence-like score
    if hasattr(svc, "decision_function"):
        df = svc.decision_function([input_vector])[0]
        # Binary case: df is scalar -> convert via sigmoid
        if np.isscalar(df):
            p = 1.0 / (1.0 + np.exp(-df))
            confidence = max(p, 1.0 - p) * 100.0
            return round(float(confidence), 1)
        else:
            # Multiclass: apply softmax over decision scores
            df = np.array(df, dtype=float)
            # numerical stability
            df = df - np.max(df)
            exp_df = np.exp(df)
            softmax = exp_df / np.sum(exp_df)
            confidence = float(np.max(softmax) * 100.0)
            return round(confidence, 1)

    # If neither method available, return None to avoid UI confusion
    return None
# ------------------------------------------------------------------------------

# creating routes========================================
@app.route("/")
def index():
    # If not logged in, redirect to login page
    if "patient_id" not in session:
        return redirect(url_for("login"))
    # If logged in, show home page

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        birth_date = request.form["birth_date"]
        blood_group = request.form["blood_group"]
        address = request.form["address"]
        phone = request.form["phone"]
        location = request.form["location"]
        email = request.form["email"]
        password = request.form["password"]

        # Calculate age from birth_date
        birth_date_obj = date.fromisoformat(birth_date)
        today = date.today()
        age = today.year - birth_date_obj.year - (
            (today.month, today.day) < (birth_date_obj.month, birth_date_obj.day)
        )

        # ✅ Use Patient.set_password() instead of manual hashing
        new_patient = Patient(
            name=name,
            gender=gender,
            birth_date=birth_date_obj,
            age=age,
            blood_group=blood_group,
            address=address,
            phone=phone,
            location=location,
            email=email
        )
        new_patient.set_password(password)   # <-- this hashes and stores password

        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for("show_patients"))  # redirect to patient list

    return render_template("register.html")




# end

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]

        patient = Patient.query.filter_by(email=email).first()
        if patient and patient.check_password(password):
            session["patient_id"] = patient.id
            session["patient_name"] = patient.name
            flash("Welcome back!", "success")
            return redirect(url_for("index"))   # ✅ go to home after login
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

@app.route("/patients")
def show_patients():
    patients = Patient.query.all()   # fetch all patients from DB
    return render_template("patients.html", patients=patients)





@app.route("/recommendations")
def list_recommendations():
    patient_id = session.get("patient_id")
    if not patient_id:
        flash("You must be logged in to view recommendations.", "danger")
        return redirect(url_for("login"))

    recs = Recommendation.query.filter_by(patient_id=patient_id).order_by(Recommendation.created_at.desc()).all()
    return render_template("recommendations.html", recs=recs)


# List recommendations for a specific patient
@app.route("/patients/<int:patient_id>/recommendations")
def patient_recommendations(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    recs = Recommendation.query.filter_by(patient_id=patient.id).order_by(Recommendation.created_at.desc()).all()
    return render_template("patient_recommendations.html", patient=patient, recs=recs)

# Create a new recommendation: GET shows form, POST saves
@app.route("/patients/<int:patient_id>/recommendations/new", methods=["GET", "POST"])
def new_recommendation(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        disease = request.form.get("disease", "").strip()

        desc_text = request.form.get("description", "").strip()
        precautions_text = request.form.getlist("precautions")  # supports multiple entries
        medications_text = request.form.getlist("medications")
        workouts_text = request.form.getlist("workout")
        diets_text = request.form.getlist("diet")

        if not disease or not desc_text:
            flash("Disease and Description are required.", "warning")
            return redirect(url_for("new_recommendation", patient_id=patient_id))

        # Create Recommendation
        rec = Recommendation(patient_id=patient.id, disease=disease)
        db.session.add(rec)
        db.session.flush()  # get rec.id before committing

        # Add normalized child records
        db.session.add(Description(recommendation_id=rec.id, detail=desc_text))

        for t in precautions_text:
            t = (t or "").strip()
            if t:
                db.session.add(Precaution(recommendation_id=rec.id, precaution=t))

        for t in medications_text:
            t = (t or "").strip()
            if t:
                db.session.add(Medication(recommendation_id=rec.id, medication=t))

        for t in workouts_text:
            t = (t or "").strip()
            if t:
                db.session.add(Workout(recommendation_id=rec.id, workout=t))

        for t in diets_text:
            t = (t or "").strip()
            if t:
                db.session.add(Diet(recommendation_id=rec.id, diet=t))

        db.session.commit()
        flash("Recommendation created successfully.", "success")
        return redirect(url_for("patient_recommendations", patient_id=patient.id))

    return render_template("new_recommendation.html", patient=patient)

# Optional: simple join view for teacher demo (read-only)
@app.route("/recommendations/join")
def recommendations_join_view():
    # Show flattened view: patient name + all attributes
    recs = Recommendation.query.order_by(Recommendation.created_at.desc()).all()
    return render_template("recommendations_join.html", recs=recs)

@app.route("/dashboard")
def dashboard():
    if "patient_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", name=session["patient_name"])

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))



@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("q")  # get search term from URL
    if query:
        # Example: search patients by name or email
        results = Patient.query.filter(
            (Patient.name.ilike(f"%{query}%")) | (Patient.email.ilike(f"%{query}%"))
        ).all()
        return render_template("search_results.html", results=results, query=query)
    else:
        flash("Please enter a search term.", "warning")
        return redirect(url_for("index"))



    ###





@app.route('/predict', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        print(symptoms)

        if symptoms == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms"
            return render_template('index.html', message=message)
        else:
            # Split the user's input into a list of symptoms (assuming they are comma-separated)
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            # Remove any extra characters, if any
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]

            predicted_disease = get_predicted_value(user_symptoms)
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            # Convert precautions to a flat list
            my_precautions = [i for i in precautions[0]]

            # ------------------------ ADDED: compute and pass confidence ------------------------
            confidence_percent = compute_confidence(user_symptoms)
            # ------------------------------------------------------------------------------------

            # -------------------- NEW: Save recommendation in DB --------------------
            patient_id = session.get("patient_id")  # patient must be logged in
            if patient_id:
                # Save recommendation
                new_reco = Recommendation(patient_id=patient_id, disease=predicted_disease)
                db.session.add(new_reco)
                db.session.commit()

                # ✅ Cleaning function
                def clean_list(values):
                    return [str(v) for v in values if v is not None and str(v).lower() != "nan"]

                # ✅ Clean all lists before inserting
                my_precautions = clean_list(my_precautions)
                medications = clean_list(medications)
                rec_diet = clean_list(rec_diet)
                workout = clean_list(workout)

                # Save child details
                new_desc = Description(recommendation_id=new_reco.id, detail=dis_des)
                db.session.add(new_desc)

                for precaution in my_precautions:
                    db.session.add(Precaution(recommendation_id=new_reco.id, precaution=precaution))

                for med in medications:
                    db.session.add(Medication(recommendation_id=new_reco.id, medication=med))

                for diet in rec_diet:
                    db.session.add(Diet(recommendation_id=new_reco.id, diet=diet))

                for work in workout:
                    db.session.add(Workout(recommendation_id=new_reco.id, workout=work))

                db.session.commit()
            # -----------------------------------------------------------------------

            return render_template(
                'index.html',
                predicted_disease=predicted_disease,
                dis_des=dis_des,
                my_precautions=my_precautions,
                medications=medications,
                my_diet=rec_diet,
                workout=workout,
                confidence_percent=confidence_percent  # ADDED
            )

    return render_template('index.html')

# about view funtion and path
@app.route('/about')
def about():
    return render_template("about.html")
# contact view funtion and path
@app.route('/contact')
def contact():
    return render_template("contact.html")

# developer view funtion and path
@app.route('/developer')
def developer():
    return render_template("developer.html")

# about view funtion and path
@app.route('/blog')
def blog():
    return render_template("blog.html")

with app.app_context():
    db.create_all()

if __name__ == '__main__':

    app.run(debug=True, port=5001)