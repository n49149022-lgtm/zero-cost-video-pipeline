# 🎬 Zero-Cost Video Pipeline | Model Manager (v0.2)
# ОБНОВЛЁННЫЙ СКЕЛЕТ. Добавлен контроль RAM, трекинг времени и безопасная выгрузка.
# Принцип: "Загружаем только нужное. Следим за памятью. Выгружаем, когда не нужно."

import time
from typing import Dict, Optional

class ModelManager:
    def __init__(self, max_ram_mb: float = 4000.0):
        self.loaded_models: Dict[str, dict] = {}
        self.max_ram_mb = max_ram_mb
        print("📦 Менеджер моделей инициализирован (v0.2)")

    def _check_ram(self, required_mb: float = 500.0) -> bool:
        """Проверяет, хватит ли памяти перед загрузкой"""
        # TODO: Интегрировать psutil.virtual_memory() для реальной проверки
        current_used_mb = len(self.loaded_models) * 1200  # Имитация: ~1.2GB на модель
        available = self.max_ram_mb - current_used_mb
        if available < required_mb:
            print(f"⚠️ [RAM] Недостаточно памяти. Свободно: {available:.0f}MB, нужно: {required_mb}MB")
            return False
        print(f"🧠 [RAM] OK. Свободно ~{available:.0f}MB")
        return True

    def load(self, model_type: str, path: str = None) -> Optional[dict]:
        """1. Загружает модель (или возвращает уже загруженную)"""
        if not self._check_ram():
            return None
        
        if model_type in self.loaded_models:
            print(f"♻️ [Model] {model_type} уже в памяти")
            return self.loaded_models[model_type]
        
        print(f"📥 [Model] Имитация загрузки: {model_type}")
        self.loaded_models[model_type] = {
            "id": model_type,
            "path": path,
            "loaded_at": time.time(),
            "status": "ready"
        }
        return self.loaded_models[model_type]

    def unload(self, model_type: str):
        """2. Выгружает модель, освобождая ресурсы"""
        if model_type in self.loaded_models:
            del self.loaded_models[model_type]
            # TODO: Вызов gc.collect() и очистка кэша ONNX/OpenVINO
            print(f"🗑️ [Model] Выгружена: {model_type}")
        else:
            print(f"ℹ️ [Model] {model_type} не была загружена")

    def get(self, model_type: str, path: str = None) -> Optional[dict]:
        """Умный доступ: если нет → загружает, если есть → возвращает"""
        return self.load(model_type, path) if model_type not in self.loaded_models else self.loaded_models[model_type]

    def list_loaded(self) -> list:
        """Показывает, какие модели сейчас в памяти"""
        return list(self.loaded_models.keys())
