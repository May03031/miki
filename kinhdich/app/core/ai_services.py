from config import settings
import traceback
import json

# OpenAI SDK
from openai import OpenAI

# Gemini SDK
from google import genai
from google.genai import types


class AIService:
    def __init__(self):
        self.agent = settings.AI_AGENT.lower().strip()
        self.client = None

        if self.agent == "openai" and settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

        elif self.agent == "gemini" and settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        else:
            print("⚠️ Không tìm thấy API key hợp lệ cho OpenAI hoặc Gemini.")

    def get_response(self, prompt: str, history_conversation: list[dict] = None) -> dict:
        """
        Sinh nội dung dựa trên AI agent đang cấu hình (OpenAI hoặc Gemini)
        """

        system_prompt = settings.PROMPT_SYSTEM_ICHING
        text_result = ""
        #print("history_conversation",history_conversation)
        try:
            if self.agent == "openai":
                completion = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *history_conversation,
                        {"role": "user", "content": prompt}
                    ]
                )
                text_result = completion.choices[0].message.content.strip()

            elif self.agent == "gemini":
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    # Cấu hình system_prompt đúng chuẩn
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    ),
                    #contents=prompt
                    contents=[
                    #{"role": "user", "parts": [{"text": "Xin chào, gieo quẻ giúp tôi hôm nay."}]},
                    #{"role": "model", "parts": [{"text": "Tất nhiên, bạn muốn hỏi về điều gì?"}]},
                    *history_conversation,
                    {"role": "user", "parts": [{"text": prompt}]},
                    ]
                    #contents=[
                    #{"role": "system", "parts": system_prompt},
                    #*history_conversation,
                    #{"role": "user", "parts": prompt}
                    #]
                    
                )
                
                text_result = response.text.strip()

            else:
                return {"error": 1, "raw": "Không có AI agent nào được cấu hình hợp lệ."}
                

        except Exception as e:
            print("❌ Lỗi khi gọi AI:", e)
            traceback.print_exc()
            return {"error": 1, "raw": "Đã xảy ra lỗi khi gọi AI."}
        

        print("AI result:"+text_result)
        # Cố gắng parse JSON
        try:
           result = json.loads(text_result)
        except json.JSONDecodeError:
           result = {"error": "1", "raw": "Không thể parse JSON"+text_result}

        return text_result
            