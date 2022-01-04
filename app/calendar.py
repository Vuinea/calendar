from flask import Blueprint, render_template, session, request, g, flash
from flask.helpers import url_for
from werkzeug.utils import redirect

from .auth import login, login_required

from .db import get_db

import datetime
from dateutil.relativedelta import relativedelta

bp = Blueprint("calendar", __name__)

today = datetime.date.today()

month, day, year = today.month, today.day, today.year

@bp.route("/day-view")
@login_required
def redirect_day_view():
  return redirect(url_for("calendar.day_view", month=today.month, day=today.day, year=today.year))

@bp.route("/day-view/<int:month>/<int:day>/<int:year>", methods=['GET', 'POST'])
@login_required
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

  today = datetime.date.today()
  

  cal_day = datetime.date(year=year, month=month, day=day)
  
  cal_tommorow = cal_day + relativedelta(days=1)
  cal_yesterday = cal_day - relativedelta(days=1)

  tommorow_url = url_for("calendar.day_view", month=cal_tommorow.month, day=cal_tommorow.day, year=cal_tommorow.year)
  yesterday_url = url_for("calendar.day_view", month=cal_yesterday.month, day=cal_yesterday.day, year=cal_yesterday.year)

  db = get_db()

  today_items = db.execute('SELECT * FROM item WHERE due = ? AND author_id = ?', (cal_day, g.user['id'])).fetchall()

  str_month = months[cal_day.month-1]

  if request.method == 'POST':
    title = request.form.get('add-title')
    body = request.form.get("add-body")
    due = request.form.get("add-due")

    db.execute("INSERT INTO item (title, body, due, author_id) VALUES (?, ?, ?, ?)", (title, body, due, g.user['id']))
    db.commit()
    flash(f"Item {title} Added!")
    return redirect(url_for("calendar.day_view", day=cal_day.day, month=cal_day.month, year=cal_day.year))
  
  
  return render_template(
    "calendar/day_view.html", 
    cal_day=cal_day, 
    str_month=str_month, 
    today=today,
    tommorow_url=tommorow_url,
    yesterday_url=yesterday_url,
    today_items=today_items,

  )



@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_item(id):
  db = get_db()
  item = db.execute("SELECT * FROM item WHERE id = ?", (id,)).fetchone()
  if item['author_id'] == g.user['id']:
    db.execute('DELETE FROM item WHERE id = ?', (id,))
    db.commit()
    flash(f"item {item['title']} was deleted successfully!")
  else:
    flash("You cannot remove this item")
  return redirect(url_for("calendar.redirect_day_view"))


