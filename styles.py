import streamlit as st

def load_css():
    st.markdown("""
    <style>
    body {
        color: #eee;
    }
    .badge-RUNNING { background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    .badge-READY { background-color: #ffc107; color: black; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    .badge-WAITING { background-color: #17a2b8; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    .badge-NEW { background-color: #6c757d; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    .badge-TERMINATED { background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    
    .metric-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        flex: 1;
    }
    .metric-value { font-size: 32px; font-weight: bold; color: #fff; }
    .metric-label { font-size: 14px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }
    
    .proc-table { width: 100%; border-collapse: collapse; margin-top: 10px; color: #eee; font-family: sans-serif; }
    .proc-table th { background-color: #2b2b36; padding: 10px; text-align: left; border-bottom: 2px solid #444; }
    .proc-table td { padding: 10px; border-bottom: 1px solid #333; }
    .proc-table tr:hover { background-color: #333344; }

    .pcb-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #444;
        font-family: monospace;
        font-size: 14px;
    }
    .pcb-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        border-bottom: 1px solid #333;
        padding-bottom: 4px;
    }
    .pcb-key { color: #888; }
    .pcb-val { color: #eee; font-weight: bold; text-align: right; }
    </style>
    """, unsafe_allow_html=True)
