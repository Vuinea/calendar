from flask import Blueprint, render_template, request, g, flash
from flask.helpers import url_for
from werkzeug.utils import redirect

from .auth import login_required

from .db import get_db

import datetime
from dateutil.relativedelta import relativedelta

from calendar import Calendar

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
    flash(f"Item '{title}' Added!")
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

@bp.route("/month-view", methods=['GET', 'POST'])
@login_required
def redirect_month_view():
  return redirect(url_for("calendar.month_view", month=today.month, year=today.year))
  

@bp.route("/month-view/<int:month>/<int:year>", methods=['GET', 'POST'])
@login_required
def month_view(month, year):
  
  db = get_db()

  months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December" 
  }

  days_of_week = [
    'Sun',
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
  ]

  cal = Calendar(firstweekday=6)

  # just putting 1 as a placeholder for the day
  cal_day = datetime.date(year=year, month=month, day=1)
  cal_month = month
  cal_year = year

  next_month = cal_day + relativedelta(months=1)
  prev_month = cal_day - relativedelta(months=1)
  
  next_month_url = url_for("calendar.month_view", month=next_month.month, year=next_month.year)
  prev_month_url = url_for("calendar.month_view", month=prev_month.month, year=prev_month.year)

  str_month = months[month]

  # getting the dates for the calendar and then getting the list for each day
  dates_in_month = cal.itermonthdates(year, month)

  items_in_month = {}

  for date in dates_in_month:
    date_items = db.execute('SELECT * FROM item WHERE author_id = ? AND due = ?', (g.user['id'], date)).fetchall()
    items_in_month[date] = date_items

  # getting the current day (Sunday, Monday, etc.)
  today = datetime.date.today()
  weekday_int = today.weekday()
  if weekday_int != 6:
    weekday_int += 1
  else:
    weekday_int = 0
  weekday_str = days_of_week[weekday_int]

  if request.method == 'POST':
    title = request.form['modal-add-title']
    body = request.form['modal-add-body']
    due = request.form["modal-add-due"]

    db.execute("INSERT INTO item (author_id, due, title, body) VALUES (?, ?, ?, ?)", (g.user['id'], due, title, body))
    db.commit()
    return redirect(url_for("calendar.month_view", month=month, year=year))
    


  return render_template("calendar/month_view.html", 
    today=today,
    days_of_week=days_of_week, 
    weekday_str=weekday_str,
    str_month=str_month,
    cal_month=month,
    cal_year=year,
    prev_month_url=prev_month_url,
    next_month_url=next_month_url,
    dates_in_month=cal.itermonthdates(year, month),
    items_in_month=items_in_month,
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


