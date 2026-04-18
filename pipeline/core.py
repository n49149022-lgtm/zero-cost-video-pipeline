# 🎬 Zero-Cost Video Pipeline | Core Orchestrator (REAL, 9:16)
import time, sys, torch, argparse
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

    def generate_real_keyframe(self, prompt: str, ratio: str = "9:16") -> str:
        pipe = self.models.get_keyframe_model()
        if not pipe:
            raise RuntimeError("Не удалось загрузить модель")
        
        # Поддержка соотношений сторон
        ratios = {
            "1:1": (512, 512),
            "16:9": (1024, 576),
            "9:16": (576, 1024),
            "4:3": (768, 576),
            "3:4": (576, 768)
        }
        width, height = ratios.get(ratio, (576, 1024))
        
        print(f"🎨 Генерация {ratio}: '{prompt[:50]}...'")
        result = pipe(
            prompt=prompt,
            num_inference_steps=4,
            guidance_scale=1.0,
            width=width,
            height=height,
            output_type="pil"
        ).images[0]
        output_path = self.config.output_dir / f"keyframe_real_{ratio.replace(':', 'x')}.png"
        result.save(output_path)
        print(f"✅ Keyframe сохранён: {output_path}")
        return str(output_path)

    def run(self, prompt: str, dry_run: bool = False, ratio: str = "9:16") -> str:
        print(f"\n🚀 ЗАПУСК | Промпт: '{prompt}' | Формат: {ratio} | Режим: {'DRY' if dry_run else 'REAL'}")
        print("-" * 60)
        
        cached = self.cache.check(prompt)
        if cached and dry_run:
            print("♻️ Кэш: пропуск генерации")
            return cached["result_path"]
        
        print("[1/5] Загрузка модели...")
        if not dry_run:
            kf_path = self.generate_real_keyframe(prompt, ratio)
        else:
            time.sleep(0.5)
            kf_path = str(self.config.output_dir / f"temp_kf_{ratio.replace(':', 'x')}.png")
            print(f"🖼️ [DRY] Keyframe: {kf_path}")
        
        print("[2/5] Маска движения (эмуляция)...")
        time.sleep(0.3)
        
        print("[3/5] Анимация зон (эмуляция)...")
        time.sleep(0.3)
        
        print("[4/5] Пост-обработка...")
        final = self.post.run(kf_path if not dry_run else str(self.config.output_dir / f"temp_clip_{ratio.replace(':', 'x')}.mp4"))
        
        print("[5/5] Сохранение в кэш...")
        self.cache.store(prompt, final, metadata={"mode": "real" if not dry_run else "dry", "ratio": ratio, "timestamp": time.time()})
        
        print("-" * 60)
        print(f"✅ ГОТОВО | Результат: {final}")
        return final

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🎬 Zero-Cost Video Pipeline")
    parser.add_argument("prompt", nargs="?", default="золотой ретривер бежит по морскому берегу на закате, брызги, замедленная съёмка, вертикальный формат --ar 9:16")
    parser.add_argument("--dry", action="store_true", help="Dry-run режим")
    parser.add_argument("--ratio", type=str, default="9:16", choices=["1:1", "16:9", "9:16", "4:3", "3:4"], help="Соотношение сторон")
    args = parser.parse_args()
    pipe = VideoPipeline()
    pipe.run(args.prompt, dry_run=args.dry, ratio=args.ratio)
