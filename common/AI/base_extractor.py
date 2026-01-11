# import os
# import io
# import json
# import uuid
# import logging
# from typing import Dict, Any, Optional
#
# import fitz  # PyMuPDF
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
#
# # Eski uslubdagi import
# from google import genai
# from google.genai import types
#
# # Logging sozlamalari
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# class ScienceQuestionExtractor:
#     """Rasmlardan fan savollarini chiqarib olish, grafik va mantiqiy rasmlarni alohida qayta ishlash"""
#
#     def __init__(
#         self,
#         api_key: str,
#         model_name: str = "gemini-2.5-flash-lite",  # yoki "gemini-2.5-flash-lite"
#         media_dir: str = "media/questions",
#         dpi: int = 300
#     ):
#         self.client = genai.Client(api_key=api_key)
#         self.model_id = model_name
#
#         self.media_dir = media_dir
#         self.dpi = dpi
#         os.makedirs(self.media_dir, exist_ok=True)
#
#     def _safe_eval_formula(self, formula: str) -> Optional[np.ndarray]:
#         """Xavfsiz matematik ifoda hisoblash"""
#         try:
#             formula = formula.replace('^', '**')
#             safe_dict = {
#                 "x": None,
#                 "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan,
#                 "sqrt": np.sqrt, "abs": np.abs, "log": np.log, "exp": np.exp,
#                 "pi": np.pi, "e": np.e
#             }
#             x = np.linspace(-10, 10, 1000)
#             safe_dict["x"] = x
#             y = eval(formula, {"__builtins__": {}}, safe_dict)
#             return y
#         except Exception as e:
#             logger.warning(f"Formula xatosi: {e} | Formula: {formula}")
#             return None
#
#     def render_graph(self, formula: str) -> Optional[str]:
#         """Matematik funksiyani PNG grafik sifatida saqlaydi"""
#         y = self._safe_eval_formula(formula)
#         if y is None:
#             return None
#
#         try:
#             fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
#             ax.plot(np.linspace(-10, 10, 1000), y, color='#1f77b4', lw=2.8)
#             ax.axhline(0, color='black', lw=1.1)
#             ax.axvline(0, color='black', lw=1.1)
#             ax.grid(True, linestyle='--', alpha=0.7)
#             ax.set_xlim(-10, 10)
#
#             ylim = np.percentile(np.abs(y), 98) * 1.2
#             ax.set_ylim(-ylim, ylim)
#
#             file_name = f"graph_{uuid.uuid4().hex[:10]}.png"
#             file_path = os.path.join(self.media_dir, file_name)
#
#             plt.savefig(file_path, bbox_inches='tight', dpi=150, format='png')
#             plt.close(fig)
#             return file_path
#         except Exception as e:
#             logger.error(f"Graph render xatosi: {e}")
#             return None
#
#     def save_svg(self, svg_code: str) -> Optional[str]:
#         """SVG kodini faylga saqlaydi"""
#         if not svg_code or not isinstance(svg_code, str):
#             return None
#         try:
#             file_name = f"logic_{uuid.uuid4().hex[:10]}.svg"
#             file_path = os.path.join(self.media_dir, file_name)
#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(svg_code.strip())
#             return file_path
#         except Exception as e:
#             logger.error(f"SVG saqlash xatosi: {e}")
#             return None
#
#     def _process_visuals(self, data: Dict[str, Any]) -> None:
#         """AI qaytargan render_type va qo‘shimcha fieldlarni qayta ishlaydi"""
#         for q in data.get("questions", []):
#             render_type = q.get("render_type", "none")
#             q["question_img"] = None
#
#             if render_type == "graph":
#                 formula = q.get("formula")
#                 if formula:
#                     img_path = self.render_graph(formula)
#                     if img_path:
#                         q["question_img"] = img_path
#                         q["visual_type"] = "graph"
#
#             elif render_type == "logic_pic":
#                 svg_code = q.get("svg_code")
#                 if svg_code:
#                     img_path = self.save_svg(svg_code)
#                     if img_path:
#                         q["question_img"] = img_path
#                         q["visual_type"] = "logic_pic"
#
#             # Keraksiz fieldlarni tozalash (ixtiyoriy)
#             q.pop("formula", None)
#             q.pop("svg_code", None)
#
#     def _get_prompt(self) -> str:
#         return """
#         Rasmdagi fan/matematik savollarni aniq chiqar. FAQAT toza JSON qaytar!
#
#         QOIDALAR (qat'iy bajarilishi shart):
#         1. Agar rasmda FUNKSION GRAFIGI bo'lsa (parabola, chiziq, sinus, modul, kvadrat ildiz va h.k.):
#            - "render_type": "graph"
#            - "formula": "numpy/matplotlib uchun to'g'ri Python formulasi" (masalan: "x**2 - 4*x + 3" yoki "abs(x-2)+1")
#            - ^ belgisini ** bilan almashtir!
#
#         2. Agar rasmda GEOMETRIK SHAKLLAR, DIAGRAMMA, MANTIQIY RASM (IQ test, Venn diagrammasi va h.k.) bo'lsa:
#            - "render_type": "logic_pic"
#            - "svg_code": to'liq SVG kodi (string sifatida)
#
#         3. Oddiy savollar uchun "render_type": "none"
#
#         4. Matematik ifodalar har doim LaTeX formatida: \\( ... \\) yoki $...$
#
#         JSON struktura (faqat shu ko'rinishda):
#         {
#           "questions": [
#             {
#               "text": "Savol matni",
#               "points": 2.5,
#               "render_type": "none|graph|logic_pic",
#               "formula": "agar graph bo'lsa — Python formulasi",
#               "svg_code": "agar logic_pic bo'lsa — SVG kodi",
#               "variants": [
#                 {"text": "A) javob", "is_correct": true/false},
#                 ...
#               ]
#             }
#           ]
#         }
#         """
#
#     def extract_from_image(self, image_path: str) -> Dict[str, Any]:
#         """Rasmni tahlil qilish va savollarni chiqarish"""
#         try:
#             img = Image.open(image_path)
#             response = self.client.models.generate_content(
#                 model=self.model_id,
#                 contents=[self._get_prompt(), img],
#                 config=types.GenerateContentConfig(
#                     response_mime_type="application/json"
#                 )
#             )
#             raw_text = response.text.strip()
#             data = json.loads(raw_text)
#             self._process_visuals(data)
#             return data
#         except Exception as e:
#             logger.error(f"Rasm ishlov berishda xato: {e}")
#             return {"questions": []}
#
#
# # ==================== ISHLATISH ====================
# if __name__ == "__main__":
#     API_KEY = "AIzaSyCKU030YyERNimgvB7F8vm7QUXSfMPlt-0"
#
#     extractor = ScienceQuestionExtractor(
#         api_key=API_KEY,
#         model_name="gemini-2.5-flash-lite"  # yoki "gemini-2.5-flash-lite" agar mavjud bo'lsa
#     )
#
#     try:
#         result = extractor.extract_from_image("pic_2.jpg")
#         print(json.dumps(result, indent=2, ensure_ascii=False))
#
#         with open("result.json", "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)
#             print("\nNatija 'result.json' fayliga saqlandi.")
#     except Exception as e:
#         logger.error(f"Asosiy jarayonda xato: {e}")