from flask import Blueprint

evaluator_bp = Blueprint('evaluator', __name__)

from .works import *
from .evaluations import *
from .password import * 