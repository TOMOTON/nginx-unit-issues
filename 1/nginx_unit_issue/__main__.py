import connexion


issues_api = connexion.FlaskApp(__name__, port=9090, specification_dir='openapi/')
issues_api.add_api('issues-api.yaml', arguments={'title': 'Issues Example'}, options={'swagger_ui': False})
issues_api.app.config.from_pyfile('config.py')


if __name__ == '__main__':
    issues_api.run()