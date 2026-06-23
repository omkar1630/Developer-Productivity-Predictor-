from flask import Flask, render_template_string, request
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("adaboost(1).pkl", "rb"))

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
            background:linear-gradient(-45deg,#667eea,#764ba2,#6a11cb,#2575fc);
            background-size:400% 400%;
            animation:gradientBG 12s ease infinite;
        }

        @keyframes gradientBG{
            0%{background-position:0% 50%;}
            50%{background-position:100% 50%;}
            100%{background-position:0% 50%;}
        }

        .container{
            width:90%;
            max-width:900px;
            background:rgba(255,255,255,0.15);
            backdrop-filter:blur(12px);
            border-radius:20px;
            padding:30px;
            box-shadow:0 8px 32px rgba(0,0,0,0.3);
            animation:slideUp 1s ease;
        }

        @keyframes slideUp{
            from{
                transform:translateY(50px);
                opacity:0;
            }
            to{
                transform:translateY(0);
                opacity:1;
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

        .input-box{
            display:flex;
            flex-direction:column;
        }

        label{
            color:white;
            margin-bottom:5px;
        }

        input{
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
            transform:scale(1.05);
        }

        .result{
            margin-top:25px;
            text-align:center;
            color:white;
            font-size:24px;
            font-weight:bold;
            animation:fadeIn 1s ease;
        }

        @keyframes fadeIn{
            from{opacity:0;}
            to{opacity:1;}
        }
    </style>
</head>

<body>

<div class="container">

<h1>🚀 Developer Productivity Predictor</h1>

<form method="POST">

<div class="grid">

<div class="input-box">
<label>Hours Coding</label>
<input type="number" step="any" name="Hours_Coding" required>
</div>

<div class="input-box">
<label>AI Usage Hours</label>
<input type="number" step="any" name="AI_Usage_Hours" required>
</div>

<div class="input-box">
<label>Lines Of Code</label>
<input type="number" step="any" name="Lines_of_Code" required>
</div>

<div class="input-box">
<label>Commits</label>
<input type="number" step="any" name="Commits" required>
</div>

<div class="input-box">
<label>Bugs Reported</label>
<input type="number" step="any" name="Bugs_Reported" required>
</div>

<div class="input-box">
<label>Sleep Hours</label>
<input type="number" step="any" name="Sleep_Hours" required>
</div>

<div class="input-box">
<label>Distractions</label>
<input type="number" step="any" name="Distractions" required>
</div>

<div class="input-box">
<label>Cognitive Load</label>
<input type="number" step="any" name="Cognitive_Load" required>
</div>

<div class="input-box">
<label>Stress Level</label>
<input type="number" step="any" name="Stress_Level" required>
</div>

</div>

<button type="submit">Predict Productivity</button>

</form>

{% if prediction %}
<div class="result">
Prediction : {{ prediction }}
</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():

    prediction = None

    if request.method == "POST":

        data = [[
            float(request.form["Hours_Coding"]),
            float(request.form["AI_Usage_Hours"]),
            float(request.form["Lines_of_Code"]),
            float(request.form["Commits"]),
            float(request.form["Bugs_Reported"]),
            float(request.form["Sleep_Hours"]),
            float(request.form["Distractions"]),
            float(request.form["Cognitive_Load"]),
            float(request.form["Stress_Level"])
        ]]

        columns = [
            'Hours_Coding',
            'AI_Usage_Hours',
            'Lines_of_Code',
            'Commits',
            'Bugs_Reported',
            'Sleep_Hours',
            'Distractions',
            'Cognitive_Load',
            'Stress_Level'
        ]

        df = pd.DataFrame(data, columns=columns)

        pred = model.predict(df)[0]

        if pred == 1:
            prediction = "🔥 High Productivity"
        else:
            prediction = "⚠️ Low Productivity"

    return render_template_string(HTML, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
