import streamlit as st
import time
from simulation import Simulation
from styles import load_css
from process import ProcessState

# Setup page
st.set_page_config(page_title="PROCESS MONITOR", layout="wide", initial_sidebar_state="expanded")
load_css()

# Initialize session state
if "sim" not in st.session_state:
    st.session_state.sim = Simulation()
    st.session_state.sim.init_processes(10)

sim = st.session_state.sim

# Main Header
st.markdown("<h1 style='text-align: center;'>PROCESS MONITOR</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #888;'>PCB + Process State Dashboard</h4>", unsafe_allow_html=True)

# Controls
st.markdown("---")
cols = st.columns([1, 1, 1, 2, 1, 1])
with cols[0]:
    if st.button("▶ Start Simulation"):
        sim.is_running = True
with cols[1]:
    if st.button("⏸ Pause Simulation"):
        sim.is_running = False
with cols[2]:
    if st.button("🔄 Reset"):
        st.session_state.sim = Simulation()
        st.session_state.sim.init_processes(10)
        sim = st.session_state.sim
with cols[3]:
    speed_map = {"Slow": 1.5, "Normal": 0.5, "Fast": 0.1}
    speed_selection = st.selectbox("Simulation Speed", ["Slow", "Normal", "Fast"], index=1, label_visibility="collapsed")
    sim.speed = speed_map[speed_selection]
with cols[4]:
    if st.button("➕ Create Process"):
        sim.create_process()
with cols[5]:
    st.write(f"**Clock:** {sim.clock}")

st.markdown("---")

# Summary metrics
total = len(sim.processes)
new_c = sum(1 for p in sim.processes if p.state == ProcessState.NEW)
ready_c = sum(1 for p in sim.processes if p.state == ProcessState.READY)
running_c = sum(1 for p in sim.processes if p.state == ProcessState.RUNNING)
waiting_c = sum(1 for p in sim.processes if p.state == ProcessState.WAITING)
term_c = sum(1 for p in sim.processes if p.state == ProcessState.TERMINATED)

