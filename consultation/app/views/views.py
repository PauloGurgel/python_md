from flask import Blueprint, request, url_for, redirect, jsonify

from app.read import read_services
from app.services import unit_of_work, services
from app.utils.date_utils import parse_date

main_views = Blueprint('main', __name__, url_prefix='/consultation/v1')


# Using only get/post semantics because I'm not doing a RestFul approach. Instead I'm using Command/Event/Query pattern

@main_views.route('/create', methods=["POST"])
def create_consult_view():
    # dispatch the event
    data = request.get_json()
    start_date = parse_date(data['start_date'])
    created_id = services.create_new_consultation(start_date=start_date,
                                                  physician_id=data['physician_id'],
                                                  patient_id=data['patient_id'],
                                                  uow=unit_of_work.SqlAlchemyUnitOfWork())

    return redirect(url_for('main.query_one_consultation', consulting_id=created_id)), 201


@main_views.route('/consultation', methods=['GET'])
def query_all_consultations():
    result = read_services.query_all_consultations(unit_of_work.SqlAlchemyUnitOfWork())
    return jsonify(result)


@main_views.route('/consultation/<consulting_id>', methods=['GET'])
def query_one_consultation(consulting_id):
    # dispatch the query
    result = read_services.query_one_consultation(consulting_id, unit_of_work.SqlAlchemyUnitOfWork())
    return jsonify(result)


@main_views.route('/finishes', methods=['POST'])
def close():
    data = request.get_json()
    consultation_id = data['id']
    end_date = parse_date(data['end_date'])
    consultation = services.close_consultation(consultation_id=consultation_id,
                                               end_date=end_date,
                                               uow=unit_of_work.SqlAlchemyUnitOfWork())
    updated_id = consultation.id

    return redirect(url_for('main.query_one_consultation', consulting_id=updated_id)), 201
