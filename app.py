# 🎬 Zero-Cost Video Pipeline | Web Interface (v0.3)
# ОБНОВЛЕНИЕ: Подключение реального оркестратора (core.py).
# Принцип: "Интерфейс принимает запрос, передаёт его в систему, показывает статус."

import gradio as gr
import sys
from pathlib import Path

# Добавляем корень проекта в путь импортов
sys.path.insert(0, str(Path(__file__).parent))

try:
    from pipeline.core import VideoPipeline
    PIPELINE_READY = True
except Exception as e:
    print(f"⚠️ Не удалось загрузить оркестратор: {e}")
    PIPELINE_READY = False

def generate_video(prompt: str, dry_run: bool = True):
    """Обработчик кнопки запуска"""
    if not prompt.strip():
        return "⚠️ Пожалуйста, введите текстовый запрос.", None
    
    if not PIPELINE_READY:
        return "❌ Ошибка загрузки модулей. Проверьте структуру проекта.", None
    
    try:
        pipeline = VideoPipeline()
        
        if dry_run:
            status_msg = "🟡 Режим проверки архитектуры (Dry-Run). Генерация эмулируется."
            log_result = pipeline.run_dry(prompt)
            return f"{status_msg}\n📝 Лог выполнения:\n{log_result}", None
        else:
            return "🔴 Реальная генерация пока недоступна. Используйте Dry-Run.", None
            
    except Exception as e:
        return f"❌ Ошибка выполнения: {str(e)}", None

# Создание интерфейса
with gr.Blocks(title="Zero-Cost Video Pipeline", theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🎬 Zero-Cost Video Pipeline")
    gr.Markdown("*CPU-Only генерация видео. Бесплатно. Без облака. Без GPU.*")
    
    with gr.Row():
        with gr.Column(scale=1):
            prompt_input = gr.Textbox(
                label="📝 Ваш промпт", 
                placeholder="монстера у окна, естественный свет",
                lines=2
            )
            run_btn = gr.Button("🚀 Запустить генерацию", variant="primary")
            dry_run_checkbox = gr.Checkbox(label="🔍 Только проверка архитектуры (Dry-Run)", value=True)
            
        with gr.Column(scale=2):
            status_output = gr.Textbox(label="📊 Статус и лог", lines=8)
            video_output = gr.Video(label="🎥 Результат")
    
    run_btn.click(
        fn=generate_video, 
        inputs=[prompt_input, dry_run_checkbox], 
        outputs=[status_output, video_output]
    )

if __name__ == "__main__":
    print("🌐 Запуск веб-интерфейса на http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)
