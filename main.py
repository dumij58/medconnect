from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from markupsafe import escape
from datetime import datetime

from .helpers import login_required, admin_only
from .models import db, DoctorPreVal, Doctor

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html')