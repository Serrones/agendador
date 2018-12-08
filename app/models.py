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

class Sala(db.Model):
    __tablename__ = 'Sala'

    # Colunas
    id_sala = db.Column(db.Integer, primary_key=True)
    sala_nome = db.Column(db.String(45), unique=True)

    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='sala', lazy='dynamic')

    def __repr__(self):
        return 'Sala {}'.format(self.sala_nome)
