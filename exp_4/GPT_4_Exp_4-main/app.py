import os
from flask import Flask, render_template, request, jsonify
from recommendation_module import generate_recommendations
from feedback_module import refine_recommendations
from save_module import save_recommendations
from intent_module import detect_intent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/personas")
def api_personas():
    personas = [
        {
            "id": "ai-engineer",
            "title": "AI Systems Engineer",
            "name": "Alex Chen",
            "age": 26,
            "background": "Computer Science (B.S.), 2 years backend Go/Python",
            "interests": "Large Language Models, Vector Databases, Agentic Systems, PyTorch",
            "skill_level": "Intermediate",
            "preference": "Hands-on projects and open-source system architectures",
            "goal": "Transition into an applied AI/ML engineering role building production RAG systems",
            "num_items": 4
        },
        {
            "id": "data-analyst",
            "title": "Data Analyst to ML",
            "name": "Priya Sharma",
            "age": 29,
            "background": "Business Analytics & SQL, Tableau, Excel",
            "interests": "Predictive Modeling, Scikit-learn, Python for Data Science, Statistics",
            "skill_level": "Beginner",
            "preference": "Interactive video courses with guided exercises",
            "goal": "Master end-to-end data science pipelines and machine learning algorithms",
            "num_items": 4
        },
        {
            "id": "cloud-devops",
            "title": "Cloud Architect",
            "name": "Jordan Miller",
            "age": 34,
            "background": "Systems Administration & Linux",
            "interests": "Kubernetes, Terraform, AWS Solutions Architecture, CI/CD, Zero-Trust",
            "skill_level": "Advanced",
            "preference": "Industry certifications and real-world deployment labs",
            "goal": "Achieve AWS Certified Solutions Architect Professional and manage multi-cloud clusters",
            "num_items": 4
        }
    ]
    return jsonify({"personas": personas})


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json(silent=True) or {}

        profile = {
            "name": data.get("name", "Learner"),
            "age": data.get("age", 25),
            "background": data.get("background", "General Tech"),
            "interests": data.get("interests", "Computer Science"),
            "skill_level": data.get("skill_level", "Intermediate"),
            "preference": data.get("preference", "Hands-on tutorials"),
            "goal": data.get("goal", "Skill advancement"),
            "num_items": int(data.get("num_items", 4))
        }

        recommendations = generate_recommendations(profile)

        return jsonify({
            "success": True,
            "profile": profile,
            "recommendations": recommendations
        })

    except Exception as e:
        app.logger.exception("Recommendation generation error")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/refine", methods=["POST"])
def refine():
    try:
        data = request.get_json(silent=True) or {}

        profile = data.get("profile", {})
        feedback = data.get("feedback", "").strip()

        if not feedback:
            return jsonify({"success": False, "error": "Feedback cannot be empty."}), 400

        recommendations = refine_recommendations(profile, feedback)

        return jsonify({
            "success": True,
            "recommendations": recommendations
        })

    except Exception as e:
        app.logger.exception("Recommendation refinement error")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/save", methods=["POST"])
def save():
    try:
        data = request.get_json(silent=True) or {}
        recommendations = data.get("recommendations", [])
        save_recommendations(recommendations)
        return jsonify({
            "success": True,
            "message": "Curated learning recommendations saved to recommendations.txt successfully!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/intent", methods=["POST"])
def intent():
    try:
        data = request.get_json(silent=True) or {}
        user_input = data.get("input", "")
        detected_intent = detect_intent(user_input)
        return jsonify({"success": True, "intent": detected_intent})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    print(f"Starting Exp 4 on port {port}")
    app.run(debug=True, port=port)
