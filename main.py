from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auther.db"
db = SQLAlchemy()
db.init_app(app)


class AutherUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    auther = db.Column(db.String(140))
    email = db.Column(db.String(140),unique=True)
    title = db.Column(db.String(140))
    date = db.Column(db.String(140))


with app.app_context():
    db.create_all()



@app.route("/create_auther",methods = ["POST"])
def auther_user():

    # print(request.data)
    # print(type(request.data))
    a = json.loads(request.data)
    # print(type(a))
    for create_auther in a:
        # print(auther)
        id=create_auther.get("new_id")
        auther=create_auther.get("auther")
        email=create_auther.get("email")
        title=create_auther.get("title")
        date = create_auther.get("date")

        entry =AutherUser(id=id,auther=auther,email=email,title=title,date=date)
        db.session.add(entry)
        db.session.commit()
    

    return jsonify("success")


@app.route("/auther", methods=["GET"])
def get_auther():
    auther = AutherUser.query.all()
    print(auther)
    new_list =[]
    for user in auther:
        print(user)
        new_list.append({"id":user.id,"auther":user.auther,"email":user.email,"title":user.title,"date":user.date})
        print(new_list)
    return jsonify(new_list)
    

    

@app.route("/auther/<int:auther_id>",methods=["GET"])
def auther_id(auther_id):
    user= AutherUser.query.get(auther_id)
    # print(user)

    auther_data=({"id":user.id,"auther":user.auther,"email":user.email,"title":user.title,"date":user.date})



    return jsonify(auther_data)

@app.route("/auther_update/<int:auther_id>" ,methods=["PUT"])
def update(auther_id):
    user=AutherUser.query.get(auther_id)

    # print(user)
    a=(json.loads(request.data))
    # print(a)
    auther=a.get("auther")
    # print(auther)
    user.auther = auther
    db.session.commit()
    new_data=({"id":user.id,"auther":user.auther,"email":user.email,"title":user.title,"date":user.date})

    return jsonify(new_data)








@app.route("/auther_delete/<int:auther_id>" , methods=["DELETE"]) 
def auther_delete(auther_id):
    user= AutherUser.query.get(auther_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify("delete successfully")





if __name__ =="__main__":
    app.run(debug=True)
