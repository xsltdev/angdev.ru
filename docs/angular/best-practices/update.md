---
description: "Как поддерживать проекты Angular в актуальном состоянии: стабильность, новые возможности и простой переход на новые версии."
---

# Как поддерживать проекты Angular в актуальном состоянии {: #keeping-your-angular-projects-up-to-date}

:date: 30.09.2026

Как и веб-платформа и вся веб-экосистема, Angular непрерывно развивается.
Angular совмещает постоянное развитие со стабильностью и простым обновлением.
Актуальное приложение получает новые возможности, оптимизации и исправления ошибок.

Здесь собраны сведения и ссылки, чтобы приложения и библиотеки Angular не отставали от фреймворка.

Политика версий и практики — поддержка, устаревание и график релизов — описаны в [версиях и релизах Angular](https://angular.dev/reference/releases 'Версии и релизы Angular').

!!! tip ""

    Если сейчас у вас AngularJS, смотрите [Обновление с AngularJS](https://angular.io/guide/upgrade 'Обновление с AngularJS'). _AngularJS_ — это имя всех версий Angular 1.x.

## Как узнавать о новых релизах {: #getting-notified-of-new-releases}

Чтобы узнавать о новых релизах, следите за [@angular](https://x.com/angular '@angular в X') в X (ранее Twitter) или подпишитесь на [блог Angular](https://blog.angular.dev 'Блог Angular').

## Что нового в релизах {: #learning-about-new-features}

Что нового? Что изменилось? Самое важное команда публикует в блоге Angular, в [анонсах релизов](https://blog.angular.dev/ 'Блог Angular — анонсы релизов').

Полный список изменений по версиям — в [журнале изменений Angular](https://github.com/angular/angular/blob/main/CHANGELOG.md 'Журнал изменений Angular').

## Как проверить свою версию Angular {: #checking-your-version-of-angular}

Версию Angular в приложении показывает команда `ng version`, запущенная из каталога проекта.

## Как узнать текущую версию Angular {: #finding-the-current-version-of-angular}

Последняя стабильная версия Angular указана [на npm](https://www.npmjs.com/package/@angular/core 'Angular на npm') в поле «Version». Например, `16.2.4`.

Текущую версию также показывает команда CLI [`ng update`](https://angular.dev/cli/update).
Без дополнительных аргументов [`ng update`](https://angular.dev/cli/update) перечисляет доступные обновления.

## Обновление окружения и приложений {: #updating-your-environment-and-apps}

Чтобы обновление не превращалось в головоломку, есть интерактивное [руководство по обновлению Angular](https://angular.dev/update-guide).

Руководство собирает шаги под указанные текущую и целевую версии.
Есть базовый и расширенный путь — под сложность приложения.
Там же — типичные сбои и ручные правки, чтобы взять от релиза максимум.

Для простого обновления хватает команды CLI [`ng update`](https://angular.dev/cli/update).
Без дополнительных аргументов [`ng update`](https://angular.dev/cli/update) показывает доступные обновления и рекомендуемые шаги до самой свежей версии.

[Версии и релизы Angular](https://angular.dev/reference/releases#angular-versioning 'Практики релизов и версии Angular') объясняют, какого масштаба изменений ждать по номеру версии.
Там же описаны поддерживаемые пути обновления.

## Сводка ресурсов {: #resource-summary}

-   Анонсы релизов:

    [Блог Angular — анонсы релизов](https://blog.angular.dev/ 'Анонсы недавних релизов в блоге Angular')

-   Подробности релиза:

    [Журнал изменений Angular](https://github.com/angular/angular/blob/main/CHANGELOG.md 'Журнал изменений Angular')

-   Инструкции по обновлению:

    [Руководство по обновлению Angular](https://angular.dev/update-guide)

-   Справочник команды обновления:

    [Справочник команды Angular CLI `ng update`](https://angular.dev/cli/update)

-   Практики версий, релизов, поддержки и устаревания:

    [Версии и релизы Angular](https://angular.dev/reference/releases 'Версии и релизы Angular')


---

Источник: [https://angular.dev/update](https://angular.dev/update)
