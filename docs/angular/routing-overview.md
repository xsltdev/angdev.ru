# Angular Routing

:date: 28.02.2022

В одностраничном приложении вы изменяете то, что видит пользователь, показывая или скрывая части экрана, соответствующие определенным компонентам, вместо того, чтобы обращаться к серверу для получения новой страницы. Когда пользователи выполняют задачи приложения, им необходимо перемещаться между различными [представлениями](glossary.md#view 'Definition of view'), которые вы определили.

Для навигации от одного [представления](glossary.md#view) к другому используется Angular **`Router`**. Маршрутизатор **`Router`** обеспечивает навигацию, интерпретируя URL-адрес браузера как инструкцию по смене представления.

Чтобы изучить пример приложения, демонстрирующий основные возможности маршрутизатора, смотрите [код](https://angular.io/generated/live-examples/router/stackblitz.html).

## Предварительные условия

Перед созданием маршрута вы должны быть знакомы со следующим:

-   [Основы компонентов](architecture-components.md)
-   [Основы шаблонов](glossary.md#template)

-   Приложение Angular &mdash; вы можете создать базовое приложение Angular, используя [Angular CLI](https://angular.io/cli.md).

## Узнайте о маршрутизации Angular

[Общие задачи маршрутизации](router.md)
: Узнайте, как реализовать многие общие задачи, связанные с маршрутизацией в Angular.

[Учебник по маршрутизации SPA](router-tutorial.md)
: Учебное пособие, в котором рассматриваются паттерны, связанные с маршрутизацией в Angular.

[Маршрутизация Тур по Героям](router-tutorial-toh.md)
: Добавьте дополнительные возможности маршрутизации в учебник Tour of Heroes.

[Учебник по выбору маршрутных матчей](routing-with-urlmatcher.md)
: Учебное пособие, в котором рассказывается о том, как использовать шаблоны пользовательских стратегий согласования в Angular routing.

[Справочник по маршрутизаторам](router-reference.md)
: Описывает некоторые основные концепции API маршрутизатора.
