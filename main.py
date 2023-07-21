from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

# from medconnect.auth import login_required
from medconnect.db import get_db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html')