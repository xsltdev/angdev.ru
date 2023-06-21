# SVG как шаблоны

Вы можете использовать файлы SVG в качестве шаблонов в своих приложениях Angular. Когда вы используете SVG в качестве шаблона, вы можете использовать директивы и привязки так же, как и в шаблонах HTML.

Используйте эти возможности для динамической генерации интерактивной графики.

<div class="alert is-helpful">

Смотрите <live-example name="template-syntax"></live-example> для рабочего примера, содержащего фрагменты кода из этого руководства.

</div>

## Пример синтаксиса SVG

В следующем примере показан синтаксис для использования SVG в качестве шаблона.

<code-example header="src/app/svg.component.ts" path="template-syntax/src/app/svg.component.ts"></code-example>.

Чтобы увидеть привязку свойств и событий в действии, добавьте следующий код в файл `svg.component.svg`:

<code-example header="src/app/svg.component.svg" path="template-syntax/src/app/svg.component.svg"></code-example>.

В приведенном примере используется привязка события `click()` и синтаксис привязки свойства \(`[attr.fill]="fillColor"`\).

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
