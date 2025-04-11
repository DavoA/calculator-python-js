from flask import Flask, render_template, request, jsonify
import mysql.connector
import re

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'calculator_db'

def parse_expression(expression):
    parts = re.findall(r'(?<!\d)-?\d+\.\d+|(?<!\d)-?\d+|[+*/×÷()-]', expression)
    if len(parts) != 3:
        raise ValueError("Invalid expression format")
    num1 = float(parts[0])
    op = parts[1]
    num2 = float(parts[2])
    result = eval(expression)
    return num1, op, num2, result

def store_calculation(num1, op, num2, result):
    conn = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port=3306
    )
    cur = conn.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS calculations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_number DECIMAL(10, 2) NOT NULL,
            operation VARCHAR(1) NOT NULL,
            second_number DECIMAL(10, 2) NOT NULL,
            result DECIMAL(10, 2) NOT NULL
        );
    """
    cur.execute(create_table_query)
    conn.commit()

    insert_query = """
        INSERT INTO calculations (first_number, operation, second_number, result)
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(insert_query, (num1, op, num2, result))
    conn.commit()

    cur.close()
    conn.close()

def validate_expression(expr):
    if not expr:
        return False, "Empty"
    
    if not re.fullmatch(r'^[\d+\-*/.×÷⌫C]+$', expr):
        return False, "Wrong symbols"
    
    if re.search(r'[\+\-\*/\.]{2,}', expr):
        return False, "Wrong operators"
    
    return True, ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    raw_expression = data.get('expression', '')

    expression = raw_expression.replace('×','*').replace('÷','/')

    is_valid, err_message = validate_expression(expression)
    if not is_valid:
        return jsonify({"error": err_message}), 400
    try:
        num1, op, num2, result = parse_expression(expression)
        store_calculation(num1, op, num2, result)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": f"Evaluate error:  {str(e)}"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
