# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for
from flask import jsonify, copy_current_request_context
#from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from .utils.blockchain.blockchain import Block, Blockchain
from pprint import pprint
import json
import random
import functools
import datetime
import os
from werkzeug.utils import secure_filename
#from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return session['email'] if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html', error = "")

# this is the signup fucntion to render the signup page
@app.route('/signup')
def signup():
	return render_template('signup.html')

# this fucntion will bassically ensure that the email does not exist in the db and then add it 
@app.route('/processsignup', methods = ["POST","GET"])
def processsignup(): 
    email_ = request.form['email']
    password_ = request.form['password']
    print("email: {}  password: {}".format(email_,password_))
    users = db.query() #get all users
    for items in users:
        print(items['email'])
        print("signup attempt!!!!!!!!!!!!")
        if items['email'] == email_:
            return render_template('/signup.html', error = "The account alredy exists! Try loggin in.")
    key = db.generate_key()
    db.createUser(email= email_ ,password= password_, role='user',key=key)
    return render_template('/login.html',error = "your account was created successfully!")

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

'''
route fucntion for processing the pogin of a user
'''
@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
    email_ = request.form['email']
    password_ = request.form['password']
    status = db.authenticate(email= email_,password= password_)
    if status['success'] == 1:
        print("status")
        session['email'] = email_
        return redirect('/') 
    
    return render_template('/login.html', error = "Log in failed! Please check credentials and try again.")


#######################################################################################
# MARKETPLACE RELATED
#######################################################################################
'''
route fucntion for the market place landing page of the maret place.
'''
@app.route('/marketplace')
@login_required
def marketplace():
    user = getUser()
    users = db.query()
    for items in users:
           if items["email"] == user:
                if items["entry"] == 0 or items["entry"] == '0':
                    print("market place print statement !!!!!!!!!!!!!!!!!!!!")
                    print(items['email'])
                    print(items['entry'])
                    # need to add db step to update the entry field 
                    query = "UPDATE users SET entry = entry + %s WHERE email = %s;"
                    db.query(query,parameters=[1,user])
                    print(query)
                    return render_template('marketplace.html', user=getUser(), first_time = True)
                elif items["entry"] > 0 or items["entry"] != '0':
                    return render_template('marketplace.html', user=getUser(), first_time = False)     
    return render_template('marketplace.html', user=getUser(), first_time = False)


'''
route fucntion for buyer page, it includes purchases 
'''
@app.route('/buyer',methods = ["POST","GET"])
@login_required
def buyer():
    user = getUser()
    users = db.query()
    user_id = None #user id of the new owner
    users_key = None #user key
    users_tokens = None #user tokens
    for items in users:
        if items["email"] == user:
            user_id = items["user_id"] #user_id of this session
            users_key = items['user_key'] #get users key
    
    wallet = db.query(query="SELECT * FROM wallet;")
    for profile in wallet:
        if profile['user_key'] == users_key:
            users_tokens = int(profile['tokens'])


    all_nft = db.query(query="SELECT * FROM nfts;")
    selling = [] #gett all that can be sold
    for items in all_nft:
        if items['owner_id'] == user_id: #if nft created by user then user cant buy
            continue
        else:
            selling.append(items)

    if request.method == 'POST' and request.form['purpose'] == 'purchase':
        nft_id = request.form['nft_id'] #
        user_2 = request.form['owner_id'] #owner that should get the money
        tokens = int(request.form['tokens']) #price of the nft
        nft_date = request.form['date']
        user2_key = None
        
        users = db.query()
        for use in users:
            if int(use["user_id"]) == int(user_2):
                user2_key = use['user_key']


        
        
        if tokens > users_tokens:
            return render_template('buyer.html',user=getUser(), for_sale = selling,message="You dont have enough in your wallet to purchase! Try another! Check your portfolio to see how much you have.") 
        elif tokens <= users_tokens:
            print(tokens,users_tokens)
            query1 = "UPDATE nfts SET owner_id = %s WHERE nft_id = %s;"
            db.query(query1, parameters=[user_id,nft_id]) #update to new user id
            
            query2 = "UPDATE wallet SET tokens = tokens - %s WHERE user_key = %s;"
            db.query(query2, parameters=[tokens,users_key]) #subtract for user 1
            
            query3 = "UPDATE wallet SET tokens = tokens + %s WHERE user_key = %s;"
            db.query(query3, parameters=[tokens,user2_key]) #add for user 2
            
            transaction_columns = ["nft_id","nft_date","amount","owner_id","transaction_date","type","buyer_id","seller_id"]
            data = []
            data.append(nft_id); data.append(nft_date);data.append(tokens);data.append(user_id);data.append(datetime.datetime.now());data.append("BUY");data.append(user_id);data.append(user_2)
            db.insertRows(table="transaction", columns=transaction_columns,parameters=data) #a buy transaction added
            
            all_nft = db.query(query="SELECT * FROM nfts;")
            selling = []
            for items in all_nft:
                if items['owner_id'] == user_id: #if nft created by user then user cant buy
                    continue
                else:
                    selling.append(items)
            return render_template('buyer.html',user=getUser(), for_sale = selling, message="")        

    return render_template('buyer.html',user=getUser(), for_sale = selling, message="") 




