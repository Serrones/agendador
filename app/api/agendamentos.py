from datetime import datetime
from flask import jsonify, request
from sqlalchemy import and_, extract
from app import db
from app.api import bp
from app.models import Agendamento, Sala


# get agendamentos
@bp.route('/agendamentos', methods=(['GET']))
def get_agendamentos():
    # Caso venha algum parâmetro de busca
    if request.args:
        # Caso sejam passados parâmetros 'sala' e 'data', a listagem é filtrada por ambos
        if 'sala' in request.args and 'data' in request.args:
            sala = request.args['sala']
            data = request.args['data']
            agendamentos = Agendamento.query.filter(and_(
                    Agendamento.id_sala == sala,
                    extract('day', Agendamento.periodo_inicio) == data[0:2],
                    extract('month', Agendamento.periodo_inicio) == data[3:5],
                    extract('year', Agendamento.periodo_inicio) == data[6:10]
                    )).order_by(Agendamento.id_sala).order_by(
                    Agendamento.periodo_inicio).all()

            return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]}), 200

        # Caso seja passado parâmetro 'sala', a listagem é filtrada por sala
        if 'sala' in request.args:
            sala = request.args['sala']
            agendamentos_sala = Agendamento.query.filter(
                                Agendamento.id_sala == sala).order_by(
                                Agendamento.periodo_inicio).all()

            return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos_sala]}), 200

        # Caso seja passado parâmetro 'data' (dd-mm-aaaa), a listagem é filtrada por data
        if 'data' in request.args:
            data = request.args['data']
            agendamentos_data = Agendamento.query.filter(and_(
                    extract('day', Agendamento.periodo_inicio) == data[0:2],
                    extract('month', Agendamento.periodo_inicio) == data[3:5],
                    extract('year', Agendamento.periodo_inicio) == data[6:10]
                    )).order_by(Agendamento.id_sala).order_by(
                    Agendamento.periodo_inicio).all()

            return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos_data]}), 200

    else:
        # Caso não seja passado nenhum parâmetro, serão retornados todos os agendamentos
        agendamentos = Agendamento.query.order_by(
                        Agendamento.id_sala).order_by(
                        Agendamento.periodo_inicio).all()

        return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]}), 200


# create agendamento
@bp.route('/agendamentos', methods=(['POST']))
def create_agendamento():

    data = request.get_json() or {}

    obrigatorios = ['titulo', 'periodo_inicio',
                    'periodo_fim', 'id_sala']

    # Verifica campos obrigatórios
    for campo in obrigatorios:
        if campo not in data:
            # TODO retorno de erro
            return jsonify({'Erro': 'Falta campo ' + campo}), 400

    # Verifica se a sala existe
    sala = Sala.query.get_or_404(data['id_sala'])

    agendamento = Agendamento()
    agendamento.from_dict(data)

    if agendamento.periodo_inicio > agendamento.periodo_fim:
        return jsonify({'Erro': 'Horário de início é maior que o Horário final'}), 400

    # Verifica se há agenda
    reservados = Agendamento.query.filter(
                Agendamento.id_sala == agendamento.id_sala)

    agenda = []
    for reserva in reservados:
        if agendamento.periodo_inicio >= reserva.periodo_inicio and agendamento.periodo_inicio < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_fim > reserva.periodo_inicio and agendamento.periodo_fim < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_inicio <= reserva.periodo_inicio and agendamento.periodo_fim >= reserva.periodo_fim:
            agenda.append(reserva)

    if agenda:
        return jsonify({'Erro': 'Sala reservada nesse período'}), 403

    db.session.add(agendamento)
    db.session.commit()

    return jsonify(agendamento.to_dict()), 201

    # put agendamento

@bp.route('/agendamentos/<int:id_agendamento>', methods=(['PUT']))
def update_agendamento(id_agendamento):

    data = request.get_json() or {}

    agendamento = Agendamento.query.get_or_404(id_agendamento)

    # Verifica se há algum campo inválido na requisição
    alteraveis = ['titulo', 'periodo_inicio',
                  'periodo_fim', 'id_sala']
    for campo in data:
        if campo not in alteraveis:
            return jsonify({'Erro': 'Campo inválido na requisição'}), 403

    if 'id_sala' in data:
        # Verifica se a sala existe
        sala = Sala.query.get_or_404(data['id_sala'])

    agendamento.from_dict(data)

    if agendamento.periodo_inicio > agendamento.periodo_fim:
        return jsonify({'Erro': 'Horário de início é maior que o Horário final'}), 403

    # Verifica se há agenda
    reservados = Agendamento.query.filter(and_(
                Agendamento.id_agendamento != agendamento.id_agendamento,
                Agendamento.id_sala == agendamento.id_sala))

    agenda = []
    for reserva in reservados:
        if agendamento.periodo_inicio >= reserva.periodo_inicio and agendamento.periodo_inicio < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_fim > reserva.periodo_inicio and agendamento.periodo_fim < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_inicio <= reserva.periodo_inicio and agendamento.periodo_fim >= reserva.periodo_fim:
            agenda.append(reserva)

    if agenda:
        return jsonify({'Erro': 'Sala reservada nesse período'}), 403

    db.session.add(agendamento)
    db.session.commit()

    return jsonify(agendamento.to_dict()), 200

# delete agendamento
@bp.route('/agendamentos/<int:id_agendamento>', methods=(['DELETE']))
def delete_agendamento(id_agendamento):

    agendamento = Agendamento.query.get_or_404(id_agendamento)

    db.session.delete(agendamento)
    db.session.commit()

    return jsonify({'Sucesso': 'Agendamento deletado com sucesso'}), 202
