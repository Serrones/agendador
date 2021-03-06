import os,sys
import json
from unittest import TestCase, main

from flask import Flask
from app import create_app
from app import db

# Caminho para criação da database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))

class TestSalas(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app.app_context().push()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        db.create_all()

    def tearDown(self):
        db.drop_all()

    """
    GET
    """
    def test_lista_salas(self):
        resposta = self.client.get('/api/salas')
        self.assertEqual(resposta.status_code, 200)

    """
    POST
    """

    def test_create_sala_sucesso(self):
        nova_sala = {'sala_nome': 'Sala 2'}
        resposta = self.client.post('api/salas',
                        data=json.dumps(nova_sala),
                        content_type='application/json'
                    )
        self.assertEqual(resposta.status_code, 201)

    def test_create_sala_sem_campo_obrigatorio(self):
        nova_sala = {'sala': 'Sala 3'}
        resposta = self.client.post('api/salas',
                        data=json.dumps(nova_sala),
                        content_type='application/json'
                    )
        self.assertEqual(resposta.status_code, 400)

    def test_create_sala_com_mesmo_nome(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )

        nova_sala = {'sala_nome': 'Sala 2'}
        resposta = self.client.post('api/salas',
                        data=json.dumps(nova_sala),
                        content_type='application/json'
                    )
        self.assertEqual(resposta.status_code, 403)

    """
    PUT
    """

    def test_update_sala_sucesso(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )

        atualiza_sala = {'sala_nome': 'sala 42'}
        resposta = self.client.put('api/salas/1',
                        data=json.dumps(atualiza_sala),
                        content_type='application/json'
                    )
        self.assertEqual(resposta.status_code, 200)

    def test_update_sala_nome_campo_errado(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )

        atualiza_sala = {'sala': 'sala 42'}
        resposta = self.client.put('api/salas/1',
                        data=json.dumps(atualiza_sala),
                        content_type='application/json'
                    )
        self.assertEqual(resposta.status_code, 400)

    def test_update_sala_id_inexistente(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )

        atualiza_sala = {'sala': 'sala 42'}
        resposta = self.client.put('api/salas/45',
                        data=json.dumps(atualiza_sala),
                        content_type='application/json'
                    )
        self.assertEqual(resposta.status_code, 404)

    def test_update_sala_com_mesmo_nome(self):
        sala_1 = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
            data=json.dumps(sala_1),
            content_type='application/json'
        )

        sala_2 = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala_2),
            content_type='application/json'
        )

        altera_sala = {'sala_nome': 'Sala 2'}
        resposta = self.client.put('api/salas/1',
                        data=json.dumps(altera_sala),
                        content_type='application/json'
                    )
        self.assertEqual(resposta.status_code, 403)

    """
    DELETE
    """

    def test_delete_sala_sucesso(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )

        deleta_sala = self.client.delete('api/salas/1')
        self.assertEqual(deleta_sala.status_code, 202)

    def test_delete_sala_id_inexistente(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )

        deleta_sala = self.client.delete('api/salas/45')
        self.assertEqual(deleta_sala.status_code, 404)

    def test_delete_sala_com_agendamento(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                   'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
                    )

        deleta_sala = self.client.delete('api/salas/1')
        self.assertEqual(deleta_sala.status_code, 403)


