from flask import Flask, render_template, request, session, redirect, url_for
from models import User, Stocks, Transaction
from models import db
import wrapper
import live
from forms import SignupForm, LoginForm, CompanyForm
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/markit.db"
db.init_app(app)
app.secret_key = "development-key"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def register():
	form = SignupForm()
	if request.method == "POST":
		
		if form.validate()==False:
			return render_template("register.html", form=form)
		newuser = User(form.name.data, form.age.data, form.phone.data, form.email.data, form.pword.data)
		db.session.add(newuser)
		db.session.commit()
		return render_template("index.html", form=form)

	elif request.method == "GET":
		return render_template("register.html", form = form)

	return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if request.method=="POST":
		if form.validate()== False:
			return render_template("login.html",form=form)
		else:
			email = form.email.data
			password = form.pword.data
			user = User.query.filter_by(email=email).first()
			print("Pass")
			if user is not None and user.check_password(password):
				session['email']= form.email.data
				session['amount'] = user.amount
				return redirect(url_for('home'))
			else:
				return render_template('login.html', form=form)
	else: 
		 request.method == "GET"
		 return render_template('login.html', form=form)

@app.route("/home", methods=["GET", "POST"])
def home():
	user = User.query.filter_by(email=session['email']).first()
	stocks = Stocks.query.filter_by(usemail=session['email']).all()
	trans = Transaction.query.filter_by(email=session['email']).all()
	return render_template('homepage.html', email=session['email'], user=user, stocks=stocks, trans=trans)
	


@app.route('/company')
def company():
	if(request.method == 'GET'):
		action = request.args.get('action')
		return render_template("company.html", action=action)
	return render_template("company.html")

@app.route('/search',methods=['GET', 'POST'])
def search():
	# form = CompanyForm()
	if(request.method == 'POST'):
		name = request.form['name']	
		check = wrapper.Markit()
		data = check.company_search(name)
		if(data is not None):
			return render_template("result.html", data=data, action="Search")
		else:
			return render_template("index.html")
	return render_template("index.html")
	

@app.route('/quote',methods=['GET', 'POST'])
def quote():
	if(request.method == 'POST'):
		sym = request.form['name']
		quote = wrapper.Markit()
		data = quote.get_quote(sym)
		if(data is not None):
			return render_template("result.html", data=data, action="Quote")
		else:
			return render_template("index.html")
		return render_template("result.html", data=data, action="Quote")

@app.route('/buy_sell')
def buy_sell():
	if(request.method == 'GET'):
		usr = request.args.get('uid')
		status = request.args.get('status')
		return render_template("buy_sell.html", uid=usr, status=status)
	return render_template("homepage.html")

@app.route('/Buy',methods=['GET', 'POST'])
def buy():
	if(request.method == 'POST'):
		sym = request.form['comp_sym']
		no = float(request.form['number'])
		quote = wrapper.Markit()
		data = quote.get_quote(sym)
		user = User.query.filter_by(email=session['email']).first()
		if(data == False):
			last_price = 0
		elif('LastPrice' not in data):
			print("No Company Like that")
			return redirect(url_for('home'))
		else:
			last_price = data["LastPrice"]
		total = no * last_price
		if(session['amount'] <= total):
			error = "Insufficient Balance"
			return render_template('homepage.html',user=user, error=error)
		stocks = Stocks.query.filter_by(usemail=session['email']).all()
		flag=0
		for i in stocks:
			if(i.symbol == sym):
				i.stocks_update(sym, no, "BUY")
				flag = 1
				break
		if flag == 0:
			newstock = Stocks(session['email'], sym, no)
			db.session.add(newstock)
			db.session.commit()
		
		newtrans = Transaction(session['email'], sym, no, last_price, total, "BUY")
		db.session.add(newtrans)
		db.session.commit()

		user.update_amount(total, "BUY")
		db.session.add(user)
		db.session.commit()
		print(user.amount)
		error = None
	return redirect(url_for('home'))

@app.route('/chart', methods=['GET', 'POST'])
def show_charts():
	company = request.args.get('company')
	chart = live.LiveData()
	z = chart.live_chart(company)
	
	ch = z['Time Series (Daily)']
	real_chart = dict()
	for k,v in ch.items():
		real_chart[k] = v['3. low']

	return render_template('charts.html', chart=real_chart, company=company)

@app.route('/Sell',methods=['GET', 'POST'])
def sell_shares():
	if(request.method == 'POST'):
		uid = request.form['uid']
		sym = request.form['comp_sym']
		no = float(request.form['number'])
		quote = wrapper.Markit()
		data = quote.get_quote(sym)
		if(data == False):
			last_price = 0
		elif('LastPrice' not in data):
			print("No Company Like that")
			return redirect(url_for('home'))
		else:
			last_price = data["LastPrice"]
		total = no * last_price
		stocks = Stocks.query.filter_by(usemail=session['email']).all()
		for i in stocks:
			if(i.symbol == sym):
				if(i.stocks >= no):
					i.stocks_update(sym, no, "SELL")
					
					newtrans = Transaction(session['email'], sym, no, last_price, total, "SELL")
					db.session.add(newtrans)
					db.session.commit()
					user = User.query.filter_by(email=session['email']).first()
					user.update_amount(total, "SELL")
					db.session.add(user)
					db.session.commit()
					break
				else:
					print("You do not have that much stocks..")
			else:
				print("You do not have stock of the specified company..")	
		
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('email', None)
	return redirect(url_for('login'))
	




if __name__ == "__main__":
	app.run(debug=True)