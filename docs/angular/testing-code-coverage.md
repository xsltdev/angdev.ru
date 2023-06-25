<a id="code-coverage"></a>

# Узнайте, какой объем кода вы тестируете

Angular CLI может запускать модульные тесты и создавать отчеты о покрытии кода. Отчеты о покрытии кода покажут вам все части вашей кодовой базы, которые не могут быть должным образом проверены вашими модульными тестами.

<div class="alert is-helpful">

Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, <live-example name="testing" noDownload>запустите его в браузере</live-example> или <live-example name="testing" downloadOnly>скачайте и запустите его локально</live-example>.

</div>

Чтобы сгенерировать отчет о покрытии, выполните следующую команду в корне вашего проекта.

<code-example format="shell" language="shell">

ng test --no-watch --code-coverage

</code-example>

После завершения тестов команда создает в проекте новый каталог `/coverage`. Откройте файл `index.html`, чтобы увидеть отчет с вашим исходным кодом и значениями покрытия кода.

Если вы хотите создавать отчеты о покрытии кода при каждом тестировании, установите следующий параметр в файле конфигурации Angular CLI, `angular.json`:

<code-example format="json" language="json">

"test": { "options": {
"codeCoverage": true

}

}

</code-example>

## Обеспечение покрытия кода

Проценты покрытия кода позволяют вам оценить, какая часть вашего кода протестирована. Если ваша команда решила установить минимальный объем, который должен быть протестирован, обеспечьте соблюдение этого минимума с помощью Angular CLI.

Например, предположим, вы хотите, чтобы кодовая база имела минимум 80% покрытия кода. Чтобы это обеспечить, откройте файл конфигурации тестовой платформы [Karma](https://karma-runner.github.io), `karma.conf.js`, и добавьте свойство `check` в ключ `coverageReporter:`.

<code-example format="javascript" language="javascript">

coverageReporter: { dir: require('path').join(\_\_dirname, './coverage/&lt;project-name&gt;'),
subdir: '.',

репортеры: [

{ type: 'html' }

{ { type: 'text-summary' }

],

check: {

глобальный: {

statements: 80,

ветви: 80,

функции: 80,

линии: 80

}

}

}

</code-example>

<div class="alert is-helpful">

Подробнее о создании и тонкой настройке конфигурации Karma читайте в [руководстве по тестированию](guide/testing#configuration).

</div>

Свойство `check` заставляет инструмент обеспечивать покрытие кода не менее 80% при выполнении модульных тестов в проекте.

Подробнее о параметрах конфигурации покрытия читайте в [документации по покрытию кармы](https://github.com/karma-runner/karma-coverage/blob/master/docs/configuration.md).

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 17.01.2023
