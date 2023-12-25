import pandas as pd
import harperdb as db
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import os

app = Flask(__name__)

app.secret_key = 'proper_finance_proper_life'

# Define routes for home, about, and contact pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/upload', methods=['POST'])
def upload():
    print(request.files)
    if 'file' not in request.files:
        return "No file"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Process the uploaded Excel file
    if file:
        # Save the file first
        file_path = 'uploads/' + file.filename
        file.save(file_path)

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Separate the data into income, expenses, and investments
        df_income = df[df['type'] == 'income']
        df_expense = df[df['type'] == 'expense']
        df_investment = df[df['type'] == 'investment']

        # Process income data
        if not df_income.empty:
            total_income = df_income['amount'].sum()
            flash(f'Total Income: ${total_income:.2f}', 'success')

        # Process expense data
        if not df_expense.empty:
            # Count occurrences of each expense source
            expense_data = df_expense.groupby('source')['amount'].sum()

            # Plotting the pie chart for expenses
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.pie(expense_data, labels=expense_data.index, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3, edgecolor='w'))
            ax.set_title('Expenses', fontsize=16)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Convert the plot to an image
            image_path = os.path.join(app.static_folder, 'images', 'exp_pie_chart.png')
            canvas = FigureCanvas(fig)
            canvas.print_png(image_path)

            # Set pie_chart_available to True
            pie_chart_available = True

        else:
            # Set pie_chart_available to False if no expense data
            pie_chart_available = False

        # Render the template with the pie chart availability
        return render_template('index.html', pie_chart_available=pie_chart_available)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

