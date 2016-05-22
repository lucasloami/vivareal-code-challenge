# import os
from api import app
import unittest
import json

class ApiTestCase(unittest.TestCase):

  def setUp(self):
    app.config['TESTING'] = True
    self.app = app.test_client()

  def tearDown(self):
    app.config['TESTING'] = False

  def test_404_code(self):
    rv = self.app.get('/')
    self.assertEqual(404, rv.status_code)

  def test_get_property(self):
    rv = self.app.get('/properties/1')
    keys = json.loads(rv.data).keys()
    expected_keys = ['id', 'x', 'y', 'provinces', 'squareMeters', 'beds', 'baths']
    self.assertEqual(sorted(keys), sorted(expected_keys))

  def test_get_property_with_id_zero(self):
    rv = self.app.get('/properties/0')
    data = json.loads(rv.data)
    expected_is_valid = False
    msg_not_blank = True
    self.assertEqual(expected_is_valid, data[0]['is_valid'])
    self.assertEqual(msg_not_blank, data[0]['msg'] is not '')

  def test_get_properties_without_args(self):
    rv = self.app.get('/properties')
    data = json.loads(rv.data)
    expected_keys = ['message']
    key = data.keys()
    self.assertEqual(sorted(expected_keys), sorted(key))

  def test_get_properties(self):
    args = dict(ax=88, ay=200, bx=100, by=200)
    rv = self.app.get('/properties', data=args)
    data = json.loads(rv.data)
    expected_keys = ['foundProperties', 'properties']
    keys = data.keys()
    self.assertEqual(sorted(expected_keys), sorted(keys))

  def test_get_properties_wrong_args(self):
    args = dict(ax=88, ay=2000, bx=100, by=200)
    rv = self.app.get('/properties', data=args)
    data = json.loads(rv.data)
    expected_keys = ['is_valid', 'msg']
    keys = data[0].keys()
    expected_is_valid = False
    msg_not_blank = True
    self.assertEqual(sorted(expected_keys), sorted(keys))
    self.assertEqual(expected_is_valid, data[0]['is_valid'])
    self.assertEqual(msg_not_blank, data[0]['msg'] is not '')

# if __name__ == '__main__':
#     unittest.main()