from flask import Flask, render_template, request, redirect, url_for, flash
import re # For email validation

app = Flask(__name__)
# Secret key needed for flashing messages
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Global list to store To-Do items [cite: 17]
# Each item will be a dictionary: {'task': '...', 'email': '...', 'priority': '...'} [cite: 9]
todo_list = []

# Email validation regex (simple version) [cite: 30]
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@app.route('/') # [cite: 10, 17]
def index():
    """
    Displays the current To-Do list and the form to add new items. [cite: 10]
    """
    return render_template('index.html', todo_list=todo_list)

@app.route('/submit', methods=['POST']) # [cite: 11, 27, 30]
def submit():
    """
    Handles the submission of new To-Do items. [cite: 11]
    Validates input and adds the item to the list if valid. [cite: 30]
    """
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    error = False
    # Data Validation [cite: 30]
    if not task:
        flash('Task description cannot be empty.')
        error = True
    if not email or not re.match(EMAIL_REGEX, email):
        flash('Invalid or missing email address.') # [cite: 30]
        error = True
    if priority not in ['Low', 'Medium', 'High']:
        flash('Invalid priority selected.') # [cite: 30]
        error = True

    if error:
        return redirect(url_for('index')) # [cite: 30]

    # Add item to the list if no errors [cite: 11, 32]
    todo_list.append({'task': task, 'email': email, 'priority': priority})
    flash('To-Do item added successfully!')
    return redirect(url_for('index')) # [cite: 11, 32]

@app.route('/clear', methods=['POST']) # [cite: 12, 35]
def clear():
    """
    Clears all items from the To-Do list. [cite: 12, 34]
    """
    global todo_list
    todo_list = [] # [cite: 34]
    flash('To-Do list cleared.')
    return redirect(url_for('index')) # [cite: 12, 35]

if __name__ == '__main__':
    # Note: debug=True is helpful for development but should be False in production
    app.run(debug=True) # [cite: 13]
