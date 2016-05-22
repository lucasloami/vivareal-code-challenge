from flask_restful import Resource, reqparse
from ..models.property import Property

class PropertyAPI(Resource):

  def get(self, id):
    result = Property.find(id)
    return result

  def put(self, id):
    pass

  def delete(self, id):
    pass

class PropertyListAPI(Resource):
  def get(self):
    p = reqparse.RequestParser()
    p.add_argument('ax', type=int, required=True, help="ax e argumento obrigatorio")
    p.add_argument('ay', type=int, required=True, help="ay e argumento obrigatorio")
    p.add_argument('bx', type=int, required=True, help="bx e argumento obrigatorio")
    p.add_argument('by', type=int, required=True, help="by e argumento obrigatorio")

    args = p.parse_args()
    result = None

    point_a = {'ax': args['ax'], 'ay': args['ay']}
    point_b = {'bx': args['bx'], 'by': args['by']}
    result = Property.where(point_a, point_b)

    return result

  def post(self):
    p = reqparse.RequestParser()
    p.add_argument('x', type=int, required=True, help="x e argumento obrigatorio")
    p.add_argument('y', type=int, required=True, help="y e argumento obrigatorio")
    p.add_argument('baths', type=int, required=True, help="baths e argumento obrigatorio")
    p.add_argument('beds', type=int, required=True, help="beds e argumento obrigatorio")
    p.add_argument('squareMeters', type=int, required=True, help="squareMeters e argumento obrigatorio")

    args = p.parse_args()
    prop = Property()
    prop.x = args['x']
    prop.y = args['y']
    prop.beds = args['beds']
    prop.baths = args['baths']
    prop.squareMeters = args['squareMeters']

    result = prop.save()

    return result