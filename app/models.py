from datetime import datetime
from app import db


class Agendamento(db.Model):
    __tablename__ = 'Agendamento'

    # Colunas
    id_agendamento = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), unique=True)
    horario_inicio = db.Column(db.DateTime)
    horario_fim = db.Column(db.DateTime)
    id_sala = db.Column(db.Integer, db.ForeignKey('Sala.id_sala'))

    def __repr__(self):
        return 'Agendamento {}'.format(self.titulo)

    def to_dict(self):
        data = {
            'id_agendamento': self.id_agendamento,
            'titulo': self.titulo,
            'horario_inicio': self.horario_inicio,
            'horario_fim': self.horario_fim,
            'sala': {
                'id_sala': self.id_sala,
                'sala_nome': self.sala.sala_nome
            }
        }
        return data

    def from_dict(self, data):
        for field in ['titulo', 'horario_inicio',
                      'horario_fim', 'id_sala']:
            if field in data:
                if field in ['horario_inicio', 'horario_fim']:
                    setattr(self, field, datetime.strptime(
                            data[field], '%d-%m-%Y %H:%M'))
                else:
                    setattr(self, field, data[field])

class Sala(db.Model):
    __tablename__ = 'Sala'

    # Colunas
    id_sala = db.Column(db.Integer, primary_key=True)
    sala_nome = db.Column(db.String(45), unique=True)

    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='sala', lazy='dynamic')

    def __repr__(self):
        return 'Sala {}'.format(self.sala_nome)

    def to_dict(self):
        data = {
            'id_sala': self.id_sala,
            'sala_nome': self.sala_nome
        }
        return data

    def from_dict(self, data):
        if 'sala_nome' in data:
            setattr(self, 'sala_nome', data['sala_nome'])
