import os
import shutil

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    flash,
)

import utils

# Initialize Flask application and sentiment analyzer
app = Flask(__name__)
app.secret_key = "very_secret"

# Create an absolute path for the upload folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "tmp_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)

    file = request.files["file"]
    context = request.form["context"]

    # Save the original file and context to the server
    file_path, context_file_path = utils.save_file_and_context(file, context)

    # Create a copy of the original file for anonymization
    anonymized_file_path = file_path.replace(".txt", "_anonymized.txt")
    shutil.copy(file_path, anonymized_file_path)

    # Analyze the context to determine the action
    action = utils.analyze_context(context)

    if action == "remove_attributes":
        # Anonymize the original file
        utils.anonymize_original_file(anonymized_file_path)

        # Preprocess and tokenize the file content
        utils.preprocess_file(file_path)
        # Tokenize and anonymize the file content
        utils.remove_attributes(file_path)

        # Generate the summary of the anonymization process
        summary = utils.generate_summary_of_anonymization()
        session["summary"] = summary
    elif action == "check_bias":
        # Check for bias
        if "unbiased" in context:
            # Debias the text
            debiased_file_path = utils.debias_text(file_path)
            if debiased_file_path:
                session["debiased_file_path"] = debiased_file_path
        else:
            label, score = utils.check_bias(file_path)
            summary = f"The news article is {label.lower()} with a score of {score}."
            summary += "\nThe score goes from 0 to 1, with 0 being the least biased and 1 the most."
            session["summary"] = summary
    # Print the summary to the console for testing

    return redirect(url_for("results"))


@app.route("/results")
def results():
    # Retrieve the path of the temporary file from the query parameter
    summary = session.get("summary", "No summary available")

    return render_template("results.html", summary=summary)


@app.route("/download_debiased")
def download_debiased():
    debiased_file_path = session.get("debiased_file_path")
    if debiased_file_path:
        return send_from_directory(
            directory=os.path.dirname(debiased_file_path),
            filename=os.path.basename(
                debiased_file_path
            ),  # Use 'filename' instead of 'path'
            as_attachment=True,
        )
    else:
        return "No debiased file available.", 404


@app.route("/cleanup", methods=["POST"])
def cleanup():
    try:
        # Delete all files in the tmp_uploads directory
        shutil.rmtree(app.config["UPLOAD_FOLDER"])
        # Recreate the tmp_uploads directory
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        flash("Temporary files cleaned up successfully.")
    except Exception as e:
        flash(f"An error occurred while cleaning up: {e}")

    # Redirect to the home page
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
