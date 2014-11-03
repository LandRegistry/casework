import logging
from flask import Blueprint, render_template

from flask_login import login_required
from application.cases import get_cases, complete_case


casework_blueprint = Blueprint('casework_blueprint', __name__, template_folder='../../frontend/templates')

@casework_blueprint.route('/casework', methods=['GET'])
@login_required
def get_casework():
    casework_items = get_cases('casework')
    return render_template("casework.html", casework_items=casework_items)

@casework_blueprint.route("/complete-case/<case_id>", methods=['POST'])
def complete_case_item(case_id):
    logging.info("POST complete-case:"+case_id)
    response = complete_case(case_id)
    if response.status_code == 200:
        return get_casework()
    else:
        return response
