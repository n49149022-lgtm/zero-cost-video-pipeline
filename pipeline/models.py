# 🎬 Zero-Cost Video Pipeline | Model Manager
# ЭТО СКЕЛЕТ. Логика загрузки моделей будет добавляться постепенно.
# Принцип: "Загружаем только то, что нужно сейчас. Выгружаем, когда не нужно.
# Следим за RAM. Работаем на CPU."

import psutil
from typing import Dict, Optional

class ModelManager:
    def __init__(self, max_ram_percent: float = 80.0):
        self.loaded_models: Dict[str, object] = {}
        self.max_ram_percent = max_ram_percent
        print("📦 Менеджер моделей инициализирован (скелет)")

    def check_memory(self) -> bool:
        """Проверяет, достаточно ли свободной RAM перед загрузкой"""
        # TODO: Интегрировать с psutil.virtual_memory()
        print("🧠 [RAM] Проверка памяти... (заглушка)")
        return True  # Позже: return available > required

    def load(self, model_type: str, path: str = None) -> Optional[object]:
        """1. Загружает модель в память (CPU/INT8/OpenVINO)"""
        if not self.check_memory():
            print(f"⚠️ [RAM] Недостаточно памяти для загрузки: {model_type}")
            return None
        
        if model_type in self.loaded_models:
            print(f"♻️ [Model] {model_type} уже загружена")
            return self.loaded_models[model_type]
        
        # TODO: Реальная загрузка через optimum.onnxruntime или openvino
        print(f"📥 [Model] Загрузка: {model_type} (скелет)")
        self.loaded_models[model_type] = {"placeholder": True}
        return self.loaded_models[model_type]

    def unload(self, model_type: str):
        """2. Выгружает модель, освобождая RAM"""
        if model_type in self.loaded_models:
            del self.loaded_models[model_type]
            # TODO: Вызов gc.collect() и очистка кэша OpenVINO/ONNX
            print(f"🗑️ [Model] Выгружена: {model_type}")
        else:
            print(f"ℹ️ [Model] {model_type} не была загружена")

    def get(self, model_type: str) -> Optional[object]:
        """Возвращает модель. Если нет → загружает"""
        if model_type not in self.loaded_models:
            return self.load(model_type)
        return self.loaded_models[model_type]

    def list_loaded(self) -> list:
        """Показывает, какие модели сейчас в памяти"""
        return list(self.loaded_models.keys())
