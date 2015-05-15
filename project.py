from flask import Flask, render_template, request, redirect, url_for, flash
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
    flash('New menu item created.')

    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    return render_template('new_menu_item.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):

  menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
  if request.method == 'POST':

    # find the original item and update it

    if menuItem != []:
      menuItem.name = request.form['name']
      menuItem.price = request.form['price']
      menuItem.description = request.form['description']
      session.add(menuItem)
      session.commit()
      flash('Menu item updated.')

    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    return render_template('edit_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=menuItem)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):

  menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()

  if request.method == 'POST':
    session.delete(menuItem)
    session.commit()
    flash('Menu item deleted.')

    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    return render_template('delete_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=menuItem)


if __name__ == "__main__":
  app.secret_key = 'the_pairs_sail_around_the_flying_monkeys'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)