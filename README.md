## Описание

`Blogicum` - это платформа, разработанная с использованием Django. 
Цель проекта - предоставить пользователям платформу, на которой они могут создавать и управлять своими постами.

## Основные функции платформы:

### Аутентификация пользователей:
Пользователи могут зарегистрироваться, войти в систему и выйти из нее.

### Профили пользователей:
Пользователи могут просматривать и обновлять информацию своего профиля.

### Создание и управление постами:
Аутентифицированные пользователи могут создавать, обновлять и удалять свои посты. 

Создатели поста могут редактировать или удалять только свои собственные посты.

### Отображение списка постов и подробной информации:
Посты можно перечислить на главной странице, и каждый пост имеет свою страницу с подробной информацией.

### Динамическое извлечение постов:
Посты и соответствующие комментарии извлекаются с помощью возможностей ORM Django.

### Просмотр категорий:
У каждой категории есть своя специальная страница, на которой перечислены все посты этой категории.

### Комментарии:
Аутентифицированные пользователи могут добавлять комментарии к посту, 
а также редактировать или удалять свои собственные комментарии.

Проект следует архитектуре MVT (Model-View-Template) Django и эффективно использует классы представлений
для отображения данных и обработки взаимодействия с пользователем. 

Представления проекта организованы в файле `views.py` внутри приложения `blog`.
Этот файл содержит несколько классов представлений для обработки различных запросов пользователей, включая:
 - `PostListView`
 - `PostDetailView`
 - `CategoryDetailView`
 - `UserProfileDetailView`
 - `UserProfileUpdateView` 

Также имеются представления, связанные с архитектурой постов и комментариев, которые позволяют пользователям создавать, обновлять и удалять посты и комментарии.

### Валидация Постов и Комментариев:

Система обеспечивает валидацию данных, когда пользователи создают или редактируют их посты и комментарии. 

Проект использует Django Forms для обработки и валидации данных формы. 
Формы обрабатывают валидацию и защиту от CSRF. 
Вьюшки для создания и обновления постов и комментариев используют эти формы для валидации введённых пользователем данных.

Проект также предотвращает редактирование или удаление постов и комментариев неавторизованными пользователями,
благодаря примеси `IsAuthorMixin`, которая проверяет, является ли текущий пользователь автором редактируемого или удаляемого поста/комментария.

### Фильтрация Запрещенных Слов:

В проекте реализована функция фильтрации запрещенных слов. 
Это дополнительный уровень валидации данных для обеспечения соблюдения норм сообщества.

Для реализации этой функции используется модель `ForbiddenWord`, которая используется для хранения всех запрещенных слов. 
Все слова, введенные пользователями в постах или комментариях, проходят через фильтр, который сверяет каждое слово со списком запрещенных слов.
Если слово соответствует одному из запрещенных, то возникает ошибка валидации.

Функция `forbidden_words(value: str)` служит для проверки введённого текста на наличие запрещённых слов. 
Запрещённые слова извлекаются из базы данных, и проводится поиск наиболее похожих слов из введённого текста. 
В случае нахождения запрещённых слов в тексте, создается исключение `ValidationError` с сообщением о наличии запрещённых слов.


### Требования

Python 3.9.7 and pip

## Установка

### 1. Клонирование репозитория

Первым шагом будет клонирование вашего репозитория на сервер. 
Вы можете сделать это с помощью команды git в терминале:
```bash
git clone https://github.com/AlexeyAlekseev/django_sprint4.git
```
### 2. Настройка
Для запуска проекта на базе PostgreSQL, nginx
```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl git python3-venv
```

Подготовка БД
```
sudo -u postgres psql
```

```
CREATE DATABASE myproject;
```
```
CREATE USER myprojectuser WITH PASSWORD 'password';
```

Зададим кодировку по умолчанию UTF-8, чего и ожидает Django.
Также мы зададим схему изоляции транзакций по умолчанию «read committed», 
которая будет блокировать чтение со стороны неподтвержденных транзакций. 
В заключение мы зададим часовой пояс. 
По умолчанию наши проекты Django настроены на использование стандарта времени UTC.

```
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
```
Предоставим созданному пользователю доступ для администрирования новой базы данных:

