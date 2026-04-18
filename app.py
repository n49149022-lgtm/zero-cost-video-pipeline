# 🎬 Zero-Cost Video Pipeline | Web Interface (Gradio)
# ЭТО СКЕЛЕТ. Веб-интерфейс будет добавляться постепенно.
# Принцип: "Простое поле ввода, кнопка запуска, статус и место для видео."

import gradio as gr
# TODO: from pipeline.core import VideoPipeline
# TODO: from pipeline.config import config

def generate_video(prompt: str, dry_run: bool = True) -> tuple:
    """Обработчик кнопки запуска"""
    if not prompt.strip():
        return "⚠️ Введите текстовый запрос", None
    
    if dry_run:
        return "🟡 Режим проверки архитектуры. Генерация отключена.", None
    
    # TODO: Подключить реальный пайплайн
    # pipeline = VideoPipeline()
    # result = pipeline.run(prompt)
    # return "✅ Видео готово!", result
    
    return "🔴 Реальная генерация пока недоступна. Дождитесь загрузки моделей.", None

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
            dry_run_checkbox = gr.Checkbox(label="🔍 Только проверка архитектуры", value=True)
            
        with gr.Column(scale=2):
            status_output = gr.Textbox(label="📊 Статус", lines=3)
            video_output = gr.Video(label="🎥 Результат")
    
    # Связываем кнопку с функцией
    run_btn.click(
        fn=generate_video, 
        inputs=[prompt_input, dry_run_checkbox], 
        outputs=[status_output, video_output]
    )

if __name__ == "__main__":
    print("🌐 Запуск веб-интерфейса на http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)
