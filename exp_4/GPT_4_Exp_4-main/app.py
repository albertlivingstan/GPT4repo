from flask import Flask, render_template, request, jsonify
from recommendation_module import generate_recommendations
from feedback_module import refine_recommendations
from save_module import save_recommendations
from intent_module import detect_intent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()

        profile = {
            "name": data["name"],
            "age": data["age"],
            "background": data["background"],
            "interests": data["interests"],
            "skill_level": data["skill_level"],
            "preference": data["preference"],
            "goal": data["goal"],
            "num_items": int(data["num_items"])
        }

        recommendations = generate_recommendations(profile)

        return jsonify({
            "success": True,
            "profile": profile,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route("/refine", methods=["POST"])
def refine():
    try:
        data = request.get_json()

        profile = data["profile"]
        feedback = data["feedback"]

        recommendations = refine_recommendations(
            profile,
            feedback
        )

        return jsonify({
            "success": True,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route("/save", methods=["POST"])
def save():
    try:
        data = request.get_json()

        recommendations = data["recommendations"]

        save_recommendations(recommendations)

        return jsonify({
            "success": True,
            "message": "Recommendations saved successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
@app.route("/intent", methods=["POST"])
def intent():

    try:
        data = request.get_json()

        user_input = data["input"]

        detected_intent = detect_intent(user_input)

        return jsonify({
            "success": True,
            "intent": detected_intent
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)