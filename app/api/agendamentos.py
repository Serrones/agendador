from flask import jsonify, request
from sqlalchemy import and_
from app import db
from app.api import bp
from app.models import Agendamento, Sala


# get agendamentos
@bp.route('/agendamentos', methods=(['GET']))
def get_agendamentos():

    # Caso seja passado parâmetro 'sala', a listagem é filtrada por sala
    if 'sala' in request.args:
        sala = request.args['sala']
        agendamentos = Agendamento.query.filter(Agendamento.id_sala == sala)

        return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]}), 200

    # Caso seja passado parâmetro 'data', a listagem é filtrada por data
    if 'data' in request.args:
        data = request.args['data']




    # Caso não seja passado nenhum parâmetro, serão retornados todos os agendamentos
    agendamentos = Agendamento.query.all()

    return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]}), 200


# create agendamento
@bp.route('/agendamentos', methods=(['POST']))
def create_agendamento():

    data = request.get_json() or {}

    obrigatorios = ['titulo', 'horario_inicio',
                    'horario_fim', 'id_sala']

    # Verifica campos obrigatórios
    for campo in obrigatorios:
        if campo not in data:
            # TODO retorno de erro
            return 'Falta campo ' + campo

    # Verifica se a sala existe
    sala = Sala.query.get_or_404(data['id_sala'])

    # TODO Verificação de disponibilidade da sala !!!! Não funciona
    # Verifica se há agenda
    agenda = Agendamento.query.filter(
            and_(Agendamento.id_sala == data['id_sala'],
            Agendamento.horario_inicio == data['horario_inicio'],
            Agendamento.horario_fim == data['horario_fim'])).first()

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
    alteraveis = ['titulo', 'horario_inicio',
                    'horario_fim', 'id_sala']
    for campo in data:
        if campo not in alteraveis:
            return 'Campo inválido na requisição'

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
