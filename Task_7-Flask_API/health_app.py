from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)


def db_conn():
    conn = None
    try:
        conn = sqlite3.connect("healthdata.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/")
def index():
    return "Hello World"


@app.route("/healthdata", methods=["GET", "POST"])
def healthdata():
    conn = db_conn()

    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("select * from healthdata")

        data = [
            dict(
                id=row[0],
                name=row[1],
                app_name=row[2],
                data=dict(
                    steps=row[3],
                    oxygen=row[4],
                    calories=row[5],
                    distance=row[6],
                ),
            )
            for row in cursor.fetchall()
        ]
        if data is not None:
            return jsonify(data)

    if request.method == "POST":
        new_name = request.form["name"]
        new_app_name = request.form["app_name"]
        new_steps = request.form["steps"]
        new_oxygen = request.form["oxygen"]
        new_calories = request.form["calories"]
        new_distance = request.form["distance"]

        sql = """insert into healthdata (name, app_name, steps, oxygen, calories, distance) values (?, ?, ?, ?, ?, ?)"""
        cursor = cursor.execute(
            sql,
            (new_name, new_app_name, new_steps, new_oxygen, new_calories, new_distance),
        )
        conn.commit()

    return f"Data with the id: {cursor.lastrowid} created successfully"


# @app.route("/healthdata/<int:id>", methods=["GET", "PUT", "DELETE"])
# def single_data(id):
#     if request.method == "GET":
#         for data in health_data:
#             if data["id"] == id:
#                 return jsonify(data)

#     if request.method == "PUT":
#         for data in health_data:
#             if data["id"] == id:
#                 data["name"] = request.form["name"]
#                 data["app_name"] = request.form["app_name"]
#                 data["steps"] = request.form["steps"]
#                 data["oxygen"] = request.form["oxygen"]
#                 data["calories"] = request.form["calories"]
#                 data["distance"] = request.form["distance"]

#                 update_data = {
#                     "id": id,
#                     "name": data["name"],
#                     "app_name": data["app_name"],
#                     "data": {
#                         "steps": data["steps"],
#                         "oxygen": data["oxygen"],
#                         "calories": data["calories"],
#                         "distance": data["distance"],
#                     },
#                 }
#                 return jsonify(update_data)

#     if request.method == "DELETE":
#         for index, data in enumerate(health_data):
#             if data["id"] == id:
#                 health_data.pop(index)
#                 return jsonify(health_data)


if __name__ == "__main__":
    app.run(debug=True)
