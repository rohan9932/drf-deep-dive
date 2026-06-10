## For generation graph models
- Command: ./manage.py graph_models api > models.dot
- Then copy the code from models.dot and paste to graphviz online

## For testing:
- use test.py
- use TestCase class where it has a self.client


## JWT Auth
- we use simplejwtauthentication as it doesn't need lookup in database
- have userid in the payload of the token so doesn't need to lookup in the database