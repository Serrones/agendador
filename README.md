# Agendador

Sistema de Gestão de Sala de Reuniões

Web Server API Restful em Flask

Integração com a extensão Flask-SQLAlchemy

## Flask e Extensões

- FLASK: [Flask](http://flask.pocoo.org/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

## Testes e Logs

- LOGGING: [Python logging](https://docs.python.org/3/library/logging.html)

- Testing: [Python unittest](https://docs.python.org/3/library/unittest.html)

- Coverage: [Coverage.py](https://docs.python.org/3/library/unittest.html)

## Databases

- Development: [SQLite](https://www.sqlite.org/docs.html)

- Testing: [SQLite](https://www.sqlite.org/docs.html)

## Instalação

Criar um ambiente virtual:
```
virtualenv -p python3 .venv
```
Instalar requerimentos com pip:
```
pip install -r requirements.txt
```

## Configuração do Projeto Flask

Clonando repositório:
```
git clone https://github.com/Serrones/agendador
```

### Ativação Flask via Linha de Comando

Inicialização do Projeto Flask:
```
export FLASK_APP=agendador.py
export FLASK_DEBUG=1
```
Criação da DataBase:
```
flask db upgrade
```
Para rodar o serviço:
```
flask run
```

## Testes

Rodando os testes:
```
python tests.py
```
ou
```
coverage run tests.py
```

Relatório de Cobertura
```
coverage report
```

## Documentação

Abrir arquivo `index.html` em um browser
```
documentacao/index.html
```
