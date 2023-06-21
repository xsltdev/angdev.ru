# Понимание шаблонов

В Angular шаблон - это чертеж фрагмента пользовательского интерфейса (UI). Шаблоны пишутся на HTML, и в шаблоне можно использовать специальный синтаксис, чтобы использовать многие возможности Angular.

## Предварительные условия

Прежде чем изучать синтаксис шаблонов, вы должны быть знакомы со следующим:

-   [Концепции Angular] (руководство/архитектура)

-   JavaScript

-   HTML

-   CSS

## Расширение HTML

Angular расширяет синтаксис HTML в ваших шаблонах с помощью дополнительных функций. Например, синтаксис привязки данных Angular помогает динамически устанавливать свойства Document Object Model (DOM).

Почти весь синтаксис HTML является допустимым синтаксисом шаблона. Однако, поскольку шаблон Angular - это только фрагмент пользовательского интерфейса, он не включает такие элементы, как `<html>`, `<body>` или `<base>`.

<div class="alert is-important">

Чтобы исключить риск атак внедрения сценариев, Angular не поддерживает элемент `<script>` в шаблонах. Angular игнорирует тег `<script>` и выводит предупреждение в консоль браузера. Для получения дополнительной информации см. страницу [Security](guide/security).

</div>

## Подробнее о синтаксисе шаблонов

Возможно, вас также заинтересует следующее:

<div class="card-container">     <a href="guide/interpolation" class="docs-card" title="Interpolation">
        <section>Interpolation</section>
        <p>Learn how to use interpolation and expressions in HTML.</p>
        <p class="card-footer">Interpolation</p>
    </a>
    <a href="guide/property-binding" class="docs-card" title="Property binding">
        <section>Property binding</section>
        <p>Set properties of target elements or directive @Input() decorators.</p>
        <p class="card-footer">Property binding</p>
    </a>
    <a href="guide/attribute-binding" class="docs-card" title="Attribute binding">
        <section>Attribute binding</section>
        <p>Set the value of attributes.</p>
        <p class="card-footer">Attribute binding</p>
    </a>
    <a href="guide/class-binding" class="docs-card" title="Class and style binding">
        <section>Class and style binding</section>
        <p>Set the value of class and style.</p>
        <p class="card-footer">Class and style binding</p>
    </a>
    <a href="guide/event-binding" class="docs-card" title="Event binding">
        <section>Event binding</section>
        <p>Listen for events and your HTML.</p>
        <p class="card-footer">Event binding</p>
    </a>
    <a href="guide/template-reference-variables" class="docs-card" title="Template reference variables">
        <section>Template reference variables</section>
        <p>Use special variables to reference a DOM element within a template.</p>
        <p class="card-footer">Template reference variables</p>
    </a>
    <a href="guide/built-in-directives" class="docs-card" title="Built-in directives">
        <section>Built-in directives</section>
        <p>Listen to and modify the behavior and layout of HTML.</p>
        <p class="card-footer">Built-in directives</p>
    </a>
    <a href="guide/inputs-outputs" class="docs-card" title="Inputs and Outputs">
        <section>Inputs and Outputs</section>
        <p>Share data between the parent context and child directives or components.</p>
        <p class="card-footer">Inputs and Outputs</p>
    </a>
</div>

@ просмотрено 2022-05-11
