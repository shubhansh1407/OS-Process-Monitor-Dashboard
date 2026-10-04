# COOS Process Monitor Dashboard

A simulated Operating System Process Monitor built with Python and Streamlit. This dashboard visually demonstrates key COOS concepts including Processes, PCB (Process Control Block), Process States, State Transitions, and Scheduling.

## Features

- **Live Process Table**: View simulated processes and their current states.
- **PCB Inspector**: Inspect detailed Process Control Block (PCB) data for a selected process.
- **Process State Visualization**: Live diagram highlighting the current state of a selected process.
- **Event Log**: Real-time log of process state transitions and OS events.
- **Simulation Controls**: Start, pause, reset, and adjust simulation speed. Add or terminate processes on the fly.

## Setup Instructions

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```
