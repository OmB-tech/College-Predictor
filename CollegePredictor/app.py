from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the data from the Excel file once when the app starts
# Ensure 'min' column is treated as float for accurate comparison
data = pd.read_excel("b1.xlsx", dtype={'min': float})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    try:
        user_score = round(float(request.form['mhcet_score']), 5)
        category = request.form['category']
    except ValueError:
        return "<p>Please enter a valid MHTCET score.</p>", 400

    # Filter data: Match category and scores above the minimum required
    filtered_data = data[(data['seat_type'] == category) & (data['min'] <= user_score)]
    
    # Sort by 'college_name' alphabetically in ascending order
    filtered_data = filtered_data.sort_values(by='college_name')

    # Extract college name and branch to display
    results = filtered_data[['college_name', 'branch']].to_dict(orient='records')
    
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
