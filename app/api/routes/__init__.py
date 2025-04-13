from app.api.routes.auth_routes import auth_bp
from app.api.routes.chat_routes import chat_bp
from app.api.routes.conversation_routes import conv_bp
from app.api.routes.message_routes import message_bp
from app.api.routes.user_routes import user_bp


def register_routes(app):
    app.include_router(auth_bp, prefix="/api/auths")
    app.include_router(chat_bp, prefix="/api/ai")
    app.include_router(conv_bp, prefix="/api/conversations")
    app.include_router(user_bp, prefix="/api/users")
    app.include_router(message_bp, prefix="/api/messages")