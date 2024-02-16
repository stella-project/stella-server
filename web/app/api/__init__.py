from flask import Blueprint


api = Blueprint("api", __name__)

"""
since many of these modules need to import the api blueprint referenced here, 
the imports are done at the bottom to help prevent errors due to circular dependencies.
"""
from . import (
    authentication,
    sessions,
    rankings,
    recommendations,
    feedbacks,
    sites,
    participants,
    systems,
)
