# Лаба 2 (минимум): nginx + gunicorn + WSGI

## 1) Gunicorn (WSGI-приложение)

```bash
python3 -m venv lab2/.venv
source lab2/.venv/bin/activate
pip install -r lab2/requirements.txt
./lab2/run_gunicorn.sh
```

Прямая проверка WSGI (без nginx):

```bash
curl -s http://127.0.0.1:8000/password
```

## 2) Nginx (статикa + прокси до gunicorn)

Установи nginx (например на macOS через Homebrew):

```bash
brew install nginx
```

Запуск nginx с конфигом `lab2/nginx.conf`:

```bash
./lab2/run_nginx.sh
```

Статика (`location /public/`, папка `lab2/public/`):

- положи любой файл в `lab2/public/`
- открой в браузере: `http://localhost:8080/public/<имя_файла>`
- готовый файл для проверки: `http://localhost:8080/public/test.txt`

Прокси (`location /gunicorn/` через `upstream`):

```bash
curl -s http://localhost:8080/gunicorn/password
```

Остановить nginx:

```bash
./lab2/stop_nginx.sh
```

## 3) Производительность (3 измерения wrk)

Установить `wrk`:

```bash
brew install wrk
```

Запустить 3 замера:

```bash
./lab2/bench_wrk.sh
```

Дальше по заданию увеличивай нагрузку (обычно `-c`) и найди порог, где при +10% появляются ошибки/таймауты.
