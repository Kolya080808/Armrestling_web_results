# Сайт для проведения турнира по армрестлингу

## Детали:

1. если кратко этот сайт был написан за меньше чем неделю, поэтому он немного убогий
2. задача была создать сайт, который будет выводить лидеров и расписание из цсв таблицы на страницу и автоматом обновлять, а так же чтобы без доступа к серверу напрямую через ссх или фтп можно было загрузить файл


## Основное:

### Страницы:

base.html - это самое базовое из хтмл, что нужно было на сайте (чтобы несколько раз не использовать одни и те же строки)
admin.html - собственно то, где мы и загружаем файл таблицы без доступа через ссх
login.html - если нет куки либо был введен неправильный пароль, вместо admin.html загружается эта страница
index.html - просто переход на таблицу лидеров и расписание
leader.html - понятно
schedule.html - понятно

### Данные:

leaders - папка с таблицами лидеров (можно загрузить несколько файлов и выбрать просто один из них, либо поудалять все файлы из папок в той же админке)
schedules - папка с таблицами расписания (то же самое)
current_leaders.txt - выбранная таблица лидеров
current_schedule.txt - выбранная таблица расписания

### app.py:


Теперь основной код. Он не шибко гениальный или большой, но все таки я его продумал.

```python
from flask import Flask, render_template, request, redirect, url_for, session # - импорт не всех библиотек, а только тех, что нужны для данного сайта
import csv # - ну, чтение цсв таблиц требует библиотеку для цсв таблиц
import os # - для удаления файла
```

Далее я просто ввел все самые дефолтные переменные, так как ломать нас никто не собирался в школе:


```python
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Простые учетные данные
USER_CREDENTIALS = {'admin': 'admin1234'}

def read_csv(filename, folder):
    with open(f'data/{folder}/{filename}') as f:
        return list(csv.reader(f, delimiter=";"))

```


Функция для чтения цсвшки:


```python
def read_csv(filename, folder):
    with open(f'data/{folder}/{filename}') as f:
        return list(csv.reader(f, delimiter=";"))

```

Дальше просто рендер разных страниц (там не сильно сложно, просто определенные запросы и ответы с данными которые нам нужны):


```python
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
    with open('data/current_leaders.txt') as f:
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
        # Обработка УДАЛЕНИЯ файла
        if 'delete' in request.form:
            filename = request.form['filename']
            folder_type = request.form['folder_type']
            try:
                os.remove(f'data/{folder_type}/{filename}')
            except FileNotFoundError:
                pass

        # Обработка ВЫБОРА активного файла
        elif 'set_active' in request.form:
            filename = request.form['filename']
            folder_type = request.form['folder_type']
            with open(f'data/current_{folder_type}.txt', 'w') as f:
                f.write(filename)

        # Обработка ЗАГРУЗКИ файла
        elif 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                folder_type = request.form['folder_type']
                file.save(f'data/{folder_type}/{file.filename}')

    # Остальной код без изменений
    schedules = os.listdir('data/schedules')
    leaders = os.listdir('data/leaders')
    return render_template('admin.html', schedules=schedules, leaders=leaders)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
```

Ну и запуск сервера на определенном порте:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

```


В принципе на этом все, но если вам что-то не понятно, или вы просто хотите поинтересоваться - [создайте issue](https://github.com/Kolya080808/Armrestling_web_results/issues/new), я вам все объясню




Создатели: @Kolya080808, @MihanN1


Всем кто читал, спасибо, что зашли :)
