from flask import Flask, request, render_template
import pytesseract
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Ty Martz\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract_text", methods=["POST"])
def extract_text():
    # Check if an image was uploaded
    if "image" not in request.files:
        return "No image file was uploaded."

    image = request.files["image"]

    # Convert the uploaded image to a PIL Image
    image = Image.open(image).convert("L")

    # Perform OCR on the image
    img_data = pytesseract.image_to_data(image, lang='eng',
                                                    config='--psm 11',
                                                    output_type='dict')
    #print(tc.keys())
    text = pytesseract.image_to_string(image, lang='eng',
                                                    config='--psm 11',
                                                    output_type='dict')

    # Get the confidence scores
    confidence_scores = img_data['conf']
    confs = round(np.mean([x for x in confidence_scores if x != -1]), 2)

    # Normalize the confidence scores to values between 0 and 1
    #confidence_scores = (confidence_scores - np.min(confidence_scores)) / (np.max(confidence_scores) - np.min(confidence_scores))

    # Generate a color map based on the confidence scores
    #color_map = (1 - confidence_scores) * np.array([255, 0, 0]) + confidence_scores * np.array([0, 255, 0])

    return render_template("extract_text.html", text=text['text'], #color_map=color_map, 
    conf=confs)

if __name__ == "__main__":
    app.run(debug=True)
