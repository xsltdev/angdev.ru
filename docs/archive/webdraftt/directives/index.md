# Директивы

**Директивы** определяют набор инструкций, которые применяются при рендеринге html-кода. Директива представляет класс с директивными метаданными. В TypeScript для прикрепления метаданных к классу применяется декоратор `@Directive`.

В Angular есть три типа директив:

-   **Компоненты**: компонент по сути также является директивой, а декоратор `@Component` расширяет возможности декоратора `@Directive` с помощью добавления функционала по работе с шаблонами.
-   **Атрибутивные**: они изменяют поведение уже существующего элемента, к которому они применяются. Например, `ngModel`, `ngStyle`, `ngClass`
-   **Структурные**: они изменяют структуру DOM с помощью добавления, изменения или удаления элементов hmtl. Например, это директивы `ngFor` и `ngIf`

-   [ngClass и ngStyle](ngclass-ngstyle.md)
-   [Создание атрибутивных директив](attr-directive.md)
-   [Взаимодействие с пользователем, @HostListener и @HostBinding](user-interaction.md)
-   [Получение параметров в директивах](params.md)
-   [Структурные директивы ngIf, ngFor, ngSwitch](structure-directive.md)
-   [Создание структурных директив](create-structure-directive.md)
