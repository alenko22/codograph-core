# main/views.py
import os
import uuid
import pyflowchart
from django.conf import settings
from django.shortcuts import render

def home(request):
    return render(request, 'main/index.html')

def generate(request):
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        # Сохраняем код в контексте, чтобы он остался в textarea после отправки
        context['code'] = code
        if not code:
            context['error'] = 'Пожалуйста, вставьте код.'
        else:
            try:
                # Генерируем DSL представление блок-схемы
                fc = pyflowchart.Flowchart.from_code(code)
                dsl_code = fc.flowchart()

                # Опционально: сохраняем HTML-файл в медиа для возможности скачивания
                # Но основное отображение будет через встроенный JS
                filename = f"flowchart_{uuid.uuid4().hex}.html"
                filepath = os.path.join(settings.MEDIA_ROOT, filename)
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Flowchart</title>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.3.0/raphael.min.js"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.17.1/flowchart.min.js"></script>
                </head>
                <body>
                    <div id="diagram"></div>
                    <script>
                        var diagram = flowchart.parse(`{dsl_code}`);
                        diagram.drawSVG('diagram');
                    </script>
                </body>
                </html>
                """
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                # Передаём в контекст DSL и URL для скачивания
                context['dsl_code'] = dsl_code
                context['download_url'] = os.path.join(settings.MEDIA_URL, filename)
                context['success'] = True
            except Exception as e:
                context['error'] = f'Ошибка при генерации диаграммы: {str(e)}'
    else:
        # Если страницу открыли методом GET (например, по прямой ссылке),
        # можно показать пример кода по умолчанию
        context['code'] = """def greet(name):
    if name == "Alice":
        print("Hello, Alice!")
    else:
        print(f"Hello, {name}!")

greet("Bob")"""

    return render(request, 'main/diagram.html', context)