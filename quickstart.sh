#!/usr/bin/env bash
# 🎬 Zero-Cost Video Pipeline | Quickstart Script (v0.3)
# ОБНОВЛЕНИЕ: Рабочий скрипт проверки среды и запуска.
# Принцип: "Проверь → Подготовь → Запусти. Без лишних действий."

set -euo pipefail

echo "🎬 Zero-Cost Video Pipeline | Quickstart v0.3"
echo "================================================"

# 1. Проверка Python
echo "🐍 [1/4] Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.10+ и повторите."
    exit 1
fi

if ! python3 -c "import sys; assert sys.version_info >= (3, 10)" 2>/dev/null; then
    echo "❌ Требуется Python 3.10+."
    exit 1
fi
PYVER=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYVER OK"

# 2. Виртуальное окружение
echo "📦 [2/4] Настройка окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ venv создан"
fi
source venv/bin/activate

# 3. Зависимости
echo "📥 [3/4] Установка пакетов..."
pip install --upgrade pip -q
# Пока устанавливаем только Gradio для запуска интерфейса
# Остальные библиотеки будут добавлены по мере готовности модулей
pip install gradio -q
echo "✅ Пакеты готовы"

# 4. Запуск
echo "🚀 [4/4] Запуск интерфейса..."
echo "🌐 Откройте в браузере: http://localhost:7860"
echo "⏹️  Для остановки нажмите Ctrl+C"
echo "================================================"
python3 app.py
