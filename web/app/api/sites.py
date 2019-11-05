from . import api


@api.route('/sites/<int:id>/users/')
def get_site_users(id):
    return 'TODO: return a list of users'
