from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import qrcode
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auditoria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

QR_DIR = os.path.join(os.path.dirname(__file__), 'static', 'qrcodes')
os.makedirs(QR_DIR, exist_ok=True)

# ── Models ──────────────────────────────────────────────────────────────────

class Item(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    codigo      = db.Column(db.String(100), unique=True, nullable=False)
    nome        = db.Column(db.String(200), nullable=False)
    descricao   = db.Column(db.Text, default='')
    categoria   = db.Column(db.String(100), default='Geral')
    quantidade  = db.Column(db.Integer, default=0)
    minimo      = db.Column(db.Integer, default=0)
    localizacao = db.Column(db.String(200), default='')
    criado_em   = db.Column(db.DateTime, default=datetime.utcnow)
    auditado_em = db.Column(db.DateTime, nullable=True)
    qr_path     = db.Column(db.String(300), default='')

    def to_dict(self):
        return {
            'id':          self.id,
            'codigo':      self.codigo,
            'nome':        self.nome,
            'descricao':   self.descricao,
            'categoria':   self.categoria,
            'quantidade':  self.quantidade,
            'minimo':      self.minimo,
            'localizacao': self.localizacao,
            'criado_em':   self.criado_em.strftime('%d/%m/%Y %H:%M') if self.criado_em else '',
            'auditado_em': self.auditado_em.strftime('%d/%m/%Y %H:%M') if self.auditado_em else 'Nunca',
            'status':      'critico' if self.quantidade < self.minimo else ('baixo' if self.quantidade <= self.minimo * 1.2 else 'ok'),
            'qr_path':     self.qr_path,
        }

class Auditoria(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    item_id     = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_codigo = db.Column(db.String(100))
    item_nome   = db.Column(db.String(200))
    tipo        = db.Column(db.String(50))   # entrada | saida | ajuste | scan
    qtd_antes   = db.Column(db.Integer)
    qtd_depois  = db.Column(db.Integer)
    variacao    = db.Column(db.Integer)
    metodo      = db.Column(db.String(50), default='manual')  # manual | barcode | qrcode
    obs         = db.Column(db.Text, default='')
    registrado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'item_codigo':  self.item_codigo,
            'item_nome':    self.item_nome,
            'tipo':         self.tipo,
            'qtd_antes':    self.qtd_antes,
            'qtd_depois':   self.qtd_depois,
            'variacao':     self.variacao,
            'metodo':       self.metodo,
            'obs':          self.obs,
            'registrado_em': self.registrado_em.strftime('%d/%m/%Y %H:%M:%S'),
        }

# ── Helpers ──────────────────────────────────────────────────────────────────

def gerar_qr(codigo):
    img = qrcode.make(codigo)
    fname = f'qr_{codigo.replace("/","_")}.png'
    path  = os.path.join(QR_DIR, fname)
    img.save(path)
    return f'qrcodes/{fname}'

def registrar_auditoria(item, tipo, qtd_antes, qtd_depois, metodo='manual', obs=''):
    aud = Auditoria(
        item_id     = item.id,
        item_codigo = item.codigo,
        item_nome   = item.nome,
        tipo        = tipo,
        qtd_antes   = qtd_antes,
        qtd_depois  = qtd_depois,
        variacao    = qtd_depois - qtd_antes,
        metodo      = metodo,
        obs         = obs,
    )
    db.session.add(aud)
    item.auditado_em = datetime.utcnow()

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

# Items CRUD
@app.route('/api/itens', methods=['GET'])
def listar_itens():
    q = request.args.get('q', '')
    cat = request.args.get('categoria', '')
    query = Item.query
    if q:
        query = query.filter(db.or_(Item.nome.ilike(f'%{q}%'), Item.codigo.ilike(f'%{q}%')))
    if cat:
        query = query.filter(Item.categoria == cat)
    itens = query.order_by(Item.nome).all()
    return jsonify([i.to_dict() for i in itens])

@app.route('/api/itens', methods=['POST'])
def criar_item():
    d = request.json
    if Item.query.filter_by(codigo=d['codigo']).first():
        return jsonify({'erro': 'Código já cadastrado'}), 400
    item = Item(
        codigo      = d['codigo'],
        nome        = d['nome'],
        descricao   = d.get('descricao', ''),
        categoria   = d.get('categoria', 'Geral'),
        quantidade  = int(d.get('quantidade', 0)),
        minimo      = int(d.get('minimo', 0)),
        localizacao = d.get('localizacao', ''),
    )
    item.qr_path = gerar_qr(d['codigo'])
    db.session.add(item)
    if item.quantidade > 0:
        db.session.flush()
        registrar_auditoria(item, 'entrada', 0, item.quantidade, 'manual', 'Cadastro inicial')
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route('/api/itens/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())

@app.route('/api/itens/<int:id>', methods=['PUT'])
def atualizar_item(id):
    item = Item.query.get_or_404(id)
    d = request.json
    item.nome        = d.get('nome', item.nome)
    item.descricao   = d.get('descricao', item.descricao)
    item.categoria   = d.get('categoria', item.categoria)
    item.minimo      = int(d.get('minimo', item.minimo))
    item.localizacao = d.get('localizacao', item.localizacao)
    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/api/itens/<int:id>', methods=['DELETE'])
def deletar_item(id):
    item = Item.query.get_or_404(id)
    Auditoria.query.filter_by(item_id=id).delete()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'ok': True})

