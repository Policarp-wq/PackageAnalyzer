### Визуализатор пакетов Ubuntu OS с графическим представлением Mermaid
Как запустить:
1. Клонируем репозиторий
```bash
git clone https://github.com/Policarp-wq/PackageAnalyzer.git
cd .\PackageAnalyzer
```
2) Создаём и запускаем виртуальное окружение
```bash
python -m venv venv
venv\Scripts\activate
```
3) Устанавливаем зависимости
```bash
pip install -r requirements.txt
```
4) Запускаем скрипт
```bash
py .\visualizer.py --path [Путь до визуализатора] --package [Название пакета] --repo [Репозиторий для поиска]
```
Пример:
```
py .\visualizer.py --path C:\Users\Policarp\AppData\Roaming\npm\mmdc --package obsession --repo http://archive.ubuntu.com/ubuntu/ubuntu/pool/universe/
```

Результат вывода:
![image](https://github.com/user-attachments/assets/4eade06f-1595-40dd-a71b-00be287dfdd5)

5) Запуск тестирования:
   ```bash
   pytest -v
   ```

Вывод: 
![image](https://github.com/user-attachments/assets/38256bb0-15a6-4745-a6a9-7968285d45e8)


