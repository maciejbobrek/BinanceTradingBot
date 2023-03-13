from flask import Blueprint,render_template,redirect,url_for,request,flash,jsonify,Response
from binance.client import Client
from binance import exceptions
from flask_login import current_user,login_required
import time
from binance.enums import *
from client_wrapper import client,Client_Wrapper
from datetime import datetime,timedelta

from db_Models import *
import dummy_config

from active_bots import active_bots
from bot_manager import activate_bot,shutdown_bot

app_home=Blueprint('app',__name__)
app_home.secret_key = 'f27e7924ddab2253381436115efc8c6529214f7d0f0212299427c871a74fa9ac'

def create_dummy_database():
    try:
        db.create_all()
    except:
        print("Database aldeary exists")
    try:
        new_bot=Bot(user_id=current_user.id,public=dummy_config.API_PUBLIC + " 1",secret=dummy_config.API_SECRET + " 1",keylabel='Dummy Bot 1')
        db.session.add(new_bot)
        new_bot=Bot(user_id=current_user.id,public=dummy_config.API_PUBLIC + " 2",secret=dummy_config.API_SECRET + " 2",keylabel='Dummy Bot 2')
        db.session.add(new_bot)
        new_bot=Bot(user_id=current_user.id,public=dummy_config.API_PUBLIC + " 3",secret=dummy_config.API_SECRET + " 3",keylabel='Dummy Bot 3')
        db.session.add(new_bot)
        new_bot=Bot(user_id=current_user.id,public=dummy_config.API_PUBLIC + " 4",secret=dummy_config.API_SECRET + " 4",keylabel='Dummy Bot 4')
        db.session.add(new_bot)
        new_bot=Bot(user_id=current_user.id,public=dummy_config.API_PUBLIC + " 5",secret=dummy_config.API_SECRET + " 5",keylabel='Dummy Bot 5')
        db.session.add(new_bot)
        db.session.commit()
    except:
        print("Already added dummies")

@app_home.route('/')
@login_required
def index():
    
    if not client.set_Client():
        client.set_dummy()

    balances = client.get_balances()
    symbols = client.Client.get_exchange_info()['symbols']
    return render_template('home.html', my_balances=balances, symbols=symbols,user=current_user)

@login_required
@app_home.route('/chart_history', methods=['POST'])
def get_exchangerate_data(exchange = "BTCUSDT", period=client.Client.KLINE_INTERVAL_15MINUTE,start=str(int(time.time())-7*24*60*60),end=str(int(time.time()))):

    """
        Fetches historical candlestick data for a exchange rate and given time interval 
    Args:
        exchange (str): given exchange rate
        period (str): candlestick period
        start (str): 
        end(str): end of the interval in unix time 

    Returns:
        response(JSON):  candlestick data in a lightweightchart data format 
    """
    candlesticks = client.Client.get_historical_klines(exchange,period,start,end,1000)
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }
        processed_candlesticks.append(candlestick)
    response =  jsonify(processed_candlesticks)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


    
@app_home.route('/bots',methods=['GET','POST'])    
@login_required
def bots():
    pairs = {}      
    for bot in db.session.query(Bot).all():
        pairs[bot.public] = bot.secret
    if request.method == 'POST':
        print(request.form)
        command = request.form.get('command')
        if request.form.get('keylabel') != None:
            keylabel = request.form.get('keylabel')
            public = request.form.get('public_key')
            secret = request.form.get('secret_key')
            print(public)
            print(secret)
            public_key = Bot.query.filter_by(public=public).first()
            if public_key:
                flash('Key pair already exists!',category='error')
            else:
                try:
                    response = Client(public,secret,tld='com').create_test_order(symbol='ETHUSDT',side='BUY',type='MARKET',quantity=10)
                    response = {}
                    if {} == response:
                        new_bot=Bot(user_id=current_user.id,public=public,secret=secret,keylabel=keylabel)
                        db.session.add(new_bot)
                        db.session.commit()
                        print("ok")
                        flash('Key pair addes successfully!',category='success')
                except exceptions.BinanceAPIException as api_err:
                    if api_err.code == -2015:
                        flash("Wrong public key!", category='error')
                    elif api_err.code == -2014:
                        flash("Invalid key format! One of your keys isn't the right length.", category='error')
                except Exception as e:
                    print("Unhandled error while adding key pair: ", e) 
        elif request.form.get('symbol'):
            pass
     
            
    return render_template('bots.html',user=current_user)

@app_home.route('/bots/commandbot_<bot_id>', methods=['POST'])    
@login_required
def command_bot(bot_id):
    command = request.form.get('command')
    # print(request.form.get)
    if command == 'activate':
        activate_bot(bot_id, request.form.get('symbol'),request.form.get('quantity'),request.form.get('period'))
    elif command == 'deactivate':
        shutdown_bot(bot_id)
    
    return redirect('/bots')
@app_home.route('/bots/delete_bot',methods=['POST'])
@login_required
def delete_bot(): 
    bot_id=request.form.get("bot_id")
    print("Deleted key pair with id: ",bot_id)
    try:
        bot = Bot.query.get(bot_id)
        if bot.user_id == current_user.id:
            db.session.delete(bot)
            db.session.commit()
    except AttributeError as err:
        print(err)

    return redirect('/bots')


@app_home.route('/bots/edit_algorithm_<bot_id>',methods=['POST','GET'])
@login_required
def edit_algorithm(bot_id):
    return render_template('edit_algorithm.html',user=current_user,bot_id=bot_id)
