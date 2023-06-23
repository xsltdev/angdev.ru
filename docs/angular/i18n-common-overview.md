# Общие задачи интернационализации

Используйте следующие задачи Angular для интернационализации вашего проекта.

-   Используйте встроенные трубы для отображения дат, чисел, процентов и валют в местном формате.

-   Пометить текст в шаблонах компонентов для перевода.

-   Пометить множественные формы выражений для перевода.

-   Пометить альтернативный текст для перевода.

После подготовки проекта для международной аудитории используйте [Angular CLI][aioclimain] для локализации проекта. Выполните следующие задачи для локализации проекта.

-   С помощью CLI извлеките отмеченный текст в файл _исходного языка_.

-   Сделайте копию файла _исходного языка_ для каждого языка и отправьте все файлы _перевода_ переводчику или службе.

-   Используйте CLI для объединения готовых файлов перевода при сборке проекта для одной или нескольких локалей.

<div class="alert is-helpful">

Создайте адаптируемый пользовательский интерфейс для всех целевых локализаций, учитывающий различия в интервалах для разных языков. Более подробную информацию см. в разделе [Как подойти к интернационализации][thinkwithgooglemarketfinderintlenusguidehowtoapproachi18noverview].

</div>

## Предварительные условия

Чтобы подготовить ваш проект к переводу, вы должны иметь базовое представление о следующих темах.

-   [Шаблоны][aioguideglossarytemplate]

-   [Компоненты][aioguideglossarycomponent]

-   [Angular CLI][aioclimain][командная строка][aioguideglossarycommandlineinterfacecli] инструмент для управления циклом разработки Angular

-   [Extensible Markup Language (XML)][w3xml] используется для файлов перевода

## Узнайте об общих задачах интернационализации Angular

<div class="card-container">
     <a href="guide/i18n-common-add-package" class="docs-card" title="Add the localize package">
        <section>Add the localize package</section>
        <p>Learn how to add the Angular Localize package to your project</p>
        <p class="card-footer">Add the localize package</p>
    </a>
    <a href="guide/i18n-common-locale-id" class="docs-card" title="Refer to locales by ID">
        <section>Refer to locales by ID</section>
        <p>Learn how to identify and specify a locale identifier for your project</p>
        <p class="card-footer">Refer to locales by ID</p>
    </a>
    <a href="guide/i18n-common-format-data-locale" class="docs-card" title="Format data based on locale">
        <section>Format data based on locale</section>
        <p>Learn how to implement localized data pipes and override the locale for your project</p>
        <p class="card-footer">Format data based on locale</p>
    </a>
    <a href="guide/i18n-common-prepare" class="docs-card" title="Prepare component for translation">
        <section>Prepare component for translation</section>
        <p>Learn how to specify source text for translation</p>
        <p class="card-footer">Prepare component for translation</p>
    </a>
    <a href="guide/i18n-common-translation-files" class="docs-card" title="Work with translation files">
        <section>Work with translation files</section>
        <p>Learn how to review and process translation text</p>
        <p class="card-footer">Work with translation files</p>
    </a>
    <a href="guide/i18n-common-merge" class="docs-card" title="Merge translations into the application">
        <section>Merge translations into the application</section>
        <p>Learn how to merge translations and build your translated application</p>
        <p class="card-footer">Merge translations into the application</p>
    </a>
    <a href="guide/i18n-common-deploy" class="docs-card" title="Deploy multiple locales">
        <section>Deploy multiple locales</section>
        <p>Learn how to deploy multiple locales for your application</p>
        <p class="card-footer">Deploy multiple locales</p>
    </a>
</div>

<!-- links -->

[aioclimain]: cli 'CLI Overview and Command Reference | Angular'
[aioguideglossarycommandlineinterfacecli]: guide/glossary#command-line-interface-cli 'command-line interface (CLI) - Glossary | Angular'
[aioguideglossarycomponent]: guide/glossary#component 'component - Glossary | Angular'
[aioguideglossarytemplate]: guide/glossary#template 'template - Glossary | Angular'

<!-- external links -->

[thinkwithgooglemarketfinderintlenusguidehowtoapproachi18noverview]: https://marketfinder.thinkwithgoogle.com/intl/en_us/guide/how-to-approach-i18n#overview 'Overview - How to approach internationalization | Market Finder | Think with Google'
[w3xml]: https://www.w3.org/XML 'Extensible Markup Language (XML) | W3C'

<!-- end links -->

:date: 7.10.2021
