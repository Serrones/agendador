from flask import jsonify, request
from app import db
from app.api import bp
from app.models import Sala


@bp.route('/salas', methods=(['GET']))
def get_salas():
    """
    @api {get} /salas
    Retorna lista de Salas de Reunião
    @apiName get_salas
    @apiGroup Sala

    @apiSuccess {Object[]} salas Lista de Salas
    @apiSuccess {Number} salas.id_sala ID da Sala
    @apiSuccess {String} salas.sala_nome Nome da Sala

    @apiSuccessExample {json} Objeto Sala
        HTTP/1.1 200 OK
        {
            "salas": [
                {
                    "id_sala": 1,
                    "sala_nome": "Sala 1"
                }
            ]
        }
    """
    # lista todas as salas
    salas = Sala.query.all()

    return jsonify({'salas': [sala.to_dict() for sala in salas]}), 200


@bp.route('/salas', methods=(['POST']))
def create_sala():
    """
    @api {post} /salas
    Cria um registro de Sala
    @apiName create_sala
    @apiGroup Sala

    @apiParam (Request body) {String} sala_nome Nome da Sala

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
             -X POST http://localhost:5000/api/salas \
             -d '{"sala_nome": "Sala 1"}'

    @apiSuccess {Object} oret Objeto Sala criado
        HTTP/1.1 201 Created

    @apiError 400 Campo obrigatório não informado
    @apiError 403 Registro já existe

    """
    data = request.get_json() or {}

    # Verifica campo obrigatório
    if 'sala_nome' not in data:
        return jsonify({'Erro': 'Falta campo sala_nome'}), 400

    existe_sala_nome = Sala.query.filter(Sala.sala_nome == data['sala_nome']).first()

    if existe_sala_nome:
        return jsonify({'Erro': 'Já existe sala com este nome'}), 403

    sala = Sala()
    sala.from_dict(data)
    db.session.add(sala)
    db.session.commit()

    return jsonify(sala.to_dict()), 201


@bp.route('/salas/<int:id_sala>', methods=(['PUT']))
def update_sala(id_sala):
    """
    @api {put} /salas/:id_sala
    Atualiza dados de uma Sala por ID
    @apiName update_sala
    @apiGroup Sala

    @apiParam {Number} id_sala ID da Sala

    @apiParam (Request body) {String} sala_nome Nome da Sala

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
         -X PUT http://localhost:5000/api/salas/:id_sala \
         -d '{"sala_nome": "Sala 2"}'

    @apiSuccess {Object} oret Objeto Sala atualizado
        HTTP/1.1 200 Ok

    @apiError 404 O id_sala não foi encontrado
    @apiError 400 Campo inválido na requisição
    """

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


@bp.route('/salas/<int:id_sala>', methods=(['DELETE']))
def delete_sala(id_sala):
    """
    @api {delete} /salas/:id_sala
    Deleção de uma Sala por ID
    @apiName delete_sala
    @apiGroup Sala

    @apiParam {Number} id_sala ID da Sala

    @apiExample Exemplo de requisição:
        curl -X DELETE -i http://localhost:5000/api/salas/:id_sala

    @apiSuccess {json} Objeto Sala deletado
        HTTP/1.1 202

    @apiError 403 O id_sala não pode ser deletado
    @apiError 404 O id_sala não foi encontrado
    """

    sala = Sala.query.get_or_404(id_sala)

    # Verifica se há agendamentos para a sala
    if sala.agendamentos.all():
        return jsonify({'Erro': 'Sala não pode ser deletada. Há agendamentos'}), 403
    else:
        db.session.delete(sala)
        db.session.commit()

        return jsonify({'Sucesso': 'Sala deletada'}), 202
