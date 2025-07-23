import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
AFFINDA_API_KEY = os.getenv("AFFINDA_API_KEY")
AFFINDA_URL = "https://api.affinda.com/v2/resumes"
HEADERS = {
    "Authorization": f"Bearer {AFFINDA_API_KEY}"
}

@app.route("/parse_resume", methods=["GET"])
def parse_resume_from_path():
    file_path = request.args.get("file_path")

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid or missing file path"}), 400

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "application/pdf")}
            response = requests.post(AFFINDA_URL, headers=HEADERS, files=files)

        if response.status_code == 201:
            return jsonify(response.json())
        else:
            return jsonify({
                "error": "Affinda API failed",
                "status_code": response.status_code,
                "message": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)


