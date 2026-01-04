from sqlalchemy import func
from database import db, Round

def get_total_count(mode):
    q = Round.query
    if mode == 'user': q = q.filter(Round.is_active == True)
    return q.count()

# NEW: Sum of all flips
def get_total_flips(mode):
    q = db.session.query(func.sum(Round.total_flips))
    if mode == 'user': q = q.filter(Round.is_active == True)
    total = q.scalar()
    return total if total else 0

def get_rarity(streak_len):
    if streak_len < 2: return None
    total = Round.query.count()
    if total == 0: return None
    achieved = Round.query.filter((Round.max_h_streak >= streak_len) | (Round.max_t_streak >= streak_len)).count()
    if achieved == 0: return "Top <0.01%"
    pct = (achieved / total) * 100
    return f"Top {round(pct, 2)}%" if pct < 1 else f"Top {round(pct, 1)}%"

def get_stubbornness(mode):
    q = db.session.query(Round.total_flips, Round.max_dist)
    if mode == 'user': q = q.filter(Round.is_active == True)
    data = q.all()
    
    if not data: return {'avg_tight': 0, 'cost_min': 0, 'cost_max': 0}
    
    tight_flips = [d[0] for d in data if d[1] <= 10]
    loose_flips = [d[0] for d in data if d[1] > 10]
    
    if not tight_flips: return {'avg_tight': 0, 'cost_min': 0, 'cost_max': 0}
    
    avg_tight = sum(tight_flips) / len(tight_flips)
    res = {'avg_tight': round(avg_tight, 1), 'cost_min': 0, 'cost_max': 0}
    
    if loose_flips:
        res['cost_min'] = round(min(loose_flips) / avg_tight, 1)
        res['cost_max'] = round(max(loose_flips) / avg_tight, 1)
        
    return res

def get_tables(mode):
    q = Round.query
    if mode == 'user': q = q.filter(Round.is_active == True)
    rounds = q.all()
    
    # Deviation Table
    dist_map = {}
    for r in rounds:
        if r.max_dist not in dist_map: dist_map[r.max_dist] = []
        dist_map[r.max_dist].append(r.total_flips)
    
    dist_stats = []
    for d in sorted(dist_map.keys()):
        avg = sum(dist_map[d]) / len(dist_map[d])
        mult = avg / d if d > 0 else 0
        dist_stats.append({'dist': d, 'avg': round(avg, 1), 'mult': round(mult, 1)})
        
    # Streak Tables
    h_map = {}; t_map = {}
    for r in rounds:
        # Heads
        if r.max_h_streak not in h_map: h_map[r.max_h_streak] = {'arr': [], 'dur': []}
        h_map[r.max_h_streak]['arr'].append(r.max_h_timestamp)
        h_map[r.max_h_streak]['dur'].append(r.total_flips)
        # Tails
        if r.max_t_streak not in t_map: t_map[r.max_t_streak] = {'arr': [], 'dur': []}
        t_map[r.max_t_streak]['arr'].append(r.max_t_timestamp)
        t_map[r.max_t_streak]['dur'].append(r.total_flips)
        
    def process(m):
        res = []
        for k,v in m.items():
            avg_arr = sum(v['arr']) / len(v['arr'])
            # Quickest Start = (Timestamp - Streak) + 1
            starts = [(t - k) + 1 for t in v['arr']]
            res.append({
                'streak': k, 
                'avg_arr': round(avg_arr, 0),
                'min_start': min(starts),
                'min_dur': min(v['dur']), 
                'max_dur': max(v['dur'])
            })
        res.sort(key=lambda x: x['streak'])
        return res
        
    return dist_stats, process(h_map), process(t_map)