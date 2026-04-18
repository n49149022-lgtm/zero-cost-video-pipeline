# 🎬 Zero-Cost Video Pipeline | Semantic Cache (v0.2)
# ОБНОВЛЁННЫЙ СКЕЛЕТ. Добавлен JSON-индекс, таймстампы и базовая очистка.
# Принцип: "Если похожий запрос уже обрабатывался → берём основу из памяти."

import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict

class SemanticCache:
    def __init__(self, cache_dir: str = "cache", max_size: int = 100):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.cache_dir / "index.json"
        self.max_size = max_size
        self._load_index()

    def _load_index(self):
        """Загружает или создаёт пустой индекс кэша"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {}

    def _save_index(self):
        """Сохраняет индекс на диск"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def check(self, prompt: str, max_age_hours: float = 72.0) -> Optional[Dict]:
        """1. Проверяет, есть ли похожий запрос в кэше (с учётом времени)"""
        prompt_hash = hashlib.md5(prompt.lower().strip().encode()).hexdigest()[:8]
        if prompt_hash in self.index:
            entry = self.index[prompt_hash]
            age_hours = (time.time() - entry.get("timestamp", 0)) / 3600
            if age_hours <= max_age_hours:
                print(f"💾 [Кэш] HIT: найдено ({prompt_hash}, возраст {age_hours:.1f}ч)")
                return entry
            else:
                print(f"🕰️ [Кэш] EXPIRED: запись старше {max_age_hours}ч, удаляю")
                del self.index[prompt_hash]
                self._save_index()
        print(f"🔍 [Кэш] MISS: запрос новый")
        return None

    def store(self, prompt: str, result_path: str, metadata: Dict = None):
        """2. Сохраняет результат в кэш для будущих запросов"""
        prompt_hash = hashlib.md5(prompt.lower().strip().encode()).hexdigest()[:8]
        self.index[prompt_hash] = {
            "prompt": prompt,
            "result_path": result_path,
            "metadata": metadata or {},
            "timestamp": time.time()
        }
        self._save_index()
        print(f"💾 [Кэш] STORE: сохранён ({prompt_hash})")
        self._enforce_limits()

    def _enforce_limits(self):
        """3. Удаляет самые старые записи, если кэш превысил max_size"""
        if len(self.index) > self.max_size:
            sorted_items = sorted(self.index.items(), key=lambda x: x[1].get("timestamp", 0))
            to_remove = len(self.index) - self.max_size
            for key, _ in sorted_items[:to_remove]:
                del self.index[key]
            self._save_index()
            print(f"🧹 [Кэш] Очищены {to_remove} старых записей")

    def clear(self):
        """Полная очистка кэша"""
        self.index = {}
        self._save_index()
        print("🧹 [Кэш] Полностью очищен")
