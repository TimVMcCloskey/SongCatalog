from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask import request, make_response

# acts like dictionary that maintains state
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import requests
import json
import random
import string
import requests

from collections import OrderedDict
from categories import Base, Category, Song, User


app = Flask(__name__)

# Client id for Google OAuth2
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

# Connect to the database
engine = create_engine('sqlite:///SongCatalog.db')
Base.metadata.bind = engine


# create database session
DBSession = sessionmaker(bind=engine)
# session variable not to be confused with login session
session = DBSession()


#######################################

# CRUD SECTION

#######################################


#######################################

# CREATE SECTION

#######################################


#######################################

# /category/new/ - Add a new category

#######################################

@app.route('/category/new/', methods=['GET', 'POST'])
def categoryNew():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newName = request.form['newName']

        if newName:
            newCategory = Category(name=newName,
                                   user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
            flash("New Category %s Successfully Created" % newCategory.name)
        return redirect(url_for('categoriesAll'))
    else:
        return render_template('newCategory.html')


###########################################################

# /category/id/song/new/ - Add a new song to this category

###########################################################

@app.route('/category/<int:category_id>/song/new', methods=['GET', 'POST'])
def songNew(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
to add songs to this category. Please create your own category in order to \
add songs.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        newTitle = request.form['newTitle']

        if newTitle:
            newSong = Song(title=newTitle,
                           category_id=category_id,
                           user_id=category.user_id)
        else:
            return redirect(url_for('categorySongs', category_id=category_id))

        newArtist = request.form['newArtist']

        if newArtist:
            newSong.artist = newArtist

        newLink = request.form['newLink']

        if newLink:
            newSong.link = newLink
        else:
            newSong.link = '#'

        session.add(newSong)
        session.commit()
        flash("New Song Created")
        return redirect(url_for('categorySongs', category_id=category_id))
    else:
        return render_template('newSong.html', category=category)


#######################################

# READ SECTION

#######################################

#########################################

# /categories/ - shows all categories

#########################################

@app.route('/categories/')
def categoriesAll():
    categories = session.query(Category).all()

    if 'username' not in login_session:
        return render_template('public_categories.html', categories=categories)

    return render_template('categories.html', categories=categories)


##################################################################

# /category/category_id/songs/ - List all songs for this category

##################################################################

@app.route('/category/<int:category_id>/songs/')
def categorySongs(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    songs = session.query(Song).filter_by(category_id=category_id).all()

    if 'username' not in login_session:
        return render_template('public_songs.html',
                               category=category,
                               songs=songs)

    return render_template('songs.html', category=category, songs=songs)


#######################################

# UPDATE SECTION

#######################################

#################################

# /category/select-edit/

#################################

@app.route('/category/select-edit/')
def selectCategoryEdit():
    categories = session.query(Category).all()

    if 'username' not in login_session:
        return render_template('public_categories.html', categories=categories)

    return render_template('sel_category_edit.html', categories=categories)


#################################

# /category/id/edit/

#################################

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def categoryEdit(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script> function myFunction() {alert('You are not authorized \
to edit this category. Please create your own category in order to edit.');}\
</script><body onload='myFunction()''>"

    if request.method == 'POST':
        newName = request.form['newName']

        if newName:
            category.name = newName
            session.add(category)
            session.commit()
            flash('Category Successfully Edited %s' % newName)
        return redirect(url_for('categoriesAll'))

    else:
        return render_template('editCategory.html', category=category)


##########################################

# /category/song/category_id/select-edit/

##########################################

@app.route('/category/song/<int:category_id>/select-edit/')
def selectSongEdit(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    songs = session.query(Song).filter_by(category_id=category_id).all()

    if 'username' not in login_session:
        return render_template('public_songs.html',
                               category=category,
                               songs=songs)

    return render_template('sel_song_edit.html',
                           category=category,
                           songs=songs)


###########################################

# /category/category_id/song/song_id/edit/

###########################################

@app.route('/category/<int:category_id>/song/<int:song_id>/edit/',
           methods=['GET', 'POST'])
def songEdit(category_id, song_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
to edit songs in this category. Please create your own category in order to \
edit songs.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        row = session.query(Song).filter_by(id=song_id).one()

        title = request.form['newTitle']
        if title:
            row.title = title
        artist = request.form['newArtist']
        if artist:
            row.artist = artist
        link = request.form["newLink"]
        if link:
            row.link = link
        session.add(row)
        session.commit()
        flash("Song Successfully Edited")
        return redirect(url_for('categorySongs', category_id=category_id))
    else:
        song = session.query(Song).filter_by(id=song_id).one()
        return render_template('editSong.html', category=category, song=song)


#######################################

# DELETE SECTION

#######################################


#######################################

# /category/select-delete/

#######################################

@app.route('/category/select-delete/')
def selectCategoryDelete():
    categories = session.query(Category).all()

    if 'username' not in login_session:
        return render_template('public_categories.html', categories=categories)

    return render_template('sel_category_delete.html', categories=categories)


#######################################

# /category/id/delete/

#######################################

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def categoryDelete(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
to delete this category. Please create your own category in order to delete.' \
);}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        # Delete Category
        session.delete(category)
        # Get all songs in this category
        songs = session.query(Song).filter_by(category_id=category_id).all()

        # Delete them too
        for song in songs:
            session.delete(song)

        session.commit()
        flash("Category Successfully Deleted")
        return redirect(url_for('categoriesAll'))
    else:
        return render_template('deleteCategory.html', category=category)


############################################

# /category/song/category_id/select-delete/

############################################

@app.route('/category/song/<int:category_id>/select-delete/')
def selectSongDelete(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    songs = session.query(Song).filter_by(category_id=category_id).all()

    if 'username' not in login_session:
        return render_template('public_songs.html',
                               category=category,
                               songs=songs)

    return render_template('sel_song_delete.html',
                           category=category,
                           songs=songs)


#############################################

# /category/category_id/song/song_id/delete/

#############################################

@app.route('/category/<int:category_id>/song/<int:song_id>/delete/',
           methods=['GET', 'POST'])
def songDelete(category_id, song_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
to delete songs from this category. Please create your own category in order \
to delete songs.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        song = session.query(Song).filter_by(id=song_id).one()
        session.delete(song)
        flash("Song Successfully Deleted")
        return redirect(url_for('categorySongs', category_id=category_id))
    else:
        song = session.query(Song).filter_by(id=song_id).one()
        return render_template('deleteSong.html',
                               category=category,
                               song=song)


#######################################

# JSON APIs

######################################


####################################

# /categories/JSON

###################################

@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    cat = []

    for i in categories:
        cat.append(i.serialize)

    return jsonify(Category=cat)


####################################

# /category/category_id/songs/JSON

####################################

@app.route('/category/<int:category_id>/songs/JSON')
def categorySongsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    songs = session.query(Song).filter_by(category_id=category_id).all()
    song = []

    for i in songs:
        song.append(i.serialize)

    return jsonify(Song=song)


#################################

# Login Logout Section

#################################


#################################

# OAuth login

#################################

@app.route('/login')
def showLogin():
    # Create anti-forgery state token
    # Token is a 32 character long combination of characters and strings
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


#########################################

# disconnect - Disconnect from OAuth login

##########################################

@app.route('/disconnect')
def disconnect():
    if 'oauth_provider' in login_session:
        if login_session['oauth_provider'] == 'google':
            gdisconnect()
            del login_session['access_token']
            del login_session['gplus_id']
        if login_session['oauth_provider'] == 'facebook_id':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['oauth_provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('categoriesAll'))
    else:
        flash("You were not logged in")
        return redirect(url_for('categoriesAll'))


#################################

# Client chose Facebook OAuth

#################################

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (  # noqa
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value
        for the server access token then we split it on colons to pull out the
        actual token value and replace the remaining quotes with nothing so
        that it can be used directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['oauth_provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
              -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


#################################

# Facebook disconnect

#################################

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s'\
          % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


#################################

# gconnect - Google OAth2 signin

#################################

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        login_session['access_token'] = credentials.access_token
        flash("you are now logged in as %s" % login_session['username'])
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['oauth_provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "width: 300px; height: 300px;border-radius: 150px;\
              -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


#################################

# gdisconnect - Google disconnect

#################################

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    # Only disconnect a connected user.
    if access_token is None:
        response = make_response(json.dumps(
                   'Current user not connected.'), 401)

        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


#################################

# User Functions

#################################


#################################

# Add new user to database

#################################

def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


######################################

# Get user's information from database

######################################

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


#################################

# user's id

#################################

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
