import logging
from datetime import datetime

from flask import jsonify, request
from sqlalchemy import and_, extract

from app import db
from app.api import bp
from app.models import Agendamento, Sala

logging.basicConfig(level=logging.INFO)

@bp.route('/agendamentos', methods=(['GET']))
def get_agendamentos():
    """
    @api {get} /agendamentos
    Retorna lista de Agendamentos
    @apiName get_agendamentos
    @apiGroup Agendamento

    @apiParam {Number} [sala] Filtra a listagem por ID da Sala
    @apiParam {Date} [data] Filtra a listagem por Data (dd-mm-aaaa)

    @apiSuccess {Object[]} agendamentos Lista de Agendamentos
    @apiSuccess {Number} agendamentos.id_agendamento ID do Agendamento
    @apiSuccess {Date} agendamentos.periodo_inicio Início do Período Agendado
    @apiSuccess {Date} agendamentos.periodo_fim Fim do Período Agendado
    @apiSuccess {String} agendamentos.titulo Título do Agendamento
    @apiSuccess {Object} agendamentos.sala Sala Agendada
    @apiSuccess {Number} agendamentos.sala.id_sala ID da Sala Agendada
    @apiSuccess {String} agendamentos.sala.sala_nome Nome da Sala Agendada

    @apiSuccessExample {json} Objeto Agendamento
        HTTP/1.1 200 OK
    "agendamentos": [
        {
            "id_agendamento": 1,
            "titulo": "Reunião Equipe X",
            "periodo_inicio": "Tue, 15 Jan 2019 13:00:00 GMT",
            "periodo_fim": "Tue, 15 Jan 2019 14:00:00 GMT",
            "sala": {
                "id_sala": 1,
                "sala_nome": "1"
            }
        }
    ]
    """
    if request.args:
        if 'sala' in request.args and 'data' in request.args:
            """Localiza agendamentos por data e sala"""
            sala = request.args['sala']
            s = Sala.query.get(sala)
            if not s:
                logging.warning('Sala não encontrada')
                return jsonify({'Erro': 'O id_sala não foi encontrado'}), 404
            else:
                data = request.args['data']
                agendamentos = Agendamento.query.filter(and_(
                        Agendamento.id_sala == sala,
                        extract('day', Agendamento.periodo_inicio) == data[0:2],
                        extract('month', Agendamento.periodo_inicio) == data[3:5],
                        extract('year', Agendamento.periodo_inicio) == data[6:10]
                        )).order_by(Agendamento.id_sala).order_by(
                        Agendamento.periodo_inicio).all()
                if len(agendamentos) == 0:
                        logging.info('Não há reservas para esta data e sala')
                        return jsonify({'agendamentos': 'Não há reservas para esta data e sala'}), 404
                else:
                    logging.info('Listagem de Agendamentos -- Filtro por Data e Sala')
                    return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]}), 200
        if 'sala' in request.args:
            """Localiza agendamentos por sala"""
            sala = request.args['sala']
            s = Sala.query.get(sala)
            if not s:
                logging.warning('Sala não encontrada')
                return jsonify({'Erro': 'O id_sala não foi encontrado'}), 404
            else:
                agendamentos_sala = Agendamento.query.filter(
                                Agendamento.id_sala == sala).order_by(
                                Agendamento.periodo_inicio).all()
                if len(agendamentos_sala) == 0:
                        logging.info('Não há reservas para esta sala')
                        return jsonify({'agendamentos': 'Não há reservas para esta sala'}), 404
                else:
                    logging.info('Listagem de Agendamentos -- Filtro por Sala')
                    return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos_sala]}), 200
        if 'data' in request.args:
            """Localiza agendamentos por data"""
            data = request.args['data']
            agendamentos_data = Agendamento.query.filter(and_(
                    extract('day', Agendamento.periodo_inicio) == data[0:2],
                    extract('month', Agendamento.periodo_inicio) == data[3:5],
                    extract('year', Agendamento.periodo_inicio) == data[6:10]
                    )).order_by(Agendamento.id_sala).order_by(
                    Agendamento.periodo_inicio).all()
            if len(agendamentos_data) == 0:
                    logging.info('Não há reservas para esta data')
                    return jsonify({'agendamentos': 'Não há reservas para esta data'}), 404
            else:
                logging.info('Listagem de Agendamentos -- Filtro por Data')
                return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos_data]}), 200
    else:
        """Caso não seja passado nenhum parâmetro, serão retornados todos os agendamentos"""
        agendamentos = Agendamento.query.order_by(
                        Agendamento.id_sala).order_by(
                        Agendamento.periodo_inicio).all()
        logging.info('Listagem de Agendamentos')
        return jsonify({'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]}), 200

@bp.route('/agendamentos', methods=(['POST']))
def create_agendamento():
    """
    @api {post} /agendamentos
    Cria um registro de Agendamento
    @apiName create_agendamento
    @apiGroup Agendamento

    @apiParam (Request body) {String} titulo Título do Agendamento
    @apiParam (Request body) {Number} id_sala ID da Sala do Agendamento
    @apiParam (Request body) {Date} periodo_inicio Início do Período do Agendamento
    @apiParam (Request body) {Date} periodo_fim Fim do Período do Agendamento

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
             -X POST http://localhost:5000/api/agendamentos \
             -d '{"titulo": "Reunião Equipe X", "id_sala": 1,
                  "periodo_inicio": "15-01-2019 13:00",
                  "periodo_fim": "15-01-2019 14:00"}'

    @apiSuccess {Object} oret Objeto Agendamneto criado
        HTTP/1.1 201 Created

    @apiSuccessExample {json} Objeto Agendamento
        HTTP/1.1 201 Created
    "agendamentos": [
        {
            "id_agendamento": 1,
            "titulo": "Reunião Equipe X",
            "periodo_inicio": "Tue, 15 Jan 2019 13:00:00 GMT",
            "periodo_fim": "Tue, 15 Jan 2019 14:00:00 GMT",
            "sala": {
                "id_sala": 1,
                "sala_nome": "1"
            }
        }
    ]
    @apiError 400 Campo obrigatório não informado || Horário de início é maior ou igual que o Horário final
    @apiError 403 Sala reservada nesse período
    @apiError 404 ID da Sala não encontrado
    """
    data = request.get_json() or {}
    obrigatorios = ['titulo', 'periodo_inicio',
                    'periodo_fim', 'id_sala']

    for campo in obrigatorios:
        if campo not in data:
            logging.warning('Agendamento não criado -- Falta Campo')
            return jsonify({'Erro': 'Falta campo ' + campo}), 400

    sala = Sala.query.get(data['id_sala'])
    if not sala:
        logging.warning('Agendamento não criado -- Sala não encontrada')
        return jsonify({'Erro': 'O id_sala não foi encontrado'}), 404

    agendamento = Agendamento()
    agendamento.from_dict(data)

    if agendamento.periodo_inicio > agendamento.periodo_fim:
        logging.warning('Agendamento não criado -- Hora começo maior que Hora término')
        return jsonify({'Erro': 'Horário de início é maior que o Horário final'}), 400

    if agendamento.periodo_inicio == agendamento.periodo_fim:
        logging.warning('Agendamento não criado -- Hora começo e término iguais')
        return jsonify({'Erro': 'Horário de início é igual que o Horário final'}), 400

    reservados = Agendamento.query.filter(
                Agendamento.id_sala == agendamento.id_sala)
    agenda = []
    for reserva in reservados:
        if agendamento.periodo_inicio >= reserva.periodo_inicio and \
            agendamento.periodo_inicio < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_fim > reserva.periodo_inicio and \
            agendamento.periodo_fim < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_inicio <= reserva.periodo_inicio and \
            agendamento.periodo_fim >= reserva.periodo_fim:
            agenda.append(reserva)
    if agenda:
        logging.warning('Agendamento não criado -- Horário Reservado')
        return jsonify({'Erro': 'Sala reservada nesse período'}), 403

    db.session.add(agendamento)
    db.session.commit()
    logging.info('Agendamento criado')
    return jsonify(agendamento.to_dict()), 201


@bp.route('/agendamentos/<int:id_agendamento>', methods=(['PUT']))
def update_agendamento(id_agendamento):
    """
    @api {put} /agendamentos/:id_agendamento
    Atualiza dados de um Agendamento por ID
    @apiName update_agendamento
    @apiGroup Agendamento

    @apiParam {Number} id_agendamento ID do Agendamento

    @apiParam (Request body) {String} [titulo] Título do Agendamento
    @apiParam (Request body) {Number} [id_sala] ID da Sala do Agendamento
    @apiParam (Request body) {Date} [periodo_inicio] Início do Período do Agendamento
    @apiParam (Request body) {Date} [periodo_fim] Fim do Período do Agendamento

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
         -X PUT http://localhost:5000/api/agendamentos/:id_agendamento \
         -d '{"periodo_fim": "15-01-2019 15:00"}'

    @apiSuccess {Object} oret Objeto Agendamento atualizado
        HTTP/1.1 200 Ok

    @apiSuccessExample {json} Objeto Agendamento
        HTTP/1.1 200 OK
    "agendamentos": [
        {
            "id_agendamento": 1,
            "titulo": "Reunião Equipe X",
            "periodo_inicio": "Tue, 15 Jan 2019 13:00:00 GMT",
            "periodo_fim": "Tue, 15 Jan 2019 14:00:00 GMT",
            "sala": {
                "id_sala": 1,
                "sala_nome": "1"
            }
        }
    ]
    @apiError 400 Campo inválido na requisição || Horário de início é maior ou igual que o Horário final
    @apiError 403 Sala reservada nesse período
    @apiError 404 O id_agendamento não foi encontrado || O id_sala não foi encontrado
    """
    data = request.get_json() or {}
    agendamento = Agendamento.query.get(id_agendamento)

    if not agendamento:
        logging.warning('Agendamento não encontrado')
        return jsonify({'Erro': 'O id_sala não foi encontrado'}), 404
    alteraveis = ['titulo', 'periodo_inicio',
                  'periodo_fim', 'id_sala']

    for campo in data:
        if campo not in alteraveis:
            logging.warning('Agendamento não atualizado -- Campo inválido')
            return jsonify({'Erro': 'Campo inválido na requisição'}), 400

    if 'id_sala' in data:
        sala = Sala.query.get(data['id_sala'])
        if not sala:
            logging.warning('Agendamento não atualizado -- Sala não encontrada')
            return jsonify({'Erro': 'O id_sala não foi encontrado'}), 404

    agendamento.from_dict(data)

    if agendamento.periodo_inicio > agendamento.periodo_fim:
        logging.warning('Agendamento não atualizado -- Hora começo maior que Hora término')
        return jsonify({'Erro': 'Horário de início é maior que o Horário final'}), 400
    if agendamento.periodo_inicio == agendamento.periodo_fim:
        logging.warning('Agendamento não atualizado -- Hora começo e término iguais')
        return jsonify({'Erro': 'Horário de início é igual que o Horário final'}), 400

    reservados = Agendamento.query.filter(and_(
                Agendamento.id_agendamento != agendamento.id_agendamento,
                Agendamento.id_sala == agendamento.id_sala))
    agenda = []
    for reserva in reservados:
        if agendamento.periodo_inicio >= reserva.periodo_inicio and \
            agendamento.periodo_inicio < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_fim > reserva.periodo_inicio and \
            agendamento.periodo_fim < reserva.periodo_fim:
            agenda.append(reserva)
        if agendamento.periodo_inicio <= reserva.periodo_inicio and \
            agendamento.periodo_fim >= reserva.periodo_fim:
            agenda.append(reserva)
    if agenda:
        """Verifica se há reserva"""
        logging.warning('Agendamento não atualizado -- Horário Reservado')
        return jsonify({'Erro': 'Sala reservada nesse período'}), 403

    db.session.add(agendamento)
    db.session.commit()
    logging.info('Agendamento atualizado')
    return jsonify(agendamento.to_dict()), 200


@bp.route('/agendamentos/<int:id_agendamento>', methods=(['DELETE']))
def delete_agendamento(id_agendamento):
    """
    @api {delete} /agendamentos/:id_agendamento
    Deleção de um Agendamento por ID
    @apiName delete_agendamento
    @apiGroup Agendamento

    @apiParam {Number} id_agendamento ID do Agendamento

    @apiExample Exemplo de requisição:
        curl -X DELETE -i http://localhost:5000/api/agendamentos/:id_agendamento

    @apiSuccess {json} Objeto Agendamento deletado
        HTTP/1.1 202

    @apiError 404 O id_agendamento não foi encontrado
    """
    agendamento = Agendamento.query.get(id_agendamento)

    if not agendamento:
        logging.warning('Agendamento não encontrado')
        return jsonify({'Erro': 'O id_sala não foi encontrado'}), 404

    db.session.delete(agendamento)
    db.session.commit()
    logging.info('Agendamento Deletado')
    return jsonify({'Sucesso': 'Agendamento deletado com sucesso'}), 202
