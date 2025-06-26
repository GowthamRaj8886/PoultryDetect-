from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
from werkzeug.utils import secure_filename
from flask import send_file

app = Flask(__name__)
model = load_model("Poultry_Disease.h5")
classes = ['Coccidiosis', 'Healthy', 'Salmonella', 'New Castle Disease']

medicine_dict = {
    'Coccidiosis': 'Amprolium or Toltrazuril',
    'Healthy': 'No medicine needed',
    'Salmonella': 'Enrofloxacin or Ciprofloxacin',
    'New Castle Disease': 'Supportive therapy, multivitamins, and control of secondary infections'
}
symptoms_dict = {
    'Coccidiosis': 'Bloody droppings, diarrhea, weight loss, ruffled feathers.',
    'Healthy': 'No visible symptoms. Active, eating and drinking normally.',
    'Salmonella': 'Diarrhea, dehydration, reduced appetite, weakness, sudden death in severe cases.',
    'New Castle Disease': 'Twisting of neck, difficulty breathing, drop in egg production, greenish diarrhea.'
}

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def predict(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    arr = image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    pred = model.predict(arr)[0]

    predicted_class = classes[np.argmax(pred)]
    confidence = round(float(np.max(pred)) * 100, 2)  # convert to percentage
    medicine = medicine_dict[predicted_class]
    symptoms = symptoms_dict[predicted_class]

    return predicted_class, confidence, medicine, symptoms


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(prediction, confidence, medicine, symptoms, img_path):
    pdf_path = os.path.join(UPLOAD_FOLDER, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "Poultry Disease Detection Report")

    c.setFont("Helvetica", 14)
    c.drawString(50, 710, f"Disease Prediction: {prediction}")
    c.drawString(50, 680, f"Confidence: {confidence}%")
    c.drawString(50, 650, f"Recommended Medicine: {medicine}")
    c.drawString(50, 620, "Common Symptoms:")
    text = c.beginText(70, 600)
    text.setFont("Helvetica", 12)
    text.textLines(symptoms)
    c.drawText(text)

    # Add image if possible
    try:
        c.drawImage(img_path, 50, 400, width=200, height=200)
    except:
        pass  # skip image if loading fails

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()
    return pdf_path
import csv

def log_research_data(prediction, confidence, medicine, symptoms, img_path):
    log_file = 'static/research_data.csv'
    file_exists = os.path.isfile(log_file)

    with open(log_file, 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Prediction', 'Confidence', 'Medicine', 'Symptoms', 'Image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Prediction': prediction,
            'Confidence': confidence,
            'Medicine': medicine,
            'Symptoms': symptoms,
            'Image': img_path
        })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/training')
def training():
    return render_template('training.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    predicted_class, confidence, medicine, symptoms = predict(path)

    pdf_path = generate_pdf(predicted_class, confidence, medicine, symptoms, path)

    log_research_data(predicted_class, confidence, medicine, symptoms, path)


    return render_template('result.html',
                       prediction=predicted_class,
                       confidence=confidence,
                       medicine=medicine,
                       symptoms=symptoms,
                       img_path=path,
                       pdf_path=pdf_path)

@app.route('/download_report')
def download_report():
    pdf_path = request.args.get('pdf_path')
    return send_file(pdf_path, as_attachment=True)

@app.route('/vet_resources')
def vet_resources():
    return render_template('vet_resources.html')

@app.route('/case_studies')
def case_studies():
    return render_template('case_studies.html')

@app.route('/treatment_guidelines')
def treatment_guidelines():
    return render_template('treatment_guidelines.html')

@app.route('/download_reports')
def download_reports():
    return render_template('download_reports.html')



if __name__ == '__main__':
    app.run(debug=True)
