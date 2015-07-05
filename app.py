#-*- coding: utf-8 -*-

from flask import Flask, request, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/users/new', methods=['GET'])
def new_user():
    return render_template('new_user.html')

@app.route('/users/show', methods=['GET'])
def show_user():
    user = {
        'name': request.args.get('name'),
        'marriage': request.args.get('marriage', default='no'),
        'gender': request.args.get('gender'),
        'from': request.args.get('from'),
        'self_intro': request.args.get('self_intro')
    }
    
    return render_template('user.html', user=user) 

@app.route('/iframe', methods=['GET'])
def iframe():
    return render_template('iframe.html')

if __name__ == "__main__":
    app.run()
