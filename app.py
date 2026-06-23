from flask import Flask, render_template_string, request
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load Model
try:
    with open("adaboost.pkl", "rb") as f:
        model = pickle.load(f)
    model_loaded = True
    model_error = None
except Exception as e:
    model_loaded = False
    model_error = str(e)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Developer Productivity Predictor</title>

    <style>
        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:'Segoe UI',sans-serif;
        }

        body{
            min-height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            padding:20px;
            background:linear-gradient(-45deg,#667eea,#764ba2,#6a11cb,#2575fc);
            background-size:400% 400%;
            animation:gradientBG 10s ease infinite;
        }

        @keyframes gradientBG{
            0%{background-position:0% 50%;}
            50%{background-position:100% 50%;}
            100%{background-position:0% 50%;}
        }

        .container{
            width:100%;
            max-width:900px;
            background:rgba(255,255,255,0.15);
            backdrop-filter:blur(12px);
            border-radius:20px;
            padding:30px;
            box-shadow:0 8px 32px rgba(0,0,0,0.3);
            animation:fadeIn 1s ease;
        }

        @keyframes fadeIn{
            from{
                opacity:0;
                transform:translateY(30px);
            }
            to{
                opacity:1;
                transform:translateY(0);
            }
        }

        h1{
            text-align:center;
            color:white;
            margin-bottom:25px;
        }

        .grid{
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
            gap:15px;
        }

        label{
            color:white;
            display:block;
            margin-bottom:5px;
        }

        input{
            width:100%;
            padding:12px;
            border:none;
            border-radius:10px;
            outline:none;
        }

        button{
            width:100%;
            margin-top:20px;
            padding:14px;
            border:none;
            border-radius:12px;
            background:#00e676;
            color:black;
            font-size:18px;
            font-weight:bold;
            cursor:pointer;
            transition:0.3s;
        }

        button:hover{
            transform:scale(1.03);
        }

        .result{
            margin-top:20px;
            padding:15px;
            border-radius:10px;
            background:rgba(255,255,255,0.2);
            color:white;
            text-align:center;
            font-size:20px;
            font-weight:bold;
        }
    </style>
</head>

<body>

<div class="container">

<h1>🚀 Developer Productivity Predictor</h1>

<form method="POST">

<div class="grid">

<div>
<label>Hours Coding</label>
<input type="number" step="any" name="Hours_Coding" required>
</div>

<div>
<label>AI Usage Hours</label>
<input type="number" step="any" name="AI_Usage_Hours" required>
</div>

<div>
<label>Lines of Code</label>
<input type="number" step="any" name="Lines_of_Code" required>
</div>

<div>
<label>Commits</label>
<input type="number" step="any" name="Commits" required>
</div>

<div>
<label>Bugs Reported</label>
<input type="number" step="any" name="Bugs_Reported" required>
</div>

<div>
<label>Sleep Hours</label>
<input type="number" step="any" name="Sleep_Hours" required>
</div>

<div>
<label>Distractions</label>
<input type="number" step="any" name="Distractions" required>
</div>

<div>
<label>Cognitive Load</label>
<input type="number" step="any" name="Cognitive_Load" required>
</div>

<div>
<label>Stress Level</label>
<input type="number" step="any" name="Stress_Level" required>
</div>

</div>

<button type="submit">Predict Productivity</button>

</form>

{% if prediction %}
<div class="result">
    {{ prediction }}
</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        try:

            if not model_loaded:
                raise Exception(model_error)

            data = pd.DataFrame([{
                "Hours_Coding": float(request.form["Hours_Coding"]),
                "AI_Usage_Hours": float(request.form["AI_Usage_Hours"]),
                "Lines_of_Code": float(request.form["Lines_of_Code"]),
                "Commits": float(request.form["Commits"]),
                "Bugs_Reported": float(request.form["Bugs_Reported"]),
                "Sleep_Hours": float(request.form["Sleep_Hours"]),
                "Distractions": float(request.form["Distractions"]),
                "Cognitive_Load": float(request.form["Cognitive_Load"]),
                "Stress_Level": float(request.form["Stress_Level"])
            }])

            pred = model.predict(data)[0]

            prediction = f"Prediction Result: {pred}"

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template_string(HTML, prediction=prediction)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
