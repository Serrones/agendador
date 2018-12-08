from flask import jsonify, request
from app import db
from app.api import bp
from app.models import Sala

# post sala
@bp.route('/salas', methods=(['POST']))
def create_sala():

    data = request.get_json() or {}

    # Verifica campo obrigatório
    if 'sala_nome' not in data:
        # TODO retorno de erro
        return 'Falta campo sala_nome'

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
            return 'Campo {} inválido na requisição'.format(campo)

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
        return 'Sala não pode ser deletada. Há agendamentos'
    else:
        db.session.delete(sala)
        db.session.commit()

        return 'Sala deletada com sucesso', 200
