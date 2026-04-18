#!/usr/bin/env bash
set -euo pipefail
echo "🎬 Zero-Cost Video Pipeline | Запуск"
echo "======================================"

if ! command -v python3 &>/dev/null; then echo "❌ Python 3 не найден"; exit 1; fi
python3 -c "import sys; assert sys.version_info >= (3, 10)" || { echo "❌ Python 3.10+ required"; exit 1; }

[ -d "venv" ] || python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✅ Готово. Запуск..."
echo "🔹 Реальная генерация: python3 -m pipeline.core 'ваш промпт'"
echo "🔹 Dry-run тест: python3 -m pipeline.core 'тест' --dry"
echo "🔹 Веб-интерфейс: python3 app.py"
echo "======================================"
python3 -m pipeline.core "$@"
