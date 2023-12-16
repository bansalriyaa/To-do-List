from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Mock database for storing tasks
tasks = [{'id': 1, 'title': 'Task 1', 'due_date': '2023-12-31', 'priority': 'High', 'user_id': 1}]

# Mock user class
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Mock users for demonstration purposes
users = {1: User(1)}

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))


@app.route('/')
@login_required
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = 1  # Mock user ID
        user = users.get(user_id)
        login_user(user)
        flash('Login successful', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        task_id = len(tasks) + 1
        tasks.append({'id': task_id, 'title': title, 'due_date': due_date, 'priority': priority, 'user_id': current_user.id})
        flash('Task added successfully', 'success')
    return redirect(url_for('index'))


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id and t['user_id'] == current_user.id), None)
    if task is None:
        flash('Task not found', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        task['title'] = title
        task['due_date'] = due_date
        task['priority'] = priority
        flash('Task updated successfully', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if not (t['id'] == task_id and t['user_id'] == current_user.id)]
    flash('Task deleted successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
