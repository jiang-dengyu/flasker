from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

############################################
app = Flask(__name__)
################# flask_jwt_extended setting ###########################
app.config["JWT_SECRET_KEY"] = "my-secret"
jwt = JWTManager(app)

################### database setting #########################
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)
class Friends(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(200), nullable=False)
  def __repr__(self):
    return 'Name %r' % self.id
class Users(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(20), nullable=False)
  password = db.Column(db.String(128),nullable=False) 
  idAdmin = db.Column(db.Boolean, default=False)
  def __repr__(self):
    return 'Name %r' % self.id

################ routers ############################
@app.route('/')
def index():
    return jsonify({"msg": "welcome to index page"})

#註冊
@app.route('/api/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
      userName = request.form['name']
      userPassword = request.form['password']
      newUser = Users(name=userName,password=userPassword)
      try:
        db.session.add(newUser)
        db.session.commit()  
        return jsonify({
            'id': newUser.id,
            'name': newUser.name,
            'isAdmin': newUser.idAdmin,
            'msg': 'User registered successfully'
        }), 200
      except:
        return jsonify({"msg": "Oops!  an error when register the new user.", "error": str(e)}), 500
    else :
       return jsonify({"msg": "welcome to register page"})

#登入
@app.route('/api/login',methods=['POST','GET'])
def logIn():
  if request.method == 'POST':
      userName = request.form['name']
      userPassword = request.form['password']
      user = Users.query.filter_by(name=userName).first()
      if user :
          access_token = create_access_token(identity={'name': user.name})
          return jsonify(access_token=access_token, msg="login success!", status=200)
      else : 
          return jsonify({"msg": "No username"}), 401
  else :
    return jsonify({"msg": "login page"})

#用戶資訊
@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_identity = get_jwt_identity()
    user = Users.query.filter_by(name=current_user_identity['name']).first()
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'isAdmin': user.idAdmin
        })
    else:
        return jsonify({"msg": "User not found"})

#更改用戶資訊
@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
def changeUserRole(user_id):
    user = Users.query.get(user_id)
    if user:
        user.idAdmin = True
        db.session.commit()
        return jsonify({"msg": "User role updated successfully"})
    else:
        return jsonify({"msg": "User not found"})

#後台
@app.route('/api/admin')
@jwt_required()
def isadmin():
    current_user_identity = get_jwt_identity()
    current_user = Users.query.filter_by(name=current_user_identity['name']).first()
    if current_user and current_user.idAdmin:
        users = Users.query.all()
        users_list = [{'id': user.id, 'name': user.name, 'isAdmin': user.idAdmin} for user in users]
        return jsonify(users=users_list)
    else:
        return jsonify({"msg": "Admin access required"}), 403


#####################################
if __name__ == "__main__":
    app.run(debug=True)