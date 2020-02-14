import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User


@api.route('/participants/<int:id>/systems')
def get_participant_systems(id):
    pass  # TODO: return all systems deployed at site with id. return as dictionary with ids as keys and names as values


@api.route('/participants/<int:id>/sessions')
def get_participant_sessions(id):
    pass  # TODO: return all sessions of site