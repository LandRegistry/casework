import logging
from flask import Blueprint, render_template

from flask_login import login_required
from application.cases import get_cases


checks_blueprint = Blueprint('checks_blueprint', __name__, template_folder='../../frontend/templates')

@checks_blueprint.route('/checks', methods=['GET'])
@login_required
def get_checks():
    checks = get_cases('checks')
    logging.info("check_items:: %s" % checks)
    return render_template("checks.html", checks=checks)
