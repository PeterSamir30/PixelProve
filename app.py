from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Static/uploads'

# Load models
model_ai = load_model('Models/AI_Image_Detector.h5')
model_deepfake = load_model('Models/DeepFake_best_model_inception.h5')

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def prepare_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict_ai', methods=['POST'])
def predict_ai():
    if 'image' not in request.files:
        return render_template('error.html', message='No image file uploaded.')
    file = request.files['image']
    if file.filename == '':
        return render_template('error.html', message='No image file selected.')
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            img = prepare_image(filepath)
            prediction = model_ai.predict(img)[0][0]
            label = "Real" if prediction > 0.5 else "Fake"
            confidence = prediction * \
                100 if prediction > 0.5 else (1 - prediction) * 100
            result = f"{label} ({confidence:.2f}% confident)"
            return render_template('result.html', filename=filename, result=result, model_name="AI Image Detector")
        except Exception as e:
            return render_template('error.html', message=f'Error during AI model prediction: {e}')

    return render_template('error.html', message='An error occurred during file upload.')


@app.route('/predict_deepfake', methods=['POST'])
def predict_deepfake():
    if 'image' not in request.files:
        return render_template('error.html', message='No image file uploaded.')
    file = request.files['image']
    if file.filename == '':
        return render_template('error.html', message='No image file selected.')
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            img = prepare_image(filepath)
            prediction = model_deepfake.predict(img)[0][0]
            label = "Real" if prediction > 0.5 else "Fake"
            confidence = prediction * \
                100 if prediction > 0.5 else (1 - prediction) * 100
            result = f"{label} ({confidence:.2f}% confident)"
            return render_template('result.html', filename=filename, result=result, model_name="DeepFake Face Detector")
        except Exception as e:
            return render_template('error.html', message=f'Error during DeepFake model prediction: {e}')

    return render_template('error.html', message='An error occurred during file upload.')


@app.route('/error')
def error(message):
    return render_template('error.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
