# 🎬 Zero-Cost Video Pipeline | Configuration (v0.2)
# ЭТО ОБНОВЛЁННЫЙ СКЕЛЕТ. Настройки теперь проверяются перед запуском.
# Принцип: "Все модули читают настройки отсюда. Меняем здесь — меняется вся система."

import os
from pathlib import Path
from typing import Dict, Tuple

class PipelineConfig:
    def __init__(self):
        # === ПУТИ (относительно корня проекта) ===
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "output"
        self.cache_dir = self.base_dir / "cache"
        self.models_dir = self.base_dir / "models"
        self.temp_dir = self.base_dir / "temp"

        # === ГЕНЕРАЦИЯ (KEYFRAME) ===
        self.keyframe_resolution = (640, 360)  # 360p — оптимально для CPU
        self.diffusion_steps = 4               # LCM: 4 шага = быстро + приемлемо
        self.guidance_scale = 7.0              # Баланс между креативностью и точностью
        self.model_id = "stabilityai/stable-diffusion-1-5" # + LCM LoRA
        self.device = "cpu"                    # Жёсткое ограничение: только CPU

        # === АНИМАЦИЯ (MOTION MASK) ===
        self.motion_threshold = 0.15           # Ниже = больше зон движения, выше = меньше
        self.max_motion_zones = 5              # Ограничение для экономии RAM
        self.base_fps = 12                     # Частота до интерполяции

        # === ПОСТ-ОБРАБОТКА ===
        self.target_fps = 30                   # Финальная плавность
        self.upscale_factor = 2                # 2x (360p → 720p)
        self.upscale_roi_only = True           # True = экономим ресурсы
        self.enable_audio = False              # Пока без музыки

        # === СИСТЕМНЫЕ ОГРАНИЧЕНИЯ ===
        self.max_ram_mb = 4000                 # Безопасный лимит
        self.enable_swap = True                # Разрешаем файл подкачки
        self.log_level = "INFO"                # DEBUG / INFO / WARNING

        # Создаём директории при инициализации
        for d in [self.output_dir, self.cache_dir, self.models_dir, self.temp_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def validate(self) -> Tuple[bool, str]:
        """Простая проверка настроек перед запуском пайплайна"""
        # TODO: Добавить проверку свободного места на диске, доступности RAM
        if self.diffusion_steps < 2 or self.diffusion_steps > 20:
            return False, "Количество шагов должно быть от 2 до 20"
        if self.target_fps not in [24, 30, 60]:
            return False, "Поддерживаются только 24, 30 или 60 FPS"
        if not self.keyframe_resolution[1] <= 480:
            return False, "Высота кадра не должна превышать 480px для CPU-режима"
        return True, "✅ Настройки валидны"

    def to_dict(self) -> Dict:
        """Возвращает настройки в виде словаря (для передачи в core.py и models.py)"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

# Глобальный экземпляр (другие файлы импортируют именно его)
config = PipelineConfig()
