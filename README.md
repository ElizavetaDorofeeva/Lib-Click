# Click 8.5.0
## Дорофеева Елизавета
## https://github.com/pallets/click

## Запуск

```bash
python -m venv .venv
source .venv\Scripts\activate        
pip install -r requirements.txt

python fail.py --count 3 Alice  # пример: три раза "Hello Alice!"
python trace.py ok               # путь выполнения внутри Click
python trace.py error            # ошибка: --count abc
python trace.py custom           # свой ParamType (custom_type.py)
```
