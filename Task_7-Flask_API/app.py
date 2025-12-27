import os
import cv2
from flask import Flask, request, jsonify, send_from_directory, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "images"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/images/<filename>")
def img_url(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    img = cv2.imread(file_path)
    rotate = cv2.rotate(img, cv2.ROTATE_180)
    _, buffer = cv2.imencode(".jpg", rotate)
    return Response(buffer.tobytes(), mimetype="image/jpeg")


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

    def to_dict(self):
        img_url = None

        if self.filename:
            img_url = url_for("img_url", filename=self.filename, _external=True)
            print(img_url)

        return {
            "id": self.id,
            "filename": img_url,
        }


def allowed_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/image", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["filename"]
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)

            file_bytes = file.read()
            file.seek(0)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            upload = Upload(filename=filename, data=file_bytes)
            db.session.add(upload)
            db.session.commit()

            return jsonify({"message": f"uploaded : {filename}"}), 201

    if request.method == "GET":
        uploads = Upload.query.all()
        data = [upload.to_dict() for upload in uploads]
        return jsonify(data)
