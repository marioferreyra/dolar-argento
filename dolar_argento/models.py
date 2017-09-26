import datetime
from sqlalchemy import (Column, Integer, String, DateTime, Time, Date, Float,
                        ForeignKey, create_engine, UniqueConstraint,
                        func, and_)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_engine(uri=None):
    if not uri:
        uri = 'sqlite:///cotizaciones.db'
    engine = create_engine(uri, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine=None):
    if not engine:
        engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def add_data(data, session=None):
    if not session:
        session = get_session()
    if isinstance(data, list):
        for __ in data:
            try:
                session.add(__)
                session.commit()
            except Exception as e:
                session.rollback()
    else:
        session.add(data)
        session.commit()


def get_bancos(session):
    return session.query(Banco).all()


def get_last_cotizaciones(date, session):

    subq = session.query(
        Cotizacion.banco_id,
        func.max(Cotizacion.time).label('lastone')
    ).filter(
        Cotizacion.date == date.date()
    ).group_by(Cotizacion.banco_id).subquery('t2')

    cotizaciones = session.query(Cotizacion).join(
        subq,
        and_(
            Cotizacion.banco_id == subq.c.banco_id,
            Cotizacion.date == date.date(),
            Cotizacion.time == subq.c.lastone
        )
    ).all()

    return cotizaciones


class Banco(Base):
    """docstring for Banco"""
    __tablename__ = 'banco'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    cotizaciones = relationship("Cotizacion", backref="banco")

    __table_args__ = (
        UniqueConstraint(
            'name',
            'url',
            name='_banco_uc'
        ),
    )

    def __str__(self):
        return self.name


class Cotizacion(Base):
    """docstring for Cotizacion"""
    __tablename__ = 'cotizacion'

    id = Column(Integer, primary_key=True)
    compra = Column(Float)
    venta = Column(Float)
    date = Column(Date)
    time = Column(Time)
    banco_id = Column(Integer, ForeignKey('banco.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return "Banco {0} en {1}: Compra=${2} Venta=${3}".format(
            self.banco.name,
            self.date,
            self.compra,
            self.venta
        )

    def check_unique(self):
        session = get_session()
        query = session.query(Cotizacion).filter(
            Cotizacion.date == self.date,
            Cotizacion.time == self.time,
            Cotizacion.banco == self.banco).exists()
        return not session.query(query).scalar()

    @property
    def timestamp(self):
        return "{0} {1}".format(
            self.date.strftime("%d/%m/%Y"),
            self.time.strftime("%H:%M")
        )