```
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```
Настройка Postgres завершена
```
\q
```
### 3. Создание и активация виртуального окружения
В каталоге вашего проекта создайте виртуальное окружение и активируйте его:
```
sudo -H pip3 install --upgrade pip

cd django_sprint4/

python3 -m venv venv
source venv/bin/activate
```
### 4. Установка зависимостей
Затем установите все необходимые зависимости с помощью pip:
```
pip install -r requirements.txt
```

```
vim /home/$USER/django_sprint4/blogicum/blogicum/settings.py
```
Убедитесь, что ваш файл настроек settings.py (или соответствующий файл настроек для вашего окружения) правильно настроен.
Это включает в себя настройку DEBUG, SECRET_KEY, DATABASES, ALLOWED_HOSTS.

```
DEBUG = False
```

```
ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . ., 'localhost']
```

```
. . .

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

. . .
```
Размещение статики

```
. . .

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```

### 5. Инициализация базы данных
Выполните миграции, чтобы инициализировать базу данных:
```
cd /home/$USER/django_sprint4/blogicum

python manage.py makemigrations
python manage.py migrate

# Создание УЗ администратора
python manage.py createsuperuser
```
### 6. Сбор статических файлов
Django не обслуживает статические файлы в продуктовом окружении по умолчанию. 
Соберите все статические файлы в указанную ваших настройках директорию:


```
python manage.py collectstatic
```
### 7. Запуск сервера
Наконец, запустите сервер Django:
```
python manage.py runserver 0.0.0.0:8000
```
```
http://server_domain_or_IP:8000
```
Учтите, что в зависимости от ваших требований в продуктовом окружении вы, вероятно, захотите настроить и использовать HTTP-сервер (например, Nginx или Apache) вместо встроенного сервера Django.
Также рекомендуется настроить менеджер процессов (такой, как Gunicorn или uWSGI) для обслуживания вашего Django-приложения.


## Настройка WEB сервера

Из виртуального окружения проверим работу gunicorn 

```
cd /home/$USER/django_sprint4/blogicum
gunicorn --bind 0.0.0.0:8000 blogicum.wsgi
```

Ожидаемый вывод в терминал: 
```
:~/django_sprint4/blogicum$ gunicorn --bind 0.0.0.0:8000 blogicum.wsgi
[2024-04-12 15:55:15 +0300] [13135] [INFO] Starting gunicorn 21.2.0
[2024-04-12 15:55:15 +0300] [13135] [INFO] Listening at: http://0.0.0.0:8000 (13135)
[2024-04-12 15:55:15 +0300] [13135] [INFO] Using worker: sync
[2024-04-12 15:55:15 +0300] [13136] [INFO] Booting worker with pid: 13136
```
Проверьте в новом окне терминала 

```
curl -v localhost:8000

*   Trying 127.0.0.1:8000...
* Connected to localhost (127.0.0.1) port 8000 (#0)
> GET / HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/7.74.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
...

```
Если всё хорошо отключите виртуальное окружение 

```
deactivate
```

Создадим socket файл: 
```
sudo vim /etc/systemd/system/gunicorn.socket
```

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Создадим unit файл
```
sudo vim /etc/systemd/system/gunicorn.service
```
```
[Unit]
Description= gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/django_sprint4/
ExecStart=/home/user/django_sprint4/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
           blogicum.wsgi:application

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

Проверить работу можно командой
```
curl -v --unix-socket /run/gunicorn.sock localhost
```
### NGINX

Создадим конфигурационный файл для приложения
```
sudo vim /etc/nginx/sites-available/blogicum
```

Создадим директорию для логов

```
 sudo mkdir -p /var/log/nginx/blog/
```
```
server {
    listen 80;
    server_name blog.rdp.ru;
    access_log /var/log/nginx/blog/access.log;
    error_log  /var/log/nginx/blog/error.log;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        autoindex on;
        root /home/user/django_sprint4/blogicum;
    }
    location /media/  {
        autoindex on;
        alias /home/user/django_sprint4/blogicum;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
```
sudo ln -s /etc/nginx/sites-available/blogicum /etc/nginx/sites-enabled/blogicum
sudo nginx -t
sudo systemctl restart nginx
```