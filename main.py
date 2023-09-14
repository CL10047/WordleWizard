from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
import time
from sqlalchemy import exc, func, desc, asc
from demo_data import demoUsers, demoUserStats, demoExtraStats, demoFeedbacks

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'WordleWizard'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WordleWizard.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	user_type = db.Column(db.Integer)
	username = db.Column(db.String(255), unique=True, nullable=False)
	
class UserStats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	num_guesses = db.Column(db.Integer)
	fails = db.Column(db.Integer)

class ExtraStats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	total_wins = db.Column(db.Integer)
	total_games = db.Column(db.Integer)
	win_percentage = db.Column(db.Float)
	avg_guesses_win = db.Column(db.Float)
	user_wins_1g = db.Column(db.Integer)
	user_wins_2g = db.Column(db.Integer)
	user_wins_3g = db.Column(db.Integer)
	user_wins_4g = db.Column(db.Integer)
	user_wins_5g = db.Column(db.Integer)
	user_wins_6g = db.Column(db.Integer)
	user_fails = db.Column(db.Integer)

class Feedback(db.Model):
	id = id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255))
	feedback = db.Column(db.String(255), nullable=False)
	
def create_user(email, password, username, user_type=0):
	user = User(email=email, password=password, username=username,user_type=user_type)
	db.session.add(user)
	db.session.commit()
	return user

def create_user_stats(user_id, num_guesses=0, fails=0):
	if (num_guesses == 0):
		stats = UserStats(user_id=user_id, num_guesses=num_guesses, fails=fails)
	else:
		stats = UserStats(user_id=user_id, num_guesses=num_guesses, fails=fails)
	db.session.add(stats)
	db.session.commit()
	return stats

def create_extra_stats(user_id, total_wins, total_games, win_percentage, avg_guesses_win, user_wins_1g, user_wins_2g, user_wins_3g, user_wins_4g, user_wins_5g, user_wins_6g, user_fails):
	extra_stats = ExtraStats(user_id=user_id, total_wins=total_wins, total_games=total_games, win_percentage=win_percentage, avg_guesses_win=avg_guesses_win, user_wins_1g=user_wins_1g, user_wins_2g=user_wins_2g, user_wins_3g=user_wins_3g, user_wins_4g=user_wins_4g, user_wins_5g=user_wins_5g, user_wins_6g=user_wins_6g, user_fails=user_fails)
	
	db.session.add(extra_stats)
	db.session.commit()
	return extra_stats

def create_feedback(feedback, email=None):
	feedback = Feedback(email=email, feedback=feedback)
	db.session.add(feedback)
	db.session.commit()
	return feedback

with app.app_context():
	db.create_all()

	num_records = User.query.count()
	if num_records == 0:
		users_data = demoUsers()
		for email, password, user_type, username in users_data:
			password_hashed = bcrypt.generate_password_hash(password)
			password_hashed_str = password_hashed.decode('utf-8')
			create_user(email, password_hashed_str, username, user_type)

	num_records = UserStats.query.count()
	if num_records == 0:
		user_stats_data = demoUserStats()
		for user_id, num_guesses, fails in user_stats_data:
			create_user_stats(user_id, num_guesses, fails)

	num_records = ExtraStats.query.count()
	if num_records == 0:
		extra_stats_data = demoExtraStats()
		for user_id, total_wins, total_games, win_percentage, avg_guesses_win, user_wins_1g, user_wins_2g, user_wins_3g, user_wins_4g, user_wins_5g, user_wins_6g, user_fails in extra_stats_data:
			create_extra_stats(user_id, total_wins, total_games, win_percentage, avg_guesses_win, user_wins_1g, user_wins_2g, user_wins_3g, user_wins_4g, user_wins_5g, user_wins_6g, user_fails)
			
	num_records = Feedback.query.count()
	if num_records == 0:
		feedback_data = demoFeedbacks()
		for feedback, email in feedback_data:
			create_feedback(feedback, email)


