import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import base64

def get_analysis_data(db_path):
    conn = sqlite3.connect(db_path)
    

    df_agency = pd.read_sql_query("SELECT id, name FROM Agency", conn)
    df_am = pd.read_sql_query("SELECT agency_id, amount FROM AgencyMission", conn)
    df_agency_budget = df_am.merge(df_agency, left_on='agency_id', right_on='id')
    budget_by_agency = df_agency_budget.groupby('name')['amount'].sum().sort_values(ascending=False).head(10)

    df_mission = pd.read_sql_query("SELECT mission_type FROM Mission", conn)
    missions_by_cat = df_mission['mission_type'].value_counts()

    df_am_time = pd.read_sql_query("SELECT transaction_date, amount FROM AgencyMission", conn)
    df_am_time['year'] = pd.to_datetime(df_am_time['transaction_date'], errors='coerce').dt.year
    budget_over_time = df_am_time.groupby('year')['amount'].sum().sort_index()
    budget_over_time = budget_over_time[budget_over_time.index.notna()]

    df_ast = pd.read_sql_query("SELECT agency_id FROM Astronaut", conn)
    ast_count = df_ast.merge(df_agency, left_on='agency_id', right_on='id')
    ast_per_agency = ast_count.groupby('name').size().sort_values(ascending=False).head(10)
    
    conn.close()
    return budget_by_agency, missions_by_cat, budget_over_time, ast_per_agency

def generate_charts(db_path):
    budget_by_agency, missions_by_cat, budget_over_time, ast_per_agency = get_analysis_data(db_path)
    

    plt.style.use('dark_background')
    
    charts = {}
    
    fig, ax = plt.subplots(figsize=(6, 4))
    budget_by_agency.plot(kind='barh', ax=ax, color='#06b6d4') 
    ax.set_title("Top 10 Agencies by Budget ($)", fontsize=11, fontweight='bold', pad=10, color='#f3f4f6')
    ax.set_xlabel("Total Budget ($)", fontsize=9, color='#9ca3af')
    ax.set_ylabel("Agency Name", fontsize=9, color='#9ca3af')
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.tick_params(axis='both', colors='#9ca3af', labelsize=8)
    ax.grid(True, linestyle='--', alpha=0.15)
    plt.tight_layout()
    charts['budget_by_agency'] = fig_to_base64(fig)
    plt.close(fig)
    

    fig, ax = plt.subplots(figsize=(6, 4))
    if len(missions_by_cat) > 5:
        top_cats = missions_by_cat.head(4)
        others = pd.Series([missions_by_cat.iloc[4:].sum()], index=['Other'])
        missions_by_cat_pie = pd.concat([top_cats, others])
    else:
        missions_by_cat_pie = missions_by_cat
        
    missions_by_cat_pie.plot(kind='pie', ax=ax, autopct='%1.1f%%', 
                             colors=['#06b6d4', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'],
                             textprops={'fontsize': 8, 'color': '#ffffff'})
    ax.set_title("Missions by Category", fontsize=11, fontweight='bold', pad=10, color='#f3f4f6')
    ax.set_ylabel("")
    plt.tight_layout()
    charts['missions_by_category'] = fig_to_base64(fig)
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    budget_over_time = budget_over_time.dropna()
    budget_over_time.plot(kind='line', ax=ax, color='#ef4444', marker='o', linewidth=2)
    ax.set_title("Yearly Budget Allocation Trend", fontsize=11, fontweight='bold', pad=10, color='#f3f4f6')
    ax.set_xlabel("Year", fontsize=9, color='#9ca3af')
    ax.set_ylabel("Total Budget ($)", fontsize=9, color='#9ca3af')
    ax.set_xticks(budget_over_time.index)
    ax.set_xticklabels(budget_over_time.index.astype(int))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax.tick_params(axis='both', colors='#9ca3af', labelsize=8)
    ax.grid(True, linestyle='--', alpha=0.15)
    plt.tight_layout()
    charts['budget_over_time'] = fig_to_base64(fig)
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ast_per_agency.plot(kind='bar', ax=ax, color='#10b981') 
    ax.set_title("Top 10 Agencies by Astronauts", fontsize=11, fontweight='bold', pad=10, color='#f3f4f6')
    ax.set_xlabel("Agency Name", fontsize=9, color='#9ca3af')
    ax.set_ylabel("Number of Astronauts", fontsize=9, color='#9ca3af')
    ax.tick_params(axis='both', colors='#9ca3af', labelsize=8)
    plt.xticks(rotation=45, ha='right')
    ax.grid(True, linestyle='--', alpha=0.15)
    plt.tight_layout()
    charts['astronauts_per_agency'] = fig_to_base64(fig)
    plt.close(fig)
    
    return charts

def fig_to_base64(fig):
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, format='png', transparent=True, dpi=140)
    img_bytes.seek(0)
    return base64.b64encode(img_bytes.read()).decode('utf-8')

def get_key_stats(db_path):
    conn = sqlite3.connect(db_path)
    
    total_budget = pd.read_sql_query("SELECT SUM(amount) FROM AgencyMission", conn).iloc[0,0]
    total_agencies = pd.read_sql_query("SELECT COUNT(*) FROM Agency", conn).iloc[0,0]
    total_missions = pd.read_sql_query("SELECT COUNT(*) FROM Mission", conn).iloc[0,0]
    total_astronauts = pd.read_sql_query("SELECT COUNT(*) FROM Astronaut", conn).iloc[0,0]
    avg_budget = pd.read_sql_query("SELECT AVG(amount) FROM AgencyMission", conn).iloc[0,0]
    
    conn.close()
    
    return {
        "total_budget": format(int(total_budget or 0), ','),
        "total_agencies": total_agencies,
        "total_missions": total_missions,
        "total_astronauts": total_astronauts,
        "avg_budget": format(int(avg_budget or 0), ',')
    }
