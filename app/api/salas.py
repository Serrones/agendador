from flask import jsonify, request
from app import db
from app.api import bp
from app.models import Sala



# get salas
@bp.route('/salas', methods=(['GET']))
def get_salas():

    # lista todas as salas
    salas = Sala.query.all()

    return jsonify({'salas': [sala.to_dict() for sala in salas]}), 200


# post sala
@bp.route('/salas', methods=(['POST']))
def create_sala():

    data = request.get_json() or {}

    # Verifica campo obrigatório
    if 'sala_nome' not in data:
        # TODO retorno de erro
        return jsonify({'Erro': 'Falta campo sala_nome'}), 400

    existe_sala_nome = Sala.query.filter(Sala.sala_nome == data['sala_nome']).first()

    if existe_sala_nome:
        return jsonify({'Erro': 'Já existe sala com este nome'}), 403

    sala = Sala()
    sala.from_dict(data)
    db.session.add(sala)
    db.session.commit()

    return jsonify(sala.to_dict()), 201


# put sala
@bp.route('/salas/<int:id_sala>', methods=(['PUT']))
def update_sala(id_sala):

    data = request.get_json() or {}

    sala = Sala.query.get_or_404(id_sala)

    # Verifica se há algum campo inválido na requisição
    for campo in data:
        if campo != 'sala_nome':
            return jsonify({'Erro': 'Campo {} inválido na requisição'.format(campo)}), 400

    sala.from_dict(data)
    db.session.add(sala)
    db.session.commit()

    return jsonify(sala.to_dict()), 200


# delete sala
@bp.route('/salas/<int:id_sala>', methods=(['DELETE']))
def delete_sala(id_sala):

    sala = Sala.query.get_or_404(id_sala)

    # Verifica se há agendamentos para a sala
    # TODO Necessário utilizar o all()?
    if sala.agendamentos.all():
        return jsonify({'Erro': 'Sala não pode ser deletada. Há agendamentos'}), 403
    else:
        db.session.delete(sala)
        db.session.commit()

        return jsonify({'Sucesso': 'Sala deletada'}), 202
