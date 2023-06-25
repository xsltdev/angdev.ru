<a id="attribute-directive"></a>

# Тестирование директив атрибутов

Директива _атрибута_ изменяет поведение элемента, компонента или другой директивы. Ее название отражает способ применения директивы: в качестве атрибута на главном элементе.

<div class="alert is-helpful">

Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, <live-example name="testing" noDownload>запустите его в браузере</live-example> или <live-example name="testing" downloadOnly>скачайте и запустите его локально</live-example>.

</div>

## Тестирование `HighlightDirective`

В примере приложения `HighlightDirective` устанавливает цвет фона элемента на основе либо связанного с данными цвета, либо цвета по умолчанию \(lightgray\). Он также устанавливает пользовательское свойство элемента \(`customProperty`\) в `true` без какой-либо причины, кроме как для того, чтобы показать, что это возможно.

<code-example header="app/shared/highlight.directive.ts" path="testing/src/app/shared/highlight.directive.ts"></code-example>.

Она используется во всем приложении, возможно, наиболее просто в `AboutComponent`:

<code-example header="app/about/about.component.ts" path="testing/src/app/about/about.component.ts"></code-example>.

Тестирование конкретного использования `HighlightDirective` в `AboutComponent` требует только техник, рассмотренных в разделе ["Тесты вложенных компонентов"](guide/testing-components-scenarios#nested-component-tests) раздела [Сценарии тестирования компонентов](guide/testing-components-scenarios).

<code-example header="app/about/about.component.spec.ts" path="testing/src/app/about/about/about.component.spec.ts" region="tests"></code-example>.

Однако тестирование одного варианта использования вряд ли позволит изучить весь спектр возможностей директивы. Поиск и тестирование всех компонентов, использующих директиву, утомителен, сложен и почти так же маловероятен для полного охвата.

Тесты _только для классов_ могут быть полезны, но директивы атрибутов, подобные этой, обычно манипулируют DOM. Изолированные модульные тесты не касаются DOM и, следовательно, не внушают уверенности в эффективности директивы.

Лучшим решением будет создание искусственного тестового компонента, который демонстрирует все способы применения директивы.

<code-example header="app/shared/highlight.directive.spec.ts (TestComponent)" path="testing/src/app/shared/highlight.directive.spec.ts" region="test-component"></code-example>.

<div class="lightbox">

<img alt="HighlightDirective spec in action" src="generated/images/guide/testing/highlight-directive-spec.png">

</div>

<div class="alert is-helpful">

Случай `<input>` связывает директиву `HighlightDirective` с именем значения цвета в поле ввода. Начальным значением является слово "cyan", которое должно быть фоновым цветом поля ввода.

</div>

Вот несколько тестов этого компонента:

<code-example header="app/shared/highlight.directive.spec.ts (selected tests)" path="testing/src/app/shared/highlight.directive.spec.ts" region="selected-tests"></code-example>.

Несколько приемов заслуживают внимания:

-   Предикат `By.directive` - отличный способ получить элементы, имеющие эту директиву, когда типы их элементов неизвестны.

-   Псевдокласс [`:not`](https://developer.mozilla.org/docs/Web/CSS/:not) в `By.css('h2:not([highlight])')` помогает найти `<h2>` элементы, которые _не_ имеют директивы.

    `By.css('*:not([highlight])')` находит _любой_ элемент, у которого нет директивы.

-   `DebugElement.styles` позволяет получить доступ к стилям элементов даже в отсутствие реального браузера, благодаря абстракции `DebugElement`.

    Но не стесняйтесь использовать `nativeElement`, если это кажется проще или понятнее, чем абстракция.

-   Angular добавляет директиву в инжектор элемента, к которому она применяется.

    Тест на цвет по умолчанию использует инжектор второго `<h2>` для получения его экземпляра `HighlightDirective` и его `defaultColor`.

-   `DebugElement.properties` предоставляет доступ к искусственному пользовательскому свойству, которое задается директивой

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
