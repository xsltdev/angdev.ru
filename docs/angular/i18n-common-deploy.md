# Развертывание нескольких локалей

:date: 28.02.2022

Если `myapp` - это каталог, содержащий распространяемые файлы вашего проекта, вы обычно делаете различные версии доступными для разных локалей в каталогах locale. Например, ваша французская версия находится в директории `myapp/fr`, а испанская версия - в директории `myapp/es`.

HTML тег `base` с атрибутом `href` определяет базовый URI, или URL, для относительных ссылок. Если вы установите опцию `"localize"` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig] в значение `true` или в массив идентификаторов локалей, CLI настроит базовый `href` для каждой версии приложения.

Чтобы настроить базовый `href` для каждой версии приложения, CLI добавляет локаль к настроенной `"baseHref"`.

Укажите `"baseHref"` для каждой локали в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig].

В следующем примере `"baseHref"` установлен на пустую строку.

```json
"projects": {
    "angular.io-example": {
      // ...
      "i18n": {
        "sourceLocale": "en-US",
        "locales": {
          "fr": {
            "translation": "src/locale/messages.fr.xlf",
            "baseHref": ""
          }
        }
      },
      "architect": {
        // ...
      }
    }
  }
  // ...
}
```

Также, чтобы объявить базовый `href` во время компиляции, используйте опцию CLI `--baseHref` с [`ng build`][aioclibuild].

## Настройка сервера

Типичное развертывание нескольких языков обслуживает каждый язык из отдельного подкаталога. Пользователи перенаправляются на предпочтительный язык, определенный в браузере с помощью HTTP-заголовка `Accept-Language`.

Если пользователь не определил предпочитаемый язык, или если предпочитаемый язык недоступен, то сервер возвращается к языку по умолчанию.

Чтобы изменить язык, измените текущее местоположение на другой подкаталог.

Смена подкаталога часто происходит с помощью меню, реализованного в приложении.

!!!note ""

    Дополнительную информацию о том, как развернуть приложения на удаленном сервере, см. в разделе [Развертывание][aioguidedeployment].

### Пример Nginx

В следующем примере показана конфигурация Nginx.

```
http {
    # Browser preferred language detection (does NOT require
    # AcceptLanguageModule)
    map $http_accept_language $accept_language {
        ~*^de de;
        ~*^fr fr;
        ~*^en en;
    }
    # ...
}

server {
    listen 80;
    server_name localhost;
    root /www/data;

    # Fallback to default language if no preference defined by browser
    if ($accept_language ~ "^$") {
        set $accept_language "fr";
    }

    # Redirect "/" to Angular application in the preferred language of the browser
    rewrite ^/$ /$accept_language permanent;

    # Everything under the Angular application is always redirected to Angular in the
    # correct language
    location ~ ^/(fr|de|en) {
        try_files $uri /$1/index.html?$args;
    }
    # ...
}
```

### Пример Apache

В следующем примере показана конфигурация Apache.

```apache
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot /www/data
    <Directory "/www/data">
        RewriteEngine on
        RewriteBase /
        RewriteRule ^../index\.html$ - [L]

        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule (..) $1/index.html [L]

        RewriteCond %{HTTP:Accept-Language} ^de [NC]
        RewriteRule ^$ /de/ [R]

        RewriteCond %{HTTP:Accept-Language} ^en [NC]
        RewriteRule ^$ /en/ [R]

        RewriteCond %{HTTP:Accept-Language} !^en [NC]
        RewriteCond %{HTTP:Accept-Language} !^de [NC]
        RewriteRule ^$ /fr/ [R]
    </Directory>
</VirtualHost>
```

<!-- links -->

[aioclibuild]: https://angular.io/cli/build
[aioguidedeployment]: deployment.md
[aioguideworkspaceconfig]: workspace-config.md

<!-- external links -->

<!-- end links -->
