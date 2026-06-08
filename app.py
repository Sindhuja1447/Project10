from flask import Flask, render_template, request, redirect, url_for, session
import os
import subprocess
import sys
import signal

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'replace-with-a-secure-random-key')

# Global variable to track the running process
monitor_process = None

@app.route('/')
def root():
    if session.get('logged_in'): 

        
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    username = session.get('username', 'User')
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    error = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if password == 'password' and username.strip():  # Accept any username with correct password
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/monitor')
def monitor():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Preserve saved values
    fatigue_threshold = session.get('fatigue_threshold', 25)
    drowsiness_threshold = session.get('drowsiness_threshold', 10)
    hydration_interval = session.get('hydration_interval', 30)
    
    return render_template('config.html', 
                         fatigue_threshold=fatigue_threshold, 
                         drowsiness_threshold=drowsiness_threshold, 
                         hydration_interval=hydration_interval)

@app.route('/config')
def config():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Show default values initially
    return render_template('config.html', 
                         fatigue_threshold=25, 
                         drowsiness_threshold=10, 
                         hydration_interval=30)

@app.route('/save_settings', methods=['POST'])
def save_settings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Get all values from form
    fatigue_threshold = request.form.get('fatigue_threshold', '25')
    drowsiness_threshold = request.form.get('drowsiness_threshold', '10')
    hydration_interval = request.form.get('hydration_interval', '').strip()
    
    # Store all values in session
    session['fatigue_threshold'] = fatigue_threshold
    session['drowsiness_threshold'] = drowsiness_threshold
    
    # Handle hydration (optional)
    if hydration_interval:
        session['hydration_interval'] = hydration_interval
    else:
        session['hydration_interval'] = 30  # Default
    
    return render_template('config.html', 
                         fatigue_threshold=session['fatigue_threshold'], 
                         drowsiness_threshold=session['drowsiness_threshold'], 
                         hydration_interval=session['hydration_interval'],
                         saved=True)

@app.route('/run', methods=['POST'])
def run_code():
    global monitor_process
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Stop existing process if running
    if monitor_process and monitor_process.poll() is None:
        monitor_process.terminate()
        monitor_process = None
    
    hydration_interval = request.form.get('hydration_interval', '30')
    fatigue_threshold = request.form.get('fatigue_threshold', '25')
    drowsiness_threshold = request.form.get('drowsiness_threshold', '10')
    
    # Handle empty hydration interval
    if not hydration_interval or hydration_interval.strip() == '':
        hydration_interval = '30'
    
    # Convert minutes to seconds
    hydration_seconds = int(hydration_interval) * 60
    app_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(app_dir, "fatigue_monitor.py")
    monitor_process = subprocess.Popen(
        [sys.executable, script_path, "--hydration_interval", str(hydration_seconds), 
         "--fatigue_threshold", str(fatigue_threshold), "--drowsiness_threshold", str(drowsiness_threshold)],
        cwd=app_dir
    )
    return render_template('started.html', hydration_interval=hydration_interval, 
                          fatigue_threshold=fatigue_threshold, drowsiness_threshold=drowsiness_threshold)

@app.route('/stop', methods=['POST'])
def stop_camera():
    global monitor_process
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if monitor_process and monitor_process.poll() is None:
        try:
            # Try graceful termination first
            monitor_process.terminate()
            monitor_process.wait(timeout=3)  # Wait up to 3 seconds for graceful termination
        except subprocess.TimeoutExpired:
            # Force kill if graceful termination fails
            monitor_process.kill()
        except:
            pass
        monitor_process = None
    
    # Preserve saved values
    fatigue_threshold = session.get('fatigue_threshold', 25)
    drowsiness_threshold = session.get('drowsiness_threshold', 10)
    hydration_interval = session.get('hydration_interval', 30)
    
    return render_template('config.html', 
                         fatigue_threshold=fatigue_threshold, 
                         drowsiness_threshold=drowsiness_threshold, 
                         hydration_interval=hydration_interval)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)