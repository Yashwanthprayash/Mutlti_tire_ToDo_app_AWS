app = Flask(__name__)
# MySQL DB Config
DB_CONFIG = {
        'host': 'cloudzendb.ccrusy86s4fy.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Admin123#',
    'database': 'CloudZenDatabase',
    'cursorclass': pymysql.cursors.DictCursor  # To return rows as dictionaries
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    desc = request.form.get('description')
    if desc:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO tasks (description) VALUES (%s)", (desc,                                                                                                             ))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE tasks SET is_done = TRUE WHERE id = %s", (task_id                                                                                                             ,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

