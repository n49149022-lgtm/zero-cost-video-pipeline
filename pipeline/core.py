# 🎬 Zero-Cost Video Pipeline | Core Orchestrator (REAL)
import time, sys, torch
from pathlib import Path
try:
    from .config import config
    from .cache import SemanticCache
    from .models import ModelManager
    from .postprocess import PostProcessor
except ImportError:
    sys.path.append(str(Path(__file__).parent.parent))
    from pipeline.config import config
    from pipeline.cache import SemanticCache
    from pipeline.models import ModelManager
    from pipeline.postprocess import PostProcessor

class VideoPipeline:
    def __init__(self):
        print("🧠 Инициализация оркестратора...")
        self.config = config
        self.cache = SemanticCache(cache_dir=str(self.config.cache_dir))
        self.models = ModelManager(max_ram_mb=self.config.max_ram_mb)
        self.post = PostProcessor(output_dir=str(self.config.output_dir))
        print("✅ Оркестратор готов.")

    def generate_real_keyframe(self, prompt: str) -> str:
        pipe = self.models.get_keyframe_model()
        if not pipe:
            raise RuntimeError("Не удалось загрузить модель")
        print(f"🎨 Генерация: '{prompt[:50]}...'")
        result = pipe(
            prompt=prompt,
            num_inference_steps=4,
            guidance_scale=1.0,
            width=512,
            height=512,
            output_type="pil"
        ).images[0]
        output_path = self.config.output_dir / "keyframe_real.png"
        result.save(output_path)
        print(f"✅ Keyframe сохранён: {output_path}")
        return str(output_path)

    def run(self, prompt: str, dry_run: bool = False) -> str:
        print(f"\n🚀 ЗАПУСК | Промпт: '{prompt}' | Режим: {'DRY' if dry_run else 'REAL'}")
        print("-" * 50)
        
        cached = self.cache.check(prompt)
        if cached and dry_run:
            print("♻️ Кэш: пропуск генерации")
            return cached["result_path"]
        
        print("[1/5] Загрузка модели...")
        if not dry_run:
            kf_path = self.generate_real_keyframe(prompt)
        else:
            time.sleep(0.5)
            kf_path = str(self.config.output_dir / "temp_kf.png")
            print(f"🖼️ [DRY] Keyframe: {kf_path}")
        
        print("[2/5] Маска движения (эмуляция)...")
        time.sleep(0.3)
        
        print("[3/5] Анимация зон (эмуляция)...")
        time.sleep(0.3)
        
        print("[4/5] Пост-обработка...")
        final = self.post.run(kf_path if not dry_run else str(self.config.output_dir / "temp_clip.mp4"))
        
        print("[5/5] Сохранение в кэш...")
        self.cache.store(prompt, final, metadata={"mode": "real" if not dry_run else "dry", "timestamp": time.time()})
        
        print("-" * 50)
        print(f"✅ ГОТОВО | Результат: {final}")
        return final

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default="монстера у окна, естественный свет, макро, мягкий свет")
    parser.add_argument("--dry", action="store_true", help="Dry-run режим")
    args = parser.parse_args()
    pipe = VideoPipeline()
    pipe.run(args.prompt, dry_run=args.dry)
