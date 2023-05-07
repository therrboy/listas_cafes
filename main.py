from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap(app)


class CafeForm(FlaskForm):
    cafeName = StringField(label='Cafe name', validators=[DataRequired()])
    cafeLocation = StringField(label='Cafe Location on Google Maps (URL)',
                               validators=[DataRequired(), URL()])
    cafeOpening = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    cafeClose = StringField(label='Closing Time e.g. 8PM', validators=[DataRequired()])
    cafeRating = SelectField(label='Cafe rating', choices=[('1', "☕️"), ('2', "☕️☕️"), ('3', "☕️☕️☕️"),
                                                           ('4', "☕️☕️☕️☕️"), ('5', "☕️☕️☕️☕️☕️")],
                             render_kw={"class": "options"}, validators=[DataRequired()])

    cafeWifi = SelectField(label='Wifi Strength Rating', choices=[('1', "✘"), ('2', "💪"), ('3', "💪💪"),
                                                                  ('4', "💪💪💪"), ('5', "💪💪💪💪"), ('6', "💪💪💪💪💪")],
                           render_kw={"class": "options"}, validators=[DataRequired()])

    cafePowerSocket = SelectField(label='Power Socket Availability', choices=[('1', "✘"), ('2', "🔌"), ('3', "🔌🔌"),
                                                                              ('4', "🔌🔌🔌"), ('5', "🔌🔌🔌🔌"),
                                                                              ('6', "🔌🔌🔌🔌🔌")],
                                  render_kw={"class": "options"}, validators=[DataRequired()])

    submit = SubmitField(label='Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():

    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafeName.data
        cafe_location = form.cafeLocation.data
        cafe_opening = form.cafeOpening.data
        cafe_close = form.cafeClose.data
        cafe_rating = form.cafeRating.data

        cafe_wifi = int(form.cafeWifi.data)
        if cafe_wifi == 1:
            cafe_wifi = "✘"
        else:
            cafe_wifi = (cafe_wifi - 1) * "💪"

        cafe_power_socket = int(form.cafePowerSocket.data)
        if cafe_power_socket == 1:
            cafe_power_socket = "✘"
        else:
            cafe_power_socket = (cafe_power_socket - 1) * "🔌"

        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([cafe_name, cafe_location, cafe_opening, cafe_close, cafe_rating, cafe_wifi, cafe_power_socket])
            return redirect("/cafes")

    return render_template("add.html", form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
