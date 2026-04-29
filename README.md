# Summarizer

Считает статистики по колонкам DataFrame и сохраняет в markdown / html / xlsx.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

Будет напечатан markdown-отчёт и созданы файлы `iris_report.html` и `iris_report.xlsx`.

## Использование

```python
import pandas as pd
from summarizer import Summarizer

df = pd.DataFrame({
    "age": [25, 32, 47],
    "city": ["Moscow", "SPb", "Moscow"],
})

s = Summarizer(df)
print(s.report("markdown"))
s.report("html", "report.html")
s.report("xlsx", "report.xlsx")
```

## Тесты

```bash
pytest
```
