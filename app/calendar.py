from flask import Blueprint, render_template

import datetime


bp = Blueprint("calendar", __name__)

@bp.route("/day-view")
def day_view():
  return render_template("calendar/day_view.html")
