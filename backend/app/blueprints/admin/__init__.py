from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from .users import *
from .works import *
from .sheets import *
from .misc import * 