@app.route('/')
def index():
	try:
		user = User.query.filter_by(id = session['user']).first()
		context = {
			"user": user,
			"guest": False,
		}
	except:
		guest_status = False
		context = {
			"guest": True,
		}

	return render_template("index.html", **context)

@app.route('/api/training', methods=['POST'])
def trainingstat():
	try:
		fails = 0
		num_guesses = 0
		user_id = request.form['user-id']
		if (request.form['count'] == '1' or request.form['count'] == '2' or request.form['count'] == '3' or request.form['count'] == '4' or request.form['count'] == '5' or request.form['count'] == '6'):
			num_guesses = request.form['count']
		else:
			fails = 1
		
		create_user_stats(user_id, num_guesses, fails)

		user = User.query.filter_by(id = session['user']).first()
		user_extra = ExtraStats.query.filter(ExtraStats.user_id == user.id).first()
		user_wins_1g = len(UserStats.query.filter(UserStats.user_id == user.id, UserStats.num_guesses == 1).all())
		user_wins_2g = len(UserStats.query.filter(UserStats.user_id == user.id, UserStats.num_guesses == 2).all())
		user_wins_3g = len(UserStats.query.filter(UserStats.user_id == user.id, UserStats.num_guesses == 3).all())
		user_wins_4g = len(UserStats.query.filter(UserStats.user_id == user.id, UserStats.num_guesses == 4).all())
		user_wins_5g = len(UserStats.query.filter(UserStats.user_id == user.id, UserStats.num_guesses == 5).all())
		user_wins_6g = len(UserStats.query.filter(UserStats.user_id == user.id, UserStats.num_guesses == 6).all())
		user_fails = len(UserStats.query.filter(UserStats.user_id == user.id, UserStats.num_guesses == 0).all())
		user_total = len(UserStats.query.filter(UserStats.user_id == user.id).all())
		
		if (user_total == 1):
			try:
				create_extra_stats(user.id, user_total-user_fails, user_total, ((user_total-user_fails) / user_total) * 100, (user_wins_1g+2*user_wins_2g+3*user_wins_3g+4*user_wins_4g+5*user_wins_5g+6*user_wins_6g)/(user_total-user_fails), user_wins_1g, user_wins_2g, user_wins_3g, user_wins_4g, user_wins_5g, user_wins_6g, user_fails)
			except:
				create_extra_stats(user.id, user_total-user_fails, user_total, 0.0, 0.0, user_wins_1g, user_wins_2g, user_wins_3g, user_wins_4g, user_wins_5g, user_wins_6g, user_fails)
		else:
			if (fails == 1):
				user_extra.user_fails += 1
			else:
				user_extra.total_wins += 1
			user_extra.user_id = user.id
			user_extra.total_games += 1
			user_extra.user_wins_1g = user_wins_1g
			user_extra.user_wins_2g = user_wins_2g
			user_extra.user_wins_3g = user_wins_3g
			user_extra.user_wins_4g = user_wins_4g
			user_extra.user_wins_5g = user_wins_5g
			user_extra.user_wins_6g = user_wins_6g
			user_extra.win_percentage = (user_total-user_fails) / user_total * 100
			if (user_total-user_fails == 0):
				user_extra.avg_guesses_win = 0.0
			else:
				user_extra.avg_guesses_win = (user_wins_1g+2*user_wins_2g+3*user_wins_3g+4*user_wins_4g+5*user_wins_5g+6*user_wins_6g)/(user_total-user_fails)
			db.session.commit()

		time.sleep(2)
		return redirect(url_for('index'))
	except exc.IntegrityError:
		flash("Something went wrong", "error")
		return redirect(url_for('index'))

