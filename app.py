from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# ✅ Replace with your actual Google Sheet file ID
FILE_ID = "1xO1wDrnLlArmLRvLwvXgqZPHdoU3vadeM5vG9py3vCY"

# ✅ This assumes only ONE sheet in the file (gid=0)
CSV_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=csv&gid=0"

@app.route('/', methods=['GET', 'POST'])
def index():
    search_term = ""
    results = None

    try:
        df = pd.read_csv(CSV_URL)
    except Exception as e:
        return f"❌ Error loading data: {e}"

    if request.method == 'POST':
        search_term = request.form.get('search_term', '')

        # Search in all text-based columns
        search_columns = df.select_dtypes(include='object').columns
        results = df[df[search_columns].apply(
            lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(),
            axis=1
        )]

    return render_template("index.html", search_term=search_term, results=results)

if __name__ == '__main__':
    app.run(debug=True)
