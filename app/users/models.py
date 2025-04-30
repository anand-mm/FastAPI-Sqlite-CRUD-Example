from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func

Base = declarative_base()

class ExpoLogin(Base):
    __tablename__ = "expo_login"
    
    id = Column(Integer, primary_key=True, index=True)
    loginid = Column(String(50), unique=True, index=True)
    password = Column(String(150), nullable=False)
    usertype = Column(String(20))
    createddate = Column(TIMESTAMP(timezone=True), server_default=func.now())
    createdby = Column(Integer)