# from sqlalchemy.dialects.postgresql import JSON
from ..common import settings
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class PsnCategoryModel(base):
    __tablename__ = 'psn_game_category'

    id = Column(Integer, primary_key=True)
    category_url = Column(String)
    category_name = Column(String)
    game_id = Column(String)
