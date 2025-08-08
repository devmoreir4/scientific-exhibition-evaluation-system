from .extensions import db

work_evaluator_association = db.Table(
    'work_evaluator_association',
    db.Column('work_id', db.Integer, db.ForeignKey('work.id'), primary_key=True),
    db.Column('evaluator_id', db.Integer, db.ForeignKey('evaluator.id'), primary_key=True)
)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Evaluator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    siape_or_cpf = db.Column(db.String(20), unique=True, nullable=False)
    birthdate = db.Column(db.String(8), nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    area = db.Column(db.String(100), nullable=False)
    subareas = db.Column(db.String(255), nullable=True)  # separadas por ponto e vírgula (;)
    workload = db.Column(db.Integer, default=0)
    evaluations = db.relationship('Evaluation', backref='evaluator', lazy=True)
    works = db.relationship('Work', secondary=work_evaluator_association, back_populates='evaluators')

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)  # separados por vírgula (,)
    advisor = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'poster_banner' ou 'oral_presentation'
    area = db.Column(db.String(100), nullable=False)
    subarea = db.Column(db.String(100), nullable=False)
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

class DistributionControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distributed = db.Column(db.Boolean, nullable=False, default=False)
    distributed_at = db.Column(db.DateTime, nullable=True)
    distributed_by = db.Column(db.String(120), nullable=True)

    @classmethod
    def is_distributed(cls):
        control = cls.query.first()
        return control and control.distributed

    @classmethod
    def mark_as_distributed(cls, admin_name):
        from datetime import datetime
        control = cls.query.first()
        if not control:
            control = cls(distributed=True, distributed_at=datetime.utcnow(), distributed_by=admin_name)
            db.session.add(control)
        else:
            control.distributed = True
            control.distributed_at = datetime.utcnow()
            control.distributed_by = admin_name
        db.session.commit()

    @classmethod
    def reset_distribution(cls):
        control = cls.query.first()
        if control:
            control.distributed = False
            control.distributed_at = None
            control.distributed_by = None

            Evaluation.query.delete()

            db.session.execute(work_evaluator_association.delete())

            evaluators = Evaluator.query.all()
            for evaluator in evaluators:
                evaluator.workload = 0

            db.session.commit()
