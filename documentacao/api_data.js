define({ "api": [
  {
    "type": "post",
    "url": "/agendamentos",
    "title": "Cria um registro de Agendamento",
    "name": "create_agendamento",
    "group": "Agendamento",
    "parameter": {
      "fields": {
        "Request body": [
          {
            "group": "Request body",
            "type": "String",
            "optional": false,
            "field": "titulo",
            "description": "<p>Título do Agendamento</p>"
          },
          {
            "group": "Request body",
            "type": "Number",
            "optional": false,
            "field": "id_sala",
            "description": "<p>ID da Sala do Agendamento</p>"
          },
          {
            "group": "Request body",
            "type": "Date",
            "optional": false,
            "field": "periodo_inicio",
            "description": "<p>Início do Período do Agendamento</p>"
          },
          {
            "group": "Request body",
            "type": "Date",
            "optional": false,
            "field": "periodo_fim",
            "description": "<p>Fim do Período do Agendamento</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Exemplo de requisição:",
        "content": "curl -H \"Content-Type: application/json\" \\\n     -X POST http://localhost:5000/api/agendamentos \\\n     -d '{\"titulo\": \"Reunião Equipe X\", \"id_sala\": 1,\n          \"periodo_inicio\": \"15-01-2019 13:00\",\n          \"periodo_fim\": \"15-01-2019 14:00\"}'",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "oret",
            "description": "<p>Objeto Agendamneto criado HTTP/1.1 201 Created</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Objeto Agendamento",
          "content": "    HTTP/1.1 201 Created\n\"agendamentos\": [\n    {\n        \"id_agendamento\": 1,\n        \"titulo\": \"Reunião Equipe X\",\n        \"periodo_inicio\": \"Tue, 15 Jan 2019 13:00:00 GMT\",\n        \"periodo_fim\": \"Tue, 15 Jan 2019 14:00:00 GMT\",\n        \"sala\": {\n            \"id_sala\": 1,\n            \"sala_nome\": \"1\"\n        }\n    }\n]",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400",
            "description": "<p>Campo obrigatório não informado || Horário de início é maior ou igual que o Horário final</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>Sala reservada nesse período</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>ID da Sala não encontrado</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/api/agendamentos.py",
    "groupTitle": "Agendamento"
  },
  {
    "type": "delete",
    "url": "/agendamentos/:id_agendamento",
    "title": "Deleção de um Agendamento por ID",
    "name": "delete_agendamento",
    "group": "Agendamento",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id_agendamento",
            "description": "<p>ID do Agendamento</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Exemplo de requisição:",
        "content": "curl -X DELETE -i http://localhost:5000/api/agendamentos/:id_agendamento",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "Objeto",
            "description": "<p>Agendamento deletado HTTP/1.1 202</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>O id_agendamento não foi encontrado</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/api/agendamentos.py",
    "groupTitle": "Agendamento"
  },
  {
    "type": "get",
    "url": "/agendamentos",
    "title": "Retorna lista de Agendamentos",
    "name": "get_agendamentos",
    "group": "Agendamento",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "sala",
            "description": "<p>Filtra a listagem por ID da Sala</p>"
          },
          {
            "group": "Parameter",
            "type": "Date",
            "optional": true,
            "field": "data",
            "description": "<p>Filtra a listagem por Data (dd-mm-aaaa)</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "agendamentos",
            "description": "<p>Lista de Agendamentos</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "agendamentos.id_agendamento",
            "description": "<p>ID do Agendamento</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "agendamentos.periodo_inicio",
            "description": "<p>Início do Período Agendado</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "agendamentos.periodo_fim",
            "description": "<p>Fim do Período Agendado</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "agendamentos.titulo",
            "description": "<p>Título do Agendamento</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "agendamentos.sala",
            "description": "<p>Sala Agendada</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "agendamentos.sala.id_sala",
            "description": "<p>ID da Sala Agendada</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "agendamentos.sala.sala_nome",
            "description": "<p>Nome da Sala Agendada</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Objeto Agendamento",
          "content": "    HTTP/1.1 200 OK\n\"agendamentos\": [\n    {\n        \"id_agendamento\": 1,\n        \"titulo\": \"Reunião Equipe X\",\n        \"periodo_inicio\": \"Tue, 15 Jan 2019 13:00:00 GMT\",\n        \"periodo_fim\": \"Tue, 15 Jan 2019 14:00:00 GMT\",\n        \"sala\": {\n            \"id_sala\": 1,\n            \"sala_nome\": \"1\"\n        }\n    }\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api/agendamentos.py",
    "groupTitle": "Agendamento"
  },
  {
    "type": "put",
    "url": "/agendamentos/:id_agendamento",
    "title": "Atualiza dados de um Agendamento por ID",
    "name": "update_agendamento",
    "group": "Agendamento",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id_agendamento",
            "description": "<p>ID do Agendamento</p>"
          }
        ],
        "Request body": [
          {
            "group": "Request body",
            "type": "String",
            "optional": true,
            "field": "titulo",
            "description": "<p>Título do Agendamento</p>"
          },
          {
            "group": "Request body",
            "type": "Number",
            "optional": true,
            "field": "id_sala",
            "description": "<p>ID da Sala do Agendamento</p>"
          },
          {
            "group": "Request body",
            "type": "Date",
            "optional": true,
            "field": "periodo_inicio",
            "description": "<p>Início do Período do Agendamento</p>"
          },
          {
            "group": "Request body",
            "type": "Date",
            "optional": true,
            "field": "periodo_fim",
            "description": "<p>Fim do Período do Agendamento</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Exemplo de requisição:",
        "content": "curl -H \"Content-Type: application/json\" \\\n -X PUT http://localhost:5000/api/agendamentos/:id_agendamento \\\n -d '{\"periodo_fim\": \"15-01-2019 15:00\"}'",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "oret",
            "description": "<p>Objeto Agendamento atualizado HTTP/1.1 200 Ok</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Objeto Agendamento",
          "content": "    HTTP/1.1 200 OK\n\"agendamentos\": [\n    {\n        \"id_agendamento\": 1,\n        \"titulo\": \"Reunião Equipe X\",\n        \"periodo_inicio\": \"Tue, 15 Jan 2019 13:00:00 GMT\",\n        \"periodo_fim\": \"Tue, 15 Jan 2019 14:00:00 GMT\",\n        \"sala\": {\n            \"id_sala\": 1,\n            \"sala_nome\": \"1\"\n        }\n    }\n]",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400",
            "description": "<p>Campo inválido na requisição || Horário de início é maior ou igual que o Horário final</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>Sala reservada nesse período</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>O id_agendamento não foi encontrado || O id_sala não foi encontrado</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/api/agendamentos.py",
    "groupTitle": "Agendamento"
  },
  {
    "type": "post",
    "url": "/salas",
    "title": "Cria um registro de Sala",
    "name": "create_sala",
    "group": "Sala",
    "parameter": {
      "fields": {
        "Request body": [
          {
            "group": "Request body",
            "type": "String",
            "optional": false,
            "field": "sala_nome",
            "description": "<p>Nome da Sala</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Exemplo de requisição:",
        "content": "curl -H \"Content-Type: application/json\" \\\n     -X POST http://localhost:5000/api/salas \\\n     -d '{\"sala_nome\": \"Sala 1\"}'",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "oret",
            "description": "<p>Objeto Sala criado HTTP/1.1 201 Created</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Objeto Sala",
          "content": "HTTP/1.1 201 Created\n{\n    \"salas\": [\n        {\n            \"id_sala\": 1,\n            \"sala_nome\": \"Sala 1\"\n        }\n    ]\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400",
            "description": "<p>Campo obrigatório não informado</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>Registro já existe</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/api/salas.py",
    "groupTitle": "Sala"
  },
  {
    "type": "delete",
    "url": "/salas/:id_sala",
    "title": "Deleção de uma Sala por ID",
    "name": "delete_sala",
    "group": "Sala",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id_sala",
            "description": "<p>ID da Sala</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Exemplo de requisição:",
        "content": "curl -X DELETE -i http://localhost:5000/api/salas/:id_sala",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "Objeto",
            "description": "<p>Sala deletado HTTP/1.1 202</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "403",
            "description": "<p>O id_sala não pode ser deletado -- Há agendamentos</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>O id_sala não foi encontrado</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/api/salas.py",
    "groupTitle": "Sala"
  },
  {
    "type": "get",
    "url": "/salas",
    "title": "Retorna lista de Salas de Reunião",
    "name": "get_salas",
    "group": "Sala",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "salas",
            "description": "<p>Lista de Salas</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "salas.id_sala",
            "description": "<p>ID da Sala</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "salas.sala_nome",
            "description": "<p>Nome da Sala</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Objeto Sala",
          "content": "HTTP/1.1 200 OK\n{\n    \"salas\": [\n        {\n            \"id_sala\": 1,\n            \"sala_nome\": \"Sala 1\"\n        }\n    ]\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api/salas.py",
    "groupTitle": "Sala"
  },
  {
    "type": "put",
    "url": "/salas/:id_sala",
    "title": "Atualiza dados de uma Sala por ID",
    "name": "update_sala",
    "group": "Sala",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id_sala",
            "description": "<p>ID da Sala</p>"
          }
        ],
        "Request body": [
          {
            "group": "Request body",
            "type": "String",
            "optional": false,
            "field": "sala_nome",
            "description": "<p>Nome da Sala</p>"
          }
        ]
      }
    },
    "examples": [
      {
        "title": "Exemplo de requisição:",
        "content": "curl -H \"Content-Type: application/json\" \\\n -X PUT http://localhost:5000/api/salas/:id_sala \\\n -d '{\"sala_nome\": \"Sala 2\"}'",
        "type": "json"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "oret",
            "description": "<p>Objeto Sala atualizado HTTP/1.1 200 Ok</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Objeto Sala",
          "content": "HTTP/1.1 200 OK\n{\n    \"salas\": [\n        {\n            \"id_sala\": 1,\n            \"sala_nome\": \"Sala 1\"\n        }\n    ]\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>O id_sala não foi encontrado</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "400",
            "description": "<p>Campo inválido na requisição</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/api/salas.py",
    "groupTitle": "Sala"
  }
] });
