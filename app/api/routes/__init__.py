from app.api.routes.auth_routes import auth_bp
from app.api.routes.chat_routes import chat_bp


def register_routes(app):
    app.include_router(auth_bp, prefix="/api/auths")
    app.include_router(chat_bp, prefix="/api/gemini")