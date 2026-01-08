from app.controller.iChing.line import Line
from typing import List, Optional
import random
from config import settings
from app.core.ai_services import AIService
from openai import OpenAI
import google.genai as genai
import json


class Hexagram:
    KING_WEN_NAMES = [
        "Càn (乾)", "Khôn (坤)", "Truân (屯)", "Mông (蒙)", "Nhu (需)", "Tụng (訟)", "Sư (師)", "Tỉ (比)",
        "Tiểu Súc (小畜)", "Lý (履)", "Thái (泰)", "Bĩ (否)", "Đồng Nhân (同人)", "Đại Hữu (大有)",
        "Khiêm (謙)", "Dự (豫)", "Tùy (隨)", "Cổ (蠱)", "Lâm (臨)", "Quán (觀)", "Bí (噬嗑)", "Bác (剝)",
        "Phục (復)", "Vô Vọng (无妄)", "Đại Súc (大畜)", "Di (頤)", "Đại Quá (大過)", "Khảm (坎)",
        "Ly (離)", "Tiểu Quá (小過)", "Hàm (咸)", "Hằng (恆)", "Độn (遯)", "Đại Trang (大壯)",
        "Tấn (晉)", "Minh Di (明夷)", "Gia Nhân (家人)", "Khuê (睽)", "Kiển (蹇)", "Giải (解)",
        "Tổn (損)", "Ích (益)", "Quải (夬)", "Cấu (姤)", "Tụy (萃)", "Thăng (升)", "Khốn (困)", "Tỉnh (井)",
        "Cách (革)", "Đỉnh (鼎)", "Chấn (震)", "Cấn (艮)", "Tiệm (漸)", "Quy Muội (歸妹)",
        "Phong (豐)", "Lữ (旅)", "Tốn (巽)", "Đoài (兌)", "Hoán (渙)", "Tiết (節)", "Trung Phu (中孚)",
        "Tiểu Quá (小過)", "Ký Tế (既濟)", "Vị Tế (未濟)"
    ]

    MEANINGS = [
    "1. Càn: Thuần dương, tượng Trời. Biểu thị sức mạnh, sáng tạo, khởi đầu và kiên cường.",
    "2. Khôn: Thuần âm, tượng Đất. Biểu thị sự nhu thuận, bao dung, tiếp nhận và sinh dưỡng.",
    "3. Truân: Khởi đầu gian nan, cần kiên nhẫn vượt qua khó khăn ban đầu.",
    "4. Mông: U tối, non nớt. Cần khai mở trí tuệ, học hỏi, có người dẫn dắt.",
    "5. Nhu: Gặp thời chờ đợi, nên kiên nhẫn chờ cơ hội thích hợp.",
    "6. Tụng: Tranh chấp, kiện tụng. Cần tránh xung đột, giữ chính nghĩa.",
    "7. Sư: Ra quân, hành động tập thể. Cần có lãnh đạo sáng suốt và kỷ luật.",
    "8. Tỷ: Gắn bó, hợp tác, đoàn kết sẽ thành công.",
    "9. Tiểu súc: Tích lũy nhỏ, kiềm chế bản thân, chờ thời cơ lớn.",
    "10. Lý: Bước đi, hành động thận trọng, giữ lễ nghĩa và chính đạo.",
    "11. Thái: Thông suốt, hòa hợp trời đất, thời vận hanh thông.",
    "12. Bĩ: Bế tắc, âm thịnh dương suy. Cần giữ chính đạo chờ thời vận đổi.",
    "13. Đồng nhân: Đồng lòng, cùng chí hướng, hợp tác mang lại kết quả tốt.",
    "14. Đại hữu: Giàu có, sung túc, phúc lộc dồi dào.",
    "15. Khiêm: Khiêm nhường, càng khiêm tốn càng được trọng dụng.",
    "16. Dự: Vui mừng, hỷ sự, nhưng cần tiết chế niềm vui để tránh bất cẩn.",
    "17. Tùy: Thuận theo thời thế, linh hoạt ứng xử để thành công.",
    "18. Cổ: Sửa lỗi cũ, chỉnh đốn, cải cách để đổi mới.",
    "19. Lâm: Tiến gần, cơ hội đến, cần hành động đúng lúc.",
    "20. Quán: Quan sát, soi xét, cần có tầm nhìn và học hỏi.",
    "21. Thệ Hạp (Cắn Cắn): Giải quyết rắc rối bằng hành động dứt khoát, có kỷ luật.",
    "22. Bí: Trang sức, làm đẹp, thể hiện giá trị chân chính.",
    "23. Bác: Mất mát, bị tước bỏ, nên buông bỏ điều cũ để đón điều mới.",
    "24. Phục: Trở lại, tái sinh, sau bĩ cực tất có thái lai.",
    "25. Vô vọng: Chân thành, không vọng tưởng, giữ chính đạo.",
    "26. Đại súc: Tích lũy lớn, kiềm chế để chờ cơ hội hành động.",
    "27. Di: Nuôi dưỡng, bồi đắp tri thức, đạo đức và sinh kế.",
    "28. Đại quá: Quá mức, gánh nặng lớn, nên giữ cân bằng.",
    "29. Khảm: Nguy hiểm, hiểm trở. Cần tỉnh táo vượt qua khó khăn.",
    "30. Ly: Sáng sủa, trí tuệ, văn minh, nhưng cần giữ trung thực.",
    "31. Hàm: Giao cảm, hòa hợp, duyên khởi tốt đẹp.",
    "32. Hằng: Kiên định, bền bỉ, giữ vững nguyên tắc.",
    "33. Độn: Ẩn mình, tránh hiểm, biết rút lui đúng lúc.",
    "34. Đại tráng: Cường thịnh, phát triển mạnh, nhưng cần kiềm chế.",
    "35. Tấn: Tiến lên, phát triển rực rỡ, thời cơ tốt.",
    "36. Minh di: Ánh sáng bị che khuất, nên thận trọng, giấu mình.",
    "37. Gia nhân: Trị gia, xây dựng gia đạo, nội hòa thì ngoại thuận.",
    "38. Khuê: Mâu thuẫn, bất đồng, nên tìm điểm chung và hòa giải.",
    "39. Kiển: Nguy nan, bị cản trở, cần kiên nhẫn vượt qua.",
    "40. Giải: Giải thoát, giải trừ khó khăn, thời vận thông suốt.",
    "41. Tổn: Giảm bớt, tiết chế, hy sinh điều nhỏ để đạt điều lớn.",
    "42. Ích: Tăng ích, được giúp đỡ, tài lộc và phúc lợi đến.",
    "43. Quải: Quyết đoán, hành động dứt khoát, cắt bỏ điều xấu.",
    "44. Cấu: Gặp gỡ, duyên khởi, nên giữ chính đạo trong quan hệ.",
    "45. Tụy: Thuận phục, làm theo chính nghĩa, phục tùng bề trên đúng mực.",
    "46. Thăng: Thăng tiến, phát triển, từng bước vững vàng.",
    "47. Khốn: Khó khăn, bị gò bó, nhưng có cơ vượt thoát.",
    "48. Tỉnh: Cải cách, làm mới, thanh lọc, cải thiện bản thân.",
    "49. Cách: Biến đổi, đổi mới toàn diện, thời cơ chuyển hóa.",
    "50. Đỉnh: Cái đỉnh, tượng văn hóa, thịnh vượng, trí tuệ và truyền thống.",
    "51. Chấn: Sấm động, khởi phát, thức tỉnh và đổi mới.",
    "52. Cấn: Núi, dừng lại, tĩnh tâm, biết lúc dừng là khôn ngoan.",
    "53. Tiệm: Tiến dần, phát triển từng bước vững chắc.",
    "54. Quy muội: Hôn nhân, kết hợp, cần hài hòa âm dương.",
    "55. Phong: Sung túc, được ban phúc, cần biết sẻ chia.",
    "56. Lữ: Lữ hành, xa xứ, cần thích nghi và cẩn trọng.",
    "57. Tốn: Gió, thuận theo, mềm dẻo và thấu hiểu người khác.",
    "58. Đoài: Hồ, vui vẻ, truyền cảm hứng, nhưng cần tiết chế.",
    "59. Hoán: Tan rã, phân tán, cần đoàn kết lại.",
    "60. Tiết: Tiết chế, giới hạn, biết đủ thì an vui.",
    "61. Trung phu: Thành tín, chân thành, lấy tín nghĩa làm trọng.",
    "62. Tiểu quá: Quá mức nhỏ, sai sót nhẹ, cần sửa sớm.",
    "63. Ký tế: Hoàn thành, viên mãn, kết quả tốt đẹp.",
    "64. Vị tế: Chưa xong, dang dở, cần kiên nhẫn hoàn thiện."
]




    def __init__(self, lines: List[Line]):
        self.lines = lines

    @classmethod
    def random(cls):
        lines = []
        for _ in range(6):
            tosses = [random.choice((2,3)) for _ in range(3)]
            total = sum(tosses)
            lines.append(Line(total, tosses))
        return cls(lines)
    def to_binary_index(self):
        bits = [l.to_bit() for l in self.lines]
        return sum((b<<i) for i,b in enumerate(bits)) + 1
    def to_binary_code(self):
        return ''.join(str(l.to_bit()) for l in reversed(self.lines))
    def display(self):
        return "\n".join(l.symbol() for l in reversed(self.lines))
    def changed(self):
        return Hexagram([l.after_change() for l in self.lines])
    def name(self):
        idx = min(self.to_binary_index()-1, len(self.KING_WEN_NAMES)-1)
        return self.KING_WEN_NAMES[idx]
    
    def meaning(self, question: Optional[str] = None, history_conversation: list[dict] = None):
        idx = min(self.to_binary_index()-1, len(self.KING_WEN_NAMES)-1)
        local = self.MEANINGS[idx]
        #print("Xin chào Python1:",settings.AI_AGENT)
        #print("Xin chào Python2:",settings.GEMINI_API_KEY)
        prompt = f"Tên quẻ: {self.name()}"
        if question:
            prompt += f"\nCâu hỏi: '{question}'"
        
        print("Prompt:",prompt)
        if settings.AI_AGENT == "local":
            return local
        else :
            ai_service = AIService()
            return ai_service.get_response(prompt, history_conversation)
        
        """
        if settings.AI_AGENT == "openai" and settings.OPENAI_API_KEY :

            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            try:
                completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                )
                return completion.choices[0].message.content
            except Exception as e:
                print("Lỗi OpenAI:", e)
                return "Không thể kết nối OpenAI"

        elif settings.AI_AGENT == "gemini" and settings.GEMINI_API_KEY:

            try:
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
                )

                return response.text
            except Exception as e:
                print("Lỗi khi gọi Gemini API:", e)
                return "Không thể kết nối đến Gemini API."

            
        else:
            return local"""