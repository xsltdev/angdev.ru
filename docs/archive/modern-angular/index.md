---
description: Modern Angular, Manfred Steyer, Современный Angular, Манфред Штейер
hide:
    - toc
---

# Современный Angular

**[Введение](chap00.md)**

<div class="grid cards" style="margin-top: 1.6em" markdown>

-   **Автономные компоненты: ментальная модель и совместимость**

    ***

    [:octicons-arrow-right-24: Почему мы вообще запустили NgModules?](chap01.md#leanpub-auto-why-did-we-even-get-ngmodules-in-the-first-place)

    [:octicons-arrow-right-24: Знакомство с автономными компонентами](chap01.md#leanpub-auto-getting-started-with-standalone-components)

    [:octicons-arrow-right-24: Ментальная модель](chap01.md#leanpub-auto-the-mental-model)

    [:octicons-arrow-right-24: Пайпы, директивы и сервисы](chap01.md#leanpub-auto-pipes-directives-and-services)

    [:octicons-arrow-right-24: Загрузка автономных компонентов](chap01.md#leanpub-auto-bootstrapping-standalone-components)

    [:octicons-arrow-right-24: Совместимость с существующим кодом](chap01.md#leanpub-auto-compatibility-with-existing-code)

    [:octicons-arrow-right-24: Попутное замечание: модуль CommonModule](chap01.md#leanpub-auto-side-note-the-commonmodule)

-   **Архитектура с отдельными компонентами**

    ***

    [:octicons-arrow-right-24: Группировка строительных блоков](chap02.md#leanpub-auto-grouping-building-blocks)

    [:octicons-arrow-right-24: Импортирование целых бочек](chap02.md#leanpub-auto-importing-whole-barrels)

    [:octicons-arrow-right-24: Бочки с красивыми именами: сопоставление путей](chap02.md#leanpub-auto-barrels-with-pretty-names-path-mappings)

    [:octicons-arrow-right-24: Библиотеки рабочих пространств и Nx](chap02.md#leanpub-auto-workspace-libraries-and-nx)

    [:octicons-arrow-right-24: Границы модулей с использованием Sheriff](chap02.md#leanpub-auto-module-boundaries-with-sheriff)

-   **Автономные API для маршрутизации и ленивой загрузки**

    ***

    [:octicons-arrow-right-24: Предоставление конфигурации маршрутизации](chap03.md#leanpub-auto-providing-the-routing-configuration)

    [:octicons-arrow-right-24: Использование директив маршрутизатора](chap03.md#leanpub-auto-using-router-directives)

    [:octicons-arrow-right-24: Ленивая загрузка с автономными компонентами](chap03.md#leanpub-auto-lazy-loading-with-standalone-components)

    [:octicons-arrow-right-24: Инжекторы среды: Службы для конкретных маршрутов](chap03.md#leanpub-auto-environment-injectors-services-for-specific-routes)

    [:octicons-arrow-right-24: Настройка NGRX и функций Slices](chap03.md#leanpub-auto-setting-up-ngrx-and-feature-slices)

    [:octicons-arrow-right-24: Настройка окружения: ENVIRONMENT_INITIALIZER](chap03.md#leanpub-auto-setting-up-your-environment-environmentinitializer)

    [:octicons-arrow-right-24: Компонентный вход привязки](chap03.md#leanpub-auto-component-input-bindings)

-   **Элементы Angular с автономными компонентами**

    ***

    [:octicons-arrow-right-24: Предоставление автономного компонента](chap04.md#leanpub-auto-providing-a-standalone-component)

    [:octicons-arrow-right-24: Установка элементов Angular](chap04.md#leanpub-auto-installing-angular-elements)

    [:octicons-arrow-right-24: Загрузка с помощью элементов Angular](chap04.md#leanpub-auto-bootstrapping-with-angular-elements)

    [:octicons-arrow-right-24: Попутная заметка: Загрузка нескольких компонентов](chap04.md#leanpub-auto-side-note-bootstrapping-multiple-components)

    [:octicons-arrow-right-24: Вызов элемента Angular](chap04.md#leanpub-auto-calling-an-angular-element)

    [:octicons-arrow-right-24: Вызов веб-компонента в компоненте Angular](chap04.md#leanpub-auto-calling-a-web-component-in-an-angular-component)

    [:octicons-arrow-right-24: Бонус: компиляция самодостаточного бандла](chap04.md#leanpub-auto-bonus-compiling-self-contained-bundle)

-   **HttpClient: автономные API и функциональные перехватчики**

    ***

    [:octicons-arrow-right-24: Автономный API для HttpClient](chap05.md#leanpub-auto-standalone-apis-for-httpclient)

    [:octicons-arrow-right-24: Функциональные перехватчики](chap05.md#leanpub-auto-functional-interceptors)

    [:octicons-arrow-right-24: Перехватчики и ленивая загрузка](chap05.md#leanpub-auto-interceptors-and-lazy-loading)

    [:octicons-arrow-right-24: Проблема с запросами, сделанными родителями](chap05.md#leanpub-auto-pitfall-with-withrequestsmadeviaparent)

    [:octicons-arrow-right-24: Устаревшие перехватчики и другие особенности](chap05.md#leanpub-auto-legacy-interceptors-and-other-features)

    [:octicons-arrow-right-24: Дополнительные возможности](chap05.md#leanpub-auto-further-features)

-   **Тестирование автономных компонентов**

    ***

    [:octicons-arrow-right-24: Настройка тестов](chap06.md#leanpub-auto-test-setup)

    [:octicons-arrow-right-24: Макет HttpClient](chap06.md#leanpub-auto-the-httpclient-mock)

    [:octicons-arrow-right-24: Неглубокое тестирование](chap06.md#leanpub-auto-shallow-testing)

    [:octicons-arrow-right-24: Макет маршрутизатора и магазина](chap06.md#leanpub-auto-mock-router-and-store)

-   **Паттерны для автономных API**

    ***

    [:octicons-arrow-right-24: Пример для паттернов](chap07.md#leanpub-auto-case-study-for-patterns)

    [:octicons-arrow-right-24: Золотое правило](chap07.md#leanpub-auto-the-golden-rule)

    [:octicons-arrow-right-24: Паттерн: фабрика провайдеров](chap07.md#leanpub-auto-pattern-provider-factory)

    [:octicons-arrow-right-24: Паттерн: Функция](chap07.md#leanpub-auto-pattern-feature)

    [:octicons-arrow-right-24: Паттерн: Фабрика поставщиков конфигурации](chap07.md#leanpub-auto-pattern-configuration-provider-factory)

    [:octicons-arrow-right-24: Паттерн: мост NgModule Bridge](chap07.md#leanpub-auto-pattern-ngmodule-bridge)

    [:octicons-arrow-right-24: Паттерн: цепочка сервисов](chap07.md#leanpub-auto-pattern-service-chain)

    [:octicons-arrow-right-24: Паттерн: функциональный сервис](chap07.md#leanpub-auto-pattern-functional-service)

-   **Как подготовиться к автономным компонентам?**

    ***

    [:octicons-arrow-right-24: Вариант 1: страусиная стратегия](chap08.md#leanpub-auto-option-1-ostrich-strategy)

    [:octicons-arrow-right-24: Вариант 2: просто выбросить модули Angular](chap08.md#leanpub-auto-option-2-just-throw-away-angular-modules)

    [:octicons-arrow-right-24: Вариант 2a: Автоматическая миграция на Standalone](chap08.md#leanpub-auto-option-2a-automatic-migration-to-standalone)

    [:octicons-arrow-right-24: Вариант 3: Заменить модули Angular на бочки](chap08.md#leanpub-auto-option-3-replace-angular-modules-with-barrels)

    [:octicons-arrow-right-24: Вариант 4: Рабочее пространство Nx с библиотеками и правилами линтинга](chap08.md#leanpub-auto-option-4-nx-workspace-with-libraries-and-linting-rules)

    [:octicons-arrow-right-24: Вариант 4a: Границы модулей на основе папок с шерифом](chap08.md#leanpub-auto-option-4a-folder-based-module-boundaries-with-sheriff)

-   **Миграция на автономные компоненты**

    ***

    [:octicons-arrow-right-24: Первый взгляд на приложение для миграции](chap09.md#leanpub-auto-a-first-look-at-the-application-to-migrate)

    [:octicons-arrow-right-24: Шаг 1](chap09.md#leanpub-auto-step-1)

    [:octicons-arrow-right-24: Шаг 2](chap09.md#leanpub-auto-step-2)

    [:octicons-arrow-right-24: Шаг 3](chap09.md#leanpub-auto-step-3)

    [:octicons-arrow-right-24: Бонус: переход на автономные API](chap09.md#leanpub-auto-bonus-moving-to-standalone-apis)

-   **Сигналы в Angular**

    ***

    [:octicons-arrow-right-24: Обнаружение изменений сегодня: Zone.js](chap10.md#leanpub-auto-change-detection-today-zonejs)

    [:octicons-arrow-right-24: Обнаружение изменений завтра: сигналы](chap10.md#leanpub-auto-change-detection-tomorrow-signals)

    [:octicons-arrow-right-24: Использование сигналов](chap10.md#leanpub-auto-using-signals)

    [:octicons-arrow-right-24: Обновление сигналов](chap10.md#leanpub-auto-updating-signals)

    [:octicons-arrow-right-24: Сигналы должны быть неизменяемыми](chap10.md#leanpub-auto-signals-need-to-be-immutable)

    [:octicons-arrow-right-24: Вычисленные значения, побочные эффекты и утверждения](chap10.md#leanpub-auto-calculated-values-side-effects-and-assertions)

    [:octicons-arrow-right-24: Эффектам нужен контекст инъекции](chap10.md#leanpub-auto-effects-need-an-injection-context)

    [:octicons-arrow-right-24: Запись сигналов в эффектах](chap10.md#leanpub-auto-writing-signals-in-effects)

    [:octicons-arrow-right-24: Сигналы и обнаружение изменений](chap10.md#leanpub-auto-signals-and-change-detection)

    [:octicons-arrow-right-24: RxJS Interop](chap10.md#leanpub-auto-rxjs-interop)

    [:octicons-arrow-right-24: NGRX и другие хранилища?](chap10.md#leanpub-auto-ngrx-and-other-stores)

-   **Связь компонентов с сигналами**

    ***

    [:octicons-arrow-right-24: Входные сигналы](chap11.md#leanpub-auto-input-signals)

    [:octicons-arrow-right-24: Двустороннее связывание данных с сигналами модели](chap11.md#leanpub-auto-two-way-data-binding-with-model-signals)

    [:octicons-arrow-right-24: Контентные запросы с сигналами](chap11.md#leanpub-auto-content-queries-with-signals)

    [:octicons-arrow-right-24: Выходной API](chap11.md#leanpub-auto-output-api)

    [:octicons-arrow-right-24: Просмотр запросов с сигналами](chap11.md#leanpub-auto-view-queries-with-signals)

    [:octicons-arrow-right-24: Запросы и ViewContainerRef](chap11.md#leanpub-auto-queries-and-viewcontainerref)

    [:octicons-arrow-right-24: Паритет характеристик между контентом и запросами вида](chap11.md#leanpub-auto-feature-parity-between-content-and-view-queries)

-   **Эффективное использование сигналов**

    ***

    [:octicons-arrow-right-24: Начальный пример с некоторыми возможностями для улучшения](chap12.md#leanpub-auto-initial-example-with-some-room-for-improvement)

    [:octicons-arrow-right-24: Правило 1: Выводить состояние синхронно везде, где это возможно](chap12.md#leanpub-auto-rule-1-derive-state-synchronously-wherever-possible)

    [:octicons-arrow-right-24: Правило 2: избегать эффектов для распространения состояния](chap12.md#leanpub-auto-rule-2-avoid-effects-for-propagating-state)

    [:octicons-arrow-right-24: Правило 3: Хранилища упрощают реактивный поток данных](chap12.md#leanpub-auto-rule-3-stores-simplify-reactive-data-flow)

-   **Встроенный поток управления и откладываемые представления**

    ***

    [:octicons-arrow-right-24: Новый синтаксис для потока управления в шаблонах](chap13.md#leanpub-auto-new-syntax-for-control-flow-in-templates)

    [:octicons-arrow-right-24: Автоматическая миграция на встроенный поток управления](chap13.md#leanpub-auto-automatic-migration-to-build-in-control-flow)

    [:octicons-arrow-right-24: Отложенная загрузка](chap13.md#leanpub-auto-delayed-loading)

-   **esbuild и новый конструктор приложений**

    ***

    [:octicons-arrow-right-24: Производительность сборки с esbuild](chap14.md#leanpub-auto-build-performance-with-esbuild)

    [:octicons-arrow-right-24: SSR без усилий с новым конструктором приложений](chap14.md#leanpub-auto-ssr-without-effort-with-the-new-application-builder)

    [:octicons-arrow-right-24: Больше, чем SSR: неразрушающая гидратация](chap14.md#leanpub-auto-more-than-ssr-non-destructive-hydration)

    [:octicons-arrow-right-24: Больше деталей о гидратации в Angular](chap14.md#leanpub-auto-more-details-on-hydration-in-angular)

</div>

<small>:material-information-outline: Источник &mdash; [Modern Angular, Manfred Steyer](https://www.angulararchitects.io/en/ebooks/modern-angular/)</small>

!!!danger "Перевод"

    Перевод этой книги сделан благодаря [подписчикам на Бусти](https://boosty.to/bndby).
