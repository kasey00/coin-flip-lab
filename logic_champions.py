from sqlalchemy import func
from database import db, Round

def get_champion(mode, side, category):
    # 1. Fetch all rounds in scope
    query = Round.query
    if mode == 'user': query = query.filter(Round.is_active == True)
    rounds = query.all()
    
    if not rounds: return None
    
    # Helper to extract Head/Tail specific data from a round object
    def get_metrics(r):
        streak = r.max_h_streak if side == 'heads' else r.max_t_streak
        # Timestamp is the flip count when the streak ENDED
        timestamp = r.max_h_timestamp if side == 'heads' else r.max_t_timestamp
        return streak, timestamp

    # 2. Logic for "Fastest" (The Efficiency Champion)
    if category == 'fastest':
        # We want the "Luckiest" streak. 
        # Formula: Expected Time / Actual Time
        # Expected time to see streak k is approx 2^(k+1)
        
        def efficiency_score(r):
            s, t = get_metrics(r)
            if s < 3 or t == 0: return 0 # Ignore tiny streaks
            
            expected_arrival = (2 ** (s + 1)) - 2
            # Higher Ratio = Arrived much faster than math predicts
            return expected_arrival / t

        champion = max(rounds, key=efficiency_score)
        s, t = get_metrics(champion)
        
        return {
            'streak': s,
            'metric_label': 'Quickest Start',
            'metric_val': t - s, # Start Index = End Timestamp - Length
            'context_label': 'Probability',
            'context_val': f"{round(((2**(s+1)-2)/t), 1)}x Norm" # e.g. "300x Norm"
        }

    # 3. Logic for "Longest" (The Endurance Champion)
    elif category == 'longest':
        # We want the Absolute Highest Streak. 
        # Tie-breaker: The Longest Game (Duration)
        
        def grind_score(r):
            s, _ = get_metrics(r)
            return (s, r.total_flips) # Tuple sorting: Prioritize Streak, then Duration
            
        champion = max(rounds, key=grind_score)
        s, t = get_metrics(champion)
        
        return {
            'streak': s,
            'metric_label': 'Longest Game',
            'metric_val': champion.total_flips,
            'context_label': 'Found at',
            'context_val': f"#{t}"
        }

def get_all_champions(mode):
    return {
        'h_fast': get_champion(mode, 'heads', 'fastest'),
        'h_long': get_champion(mode, 'heads', 'longest'),
        't_fast': get_champion(mode, 'tails', 'fastest'),
        't_long': get_champion(mode, 'tails', 'longest')
    }