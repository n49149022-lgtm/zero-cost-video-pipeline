# 🎬 Zero-Cost Video Pipeline | Semantic Cache
# ЭТО СКЕЛЕТ. Логика кэширования будет добавляться постепенно.
# Принцип: "Если похожий запрос уже обрабатывался → не генерируем заново,
# а берём основу из памяти и слегка адаптируем."

import hashlib
import json
from pathlib import Path

class SemanticCache:
    def __init__(self, cache_dir: str = "cache", max_size: int = 100):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
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

    def check(self, prompt: str):
        """1. Проверяет, есть ли похожий запрос в кэше"""
        # TODO: Заменить хеш на FAISS/векторный поиск по смыслу
        prompt_hash = hashlib.md5(prompt.lower().encode()).hexdigest()[:8]
        if prompt_hash in self.index:
            print(f"💾 [Кэш] HIT: найден похожий запрос ({prompt_hash})")
            return self.index[prompt_hash]
        print(f"🔍 [Кэш] MISS: запрос новый, потребуется генерация")
        return None

    def store(self, prompt: str, result_path: str, metadata: dict = None):
        """2. Сохраняет результат в кэш для будущих запросов"""
        # TODO: Добавить эмбеддинг промпта для нечёткого поиска
        prompt_hash = hashlib.md5(prompt.lower().encode()).hexdigest()[:8]
        self.index[prompt_hash] = {
            "prompt": prompt,
            "result_path": result_path,
            "metadata": metadata or {},
            "timestamp": "now"  # TODO: заменить на datetime.now().isoformat()
        }
        self._save_index()
        print(f"💾 [Кэш] STORE: сохранён результат ({prompt_hash})")

    def clear(self):
        """3. Очищает кэш (для сброса или экономии места)"""
        self.index = {}
        self._save_index()
        # TODO: Добавить удаление физических файлов из cache_dir/
        print("🧹 [Кэш] Очищен")