@app.route('/userstats')
def userstats():
	if("user" not in session or session['user_type'] == 0):
		flash("admin only", "info")
		return redirect(url_for('login'))			
	else:
		user = User.query.filter_by(id = 3).first()
		try:
			extra_stats = ExtraStats.query.filter(ExtraStats.user_id == user.id).order_by(ExtraStats.id.desc()).first()
		except:
			extra_stats = ExtraStats.query.filter(ExtraStats.user_id == user.id).order_by(ExtraStats.id.desc()).first()
		
		context = {
			"user" : user,
			"extra_stats" : extra_stats
		}
		return render_template("userstats.html", **context)

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/api/contact', methods=['POST'])
def contacts():
	try:
		email = request.form['email']
		feedback = request.form['feedback']
		create_feedback(feedback, email)
		flash("Feedback successfully submitted", "success")
		return redirect(url_for('contact'))
	except exc.IntegrityError:
		flash("Error submitting feedback", "error")
		return redirect(url_for('contact'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	if(request.method == "POST"):
		email = request.form['email']
		password = request.form['password']

		user = User.query.filter_by(email = email).first()
		if(not user):
			flash("No such user: " + email, "error")
			return render_template("login.html")
		elif(not bcrypt.check_password_hash(user.password, password)):
			flash("Sorry, wrong password", "error")
			return render_template("login.html")
		else:
			session['user'] = user.id
			session['user_type'] = user.user_type
			if (session['user_type'] == 0):
				return redirect(url_for('index'))
			return redirect(url_for('viewfeedback'))
	elif "user" in session:
		return redirect(url_for('index'))
	else:
		return render_template("login.html")

@app.route('/logout')
def logout():
	session.pop("user", None)
	session.pop("user_type", None)
	return redirect(url_for('index'))

@app.route('/profile')
def profile():
	if("user" not in session):
		flash("must log in before you can access this page", "info")
		return redirect(url_for('login'))
	else:
		user = User.query.filter_by(id = session['user']).first()

		context = {
			"user" : user
		}
		return render_template("profile.html", **context)

@app.route('/api/changeusername', methods=['POST'])
def changeusername():
	if (request.method == 'POST'):
		user = User.query.filter_by(id = session['user']).first()
		new_info = request.form['new_info']
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		if (password != confirm_password):
			flash("Password does not match", "error")
			return redirect(url_for('profile'))
		
		if(not bcrypt.check_password_hash(user.password, password)):
			flash("Sorry, wrong password", "error")
			return redirect(url_for('profile'))
		
		try:
			user.username = new_info
			db.session.commit()
			flash("Profile successfully updated", "success")
			return redirect(url_for('profile'))
		except exc.IntegrityError:
			flash("Username already exists", "error")
			return redirect(url_for('profile'))
	else:
		return redirect(url_for('profile'))

@app.route('/api/changeemail', methods=['POST'])
def changeemail():
	if (request.method == 'POST'):
		user = User.query.filter_by(id = session['user']).first()
		new_info = request.form['new_info']
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		if (password != confirm_password):
			flash("Password does not match", "error")
			return redirect(url_for('profile'))
		
		if(not bcrypt.check_password_hash(user.password, password)):
			flash("Sorry, wrong password", "error")
			return redirect(url_for('profile'))
		
		try:
			user.email = new_info
			db.session.commit()
			flash("Profile successfully updated", "success")
			return redirect(url_for('profile'))
		except exc.IntegrityError:
			flash("Email already exists", "error")
			return redirect(url_for('profile'))
	else:
		return redirect(url_for('profile'))
	
@app.route('/api/changepassword', methods=['POST'])
def changepassword():
	if (request.method == 'POST'):
		user = User.query.filter_by(id = session['user']).first()
		new_info = request.form['new_info']
		confirm_new_info = request.form['confirm_new_info']
		password = request.form['password']
		confirm_password = request.form['confirm_password']

		password_hashed = bcrypt.generate_password_hash(new_info)
		password_hashed_str = password_hashed.decode('utf-8')
		confirm_password_hashed = bcrypt.generate_password_hash(confirm_new_info)

		confirm_password_hashed_str = confirm_password_hashed.decode('utf-8')
		if (password != confirm_password):
			flash("Old Password does not match", "error")
			return redirect(url_for('profile'))
		
		if (new_info != confirm_new_info):
			flash("New Password does not match", "error")
			return redirect(url_for('profile'))
		
		if(not bcrypt.check_password_hash(user.password, password)):
			flash("Sorry, wrong password", "error")
			return redirect(url_for('profile'))
		
		try:
			user.password = password_hashed_str
			db.session.commit()
			flash("Profile successfully updated", "success")
			return redirect(url_for('profile'))
		except exc.IntegrityError:
			flash("Email already exists", "error")
			return redirect(url_for('profile'))
	else:
		return redirect(url_for('profile'))

@app.route('/viewfeedback')
def viewfeedback():
	if("user" not in session or session['user_type'] == 0):
		flash("admin only", "info")
		return redirect(url_for('login'))			
	else:
		feedbacks = Feedback.query.all()
		context = {
			"feedbacks": feedbacks
		}
		return render_template("viewfeedback.html", **context)
		

@app.route('/viewusers')
def viewusers():
	if("user" not in session or session['user_type'] == 0):
		flash("admin only", "info")
		return redirect(url_for('login'))
	else:
		lead_admins = admins = User.query\
		.filter(User.user_type==2)\
		.order_by((User.id))\
		.all()

		admins = User.query\
		.filter(User.user_type==1)\
		.order_by((User.id))\
		.all()

		users = User.query\
		.filter(User.user_type==0)\
		.order_by((User.id))\
		.all()

		context = {
			"lead_admins": lead_admins,
			"admins": admins,
			"users": users
		}
		return render_template("viewusers.html", **context)
		

@app.route('/rankings')
def rankings():
	if("user" not in session):
		flash("must log in before you can access this page", "info")
		return redirect(url_for('login'))
	else:
		user = User.query.filter_by(id = session['user']).first()
		
		num_wins_rankings = db.session.query(ExtraStats, User)\
			.join(User, ExtraStats.user_id == User.id)\
			.order_by(desc(ExtraStats.total_wins))\
			.limit(5)\
			.all()
		
		win_percentage_rankings = db.session.query(ExtraStats, User)\
			.join(User, ExtraStats.user_id == User.id)\
			.order_by(desc(ExtraStats.win_percentage))\
			.limit(5)\
			.all()
		
		avg_guesses_rankings = db.session.query(ExtraStats, User)\
			.join(User, ExtraStats.user_id == User.id)\
			.order_by(asc(ExtraStats.avg_guesses_win))\
			.limit(5)\
			.all()
		
		context = {
			"user": user,
			"num_wins_rankings": num_wins_rankings,
			"win_percentage_rankings": win_percentage_rankings,
			"avg_guesses_rankings": avg_guesses_rankings,
		}


		return render_template("rankings.html", **context)
	
@app.route('/stats')
def stats():
	if("user" not in session):
		flash("must log in before you can access this page", "info")
		return redirect(url_for('login'))
	else:
		user = User.query.filter_by(id = session['user']).first()
		try:
			extra_stats = ExtraStats.query.filter(ExtraStats.user_id == user.id).order_by(ExtraStats.id.desc()).first()
		except:
			extra_stats = ExtraStats.query.filter(ExtraStats.user_id == user.id).order_by(ExtraStats.id.desc()).first()
		context = {
			"user" : user,
			"extra_stats" : extra_stats
		}

		return render_template("stats.html", **context)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if(request.method == "POST"):
		email = request.form['email']
		password = request.form['password']
		username = request.form['username']
		password_hashed = bcrypt.generate_password_hash(password)
		password_hashed_str = password_hashed.decode('utf-8')
		try:
			create_user(email, password_hashed_str, username, 0)
			flash("User successfully added", "success")
			user = User.query.filter_by(email = email).first()
			session['user'] = user.id
			session['user_type'] = user.user_type
			if (session['user_type'] == 0):
				return redirect(url_for('index'))
			return redirect(url_for('viewfeedback'))
		except exc.IntegrityError:
			flash("Username/Email already exists", "error")
			return render_template('signup.html')
	elif "user" in session:
		return redirect(url_for('index'))
	else:
		return render_template('signup.html')

app.run(host='0.0.0.0', port=72, debug=True)