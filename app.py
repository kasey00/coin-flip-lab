import os
import random
from flask import Flask, render_template, request, redirect, url_for, session
from database import db, Round
import logic_champions
import logic_stats

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def run_one_round():
    balance = 0; flips = 0; max_dist = 0; curr = 0; last = -1
    max_h = 0; max_t = 0; h_time = 0; t_time = 0
    
    while True:
        flip = random.randint(0, 1)
        flips += 1
        curr = curr + 1 if flip == last else 1
        last = flip
        
        if flip == 0: 
            balance += 1
            if curr > max_h: max_h = curr; h_time = flips
        else: 
            balance -= 1
            if curr > max_t: max_t = curr; t_time = flips
            
        if abs(balance) > max_dist: max_dist = abs(balance)
        if balance == 0: break
            
    return Round(
        total_flips=flips, max_dist=max_dist,
        max_h_streak=max_h, max_t_streak=max_t,
        max_h_timestamp=h_time, max_t_timestamp=t_time,
        is_active=True
    )

def render_dashboard(mode):
    manual = session.get('manual', {'h':0,'t':0,'s':0,'hist':[]})
    rarity = logic_stats.get_rarity(manual['s']) if manual['s'] > 1 else None
    
    count = logic_stats.get_total_count(mode)
    total_flips = logic_stats.get_total_flips(mode) # New
    
    champs = logic_champions.get_all_champions(mode)
    stubborn = logic_stats.get_stubbornness(mode)
    d_tab, h_tab, t_tab = logic_stats.get_tables(mode)
    
    return render_template('index.html', 
                           mode=mode, count=count, total_flips=total_flips,
                           manual=manual, rarity=rarity,
                           champs=champs, stubborn=stubborn,
                           d_tab=d_tab, h_tab=h_tab, t_tab=t_tab)

@app.route('/')
def index():
    return render_dashboard('user')

@app.route('/global')
def global_view():
    return render_dashboard('global')

@app.route('/run')
def run_batch():
    batch = [run_one_round() for _ in range(100)]
    db.session.add_all(batch)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/archive')
def archive():
    Round.query.filter_by(is_active=True).update({'is_active': False})
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/manual/flip', methods=['POST'])
def manual_flip():
    m = session.get('manual', {'h':0,'t':0,'s':0,'last':None,'hist':[]})
    res = random.choice(['H','T'])
    m['hist'].append(res)
    if len(m['hist']) > 15: m['hist'].pop(0)
    
    if res == 'H':
        m['h'] += 1
        m['s'] = m['s'] + 1 if m.get('last') == 'H' else 1
    else:
        m['t'] += 1
        m['s'] = m['s'] + 1 if m.get('last') == 'T' else 1
    
    m['last'] = res
    session['manual'] = m
    return redirect(request.referrer)

@app.route('/manual/reset', methods=['POST'])
def manual_reset():
    session['manual'] = {'h':0,'t':0,'s':0,'last':None,'hist':[]}
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)