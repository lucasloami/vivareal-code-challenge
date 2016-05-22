import json
from province import Province
import os

class Property:
  data = None
  db_path = os.path.join(os.path.dirname(__file__), '../databases/database_properties.json')
  required_attr = ['x', 'y', 'beds', 'baths', 'squareMeters']
  error_result = []

  def __init__(self):
    with open(self.db_path, 'r') as f:
      self.data = json.loads(f.read())
      f.close()

  ############################
  # DECORATOR FUNCTIONS

  # Simulates db connection and access to data
  def __loads_json(func):
    def wrapper(*args):
      cls = args[0]
      with open(cls.db_path, 'r') as f:
        cls.data = json.loads(f.read())
        f.close()
        return func(*args)

    return wrapper

  # Perform all the validations in the data

  def __validate_points(func):
    def wrapper(*args):
      cls = args[0]
      point_a = args[1]
      point_b = args[2]

      if 'ax' not in point_a or 'ay' not in point_a or 'bx' not in point_b or 'by' not in point_b:
        cls.error_result.append({'is_valid': False, 'msg': 'Erro! point_a ou point_b com estrutura errada'})

      else:
        if point_a['ax'] < 0 or point_b['bx'] < 0 or point_a['ax'] > 1400 or point_b['bx'] > 1400:
          cls.error_result.append( {'is_valid': False, 'msg': 'Erro! valor de x dos pontos A e/ou B estao fora do range'})

        if point_a['ay'] < 0 or point_b['by'] < 0 or point_a['ay'] > 1000 or point_b['by'] > 1000:
          cls.error_result.append( {'is_valid': False, 'msg': 'Erro! valor de y dos pontos A e/ou B estao fora do range'})

      return func(*args)

    return wrapper

  def __validate_property_constraints(func):
    def wrapper(self):
      if self.error_result:
        return func(self)

      if self.beds > 5 or self.beds < 1:
        self.error_result.append( {'is_valid': False, 'msg': 'Erro! O imovel deve ter entre 1 e 5 quartos'})

      if self.baths > 4 or self.baths < 1:
        self.error_result.append( {'is_valid': False, 'msg': 'Erro! O imovel deve ter entre 1 e 4 banheiros'})

      if self.squareMeters > 240 or self.squareMeters < 20:
        self.error_result.append( {'is_valid': False, 'msg': 'Erro! O imovel deve ter entre 20 e 240 m2'})

      return func(self)

    return wrapper

  def __validate_required_attr(func):
    def wrapper(self):
      for req_attr in self.required_attr:
        if not hasattr(self, req_attr):
          self.error_result.append( {'is_valid': False, 'msg': 'Erro! O atributo ' + req_attr +' e obrigatorio'})

      return func(self)

    return wrapper

  def __validate_identifier(func):
    def wrapper(*args):
      cls = args[0]
      identifier = args[1]

      if identifier == 0:
        cls.error_result.append( {'is_valid': False, 'msg': 'Erro! ID nao pode ser 0 (zero)'})

      return func(*args)

    return wrapper


  ############################
  # INSTANCE FUNCTIONS

  @__validate_required_attr
  @__validate_property_constraints
  def save(self):
    if self.error_result:
      return self.return_error()

    last_el = self.last()

    prop = {
      "id": int(last_el['id']) + 1,
      "x": self.x,
      "y": self.y,
      "beds": self.beds,
      "baths": self.baths,
      "squareMeters": self.squareMeters
    }

    self.data['properties'].append(prop)
    self.data['totalProperties'] = len(self.data['properties'])

    with open(self.db_path, 'w') as f:
      f.write(json.dumps(self.data))
      f.close()

    return prop

  def delete(self, identifier):
    pass


  ############################
  # CLASS METHODS

  @classmethod
  def return_error(cls):
    error = cls.error_result
    cls.error_result = []
    return error

  @classmethod
  @__loads_json
  @__validate_points
  def where(cls, point_a = {}, point_b = {}):
    if cls.error_result:
      return cls.return_error()

    results = {'properties': []}

    ax = point_a['ax']
    ay = point_a['ay']
    bx = point_b['bx']
    by = point_b['by']

    for prop in cls.data['properties']:
      if prop['x'] > ax and prop['x'] < bx and prop['y'] < ay and prop['y'] > by:
        results['properties'].append(prop)

    results['foundProperties'] = len(results['properties'])

    return results

  @classmethod
  @__loads_json
  def first(cls):
    return cls.many2many(cls.data["properties"][0])

  @classmethod
  @__loads_json
  def last(cls):
    return cls.many2many(cls.data["properties"][-1])

  @classmethod
  @__loads_json
  @__validate_identifier
  def find(cls, identifier):
    if cls.error_result:
      return cls.return_error()

    return cls.many2many(cls.data["properties"][identifier-1])

  @classmethod
  @__loads_json
  def find_by(cls, condition = {}):
    key = condition.keys()[0]
    value = condition[key]
    result = ''

    for prop in cls.data["properties"]:
      if prop[key] == value:
        result = prop
        break

    return cls.many2many(result)

  @classmethod
  @__loads_json
  def count(cls):
    return cls.data['totalProperties']

  @classmethod
  @__loads_json
  def all(cls):
    return cls.data["properties"]

  @staticmethod
  def many2many(prop):
    province = Province.where(prop['x'], prop['y'])
    prop['provinces'] = province
    return prop


# a = Property()
# a.x = 10
# a.y = 20
# a.beds = 5
# a.baths = 3
# a.squareMeters = 15
# print(a.save())
# print(Property.count())
# print(Property.first())
# print(Property.last())
# print(Property.find(3))
# print(Property.find_by({"squareMeters": 158}))
# print(Property.where({'ax': 5, 'ay': 500}, {'bx': 10, 'by': 200}))
# print(Property.where({'ax': 20000, 'ay': 200}, {'bx': 100, 'by': 200}))
# print(Property.where({'ax': 88, 'ay': 200}, {'bx': 100, 'by': 200}))
