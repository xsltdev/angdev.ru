---
description: Как и Web и вся веб-экосистема, Angular постоянно совершенствуется. Angular балансирует между постоянным совершенствованием и стабильностью и простотой обновления
---

# Поддержание ваших проектов Angular в актуальном состоянии

:date: 28.02.2022

Как и Web и вся веб-экосистема, Angular постоянно совершенствуется. Angular балансирует между постоянным совершенствованием и стабильностью и простотой обновления.

Постоянное обновление вашего приложения Angular позволяет вам использовать преимущества передовых новых функций, а также оптимизаций и исправлений ошибок.

Этот документ содержит информацию и ресурсы, которые помогут вам поддерживать ваши приложения и библиотеки Angular в актуальном состоянии.

Информацию о нашей политике и практике версионирования &mdash; включая практику поддержки и обесценивания, а также график выпуска версий&mdash; смотрите в [Angular versioning and releases](https://angular.io/guide/releases).

!!!note ""

    Если вы сейчас используете AngularJS, смотрите [Upgrading from AngularJS](https://angular.io/guide/upgrade). _AngularJS_ - это название для всех версий Angular v1.x.

## Получение уведомлений о новых релизах {: #announce}

Чтобы получать уведомления о выходе новых релизов, следите за [@angular](https://twitter.com/angular '@angular on Twitter') в Twitter или подпишитесь на [Angular blog](https://blog.angular.io 'Angular blog').

## Узнайте о новых возможностях {: #learn}

Что нового? Что изменилось? Мы рассказываем о самых важных вещах, которые вам нужно знать, в блоге Angular в [анонсах релизов](https://blog.angular.io/tagged/release%20notes 'Angular blog - release announcements').

Чтобы просмотреть полный список изменений, организованный по версиям, смотрите [Angular change log](https://github.com/angular/angular/blob/main/CHANGELOG.md 'Angular change log').

## Проверка версии Angular {: #checking-version-app}

Чтобы проверить версию Angular для вашего приложения: Находясь в директории проекта, используйте команду `ng version`.

## Поиск текущей версии Angular {: #checking-version-angular}

Самая последняя стабильная версия Angular отображается в Angular документации в нижней части левой навигационной панели. Например, `stable (v13.0.3)`.

Вы также можете найти самую актуальную версию Angular с помощью команды CLI [`ng update`](https://angular.io/cli/update). По умолчанию команда [`ng update`](https://angular.io/cli/update) (без дополнительных аргументов) выводит список доступных обновлений.

## Обновление среды и приложений {: #update}

Чтобы упростить процесс обновления, мы предоставляем полные инструкции в интерактивном [Angular Update Guide](https://update.angular.io/ 'Angular Update Guide').

Руководство по обновлению Angular предоставляет настраиваемые инструкции по обновлению, основанные на текущей и целевой версиях, которые вы указали. Оно включает базовые и расширенные пути обновления в соответствии со сложностью ваших приложений.

Оно также содержит информацию об устранении неполадок и любые рекомендуемые изменения в руководстве, чтобы помочь вам получить максимальную отдачу от нового релиза.

Для простых обновлений достаточно выполнить команду CLI `ng update`. Без дополнительных аргументов команда `ng update` перечисляет доступные обновления и предоставляет рекомендуемые шаги для обновления вашего приложения до самой актуальной версии.

[Angular Versioning and Releases](https://angular.io/guide/releases#versioning 'Angular Release Practices, Versioning') описывает уровень изменений, которые вы можете ожидать, основываясь на номере версии релиза. В нем также описаны поддерживаемые пути обновления.

## Резюме ресурсов {: #resources}

-   Анонсы релизов:

    [Angular blog - release announcements](https://blog.angular.io/tagged/release%20notes 'Angular blog announcements about recent releases')

-   Анонсы релизов (старше):

    [Angular blog - announcements about releases before August 2017](https://blog.angularjs.org/search?q=available&by-date=true 'Angular blog announcements about releases before August 2017')

-   Подробности релиза:

    [Журнал изменений Angular](https://github.com/angular/angular/blob/main/CHANGELOG.md 'Журнал изменений Angular')

-   Инструкции по обновлению:

    [Angular Update Guide](https://update.angular.io/ 'Руководство по обновлению Angular')

-   Ссылка на команду обновления:

    [Angular CLI `ng update` command reference](https://angular.io/cli/update)

-   Практика создания версий, релизов, поддержки и устаревания:

    [Angular versioning and releases](https://angular.io/guide/releases)

## Ссылки

-   [Keeping your Angular projects up-to-date](https://angular.io/guide/updating)
