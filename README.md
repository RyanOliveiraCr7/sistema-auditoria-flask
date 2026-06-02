# 📦 Sistema de Auditoria de Estoque

Sistema web desenvolvido em **Python + Flask** para gerenciamento e auditoria de estoque. Permite cadastrar itens, registrar movimentações de entrada e saída, acompanhar histórico completo de auditorias e visualizar alertas de estoque crítico em tempo real.

---

## 🖥️ Interface

A aplicação possui uma interface web interativa com três seções principais:

- **Dashboard** — cards com estatísticas em tempo real e tabela de itens com estoque crítico
- **Itens** — listagem completa com busca, filtro por categoria e ações de cadastro, edição, movimentação e exclusão
- **Histórico** — log completo de todas as movimentações registradas

---

## 🚀 Funcionalidades

- Cadastro, edição e exclusão de itens de estoque
- Controle de entrada, saída e ajuste de quantidade
- Alertas automáticos de estoque crítico e baixo
- Histórico completo de auditorias com data, hora e método
- Dashboard com estatísticas gerais (total de itens, unidades, críticos, movimentações do dia)
- Geração automática de QR Code para cada item cadastrado
- API REST completa para integração com outros sistemas
- Dados persistidos em banco SQLite local
- Dados de demonstração carregados automaticamente no primeiro uso

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3, Flask, Flask-SQLAlchemy |
| Banco de dados | SQLite (via SQLAlchemy ORM) |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Utilitários | QRCode, Pillow |

---

## 📁 Estrutura do Projeto

```
sistema-auditoria-flask/
│
├── static/
│   └── qrcodes/          # QR Codes gerados automaticamente
│
├── templates/
│   └── index.html        # Interface web completa (SPA)
│
├── instance/
│   └── auditoria.db      # Banco de dados SQLite (gerado na 1ª execução)
│
├── Sitema_de_Auditoria.py  # Aplicação principal (backend + API)
├── .gitignore
└── README.md
```

---

## ⚙️ Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/RyanOliveiraCr7/sistema-auditoria-flask.git
cd sistema-auditoria-flask
```

**2. Instale as dependências**
```bash
pip install flask flask-sqlalchemy qrcode pillow
```

**3. Execute a aplicação**
```bash
python Sitema_de_Auditoria.py
```

**4. Acesse no navegador**
```
http://127.0.0.1:5000
```

> Na primeira execução, o banco de dados é criado automaticamente e 6 itens de demonstração são inseridos.

---

## 🔌 Endpoints da API

A aplicação expõe uma API REST completa. Todos os endpoints retornam e recebem JSON.

### Itens

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/itens` | Lista todos os itens (aceita `?q=busca` e `?categoria=X`) |
| `POST` | `/api/itens` | Cadastra um novo item |
| `GET` | `/api/itens/<id>` | Retorna um item específico |
| `PUT` | `/api/itens/<id>` | Atualiza dados de um item |
| `DELETE` | `/api/itens/<id>` | Remove um item e seu histórico |

**Exemplo de payload para `POST /api/itens`:**
```json
{
  "codigo": "TOOL-001",
  "nome": "Chave de Fenda",
  "categoria": "Ferramentas",
  "quantidade": 10,
  "minimo": 3,
  "localizacao": "Galpão A",
  "descricao": "Phillips tamanho médio"
}
```

### Movimentações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/movimentar` | Registra entrada, saída ou ajuste |

**Payload:**
```json
{
  "item_id": 1,
  "tipo": "entrada",
  "quantidade": 5,
  "obs": "Reposição mensal"
}
```

> Tipos disponíveis: `entrada`, `saida`, `ajuste`

### Consultas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/historico` | Histórico de movimentações (aceita `?item_id=X`) |
| `GET` | `/api/stats` | Estatísticas gerais do estoque |
| `GET` | `/api/categorias` | Lista de categorias distintas |
| `POST` | `/api/scan` | Busca item por código (barcode/QR) |

---

## 📊 Status de Estoque

Cada item recebe um status automático com base na quantidade atual e no estoque mínimo definido:

| Status | Condição | Cor |
|--------|----------|-----|
| `ok` | Quantidade acima de 120% do mínimo | 🟢 Verde |
| `baixo` | Quantidade entre 100% e 120% do mínimo | 🟡 Amarelo |
| `critico` | Quantidade abaixo do mínimo | 🔴 Vermelho |

---

## 🎯 Objetivo do Projeto

Projeto desenvolvido para fins educacionais e de portfólio, praticando conceitos de:

- Desenvolvimento back-end com Flask e ORM
- Design e consumo de APIs REST
- Banco de dados relacional com SQLAlchemy
- Frontend interativo com JavaScript puro (fetch API, manipulação de DOM)
- Controle de estoque e auditoria de dados

---

## 👨‍💻 Autor

**Ryan Oliveira**

[![GitHub](https://img.shields.io/badge/GitHub-RyanOliveiraCr7-181717?logo=github)](https://github.com/RyanOliveiraCr7)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-ryan--oliveira-0A66C2?logo=linkedin)](https://www.linkedin.com/in/ryan-oliveira-a2b5591a8/)
