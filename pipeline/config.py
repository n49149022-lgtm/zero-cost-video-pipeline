# 🎬 Zero-Cost Video Pipeline | Configuration
# ЭТО СКЕЛЕТ. Все настройки пайплайна собраны в одном месте.
# Принцип: "Меняй параметры здесь, не трогая логику кода."

import os
from pathlib import Path

class PipelineConfig:
    def __init__(self):
        # === ПУТИ ===
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "output"
        self.cache_dir = self.base_dir / "cache"
        self.models_dir = self.base_dir / "models"
        self.temp_dir = self.base_dir / "temp"

        # === ГЕНЕРАЦИЯ (KEYFRAME) ===
        self.keyframe_resolution = (640, 360)  # 360p для CPU
        self.diffusion_steps = 4              # LCM: 4-8 шагов достаточно
        self.guidance_scale = 7.0
        self.model_id = "stabilityai/stable-diffusion-1-5" # + LCM LoRA
        self.device = "cpu"                   # Только CPU

        # === АНИМАЦИЯ (MOTION MASK) ===
        self.motion_threshold = 0.15          # Чувствительность к движению
        self.max_motion_zones = 5             # Лимит активных зон
        self.interpolation_fps = 12           # Базовая частота до апскейла

        # === ПОСТ-ОБРАБОТКА ===
        self.target_fps = 30                  # Финальная плавность
        self.upscale_factor = 2               # 2x (360p → 720p)
        self.upscale_roi_only = True          # Улучшать только важные зоны
        self.add_background_music = False     # Пока отключено
        self.audio_volume = 0.15              # Громкость фоновой музыки

        # === СИСТЕМНЫЕ ОГРАНИЧЕНИЯ ===
        self.max_ram_mb = 4000                # Лимит памяти (4 GB)
        self.enable_swap = True               # Разрешить использование файла подкачки
        self.enable_caching = True            # Включить кэш промптов/кадров
        self.log_level = "INFO"               # DEBUG / INFO / WARNING

        # Создаём директории при инициализации
        for d in [self.output_dir, self.cache_dir, self.models_dir, self.temp_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def to_dict(self) -> dict:
        """Возвращает настройки в виде словаря (для передачи в модули)"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

# Глобальный экземпляр конфигурации
config = PipelineConfig()
