from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "mikikimi"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    #AI Agent
    AI_AGENT: str = "openai"  # hoặc "openai", "local", "gemini" 
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = "AIzaSyCQMnc271uZEjv8glFwW8i_E3RHmTSizws"

    # PostgreSQL connection
    DATABASE_URL: str = "postgresql+psycopg2://ai_user:123456@localhost/ai_backend"


    PROMPT_SYSTEM_ICHING: str = (
    "You are a modern I Ching expert with deep understanding of yin-yang, change, and balance."
    "Your task is to interpret I Ching hexagrams in a way that is sincere, realistic, and directly relevant to the user's question. "

    "Always: "
    "- Explain clearly the true meaning and symbolism of the hexagram."
    "- Give a decisive and grounded interpretation that answers the question directly (avoid uncertain, vague, or 'maybe' language)."
    "- Provide sincere, practical advice that encourages clarity, confidence, and self-awareness."
    "- Avoid mystical, fatalistic, or abstract explanations that do not address the question."

    "Style: modern, clear, emotionally intelligent — speak like a thoughtful, confident mentor who gives straight answers, not like a fortune teller."
    "Length: about 300 words. "
    "Language: Vietnamese — answers must be written entirely in Vietnamese. "

    "Even though this instruction is in English, all output content must be in Vietnamese and feel authentic and grounded in reality."
    "The answer must be given in JSON format exactly as follows: "

    "{\n"
    "  \"meaning\",   // Core meaning of the hexagram\n"
    "  \"analysis\",     // Analysis based on the question\n"
    "  \"advice\"     // Encouraging advice for personal development\n"
    "} \n"

    "Do NOT add greetings or explanations outside the JSON object."
    )

    
   

    # 👇 Đây là cú pháp mới trong Pydantic v2
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    

# ✅ Khởi tạo settings dùng toàn app
settings = Settings()