st.markdown(f"""
<div style="display: flex; justify-content: space-between; gap: 10px;">
    <div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">Total Processes</div></div>
    <div class="metric-card"><div class="metric-value">{new_c}</div><div class="metric-label">New</div></div>
    <div class="metric-card"><div class="metric-value">{ready_c}</div><div class="metric-label">Ready</div></div>
    <div class="metric-card"><div class="metric-value">{running_c}</div><div class="metric-label">Running</div></div>
    <div class="metric-card"><div class="metric-value">{waiting_c}</div><div class="metric-label">Waiting</div></div>
    <div class="metric-card"><div class="metric-value">{term_c}</div><div class="metric-label">Terminated</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Dashboard Layout
col_main, col_side = st.columns([7, 3])

with col_main:
    st.markdown("### Live Process Table")
    
    html = """
    <table class="proc-table">
    <tr>
        <th>PID</th><th>Process Name</th><th>State</th><th>Priority</th>
        <th>CPU Usage</th><th>Memory</th><th>PC</th><th>I/O Status</th>
    </tr>
    """
    for p in sim.processes:
        badge = f'<span class="badge-{p.state.value}">{p.state.value}</span>'
        html += f"<tr><td>{p.pid}</td><td>{p.name}</td><td>{badge}</td><td>{p.priority}</td><td>{p.cpu_usage}/{p.total_burst_time}</td><td>{p.memory_usage} MB</td><td>{p.program_counter}</td><td>{p.io_status}</td></tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

with col_side:
    st.markdown("### PCB Inspector")
    process_options = {p.pid: f"PID {p.pid} - {p.name}" for p in sim.processes}
    
    selected_pid = st.selectbox("Select Process", options=list(process_options.keys()), format_func=lambda x: process_options[x], label_visibility="collapsed")
    
    if selected_pid:
        p = sim.get_process(selected_pid)
        if p:
            st.markdown(f"""
            <div class="pcb-card">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span class="badge-{p.state.value}" style="font-size: 16px;">{p.state.value}</span>
                </div>
                <div class="pcb-row"><span class="pcb-key">PID:</span><span class="pcb-val">{p.pid}</span></div>
                <div class="pcb-row"><span class="pcb-key">Process Name:</span><span class="pcb-val">{p.name}</span></div>
                <div class="pcb-row"><span class="pcb-key">Unique ID:</span><span class="pcb-val">{p.unique_id[:8]}...</span></div>
                <div class="pcb-row"><span class="pcb-key">State:</span><span class="pcb-val">{p.state.value}</span></div>
                <div class="pcb-row"><span class="pcb-key">Priority:</span><span class="pcb-val">{p.priority}</span></div>
                <div class="pcb-row"><span class="pcb-key">Parent PID:</span><span class="pcb-val">{p.parent_pid}</span></div>
                <div class="pcb-row"><span class="pcb-key">Creation Time:</span><span class="pcb-val">{p.creation_time}</span></div>
                <div class="pcb-row"><span class="pcb-key">CPU Usage:</span><span class="pcb-val">{p.cpu_usage} / {p.total_burst_time}</span></div>
                <div class="pcb-row"><span class="pcb-key">Memory Usage:</span><span class="pcb-val">{p.memory_usage} MB</span></div>
                <div class="pcb-row"><span class="pcb-key">Prog Counter (PC):</span><span class="pcb-val">{p.program_counter}</span></div>
                <div class="pcb-row"><span class="pcb-key">I/O Status:</span><span class="pcb-val">{p.io_status}</span></div>
                <div class="pcb-row"><span class="pcb-key">Registers:</span><span class="pcb-val">{p.cpu_registers}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if p.state != ProcessState.TERMINATED:
                if st.button("🛑 Terminate Process", key="term_btn", use_container_width=True):
                    sim.terminate_process(p.pid)
                    st.rerun()

st.markdown("---")
col_bottom1, col_bottom2 = st.columns([1, 1])

with col_bottom1:
    st.markdown("### Process State Visualization")
    st.markdown("Current state of selected process is highlighted.", unsafe_allow_html=True)
    
    if selected_pid:
        p = sim.get_process(selected_pid)
        state = p.state.value if p else "NEW"
        
        def get_color(node_state):
            colors = {
                "NEW": "#6c757d",
                "READY": "#ffc107",
                "RUNNING": "#28a745",
                "WAITING": "#17a2b8",
                "TERMINATED": "#dc3545"
            }
            if node_state == state:
                return colors[node_state]
            return "#444"
            
        diagram_html = f"""
        <div style="text-align: center; font-family: monospace; font-size: 18px; background: #1e1e2f; padding: 30px; border-radius: 8px; border: 1px solid #333; margin-top: 10px;">
            <span style="color: {get_color('NEW')}; font-weight: bold; border: 2px solid {get_color('NEW')}; padding: 5px; border-radius: 5px;">NEW</span>
            &nbsp; ➔ &nbsp;
            <span style="color: {get_color('READY')}; font-weight: bold; border: 2px solid {get_color('READY')}; padding: 5px; border-radius: 5px;">READY</span>
            &nbsp; ➔ &nbsp;
            <span style="color: {get_color('RUNNING')}; font-weight: bold; border: 2px solid {get_color('RUNNING')}; padding: 5px; border-radius: 5px;">RUNNING</span>
            &nbsp; ➔ &nbsp;
            <span style="color: {get_color('TERMINATED')}; font-weight: bold; border: 2px solid {get_color('TERMINATED')}; padding: 5px; border-radius: 5px;">TERMINATED</span>
            <br><br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            ↖ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↙
            <br><br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span style="color: {get_color('WAITING')}; font-weight: bold; border: 2px solid {get_color('WAITING')}; padding: 5px; border-radius: 5px;">WAITING</span>
        </div>
        """
        st.markdown(diagram_html, unsafe_allow_html=True)
        
with col_bottom2:
    st.markdown("### Event Log")
    event_html = """
    <div style="height: 250px; overflow-y: auto; background-color: #1e1e2f; padding: 10px; border-radius: 8px; border: 1px solid #333; margin-top: 10px;">
    <table class="proc-table" style="font-size: 14px; margin-top: 0;">
    <tr><th>Time</th><th>PID</th><th>Process</th><th>Transition</th><th>Event</th></tr>
    """
    for e in sim.events[:20]:
        transition = f"{e['old_state']} ➔ {e['new_state']}"
        event_html += f"<tr><td>{e['timestamp']}</td><td>{e['pid']}</td><td>{e['process']}</td><td>{transition}</td><td>{e['event']}</td></tr>"
    event_html += "</table></div>"
    st.markdown(event_html, unsafe_allow_html=True)

st.markdown("---")
with st.expander("COOS Concepts Demonstrated"):
    st.markdown("""
    - **Process**: A program in execution. Here simulated with randomly generated burst times and memory requirements.
    - **PCB (Process Control Block)**: A data structure containing information about the process (PID, State, Program Counter, CPU Registers, Memory, etc.). Selecting a process shows its live PCB.
    - **Process States**: The lifecycle of a process (NEW, READY, RUNNING, WAITING, TERMINATED).
    - **State Transitions**: Processes change state according to OS rules (e.g., admitting to READY, dispatching to RUNNING, interrupting via time-slice to READY, requesting I/O to WAITING).
    - **Scheduling**: The OS must decide which process in the READY queue gets the CPU next. This simulator uses a basic Priority Scheduling approach.
    - **CPU Utilization & I/O Waiting**: When a process is RUNNING, it consumes CPU time. If it requires I/O, it transitions to WAITING, freeing the CPU for another process.
    """)

# Simulation loop handler
if sim.is_running:
    sim.tick()
    time.sleep(sim.speed)
    st.rerun()
