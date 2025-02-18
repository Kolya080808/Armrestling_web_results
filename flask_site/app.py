from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Простые учетные данные
USER_CREDENTIALS = {'admin': 'admin1234'}

def read_csv(filename, folder):
    with open(f'data/{folder}/{filename}') as f:
        return list(csv.reader(f))

@app.route('/')
def index():
    return render_template('index.html', title="Главная страница")

@app.route('/schedule')
def schedule():
    with open('data/current_schedule.txt') as f:
        filename = f.read().strip()
    data = read_csv(filename, 'schedules')
    return render_template('schedule.html', data=data, title="Расписание")

@app.route('/leaders')
def leaders():
    with open('data/current_leaderboard.txt') as f:
        filename = f.read().strip()
    data = read_csv(filename, 'leaders')
    return render_template('leaders.html', data=data, title="Таблица лидеров")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USER_CREDENTIALS.get(username) == password:
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Обработка загрузки файлов
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            folder = 'schedules' if 'schedule' in request.form else 'leaders'
            file.save(f'data/{folder}/{file.filename}')
        
        # Обработка удаления файлов
        if 'delete' in request.form:
            filename = request.form['filename']
            folder = 'schedules' if 'schedule' in request.form else 'leaders'
            os.remove(f'data/{folder}/{filename}')
        
        # Обработка выбора активного файла
        if 'set_active' in request.form:
            filename = request.form['filename']
            folder = 'schedules' if 'schedule' in request.form else 'leaders'
            with open(f'data/current_{folder}.txt', 'w') as f:
                f.write(filename)
    
    schedules = os.listdir('data/schedules')
    leaders = os.listdir('data/leaders')
    return render_template('admin.html', schedules=schedules, leaders=leaders)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
