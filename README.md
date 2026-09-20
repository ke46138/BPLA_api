# BPLA_api
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ke46138/BPLA_api?style=flat-square&color=2a5c03)

gRPC API для получения информации о красных уровнях из макса.

## Запуск

1. Склонируйте репозиторий
    - Через HTTP `git clone https://github.com/ke46138/BPLA_api`
    - Через RNS `rns://7cf12e0bb855cb6167df9c5f20d9cfd3/public/BPLA_api`
2. Перейдите в склонированный репозиторий
    - `cd BPLA_api`
2. Установите зависимости
    - `pip install -r requirements.txt`
3. Скопируйте и настройте конфиг по вкусу
    - `cp config.example.py config.py`
    - `nano config.py`
4. Сгенерируйте gRPC файлы
```bash
python3 -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated ./proto/max_bridge.proto
```
5. Измените строку `import max_bridge_pb2 as max__bridge__pb2` в файле `generated/max_bridge_pb2_grpc.py` на `from generated import max_bridge_pb2 as max__bridge__pb2`
6. Запустите
    - `python3 main.py`