# Scan (barcode / qr)
@app.route('/api/scan', methods=['POST'])
def scan():
    d = request.json
    codigo = d.get('codigo', '').strip()
    metodo = d.get('metodo', 'barcode')
    item = Item.query.filter_by(codigo=codigo).first()
    if not item:
        return jsonify({'erro': 'Item não encontrado', 'codigo': codigo}), 404
    return jsonify({'item': item.to_dict(), 'metodo': metodo})

# Movimentações
@app.route('/api/movimentar', methods=['POST'])
def movimentar():
    d = request.json
    item = Item.query.get_or_404(d['item_id'])
    tipo    = d['tipo']           # entrada | saida | ajuste
    qtd     = int(d['quantidade'])
    metodo  = d.get('metodo', 'manual')
    obs     = d.get('obs', '')
    antes   = item.quantidade

    if tipo == 'entrada':
        item.quantidade += qtd
    elif tipo == 'saida':
        if item.quantidade < qtd:
            return jsonify({'erro': 'Estoque insuficiente'}), 400
        item.quantidade -= qtd
    elif tipo == 'ajuste':
        item.quantidade = qtd

    registrar_auditoria(item, tipo, antes, item.quantidade, metodo, obs)
    db.session.commit()
    return jsonify(item.to_dict())

# Histórico
@app.route('/api/historico', methods=['GET'])
def historico():
    item_id = request.args.get('item_id')
    query   = Auditoria.query
    if item_id:
        query = query.filter_by(item_id=item_id)
    registros = query.order_by(Auditoria.registrado_em.desc()).limit(200).all()
    return jsonify([r.to_dict() for r in registros])

# Dashboard stats
@app.route('/api/stats', methods=['GET'])
def stats():
    total_itens    = Item.query.count()
    total_estoque  = db.session.query(db.func.sum(Item.quantidade)).scalar() or 0
    criticos       = Item.query.filter(Item.quantidade < Item.minimo).count()
    categorias     = db.session.query(Item.categoria, db.func.count(Item.id)).group_by(Item.categoria).all()
    mov_hoje       = Auditoria.query.filter(
        db.func.date(Auditoria.registrado_em) == datetime.utcnow().date()
    ).count()
    return jsonify({
        'total_itens':   total_itens,
        'total_estoque': total_estoque,
        'criticos':      criticos,
        'mov_hoje':      mov_hoje,
        'categorias':    [{'cat': c, 'total': t} for c, t in categorias],
    })

# Categorias
@app.route('/api/categorias', methods=['GET'])
def categorias():
    cats = db.session.query(Item.categoria).distinct().order_by(Item.categoria).all()
    return jsonify([c[0] for c in cats])

# QR image
@app.route('/static/qrcodes/<path:fname>')
def qr_img(fname):
    return send_from_directory(QR_DIR, fname)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # seed demo
        if Item.query.count() == 0:
            demo = [
                ('TOOL-001', 'Chave de Fenda Phillips', 'Ferramentas', 15, 5, 'Galpão A'),
                ('TOOL-002', 'Martelo 500g', 'Ferramentas', 8, 3, 'Galpão A'),
                ('EPI-001', 'Capacete de Segurança', 'EPI', 22, 10, 'Almoxarifado'),
                ('EPI-002', 'Luva de Proteção', 'EPI', 3, 15, 'Almoxarifado'),
                ('ELECT-001', 'Multímetro Digital', 'Elétrica', 6, 2, 'Lab Elétrica'),
                ('CONS-001', 'Parafuso M6x20', 'Consumíveis', 450, 100, 'Prateleira B3'),
            ]
            for cod, nome, cat, qtd, minimo, loc in demo:
                it = Item(codigo=cod, nome=nome, categoria=cat,
                          quantidade=qtd, minimo=minimo, localizacao=loc)
                it.qr_path = gerar_qr(cod)
                db.session.add(it)
                db.session.flush()
                registrar_auditoria(it, 'entrada', 0, qtd, 'manual', 'Carga inicial demo')
            db.session.commit()
    app.run(debug=True, port=5000)