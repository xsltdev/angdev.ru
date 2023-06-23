# Развертывание нескольких локалей

Если `myapp` - это каталог, содержащий распространяемые файлы вашего проекта, вы обычно делаете различные версии доступными для разных локалей в каталогах locale. Например, ваша французская версия находится в директории `myapp/fr`, а испанская версия - в директории `myapp/es`.

HTML тег `base` с атрибутом `href` определяет базовый URI, или URL, для относительных ссылок. Если вы установите опцию `"localize"` в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig] в значение `true` или в массив идентификаторов локалей, CLI настроит базовый `href` для каждой версии приложения.

Чтобы настроить базовый `href` для каждой версии приложения, CLI добавляет локаль к настроенной `"baseHref"`.

Укажите `"baseHref"` для каждой локали в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig].

В следующем примере `"baseHref"` установлен на пустую строку.

<code-example header="angular.json" path="i18n/angular.json" region="i18n-baseHref"></code-example>.

Также, чтобы объявить базовый `href` во время компиляции, используйте опцию CLI `--baseHref` с [`ng build`][aioclibuild].

## Настройка сервера

Типичное развертывание нескольких языков обслуживает каждый язык из отдельного подкаталога. Пользователи перенаправляются на предпочтительный язык, определенный в браузере с помощью HTTP-заголовка `Accept-Language`.

Если пользователь не определил предпочитаемый язык, или если предпочитаемый язык недоступен, то сервер возвращается к языку по умолчанию.

Чтобы изменить язык, измените текущее местоположение на другой подкаталог.

Смена подкаталога часто происходит с помощью меню, реализованного в приложении.

<div class="alert is-helpful">

Дополнительную информацию о том, как развернуть приложения на удаленном сервере, см. в разделе [Развертывание][aioguidedeployment].

</div>

### Пример Nginx

В следующем примере показана конфигурация Nginx.

<code-example path="i18n/doc-files/nginx.conf" language="nginx"></code-example>.

### Пример Apache

В следующем примере показана конфигурация Apache.

<code-example path="i18n/doc-files/apache2.conf" language="apache"></code-example>

<!-- links -->

[aioclibuild]: cli/build 'ng build | CLI | Angular'
[aioguidedeployment]: guide/deployment 'Deployment | Angular'
[aioguideworkspaceconfig]: guide/workspace-config 'Angular workspace configuration | Angular'

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
