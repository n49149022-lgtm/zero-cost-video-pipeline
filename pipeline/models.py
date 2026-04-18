# 🎬 Zero-Cost Video Pipeline | Model Manager (CPU PyTorch)
import os, time, gc, torch
from pathlib import Path
from typing import Dict, Optional
from diffusers import LCMScheduler, StableDiffusionPipeline

class ModelManager:
    def __init__(self, max_ram_mb: float = 4000.0, models_dir: str = "models"):
        self.loaded_models: Dict[str, object] = {}
        self.max_ram_mb = max_ram_mb
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        print("📦 ModelManager initialized (CPU PyTorch)")

    def _check_ram(self, required_mb: float = 2500.0) -> bool:
        import psutil
        available_mb = psutil.virtual_memory().available / 1024 / 1024
        if available_mb < required_mb:
            print(f"⚠️ [RAM] Недостаточно: свободно {available_mb:.0f}MB, нужно {required_mb}MB")
            return False
        print(f"🧠 [RAM] OK: свободно ~{available_mb:.0f}MB")
        return True

    def load_keyframe_model(self) -> Optional[StableDiffusionPipeline]:
        if "keyframe" in self.loaded_models:
            return self.loaded_models["keyframe"]
        if not self._check_ram(2500):
            return None
        try:
            model_id = "SimianLuo/LCM_Dreamshaper_v7"
            print(f"📥 Загрузка LCM модели: {model_id}")
            
            torch.set_grad_enabled(False)
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                cache_dir=str(self.models_dir),
                torch_dtype=torch.float32,
                safety_checker=None,
                local_files_only=False
            )
            pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
            pipe.to("cpu")
            pipe.set_progress_bar_config(disable=True)
            
            self.loaded_models["keyframe"] = pipe
            print("✅ Модель загружена (CPU, torch.float32, LCM)")
            return pipe
        except Exception as e:
            print(f"❌ Ошибка загрузки модели: {e}")
            return None

    def unload(self, model_type: str):
        if model_type in self.loaded_models:
            del self.loaded_models[model_type]
            gc.collect()
            print(f"🗑️ [Model] Выгружена: {model_type}")

    def get_keyframe_model(self):
        return self.load_keyframe_model() if "keyframe" not in self.loaded_models else self.loaded_models["keyframe"]
