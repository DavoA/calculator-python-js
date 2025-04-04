from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__, template_folder="templates", static_folder="static")

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
        result = eval(expression)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": f"Evaluate error:  {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)