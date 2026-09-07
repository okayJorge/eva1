from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100))
    rol = db.Column(db.String(20), default='admin')


class Residente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    medidor = db.Column(db.String(30))
    telefono = db.Column(db.String(30))
    activo = db.Column(db.Boolean, default=True)

    lecturas = db.relationship('LecturaAgua', backref='residente', lazy=True, cascade='all, delete-orphan')
    deudas_extra = db.relationship('DeudaExtra', backref='residente', lazy=True)


class Configuracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto_expensa = db.Column(db.Float, default=170)
    precio_m3 = db.Column(db.Float, default=8)
    precio_limpieza_edificio = db.Column(db.Float, default=400)
    precio_limpieza_parqueo = db.Column(db.Float, default=80)
    multa_mora = db.Column(db.Float, default=0)
    dia_limite_pago = db.Column(db.Integer, default=15)
    fecha_inicio_administracion = db.Column(db.Date)
    nombre_edificio = db.Column(db.String(120), default='Mi Edificio')


class MovimientoCaja(db.Model):
    """Libro diario: ingresos y egresos de caja/banco."""
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # INGRESO / EGRESO
    categoria = db.Column(db.String(50))
    detalle = db.Column(db.String(400), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    medio_pago = db.Column(db.String(20))  # Efectivo / Banco / QR
    residente_id = db.Column(db.Integer, db.ForeignKey('residente.id'), nullable=True)
    observaciones = db.Column(db.String(300))
    creado = db.Column(db.DateTime, default=datetime.utcnow)

    residente = db.relationship('Residente')


class LecturaAgua(db.Model):
    """Lectura mensual de medidor + cobro de expensa + agua."""
    id = db.Column(db.Integer, primary_key=True)
    residente_id = db.Column(db.Integer, db.ForeignKey('residente.id'), nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    fecha_lectura = db.Column(db.Date)
    lectura_anterior = db.Column(db.Float, default=0)
    lectura_actual = db.Column(db.Float, default=0)
    consumo_m3 = db.Column(db.Float, default=0)
    costo_agua = db.Column(db.Float, default=0)
    monto_expensa = db.Column(db.Float, default=0)
    multa = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    pagado = db.Column(db.Boolean, default=False)
    fecha_pago = db.Column(db.Date, nullable=True)
    observaciones = db.Column(db.String(300))


class DeudaExtra(db.Model):
    """Deudas especiales (prestamos, multas, otros) fuera de expensas/agua."""
    id = db.Column(db.Integer, primary_key=True)
    residente_id = db.Column(db.Integer, db.ForeignKey('residente.id'), nullable=True)
    nombre_deudor = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    concepto = db.Column(db.String(300))
    monto = db.Column(db.Float, default=0)
    pagado_monto = db.Column(db.Float, default=0)
