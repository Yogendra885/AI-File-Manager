from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Folder managed by the application
BASE_FOLDER = os.path.join(os.getcwd(), "managed_files")

# Create the folder if it does not exist
os.makedirs(BASE_FOLDER, exist_ok=True)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Chat commands
@app.route("/command", methods=["POST"])
def command():

    data = request.get_json()
    message = data.get("message", "").lower().strip()


    # Show files
    if "show" in message and "file" in message:

        files = os.listdir(BASE_FOLDER)

        if not files:
            return jsonify({
                "response": "📁 The managed folder is empty."
            })

        result = "📂 Files in your folder:<br><br>"

        for file in files:
            result += "📄 " + file + "<br>"

        return jsonify({
            "response": result
        })


    # Find PDF files
    if "pdf" in message:

        files = [
            file
            for file in os.listdir(BASE_FOLDER)
            if file.lower().endswith(".pdf")
        ]

        if not files:
            return jsonify({
                "response": "❌ No PDF files found."
            })

        result = "📄 PDF files:<br><br>"

        for file in files:
            result += file + "<br>"

        return jsonify({
            "response": result
        })


    # Create folder
    if message.startswith("create folder"):

        folder_name = message.replace(
            "create folder", "", 1
        ).strip()

        if folder_name == "":
            return jsonify({
                "response": "⚠️ Please provide a folder name."
            })

        folder_path = os.path.join(
            BASE_FOLDER,
            folder_name
        )

        os.makedirs(folder_path, exist_ok=True)

        return jsonify({
            "response":
            f"📁 Folder '{folder_name}' created successfully."
        })

    # Rename folder
    if message.startswith("rename folder"):

        parts = message.replace(
            "rename folder", "", 1
        ).strip().split(" to ")

        if len(parts) != 2:
            return jsonify({
                "response": "Use: Rename folder OldName to NewName"
            })

        old_name = parts[0].strip()
        new_name = parts[1].strip()

        old_path = os.path.join(BASE_FOLDER, old_name)
        new_path = os.path.join(BASE_FOLDER, new_name)

        if not os.path.exists(old_path):
            return jsonify({
                "response": "Folder not found."
            })

        os.rename(old_path, new_path)

        return jsonify({
            "response": "Folder renamed successfully."
        })
    # Unknown command
    return jsonify({
        "response":
        "🤖 Try:<br><br>"
        "• Show my files<br>"
        "• Find PDF files<br>"
        "• Create folder College"
    })


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)