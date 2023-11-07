from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
import os
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hellokaran'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_processing(filename, operation):
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            fileName = f"static/{filename}"
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(fileName, gray_image)
            return fileName
        case "cpng":
            fileName = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(fileName, img)
            return fileName
        case "cjpg":
            fileName = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(fileName, img)
            return fileName
        case "cjpeg":
            fileName = f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(fileName, img)
            return fileName
        case "acont":
            image = Image.open(f"uploads/{filename}")
            img = ImageOps.autocontrast(image, cutoff=7)
            img.save(f"static/{filename}")
            fileName = f"static/{filename}"
            return fileName
        case "posterized":
            image = Image.open(f"uploads/{filename}")
            img = ImageOps.posterize(image, bits=2)
            img.save(f"static/{filename}")
            fileName = f"static/{filename}"
            return fileName
        case "mirror":
            image = Image.open(f"uploads/{filename}")
            img = ImageOps.mirror(image)
            img.save(f"static/{filename}")
            fileName = f"static/{filename}"
            return fileName
        case "border":
            image = Image.open(f"uploads/{filename}")
            img = ImageOps.expand(image, border=20, fill=(255,255,255))
            img.save(f"static/{filename}")
            fileName = f"static/{filename}"
            return fileName
        case _:
            print("You do not have any access to the code")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template('home.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            operation = request.form.get("operation")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = image_processing(filename, operation)
            flash(f"Your Image has been edited successfully. You can view <a target='_blank' href='/{new}'>here<a>")
            return render_template('home.html')
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
