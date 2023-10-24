from flask import Flask, render_template,request

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/back")
def back():
    return render_template("index_back.html")

@app.route("/Writinglawyer")
def Writinglawyer():
    return render_template("Writinglawyer.html")




if __name__ == "__main__":
    app.run()