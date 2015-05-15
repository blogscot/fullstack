from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

  return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):

  if request.method == 'POST':

    newItem = MenuItem(name = request.form['name'], 
        price = request.form['price'],
        description = request.form['description'],
      restaurant_id = restaurant_id)
    session.add(newItem)
    session.commit()

    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    return render_template('new_menu_item.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()

  return render_template('edit_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, name=menuItem.name, price=menuItem.price, description=menuItem.description)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"



if __name__ == "__main__":
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)