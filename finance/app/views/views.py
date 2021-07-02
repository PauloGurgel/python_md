from flask import Blueprint, jsonify

from app.read import read_services
from app.services import unit_of_work

main_views = Blueprint('main', __name__, url_prefix='/appointment/v1')


@main_views.route('/appointment', methods=['GET'])
def query_all_appointments():
    result = read_services.query_all_appointments(unit_of_work.SqlAlchemyUnitOfWork())
    return jsonify(result)


@main_views.route('/appointment/<appointment_id>', methods=['GET'])
def query_one_appointment(appointment_id):
    # dispatch the query
    result = read_services.query_one_appointment(appointment_id, unit_of_work.SqlAlchemyUnitOfWork())
    return jsonify(result)


