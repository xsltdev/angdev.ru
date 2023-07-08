# Оболочка приложения

:date: 28.02.2022

**Оболочка приложения** - это способ визуализации части вашего приложения с помощью маршрута во время сборки. Она может улучшить пользовательский опыт, быстро запуская статическую страницу (скелет, общий для всех страниц), в то время как браузер загружает полную версию клиента и автоматически переключается на нее после загрузки кода.

Это дает пользователям значимую первую картину вашего приложения, которая появляется быстро, потому что браузер может отрисовать HTML и CSS без необходимости инициализации JavaScript.

Узнайте больше в [The App Shell Model](https://developers.google.com/web/fundamentals/architecture/app-shell).

## Шаг 1: Подготовьте приложение

Сделайте это с помощью следующей команды Angular CLI:

```shell
ng new my-app --routing
```

Для существующего приложения вы должны вручную добавить `RouterModule` и определить `<router-outlet>` в вашем приложении.

## Шаг 2: Создайте оболочку приложения

Используйте Angular CLI для автоматического создания оболочки приложения.

```shell
ng generate app-shell
```

Более подробную информацию об этой команде смотрите в [App shell command](https://angular.io/cli/generate#app-shell-command).

После выполнения этой команды вы увидите, что конфигурационный файл `angular.json` был обновлен для добавления двух новых целей, а также несколько других изменений.

```json
"server": {
  "builder": "@angular-devkit/build-angular:server",
  "defaultConfiguration": "production",
  "options": {
    "outputPath": "dist/my-app/server",
    "main": "src/main.server.ts",
    "tsConfig": "tsconfig.server.json"
  },
  "configurations": {
    "development": {
      "outputHashing": "none",
    },
    "production": {
      "outputHashing": "media",
      "fileReplacements": [
        {
          "replace": "src/environments/environment.ts",
          "with": "src/environments/environment.prod.ts"
        }
      ],
      "sourceMap": false,
      "optimization": true
    }
  }
},
"app-shell": {
  "builder": "@angular-devkit/build-angular:app-shell",
  "defaultConfiguration": "production",
  "options": {
    "route": "shell"
  },
  "configurations": {
    "development": {
      "browserTarget": "my-app:build:development",
      "serverTarget": "my-app:server:development",
    },
    "production": {
      "browserTarget": "my-app:build:production",
      "serverTarget": "my-app:server:production"
    }
  }
}
```

## Шаг 3: Убедитесь, что приложение собрано с содержимым оболочки

Используйте Angular CLI для создания цели `app-shell`.

```shell
ng run my-app:app-shell:development
```

Или использовать производственную конфигурацию.

```shell
ng run my-app:app-shell:production
```

Чтобы проверить вывод сборки, откройте `dist/my-app/browser/index.html`. Найдите текст по умолчанию `app-shell works!`, чтобы показать, что маршрут оболочки приложения был отображен как часть вывода.

<!-- links -->

<!-- external links -->

<!-- end links -->
