import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pedido_db_dev_z6u8_user:iS24WyCcENsNGlRYCqpPMYVkuZsqtlEM@dpg-d8fo5c58nd3s738r5360-a/pedido_db_dev_z6u8")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    
    class Base(DeclarativeBase):
        pass
