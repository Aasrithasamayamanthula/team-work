from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")  # Update URI if needed
db = client.portfolio_website
contacts_collection = db.contacts

# Sample project data
PROJECTS = [
    {"title": "Project One", "description": "Description of project one.", "link": "#"},
    {"title": "Project Two", "description": "Description of project two.", "link": "#"},
    {"title": "Project Three", "description": "Description of project three.", "link": "#"},
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        if name and email and message:
            contacts_collection.insert_one({"name": name, "email": email, "message": message})
            flash("Message sent successfully!", "success")
        else:
            flash("Please fill in all fields.", "error")
        
        return redirect(url_for("contact"))
    
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