'''
this is the seller route fucntion, responsible for edits and upload of nfts
'''
@app.route('/seller', methods = ["POST","GET"])
@login_required
def seller():
    message = ""
    user_id = None #user id of this session
    users = db.query() #get all the users
    nfts = db.query(query="SELECT * FROM nfts;")
    for items in users:
        if items['email'] == getUser():
            user_id = items['user_id'] 

    nfts = db.query(query="SELECT * FROM nfts;")
    owned = []
    for img in nfts:
        if img['owner_id'] == user_id:
            owned.append(img)    
    
    if request.method == 'POST' and request.form['purpose'] == 'file': #to create nft and create transaction
        description = request.form['desc']
        tokens = request.form['token']
        file = request.files['file']
        filename = secure_filename(file.filename)
        path = os.path.join("./flask_app/static/nft/", filename)
        for img in nfts:
            if img['nft_path'] == path:
                return render_template('seller.html',user=getUser(), Created = owned, error = "THIS NFT EXISTS ALREDY!!")
        
        file.save(path)
        columns = ["nft_path", "owner_id","description","amount","created_at","creator_id"]
        fields = []
        fields.append(path); fields.append(user_id); fields.append(description);fields.append(tokens);fields.append(datetime.datetime.now());fields.append(user_id)
        db.insertRows(table="nfts", columns=columns,parameters=fields) #new nft has been uploaded
        id_nft = None
        date_nft = None
        nfts = db.query(query="SELECT * FROM nfts;")
        for items in nfts:
            if items['nft_path'] == path:
                id_nft = items['nft_id']
                date_nft = items['created_at']
        transaction_columns = ["nft_id","nft_date","amount","owner_id","transaction_date","type","seller_id"]
        tran_fields = []
        tran_fields.append(id_nft);tran_fields.append(date_nft);tran_fields.append(tokens);tran_fields.append(user_id);tran_fields.append(datetime.datetime.now());tran_fields.append("SELL");tran_fields.append(user_id)
        db.insertRows(table="transaction", columns=transaction_columns,parameters=tran_fields) #a sel transaction added


    elif request.method == 'POST' and request.form['purpose'] == 'edit': #edit description of specific 
        description = request.form['description']
        nft_id = request.form['nft_id']
        tokens = request.form['tokens']
        query = "UPDATE nfts SET description = %s, amount = %s WHERE nft_id = %s;"
        

        nft_date = None
        nfts = db.query(query="SELECT * FROM nfts;")
        for x in nfts:
            if int(x['nft_id']) == int(nft_id):
                nft_date = x['created_at']
                if int(x['amount']) != int(tokens):
                    transaction_columns = ["nft_id","nft_date","amount","owner_id","transaction_date","type","seller_id"]
                    tran_fields = []
                    tran_fields.append(nft_id);tran_fields.append(nft_date);tran_fields.append(tokens);tran_fields.append(user_id);tran_fields.append(datetime.datetime.now());tran_fields.append("UPDATE");tran_fields.append(user_id)
                    db.insertRows(table="transaction", columns=transaction_columns,parameters=tran_fields)
        
        db.query(query, parameters = [description, tokens, nft_id]) #then edit the description and tokens
        print("UPDATE COMPLETE !!!!!!!!!!!!!")

    #get all the nfts and updates again
    nfts = db.query(query="SELECT * FROM nfts;")
    owned = []
    for img in nfts:
        if img['owner_id'] == user_id:
            owned.append(img)
    return render_template('seller.html',user=getUser(), Created = owned, error = message)



