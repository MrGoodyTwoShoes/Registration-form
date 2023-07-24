from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'SST'
}

# Route to render the registration form
@app.route('/')
def registration_form():
    return render_template('reg_form.html')

# Route to handle the form submission and store data in the database
@app.route('/register', methods=['POST'])
def register():
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Connect to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user already exists by querying the database
        sql_check = "SELECT COUNT(*) FROM reg_dets WHERE username = %s OR email = %s"
        data_check = (name, email)
        cursor.execute(sql_check, data_check)
        result = cursor.fetchone()

        if result and result[0] > 0:
            # User with the same username or email already exists
            cursor.close()
            conn.close()
            return redirect('/reg_error')

        # Insert user details into the database
        sql_insert = "INSERT INTO reg_dets (username, email, password) VALUES (%s, %s, %s)"
        data_insert = (name, email, password)
        cursor.execute(sql_insert, data_insert)

        # Commit the changes
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        # Redirect to the success page (GET request)
        return render_template('reg_success.html')
    except Exception as e:
        return f"Error: {str(e)}"

# Route to handle the registration success page (GET request)
@app.route('/reg_success')
def registration_success():
    return render_template('reg_success.html')

# Route to handle the registration error page (GET request)
@app.route('/reg_error')
def reg_error():
    return render_template('reg_error.html')


if __name__ == '__main__':
    app.run(debug=True)
