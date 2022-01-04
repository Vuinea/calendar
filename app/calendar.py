from flask import Blueprint, render_template, session, request, g
from flask.helpers import url_for
from werkzeug.utils import redirect

from .db import get_db

import datetime


bp = Blueprint("calendar", __name__)

today = datetime.date.today()

month, day, year = today.month, today.day, today.year

@bp.route("/day-view")
def redirect_day_view():
  return redirect(url_for("calendar.day_view", month=today.month, day=today.day, year=today.year))

@bp.route("/day-view/<int:month>/<int:day>/<int:year>")
def day_view(month, day, year):

  months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ]

  cal_day = datetime.date(year=year, month=month, day=day)
  
  db = get_db()

  today_items = db.execute('SELECT * FROM item WHERE due = ? AND author_id = ?', (cal_day, g.user['id'])).fetchall()
  
  str_month = months[cal_day.month-1]

  return render_template("calendar/day_view.html", cal_day=cal_day, str_month=str_month)