'''
route fucntion for getiing users portfolio, includes basic info and their collection of nft
'''
@app.route('/portfolio')
@login_required
def portfolio():
    user = getUser()
    users = db.query()

    id = None
    for items in users:
           if items["email"] == user:
                id = items["user_id"] 
                owned = []
                nfts = db.query(query="SELECT * FROM nfts;")
                for pics in nfts:
                    if int(pics['owner_id']) == int(id):
                        owned.append(pics)
                if len(owned) < 1:
                    return  render_template('portfolio.html',user=getUser(), data = items, collection = "")
                return  render_template('portfolio.html',user=getUser(), data = items, collection = owned)


'''
route fucntion to get all the transactions on the realted to selling and buysing NFT
'''
@app.route('/transactionrecord')
@login_required
def transactionrecord():
    transactions = db.query(query="SELECT * FROM transaction;")
    if len(transactions) < 1:
        transactions = []
    user = getUser()
    users = db.query()
    for items in users:
        if items["email"] == user:
            if items["role"] == "admin":
                    return render_template('transactionrecord.html',user=getUser(), valid=True, data = transactions)
    
    return render_template('transactionrecord.html',user=getUser(), valid=False)

"""
@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')

"""
#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')


'''
route fucntion for home  page
'''
@app.route('/home')
# @login_required
def home():
    print(db.query('SELECT * FROM users'))
    x     = random.choice(['I started playing football for my highschool at the age of 14.',
            'I love cats.','I am currently looking for a job.',
            'I am from Chittagong Bangladesh which has the longest sea beach in the world.'])
    return render_template('home.html', user=getUser(), fun_fact = x)


'''
route fucntion for resume page
'''
@app.route('/resume')
# @login_required
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data, user=getUser())

'''
route fucntion for project  page
'''
@app.route('/projects')
# @login_required
def projects():
	return render_template('projects.html', user=getUser())

'''
route fucntion for piano page
'''
@app.route('/piano')
@login_required
def piano():
	return render_template('piano.html', user=getUser())

'''
function for processing feedback when entered

'''
@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	name = request.form['name']
	email = request.form['email']
	message = request.form['comment']

	# db.query("INSERT IGNORE INTO()")
	sql_statement = "INSERT IGNORE INTO feedback (name,email,comment) VALUES ('{}', '{}', '{}');".format(name,email,message)
	db.query(sql_statement)

	results = db.query("SELECT * FROM feedback;")
	return render_template('feedback.html',feedbacks=results)


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r




@app.route("/test1")
def test1():
    # res = db.getResumeData() 
    res = db.query(query="Select * From users;")
    return res 

@app.route("/test2")
def test2():
    # res = db.getResumeData() 
    res = db.query(query="Select * From transaction;")
    return res 




@app.route("/Error")
def Error():
    return "ERROR"

@app.route("/nft")
def nft():
    nfts = db.query(query="SELECT * FROM nfts;") 
    return  nfts
