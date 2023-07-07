# Поддержание ваших проектов Angular в актуальном состоянии

Как и Web и вся веб-экосистема, Angular постоянно совершенствуется. Angular балансирует между постоянным совершенствованием и стабильностью и простотой обновления.

Постоянное обновление вашего приложения Angular позволяет вам использовать преимущества передовых новых функций, а также оптимизаций и исправлений ошибок.

Этот документ содержит информацию и ресурсы, которые помогут вам поддерживать ваши приложения и библиотеки Angular в актуальном состоянии.

Информацию о нашей политике и практике версионирования &mdash; включая практику поддержки и обесценивания, а также график выпуска версий&mdash; смотрите в [Angular versioning and releases](guide/releases 'Angular versioning and releases').

<div class="alert is-helpful">

Если вы сейчас используете AngularJS, смотрите [Upgrading from AngularJS](guide/upgrade 'Upgrading from Angular JS'). _AngularJS_ - это название для всех версий Angular v1.x.

</div>

<a id="announce"></a>

## Получение уведомлений о новых релизах

Чтобы получать уведомления о выходе новых релизов, следите за [@angular](https://twitter.com/angular '@angular on Twitter') в Twitter или подпишитесь на [Angular blog](https://blog.angular.io 'Angular blog').

<a id="learn"></a>

## Узнайте о новых возможностях

Что нового? Что изменилось? Мы рассказываем о самых важных вещах, которые вам нужно знать, в блоге Angular в [анонсах релизов](https://blog.angular.io/tagged/release%20notes 'Angular blog - release announcements').

Чтобы просмотреть полный список изменений, организованный по версиям, смотрите [Angular change log](https://github.com/angular/angular/blob/main/CHANGELOG.md 'Angular change log').

<a id="checking-version-app"></a>

## Проверка версии Angular

Чтобы проверить версию Angular для вашего приложения: Находясь в директории проекта, используйте команду `ng version`.

<a id="checking-version-angular"></a>

## Поиск текущей версии Angular

Самая последняя стабильная версия Angular отображается в [Angular documentation](docs 'Angular documentation') в нижней части левой навигационной панели. Например, `stable (v13.0.3)`.

Вы также можете найти самую актуальную версию Angular с помощью команды CLI [`ng update`](cli/update). По умолчанию команда [`ng update`](cli/update) (без дополнительных аргументов) выводит список доступных обновлений.

<a id="update"></a>

## Обновление среды и приложений

Чтобы упростить процесс обновления, мы предоставляем полные инструкции в интерактивном [Angular Update Guide] (https://update.angular.io/ 'Angular Update Guide').

Руководство по обновлению Angular предоставляет настраиваемые инструкции по обновлению, основанные на текущей и целевой версиях, которые вы указали. Оно включает базовые и расширенные пути обновления в соответствии со сложностью ваших приложений.

Оно также содержит информацию об устранении неполадок и любые рекомендуемые изменения в руководстве, чтобы помочь вам получить максимальную отдачу от нового релиза.

Для простых обновлений достаточно выполнить команду CLI [`ng update`](cli/update). Без дополнительных аргументов команда [`ng update`](cli/update) перечисляет доступные обновления и предоставляет рекомендуемые шаги для обновления вашего приложения до самой актуальной версии.

[Angular Versioning and Releases](guide/releases#versioning 'Angular Release Practices, Versioning') описывает уровень изменений, которые вы можете ожидать, основываясь на номере версии релиза. В нем также описаны поддерживаемые пути обновления.

<a id="resources"></a>

## Резюме ресурсов

-   Анонсы релизов:

    [Angular blog - release announcements](https://blog.angular.io/tagged/release%20notes 'Angular blog announcements about recent releases')

-   Анонсы релизов\(старше\):

    [Angular blog - announcements about releases before August 2017](https://blog.angularjs.org/search?q=available&by-date=true 'Angular blog announcements about releases before August 2017')

-   Подробности релиза:

    [Журнал изменений Angular](https://github.com/angular/angular/blob/main/CHANGELOG.md 'Журнал изменений Angular')

-   Инструкции по обновлению:

    [Angular Update Guide](https://update.angular.io/ 'Руководство по обновлению Angular')

-   Ссылка на команду обновления:

    [Angular CLI `ng update` command reference](cli/update)

-   Практика создания версий, релизов, поддержки и устаревания:

    [Angular versioning and releases](guide/releases 'Angular versioning and releases')

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
