from main import app, db, Patient

with app.app_context():
    patients = Patient.query.all()
    for p in patients:
        print(p.id, p.name, p.email, p.password_hash)