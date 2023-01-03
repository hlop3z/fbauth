"""
    Security Configurations
"""

import fastberry as fb

AUTH = fb.config.get("spoc", {}).get("spoc", {}).get("auth", {})


SECRET_KEY = fb.config["env"].get("SECRET_KEY", False)
ACCESS_TOKEN_URL = AUTH.get("access_token_url", "token")
ACCESS_TOKEN_EXPIRE_WEEKS = AUTH.get("access_token_expire_weeks", 0)
ACCESS_TOKEN_EXPIRE_HOURS = AUTH.get("access_token_expire_hours", 0)
ACCESS_TOKEN_EXPIRE_MINUTES = AUTH.get("access_token_expire_minutes", 15)
