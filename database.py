# database.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'janitorial_app.db')

engine = create_engine(f'sqlite:///{DB_PATH}', echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define Models

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    payment_terms = Column(String)
    contact_info = Column(String)
    jobs = relationship('Job', back_populates='company', cascade="all, delete-orphan")

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job_type = Column(String, nullable=False)
    status = Column(String, default='pending')  # pending, in progress, complete
    company_id = Column(Integer, ForeignKey('companies.id'))
    created_at = Column(DateTime, default=func.now())
    company = relationship('Company', back_populates='jobs')
    invoice = relationship('Invoice', uselist=False, back_populates='job', cascade="all, delete-orphan")

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    amount = Column(Float, nullable=False)
    pdf_path = Column(String)
    job = relationship('Job', back_populates='invoice')

# Create Tables
def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