class TestAgendamentos(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app.app_context().push()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        db.create_all()

    def tearDown(self):
        db.session.commit()
        db.drop_all()

    """
    GET
    """

    def test_lista_agendamentos(self):
        response = self.client.get('/api/agendamentos')
        self.assertEqual(response.status_code, 200)

    def test_lista_agendamentos_parametro_sala_correto(self):
        sala = {'sala_nome': 'Sala 1'}
        cria_sala = self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
                    )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        response = self.client.get('/api/agendamentos?sala=1')
        self.assertEqual(response.status_code, 200)

    def test_lista_agendamentos_parametro_sala_incorreto(self):
        sala = {'sala': 'Sala 1'}
        cria_sala = self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
                    )
        response = self.client.get('/api/agendamentos?sala=10')
        self.assertEqual(response.status_code, 404)

    def test_lista_agendamentos_parametro_data(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        response = self.client.get('/api/agendamentos?data=01-01-2019')
        self.assertEqual(response.status_code, 200)

    def test_lista_agendamentos_parametros_data_sala_correta(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        response = self.client.get('/api/agendamentos?sala=1&data=01-01-2019')
        self.assertEqual(response.status_code, 200)

    def test_lista_agendamentos_parametros_data_sala_incorreta(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        response = self.client.get('/api/agendamentos?sala=10&data=01-01-2019')
        self.assertEqual(response.status_code, 404)

    def test_lista_sem_agendamentos_parametros_data_sala_correta(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        response = self.client.get('/api/agendamentos?sala=1&data=02-01-2019')
        self.assertEqual(response.status_code, 404)

    def test_lista_sem_agendamentos_parametros_data_correta(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        response = self.client.get('/api/agendamentos?data=02-01-2019')
        self.assertEqual(response.status_code, 404)

    def test_lista_sem_agendamentos_parametros_sala_correta(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
            data=json.dumps(sala),
            content_type='application/json'
        )
        response = self.client.get('/api/agendamentos?sala=1')
        self.assertEqual(response.status_code, 404)

    """
    POST
    """

    def test_create_agendamento_sucesso(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 201)

    def test_create_agendamento_faltando_item_obrigatorio(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'periodo_inicio': '01-01-2019 08:00',
                   'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 400)

    def test_create_agendamento_sala_nao_existe(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 45}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 404)

    def test_create_agendamento_hora_inicio_maior_hora_fim(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 18:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 400)

    def test_create_agendamento_hora_inicio_igual_hora_fim(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 18:00',
                        'periodo_fim': '01-01-2019 18:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 400)

    def test_create_agendamento_horario_reservado_versao_1(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
        )

        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 403)

    def test_create_agendamento_horario_reservado_versao_2(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
        )

        reserva_2 = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 07:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva_2),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 403)

    def test_create_agendamento_horario_reservado_versao_3(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
        )

        reserva_2 = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 07:00',
                        'periodo_fim': '01-01-2019 10:00', 'id_sala': 1}
        agendamento = self.client.post('api/agendamentos',
                            data=json.dumps(reserva_2),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 403)

    """
    PUT
    """

    def test_update_agendamento_sucesso(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )

        atualiza_reserva = {'periodo_inicio': '01-01-2019 07:00'}
        agendamento = self.client.put('api/agendamentos/1',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )

        self.assertEqual(agendamento.status_code, 200)

    def test_update_agendamento_id_agendamento_inexistente(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )

        atualiza_reserva = {'periodo_inicio': '01-01-2019 07:00'}
        agendamento = self.client.put('api/agendamentos/45',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )

        self.assertEqual(agendamento.status_code, 404)

    def test_update_agendamento_nome_campo_errado(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )

        atualiza_reserva = {'inicio': '01-01-2019 07:00'}
        agendamento = self.client.put('api/agendamentos/1',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )

        self.assertEqual(agendamento.status_code, 400)

    def test_update_agendamento_id_sala_inexistente(self):
        sala = {'sala_nome': 'Sala 2'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )

        atualiza_reserva = {'id_sala': 45}
        agendamento = self.client.put('api/agendamentos/1',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )

        self.assertEqual(agendamento.status_code, 404)

    def test_update_agendamento_hora_inicio_maior_hora_fim(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )
        atualiza_reserva = {'periodo_inicio': '01-01-2019 10:00'}
        agendamento = self.client.put('api/agendamentos/1',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 400)

    def test_update_agendamento_hora_inicio_igual_hora_fim(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )
        atualiza_reserva = {'periodo_inicio': '01-01-2019 09:00'}
        agendamento = self.client.put('api/agendamentos/1',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 400)

    def test_update_agendamento_horario_reservado_versao_1(self):
            sala = {'sala_nome': 'Sala 1'}
            self.client.post('api/salas',
                            data=json.dumps(sala),
                            content_type='application/json'
            )

            reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                            'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
            self.client.post('api/agendamentos',
                            data=json.dumps(reserva),
                            content_type='application/json'
            )

            reserva_2 = {'titulo': 'Reunião 2', 'periodo_inicio': '01-01-2019 09:00',
                            'periodo_fim': '01-01-2019 10:00', 'id_sala': 1}
            self.client.post('api/agendamentos',
                            data=json.dumps(reserva_2),
                            content_type='application/json'
            )
            atualiza_reserva = {'periodo_inicio': '01-01-2019 07:00'}
            agendamento = self.client.put('api/agendamentos/2',
                                data=json.dumps(atualiza_reserva),
                                content_type='application/json'
                        )

            self.assertEqual(agendamento.status_code, 403)

    def test_update_agendamento_horario_reservado_versao_2(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )
        reserva_2 = {'titulo': 'Reunião 2', 'periodo_inicio': '01-01-2019 09:00',
                        'periodo_fim': '01-01-2019 10:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva_2),
                        content_type='application/json'
        )
        atualiza_reserva = {'periodo_inicio': '01-01-2019 08:00'}
        agendamento = self.client.put('api/agendamentos/2',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 403)

    def test_update_agendamento_horario_reservado_versao_3(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )
        reserva_2 = {'titulo': 'Reunião 2', 'periodo_inicio': '01-01-2019 09:00',
                        'periodo_fim': '01-01-2019 10:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva_2),
                        content_type='application/json'
        )
        atualiza_reserva = {'periodo_inicio': '01-01-2019 07:00'}
        agendamento = self.client.put('api/agendamentos/2',
                            data=json.dumps(atualiza_reserva),
                            content_type='application/json'
                    )
        self.assertEqual(agendamento.status_code, 403)

    """
    DELETE
    """

    def test_delete_agendamento_sucesso(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )

        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )

        agendamento = self.client.delete('api/agendamentos/1')
        self.assertEqual(agendamento.status_code, 202)

    def test_delete_agendamento_id_inexistente(self):
        sala = {'sala_nome': 'Sala 1'}
        self.client.post('api/salas',
                        data=json.dumps(sala),
                        content_type='application/json'
        )
        reserva = {'titulo': 'Reunião', 'periodo_inicio': '01-01-2019 08:00',
                        'periodo_fim': '01-01-2019 09:00', 'id_sala': 1}
        self.client.post('api/agendamentos',
                        data=json.dumps(reserva),
                        content_type='application/json'
        )
        agendamento = self.client.delete('api/agendamentos/45')
        self.assertEqual(agendamento.status_code, 404)

if __name__ == '__main__':
    main(verbosity=2)
