import json
import os

class Province:
  data = None
  db_path = os.path.join(os.path.dirname(__file__), '../databases/database_provinces.json')
  required_attr = []

  def __init__(self):
    with open(self.db_path, 'r') as f:
      self.data = json.loads(f.read())
      f.close()

  def save(self):
    pass

  def delete(self, identifier):
    pass


  ############################
  # LOADS DATA

  # Simulates db connection and access to data

  def __loads_json(func):
    def wrapper(*args):
      cls = args[0]
      with open(cls.db_path, 'r') as f:
        cls.data = json.loads(f.read())
        f.close()
        return func(*args)

    return wrapper

  ############################
  # CLASS METHODS
  @classmethod
  @__loads_json
  def where(cls, x, y):
    results = []
    for province_name in cls.data:
      ax  = cls.data[province_name]['boundaries']['upperLeft']['x']
      ay  = cls.data[province_name]['boundaries']['upperLeft']['y']
      bx  = cls.data[province_name]['boundaries']['bottomRight']['x']
      by  = cls.data[province_name]['boundaries']['bottomRight']['y']

      if x > ax and x < bx and y < ay and y > by:
        results.append(province_name)

    return results

  @classmethod
  @__loads_json
  def first(cls):
    return sorted(cls.data)[0]

  @classmethod
  @__loads_json
  def last(cls):
    return sorted(cls.data)[-1]

  @classmethod
  @__loads_json
  def find(cls, identifier):
    pass

  @classmethod
  @__loads_json
  def find_by(cls, condition = {}):
    pass

  @classmethod
  @__loads_json
  def count(cls):
    return len(cls.data.keys())

  @classmethod
  @__loads_json
  def all(cls):
    return cls.data


# a = Province()
# a.loads_json()
# print(Province.count())
# print(Province.first())
# print(Province.last())
# print(Province.where(88, 521))