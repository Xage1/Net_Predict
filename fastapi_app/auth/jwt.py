from datetime import datetime, timedelta
import jwt

SECRET = "NETPREDICT_SUPER_SECRET"

def create_token(user_id):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")