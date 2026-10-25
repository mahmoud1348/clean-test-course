from api.controllers import Delivery
class MockModel:
  def __init__(self, **fields):
    for field, value in fields.items():
      setattr(self, field, value)


class MockSet(list):
  def add(self, item):
    self.append(item)

def test_LotsOfItems():
  #Arrange
  order = MockSet()
  order.add(MockModel(quantity=5))
  order.add(MockModel(quantity=5))
  order.add(MockModel(quantity=5))
  delivery_distance = 6
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 7.5

def test_MiddleOfTheRoadItems():
  #Arrange
  order = MockSet()
  order.add(MockModel(quantity=2))
  order.add(MockModel(quantity=2))
  order.add(MockModel(quantity=2))
  delivery_distance = 4
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 5

def test_LittleItems():
  #Arrange
    order = MockSet()
    order.add(MockModel(quantity=3))
    order.add(MockModel(quantity=1))
    delivery_distance = 2
  #Act
    cost = Delivery.calculate(order,delivery_distance)
  #Assert
    assert cost == 3.50

