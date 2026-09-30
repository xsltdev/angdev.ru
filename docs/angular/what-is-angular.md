---
description: "Angular — веб-фреймворк для быстрых и надёжных приложений: компоненты, сигналы, маршрутизация, формы и инструменты сборки"
---

# Что такое Angular? {: #what-is-angular}

:date: 30.09.2026

Angular — веб-фреймворк, на котором делают быстрые и надёжные приложения.

Его развивает отдельная команда Google. Вместе с фреймворком поставляются API, библиотеки и инструменты, которые упрощают повседневную разработку. Платформа рассчитана и на небольшую команду, и на крупную кодовую базу. Официальная документация живёт на [angular.dev](https://angular.dev/).

<div class="grid cards" markdown>

-   :simple-angular:{ .lg .middle } **Основы**

    ***

    Как устроено приложение Angular.

    [:octicons-arrow-right-24: Основы](essentials/overview.md)

-   :material-school:{ .lg .middle } **Учебники**

    ***

    Пошаговые уроки в браузере на официальном сайте.

    [:octicons-arrow-right-24: Учебники](https://angular.dev/tutorials)

</div>

## Возможности {: #features-that-power-your-development}

**Компоненты.** Приложение делится на изолированные части со своим шаблоном и логикой. [Компоненты](essentials/components.md)

**Сигналы.** Мелкая модель реактивности и оптимизации на этапе компиляции упрощают код и ускоряют интерфейс. [Сигналы](essentials/signals.md)

**Серверный рендеринг.** Angular умеет серверный рендеринг (SSR), статическую генерацию (SSG) и гидратацию DOM. [Гидратация](hydration.md)

**Инъекция зависимостей.** Общий код подключается к компонентам через инжектор, а не через ручную передачу зависимостей. [Инъекция зависимостей](essentials/dependency-injection.md)

**Маршрутизация.** Навигация, охранники, подготовка данных и ленивая загрузка. [Маршрутизация](routing/overview.md)

**Формы.** Единая модель участия полей и проверки значений. [Формы](forms/overview.md)

## Инструменты {: #develop-applications-faster-than-ever}

**CLI.** [Angular CLI](tools/cli/overview.md) поднимает проект за минуту и даёт команды, с которыми приложение дорастает до продакшена.

**DevTools.** [Angular DevTools](https://angular.dev/tools/devtools) ставится рядом с инструментами браузера: дерево компонентов, дерево инжекторов и профилирование.

**`ng update`.** Команда запускает автоматические преобразования кода и снимает рутину ломающих изменений между мажорными версиями. [Обновление](best-practices/update.md)

**Language Service.** Языковой сервис даёт автодополнение, навигацию, рефакторинг и диагностику шаблонов в редакторе. [Language Service](https://angular.dev/tools/language-service)

## Стабильность {: #ship-with-confidence}

Каждый коммит Angular прогоняется через сотни тысяч тестов во внутреннем монорепозитории Google. От стабильности зависят крупные продукты, включая Google Cloud, поэтому изменения проверяют на совместимость и по возможности сопровождают схемами миграции. Подробнее о [монорепозитории Google](https://cacm.acm.org/research/why-google-stores-billions-of-lines-of-code-in-a-single-repository/).

Релизы выходят по расписанию. Окна долгосрочной поддержки закрывают критичные исправления безопасности. Схемы миграции и [политика версий](https://angular.dev/reference/releases) помогают не отставать от фреймворка и платформы.

## Масштаб {: #works-at-any-scale}

Интернационализация закрывает перевод сообщений и форматирование, в том числе синтаксис ICU. [Интернационализация](https://angular.dev/guide/i18n)

Безопасность закладывается по умолчанию: санитизация HTML и Trusted Types снижают риск межсайтового скриптинга и подделки запросов. [Безопасность](security.md)

Сборка в CLI идёт через Vite и esbuild. Проекты на сотни тысяч строк собираются быстрее, чем на прежнем конвейере. [Сборка](https://angular.dev/tools/cli/build-system-migration)

На архитектуре Angular работают крупные продукты Google — от [Google Fonts](https://fonts.google.com/) до [Google Cloud](https://console.cloud.google.com).

## Открытая разработка {: #open-source-first}

Исходный код, пул-реквесты и коммиты лежат на [GitHub](https://github.com/angular/angular). Команда регулярно разбирает issues.

План работ публикуется открыто, крупные изменения проходят через RFC. [Дорожная карта](https://angular.dev/roadmap)

## Сообщество {: #a-thriving-community}

Вокруг фреймворка есть курсы, блоги и подборки. Одна из них — [DevLibrary](https://devlibrary.withgoogle.com/products/angular?sort=added).

Вклад в проект начинается с правки опечатки и заканчивается крупной функцией. [Как участвовать](https://github.com/angular/angular/blob/main/CONTRIBUTING.md)

Angular GDE ведут сообщества по всему миру. [Каталог экспертов](https://developers.google.com/community/experts/directory?specialization=angular)

Команда Angular работает вместе с Chrome Aurora (оптимизации вроде `NgOptimizedImage` и Core Web Vitals), а также с Firebase, TensorFlow, Flutter, Material Design и Google Cloud.

!!! info "Куда смотреть дальше"

    -   [Дорожная карта](https://angular.dev/roadmap)
    -   [Песочница](https://angular.dev/playground)
    -   [Учебники](https://angular.dev/tutorials)
    -   [Курс на YouTube](https://youtube.com/playlist?list=PL1w1q3fL4pmj9k1FrJ3Pe91EPub2_h4jF)
    -   [Справочник API](https://angular.dev/api)

---

Источник: [https://angular.dev/overview](https://angular.dev/overview)
