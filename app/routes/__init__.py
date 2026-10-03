from flask import Blueprint

from app.routes.auth import auth_bp
from app.routes.index import index_bp
from app.routes.loop import loop_bp

blueprints = [auth_bp, index_bp, loop_bp]
