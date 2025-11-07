from flask import Blueprint, render_template
from src.apps.portfolio.db import db  # shared database
from sqlalchemy import text

exchange_bp = Blueprint('exchange_rates', __name__, template_folder='templates')

@exchange_bp.route('/top10')
def top10():
    query = text("SELECT * FROM public.exchange_rates ORDER BY date DESC LIMIT 10")
    with db.engine.connect() as conn:
        result = conn.execute(query).fetchall()
    
    # Convert each Row to a dictionary using _mapping
    rows = [dict(row._mapping) for row in result]
    
    return render_template('top10.html', rows=rows, title="Top 10 Exchange Rates")
