from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


def printMenuItem(item):
  print 'Restaurant: ' + item.restaurant.name
  # print item.course
  print item.name
  print item.description
  print item.price + '\n'
  

def printMenuItems(items):

  for item in items:
    print 'Restaurant: ' + item.restaurant.name
    # print item.course
    print item.name
    print item.description
    print item.price + '\n'

def setNewPrice(items):

  for item in items:
    if (item.price != "$2.99"):
      item.price = "$2.99"

      session.add(item)
      session.commit()


menuItem = session.query(MenuItem).filter_by(restaurant_id='4', id='18').one()
printMenuItem(menuItem)

# Example Use Cases

# item = session.query(Restaurant).first()
# item.name = "Iain's Pizza Palace"
# session.add(item)
# session.commit()

# printMenuItem(item)
# session.delete(item)
# session.commit()

# restaurant1 = session.query(Restaurant).filter_by(name="Urban Burger").one()
# items = session.query(MenuItem).filter_by(name="Veggie Burger").all()
# # setNewPrice(items)
# print printMenuItems(items)
