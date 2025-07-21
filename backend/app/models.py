from .extensions import db

work_evaluator_association = db.Table(
    'work_evaluator_association',
    db.Column('work_id', db.Integer, db.ForeignKey('work.id'), primary_key=True),
    db.Column('evaluator_id', db.Integer, db.ForeignKey('evaluator.id'), primary_key=True)
)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Evaluator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    siape_or_cpf = db.Column(db.String(20), unique=True, nullable=False)  # login
    birthdate = db.Column(db.String(8), nullable=False)  # password (formato DDMMAAAA)
    area = db.Column(db.String(100), nullable=False)  # área de atuação
    subareas = db.Column(db.String(255), nullable=True)  # subáreas de interesse, separadas por vírgula
    carga = db.Column(db.Integer, default=0)
    evaluations = db.relationship('Evaluation', backref='evaluator', lazy=True)
    works = db.relationship('Work', secondary=work_evaluator_association, back_populates='evaluators')

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    subarea = db.Column(db.String(100), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    has_technical_student = db.Column(db.Boolean, default=False)
    has_prototype = db.Column(db.Boolean, default=False)
    evaluations = db.relationship('Evaluation', backref='work', lazy=True)
    evaluators = db.relationship('Evaluator', secondary=work_evaluator_association, back_populates='works')

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    criterion1 = db.Column(db.Float, nullable=False)
    criterion2 = db.Column(db.Float, nullable=False)
    criterion3 = db.Column(db.Float, nullable=False)
    criterion4 = db.Column(db.Float, nullable=False)
    criterion5 = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(32), nullable=False, default='online')
    evaluator_id = db.Column(db.Integer, db.ForeignKey('evaluator.id'), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False) 