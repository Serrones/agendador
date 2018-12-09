from datetime import datetime
from flask import jsonify, request
from sqlalchemy import and_, or_, extract
from app import db
from app.api import bp
from app.models import Agendamento, Sala


# get agendamentos
@bp.route('/agendamentos', methods=(['GET']))
def get_agendamentos():
    # TODO Ajustar soma das queries
    if request.args:
        # Caso seja passado parâmetro 'sala', a listagem é filtrada por sala
        agendamentos = {}
        if 'sala' in request.args:
            sala = request.args['sala']
            agendamentos_sala = Agendamento.query.filter(
                                Agendamento.id_sala == sala).order_by(
                                Agendamento.periodo_inicio).all()
            # agendamentos.update(*agendamentos_sala)

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
            # agendamentos.add(*agendamentos_data)
            return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos_data]}), 200

        # return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]}), 200
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
            return 'Falta campo ' + campo

    # Verifica se a sala existe
    sala = Sala.query.get_or_404(data['id_sala'])

    # Verifica se há agenda
    #TODO ainda tem falha na verificação de horário
    agenda = Agendamento.query.filter(and_(
            Agendamento.id_sala == data['id_sala'],
            extract('month', Agendamento.periodo_inicio) == data['periodo_inicio'][3:5],
            extract('year', Agendamento.periodo_inicio) == data['periodo_inicio'][6:10],
            extract('day', Agendamento.periodo_inicio) == data['periodo_inicio'][0:2],
            extract('hour', Agendamento.periodo_inicio) <= data['periodo_inicio'][11:13],
            extract('hour', Agendamento.periodo_fim) > data['periodo_inicio'][11:13]).or_(
            and_(Agendamento.id_sala == data['id_sala'],
            extract('month', Agendamento.periodo_inicio) == data['periodo_inicio'][3:5],
            extract('year', Agendamento.periodo_inicio) == data['periodo_inicio'][6:10],
            extract('day', Agendamento.periodo_inicio) == data['periodo_inicio'][0:2],
            extract('hour', Agendamento.periodo_inicio) < data['periodo_fim'][11:13],
            extract('hour', Agendamento.periodo_fim) >= data['periodo_fim'][11:13]))).all()

    if agenda:
        return 'Sala reservada nesse período'

    agendamento = Agendamento()
    agendamento.from_dict(data)
    db.session.add(agendamento)
    db.session.commit()

    return jsonify(agendamento.to_dict()), 201


# put agendamento
@bp.route('/agendamentos/<int:id_agendamento>', methods=(['PUT']))
def update_agendamento(id_agendamento):

    data = request.get_json() or {}

    agendamento = Agendamento.query.get_or_404(id_agendamento)

    # Verifica se há algum campo inválido na requisição
    alteraveis = ['titulo', 'data_agendamento', 'horario_inicio',
                    'horario_fim', 'id_sala']
    for campo in data:
        if campo not in alteraveis:
            return 'Campo inválido na requisição'

    #TODO Verifica se entra periodo e se pode alterar

    agendamento.from_dict(data)
    db.session.add(agendamento)
    db.session.commit()

    return jsonify(agendamento.to_dict()), 200

# delete agendamento
@bp.route('/agendamentos/<int:id_agendamento>', methods=(['DELETE']))
def delete_agendamento(id_agendamento):

    agendamento = Agendamento.query.get_or_404(id_agendamento)

    db.session.delete(agendamento)
    db.session.commit()

    return 'Agendamento deletado com sucesso', 200
