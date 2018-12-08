from app import create_app, db
from app.models import Agendamento, Sala


app = create_app()



@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Agendamento': Agendamento,
            'Sala': Sala
    }
