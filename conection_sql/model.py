from operator import index
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from conection_sql.conection import Base, SessionLocal, engine




class TripAdvisorTable(Base):
    __tablename__ = "tripadvisor"
    
    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String(50))
    titulo = Column(String(100))
    review = Column(String(800))
    estadia = Column(String(50))
    rating = Column(String(16))
    date_extract = Column(String(16))

class FacebookTable(Base):
    __tablename__ = "facebook"
    
    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String(50))
    review = Column(String(800))
    date_extract = Column(String(16))

class GoogleTable(Base):
    __tablename__ = "google"
    
    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String(50))
    ranking = Column(String(16))
    fecha = Column(String(30))
    review = Column(String(800))
    date_extract = Column(String(16))

class BookingTable(Base):
    __tablename__ = "booking"
    
    id = Column(Integer, primary_key = True, index = True)
    nombre           = Column(String(50))
    Fecha_comentario = Column(String(50))
    rating           = Column(String(20))
    titulo           = Column(String(100))
    review_good      = Column(String(2000))
    review           = Column(String(2000))
    date_extract     = Column(String(30))
    
class ExpediaTable(Base):
    __tablename__ = "expedia"
    
    id           = Column(Integer, primary_key = True, index = True)
    nombre       = Column(String(50))
    conceptop    = Column(String(100))
    fecha_review = Column(String(30))
    critica      = Column(String(200))
    review       = Column(String(1000))
    estadia      = Column(String(100))
    date_extract = Column(String(30))