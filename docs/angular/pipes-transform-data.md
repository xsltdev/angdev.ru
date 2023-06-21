# Transforming data with parameters and chained pipes

Use optional parameters to fine-tune a pipe's output.
For example, use the [`CurrencyPipe`](api/common/CurrencyPipe 'API reference') with a country code such as EUR as a parameter.
The template expression `{{ amount | currency:'EUR' }}` transforms the `amount` to currency in euros.
Follow the pipe name (`currency`) with a colon (`:`) and the parameter value (`'EUR'`).

# Преобразование данных с помощью параметров и цепочки труб

Используйте дополнительные параметры для точной настройки вывода трубы. Например, используйте [`CurrencyPipe`](api/common/CurrencyPipe 'API reference') с кодом страны, например EUR, в качестве параметра.

Шаблонное выражение `{{ amount | currency:'EUR' }}` преобразует `amount` в валюту в евро.

После имени трубы (`currency`) следует двоеточие (`:`) и значение параметра (`'EUR'`).

Если труба принимает несколько параметров, разделите значения двоеточиями. Например, `{{ amount | currency:'EUR':'Euros'}}` добавляет второй параметр, строковый литерал `'Euros'``, в выходную строку. В качестве параметра можно использовать любое допустимое выражение шаблона, например, строковый литерал или свойство компонента.

Некоторые трубы требуют как минимум один параметр и допускают больше необязательных параметров, например [`SlicePipe`](/api/common/SlicePipe 'API reference for SlicePipe'). Например, `{{ slice:1:5 }}` создает новый массив или строку, содержащую подмножество элементов, начиная с элемента `1` и заканчивая элементом `5`.

## Пример: Форматирование даты

Вкладки в следующем примере демонстрируют переключение между двумя различными форматами (`'shortDate'` и `'fullDate'`):

-   Шаблон `app.component.html` использует параметр формата для [`DatePipe`](api/common/DatePipe) (с именем `date`), чтобы показать дату как **04/15/88**.

-   Компонент `hero-birthday2.component.ts` привязывает параметр формата трубы к свойству `format` компонента в секции `template` и добавляет кнопку для события click, привязанную к методу `toggleFormat()` компонента.

-   Метод `toggleFormat()` компонента `hero-birthday2.component.ts` переключает свойство `format` компонента между краткой формой

(`'shortDate'`) и более длинной формой (`'fullDate'`).

<code-tabs> <code-pane header="src/app/app.component.html" region="format-birthday" path="pipes/src/app/app.component.html"></code-pane>
<code-pane header="src/app/hero-birthday2.component.ts (template)" region="template" path="pipes/src/app/hero-birthday2.component.ts"></code-pane>
<code-pane header="src/app/hero-birthday2.component.ts (class)" region="class" path="pipes/src/app/hero-birthday2.component.ts"></code-pane>
</code-tabs>

При нажатии на кнопку **Toggle Format** формат даты меняется между **04/15/1988** и **Пятница, 15 апреля 1988**.

<div class="alert is-helpful">

Параметры формата трубы `даты` см. в [DatePipe] (api/common/DatePipe "Справочная страница API DatePipe").

</div>

## Пример: Применение двух форматов с помощью цепочки труб

Соедините трубы в цепочку так, чтобы выход одной трубы стал входом для следующей.

В следующем примере цепочка труб сначала применяет формат к значению даты, а затем преобразует отформатированную дату в заглавные символы. Первая вкладка шаблона `src/app/app.component.html` связывает `DatePipe` и `UpperCasePipe` для отображения даты рождения как **APR 15, 1988**.

Вторая вкладка шаблона `src/app/app.component.html` передает параметр `fullDate` в `date` перед цепочкой в `uppercase`, что выводит **FRIDAY, APRIL 15, 1988**.

<code-tabs> <code-pane header="src/app/app.component.html (1)" region="chained-birthday" path="pipes/src/app/app.component.html"></code-pane>
<code-pane header="src/app/app.component.html (2)" region="chained-parameter-birthday" path="pipes/src/app/app.component.html"></code-pane>
</code-tabs>

@ просмотрено 2022-4-01

If the pipe accepts multiple parameters, separate the values with colons.
For example, `{{ amount | currency:'EUR':'Euros '}}` adds the second parameter, the string literal `'Euros '`, to the output string. Use any valid template expression as a parameter, such as a string literal or a component property.

Some pipes require at least one parameter and allow more optional parameters, such as [`SlicePipe`](/api/common/SlicePipe 'API reference for SlicePipe'). For example, `{{ slice:1:5 }}` creates a new array or string containing a subset of the elements starting with element `1` and ending with element `5`.

## Example: Formatting a date

The tabs in the following example demonstrates toggling between two different formats (`'shortDate'` and `'fullDate'`):

-   The `app.component.html` template uses a format parameter for the [`DatePipe`](api/common/DatePipe) (named `date`) to show the date as **04/15/88**.
-   The `hero-birthday2.component.ts` component binds the pipe's format parameter to the component's `format` property in the `template` section, and adds a button for a click event bound to the component's `toggleFormat()` method.
-   The `hero-birthday2.component.ts` component's `toggleFormat()` method toggles the component's `format` property between a short form
    (`'shortDate'`) and a longer form (`'fullDate'`).

<code-tabs>
    <code-pane header="src/app/app.component.html" region="format-birthday" path="pipes/src/app/app.component.html"></code-pane>
    <code-pane header="src/app/hero-birthday2.component.ts (template)" region="template" path="pipes/src/app/hero-birthday2.component.ts"></code-pane>
    <code-pane header="src/app/hero-birthday2.component.ts (class)" region="class" path="pipes/src/app/hero-birthday2.component.ts"></code-pane>
</code-tabs>

Clicking the **Toggle Format** button alternates the date format between **04/15/1988** and **Friday, April 15, 1988**.

<div class="alert is-helpful">

For `date` pipe format options, see [DatePipe](api/common/DatePipe 'DatePipe API Reference page').

</div>

## Example: Applying two formats by chaining pipes

Chain pipes so that the output of one pipe becomes the input to the next.

In the following example, chained pipes first apply a format to a date value, then convert the formatted date to uppercase characters.
The first tab for the `src/app/app.component.html` template chains `DatePipe` and `UpperCasePipe` to display the birthday as **APR 15, 1988**.
The second tab for the `src/app/app.component.html` template passes the `fullDate` parameter to `date` before chaining to `uppercase`, which produces **FRIDAY, APRIL 15, 1988**.

<code-tabs>
    <code-pane header="src/app/app.component.html (1)" region="chained-birthday" path="pipes/src/app/app.component.html"></code-pane>
    <code-pane header="src/app/app.component.html (2)" region="chained-parameter-birthday" path="pipes/src/app/app.component.html"></code-pane>
</code-tabs>

@reviewed 2022-4-01
