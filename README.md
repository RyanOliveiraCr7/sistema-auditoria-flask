# 📦 Sistema de Auditoria de Estoque

Sistema desenvolvido em Python com Flask para gerenciamento e auditoria de estoque, permitindo o controle de itens, movimentações, histórico de auditorias e geração de QR Codes para identificação dos produtos.

## 🚀 Funcionalidades

* Cadastro de itens de estoque
* Controle de entrada e saída de materiais
* Ajuste de quantidades em estoque
* Histórico completo de auditorias
* Dashboard com estatísticas
* Geração automática de QR Codes
* API REST para integração com outros sistemas
* Controle de estoque mínimo
* Consulta por categorias
* Registro de movimentações

## 🛠️ Tecnologias Utilizadas

* Python 3
* Flask
* SQLAlchemy
* SQLite
* QRCode
* HTML5
* CSS3
* Git
* GitHub

## 📁 Estrutura do Projeto

```text
Sistema-Auditoria/
│
├── static/
│   └── qrcodes/
│
├── templates/
│   └── index.html
│
├── instance/
│   └── auditoria.db
│
├── Sistema_de_Auditoria.py
├── .gitignore
└── README.md
```

## ⚙️ Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/RyanOliveiraCr7/sistema-auditoria-flask.git
```

### 2. Acessar a pasta

```bash
cd sistema-auditoria-flask
```

### 3. Instalar dependências

```bash
pip install flask flask-sqlalchemy qrcode pillow
```

### 4. Executar o projeto

```bash
python Sistema_de_Auditoria.py
```

### 5. Acessar no navegador

```text
http://127.0.0.1:5000
```

## 📊 Endpoints Disponíveis

### Itens

```http
GET /api/itens
POST /api/itens
GET /api/itens/<id>
PUT /api/itens/<id>
DELETE /api/itens/<id>
```

### Movimentação

```http
POST /api/movimentar
```

### Auditoria

```http
GET /api/historico
```

### Dashboard

```http
GET /api/stats
```

### Categorias

```http
GET /api/categorias
```

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido com fins educacionais e de portfólio para praticar conceitos de:

* Desenvolvimento Back-End
* APIs REST
* Banco de Dados Relacional
* ORM com SQLAlchemy
* Controle de Estoque
* Auditoria de Dados
* Versionamento com Git e GitHub

## 📚 Aprendizados

Durante o desenvolvimento foram aplicados conceitos como:

* CRUD completo
* Modelagem de banco de dados
* Relacionamentos entre tabelas
* Geração de QR Codes
* Estruturação de APIs REST
* Controle de inventário
* Boas práticas com Flask

## 👨‍💻 Autor

Ryan Oliveira

GitHub:
https://github.com/RyanOliveiraCr7

LinkedIn:
(Adicione aqui o link do seu perfil)

---

⭐ Se este projeto foi útil para você, deixe uma estrela no repositório.
