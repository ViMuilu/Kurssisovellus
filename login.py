from db import db

def login(username, password):

    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()   
    
    if user == None:       
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = user[1]

            sql = "SELECT type FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            
            type1 = result.fetchone()[0]
            session["accountType"] = type1
            return True
        else:
            
            return False   