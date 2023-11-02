from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from helpers import token_required
from models import db, User, Book, book_schema, books_schema
from forms import ProfileButton, EditProfile
from flask_login import login_required, current_user

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = ProfileButton()
    try:
        if request.method == 'POST' and form.validate_on_submit():
        
            return redirect(url_for('api.editprofile', id = current_user.id))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('profile.html', form=form)

@api.route('/profile/<id>', methods = ['GET', 'POST'])
@login_required
def editprofile(id):
    form = EditProfile()
    user = User.query.get(id) 
    try:
        if request.method == 'POST' and form.validate_on_submit():

            if form.first_name.data == '':
                user.first_name = user.first_name
            else:
                user.first_name = form.first_name.data

            if form.last_name.data == '':
                user.last_name = user.last_name
            else:
                user.last_name = form.last_name.data

            if form.phone_number.data == '':
                user.phone_number = user.phone_number
            else:
                user.phone_number = form.phone_number.data
            
            if form.address.data == '':
                user.address = user.address
            else:
                user.address = form.address.data
            
            db.session.commit()

            flash(f'You have successfully created a vehicle trim')
            return redirect(url_for('api.profile'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('editprofile.html', form=form)

# @api.route('/vehicles', methods = ['GET', 'POST'])
# def selectvehicle():
#     form = VehiclesForm()
#     try:
#         if request.method == 'POST' and form.validate_on_submit():
#             print(form.data)
#             make = 'Tesla'
#             if form.submitModel3.data:
#                 model = 'model3'
#             elif form.submitModelS.data:
#                 model = 'models'
#             elif form.submitModelX.data:
#                 model = 'modelx'
#             elif form.submitModelY.data:
#                 model = 'modely'
#             year = '2023'
#             color = ''
#             trim = ''
#             cost = 0
#             try:
#                 user_token  = current_user.token
#             except:
#                 user_token = None

#             vehicle = Vehicle(make, model, year, color, trim, cost, user_token)

#             db.session.add(vehicle)
#             db.session.commit()

#             return redirect(url_for('api.selectcolortrim', id = vehicle.id))
#     except:
#         raise Exception('Invalid form data: Please check your form')
#     return render_template('vehicles.html', form=form)

# @api.route('/vehicles/<id>', methods = ['GET', 'POST'])
# def selectcolortrim(id):
#     form = ColorTrimForm()
#     vehicle = Vehicle.query.get(id) 

#     try:
#         if request.method == 'POST' and form.validate_on_submit():
#             color = form.color.data
#             trim = form.trim.data
#             if trim == "trim1":
#                 cost = 26490
#             elif trim == "trim2":
#                 cost = 34990
#             elif trim == "trim3":
#                 cost = 39990

#             vehicle.color = color
#             vehicle.trim = trim
#             vehicle.cost = cost

#             db.session.commit()

#             return render_template('index.html')
#     except:
#         raise Exception('Invalid form data: Please check your form')
#     return render_template(f'{vehicle.model}.html', form=form)

############################################################################

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    year = request.json['year']
    isbn = request.json['isbn']
    hardcover = request.json['hardcover']
    pagecount = request.json['pagecount']
    price = request.json['price']
    image = request.json['image']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, year, isbn, hardcover, pagecount, price, image, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    book = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(book)
    return jsonify(response)

@api.route('/cart', methods = ['GET'])
@login_required
def bookcart():
    a_user = current_user.token
    book = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(book)
    return render_template('cart.html', response=response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.title = request.json['title']
    book.author = request.json['author']
    book.year = request.json['year']
    book.isbn = request.json['isbn']
    book.hardcover = request.json['hardcover']
    book.pagecount = request.json['pagecount']
    book.price = request.json['price']
    book.image = request.json['image']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# DELETE car ENDPOINT
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)