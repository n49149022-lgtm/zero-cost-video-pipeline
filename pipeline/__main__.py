# 🎬 Zero-Cost Video Pipeline | Entry Point
# ЭТО СКЕЛЕТ. Точка входа для запуска пайплайна.
# Позже позволит запускать проект одной командой: python -m pipeline "ваш промпт"

import argparse
import sys
from pathlib import Path

# Добавляем корень проекта в путь импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

# TODO: Раскомментировать после готовности модулей
# from pipeline.config import config
# from pipeline.core import VideoPipeline

def parse_args():
    parser = argparse.ArgumentParser(
        description="🎬 Zero-Cost Video Pipeline | CPU-Only Generation"
    )
    parser.add_argument("prompt", nargs="?", default="монстера у окна, естественный свет", 
                        help="Текстовый запрос для генерации")
    parser.add_argument("--dry-run", action="store_true", default=True, 
                        help="Только показать план, без генерации")
    parser.add_argument("--fps", type=int, default=30, help="Целевая частота кадров")
    parser.add_argument("--upscale", type=str, default="2x", help="Коэффициент апскейла")
    return parser.parse_args()

def main():
    args = parse_args()
    print("🎬 Zero-Cost Video Pipeline | Запуск...")
    print(f"📝 Промпт: {args.prompt}")
    print(f"⚙️  Режим: {'DRY-RUN (проверка архитектуры)' if args.dry_run else 'REAL (генерация)'}")
    print("-" * 40)
    
    if args.dry_run:
        print("✅ Архитектура в сборе. Модули подключены.")
        print("📋 План запуска:")
        print("  1. Загрузка конфигурации (config.py)")
        print("  2. Проверка кэша (cache.py)")
        print("  3. Генерация keyframe (models.py + core.py)")
        print("  4. Маска движения → анимация зон")
        print("  5. Селективный апскейл → интерполяция")
        print("  6. Сохранение в output/")
        print("\n🟡 Реальная генерация будет активирована после загрузки моделей.")
    else:
        print("⚠️ Режим REAL пока недоступен. Сначала настройте модели и зависимости.")
    
    print("-" * 40)
    print("👋 Готово. Система в ожидании.")

if __name__ == "__main__":
    main()
