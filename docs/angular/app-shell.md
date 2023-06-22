# Оболочка приложения

Оболочка приложения - это способ визуализации части вашего приложения с помощью маршрута во время сборки. Она может улучшить пользовательский опыт, быстро запуская статическую страницу \(скелет, общий для всех страниц\), в то время как браузер загружает полную версию клиента и автоматически переключается на нее после загрузки кода.

Это дает пользователям значимую первую картину вашего приложения, которая появляется быстро, потому что браузер может отрисовать HTML и CSS без необходимости инициализации JavaScript.

Узнайте больше в [The App Shell Model](https://developers.google.com/web/fundamentals/architecture/app-shell).

## Шаг 1: Подготовьте приложение

Сделайте это с помощью следующей команды Angular CLI:

<code-example format="shell" language="shell">

ng new my-app --routing

</code-example>

Для существующего приложения вы должны вручную добавить `RouterModule` и определить `<router-outlet>` в вашем приложении.

## Шаг 2: Создайте оболочку приложения

Используйте Angular CLI для автоматического создания оболочки приложения.

<code-example format="shell" language="shell">

ng generate app-shell

</code-example>

Более подробную информацию об этой команде смотрите в [App shell command](cli/generate#app-shell-command).

После выполнения этой команды вы увидите, что конфигурационный файл `angular.json` был обновлен для добавления двух новых целей, а также несколько других изменений.

<code-example language="json">

"server": { "builder": "&commat;angular-devkit/build-angular:server",
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

"fileReplacesments": [

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

"builder": "&commat;angular-devkit/build-angular:app-shell",

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

</code-example>

## Шаг 3: Убедитесь, что приложение собрано с содержимым оболочки

Используйте Angular CLI для создания цели `app-shell`.

<code-example format="shell" language="shell">

ng run my-app:app-shell:development

</code-example>

Или использовать производственную конфигурацию.

<code-example format="shell" language="shell">

ng run my-app:app-shell:production

</code-example>

Чтобы проверить вывод сборки, откройте <code class="no-auto-link">dist/my-app/browser/index.html</code>. Найдите текст по умолчанию `app-shell works!`, чтобы показать, что маршрут оболочки приложения был отображен как часть вывода.

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
