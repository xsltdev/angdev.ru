# Отображение списка выбора

В этом руководстве показано, как:

-   Развернуть приложение Tour of Heroes для отображения списка героев.

-   Позволить пользователям выбрать героя и отобразить его подробную информацию.

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, см. в <live-example></live-example>.

</div>

## Создайте героев

Первым шагом будет создание героев для отображения.

Создайте файл `mock-heroes.ts` в каталоге `src/app/`. Определите константу `HEROES` как массив из десяти героев и экспортируйте его.

Файл должен выглядеть следующим образом.

<code-example header="src/app/mock-heroes.ts" path="toh-pt2/src/app/mock-heroes.ts"></code-example>.

## Отображение героев

Откройте файл класса `HeroesComponent` и импортируйте макет `HEROES`.

<code-example header="src/app/heroes/heroes.component.ts (import HEROES)" path="toh-pt2/src/app/heroes/heroes.component.ts" region="import-heroes"></code-example>.

В классе `HeroesComponent` определите свойство компонента под названием `heroes`, чтобы открыть массив `HEROES` для привязки.

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt2/src/app/heroes/heroes.component.ts" region="component"></code-example>

### List heroes with `*ngFor`

Open the `HeroesComponent` template file and make the following changes:

1.  Add an `<h2>` at the top.

2.  Below the `<h2>`, add a `<ul>` element.

3.  In the `<ul>` element, insert an `<li>`.

4.  Place a `<button>` inside the `<li>` that displays properties of a `hero` inside `<span>` elements.

5.  Add CSS classes to style the component.

to look like this:

<code-example header="heroes.component.html (heroes template)" path="toh-pt2/src/app/heroes/heroes.component.1.html" region="list"></code-example>

That displays an error since the `hero` property doesn't exist. To have access to each individual hero and list them all, add an `*ngFor` to the `<li>` to iterate through the list of heroes:

<code-example path="toh-pt2/src/app/heroes/heroes.component.1.html" region="li"></code-example>

The [`*ngFor`](guide/built-in-directives#ngFor) is Angular's _repeater_ directive. It repeats the host element for each element in a list.

The syntax in this example is as follows:

| Syntax | Details | | :------- | :--------------------------------------------------------------------------------- |

| `<li>` | The host element. |

| `heroes` | Holds the mock heroes list from the `HeroesComponent` class, the mock heroes list. |

| `hero` | Holds the current hero object for each iteration through the list. |

<div class="alert is-important">

Не забудьте поставить звездочку `*` перед `ngFor`. Это важная часть синтаксиса.

</div>

После обновления браузера появится список героев.

<div class="callout is-helpful">

<header>Interactive elements</header>

Inside the `<li>` element, add a `<button>` element to wrap the hero's details, and then make the hero clickable. To improve accessibility, use HTML elements that are inherently interactive instead of adding an event listener to a non-interactive element. In this case, the interactive `<button>` element is used instead of adding an event to the `<li>` element.

For more details on accessibility, see [Accessibility in Angular](guide/accessibility).

</div>

<a id="styles"></a>

### Стиль героев

Список героев должен быть привлекательным и визуально реагировать, когда пользователи наводят курсор и выбирают героя из списка.

В [первом уроке] (tutorial/tour-of-heroes/toh-pt0#app-wide-styles) вы задали основные стили для всего приложения в `styles.css`. Эта таблица стилей не включала стили для этого списка героев.

Вы можете добавить больше стилей в `styles.css` и продолжать расширять эту таблицу стилей по мере добавления компонентов.

Вместо этого вы можете определить частные стили для конкретного компонента. В этом случае все, что нужно компоненту, например, код, HTML и CSS, будет собрано в одном месте.

Такой подход облегчает повторное использование компонента в других местах и обеспечивает нужный внешний вид компонента, даже если глобальные стили отличаются.

Вы определяете частные стили либо в строке в массиве `@Component.styles`, либо в виде файлов таблиц стилей, определенных в массиве `@Component.styleUrls`.

Когда `ng generate` создал `HeroesComponent`, он создал пустую таблицу стилей `heroes.component.css` для `HeroesComponent` и указал на нее в `@Component.styleUrls` следующим образом.

<code-example header="src/app/heroes/heroes.component.ts (@Component)" path="toh-pt2/src/app/heroes/heroes.component.ts" region="metadata"></code-example>.

Откройте файл `heroes.component.css` и вставьте частные CSS стили для `HeroesComponent` из [финального обзора кода](#final-code-review).

<div class="alert is-important">

Стили и таблицы стилей, определенные в метаданных `@Component`, привязаны к конкретному компоненту. Стили `heroes.component.css` применяются только к `HeroesComponent` и не влияют на внешний HTML или HTML в любом другом компоненте.

</div>

## Viewing details

When the user clicks a hero in the list, the component should display the selected hero's details at the bottom of the page.

The code in this section listens for the hero item click event and display/update the hero details.

### Add a click event binding

Add a click event binding to the `<button>` in the `<li>` like this:

<code-example header="heroes.component.html (template excerpt)" path="toh-pt2/src/app/heroes/heroes.component.1.html" region="selectedHero-click"></code-example>

This is an example of Angular's [event binding](guide/event-binding) syntax.

The parentheses around `click` tell Angular to listen for the `<button>` element's `click` event. When the user clicks in the `<button>`, Angular executes the `onSelect(hero)` expression.

In the next section, define an `onSelect()` method in `HeroesComponent` to display the hero that was defined in the `*ngFor` expression.

### Add the click event handler

Rename the component's `hero` property to `selectedHero` but don't assign any value to it since there is no _selected hero_ when the application starts.

Add the following `onSelect()` method, which assigns the clicked hero from the template to the component's `selectedHero`.

<code-example header="src/app/heroes/heroes.component.ts (onSelect)" path="toh-pt2/src/app/heroes/heroes.component.ts" region="on-select"></code-example>.

### Добавьте раздел подробностей

В настоящее время у вас есть список в шаблоне компонента. Чтобы показать подробную информацию о герое, когда вы нажимаете на его имя в списке, добавьте секцию

в шаблон, который отображает подробную информацию о герое.

Добавьте следующее в `heroes.component.html` под секцией списка:

<code-example header="heroes.component.html (selected hero details)" path="toh-pt2/src/app/heroes/heroes.component.html" region="selectedHero-details"></code-example>

The hero details should only be displayed when a hero is selected. When a component is created initially, there is no selected hero. Add the `*ngIf` directive to the `<div>` that wraps the hero details. This directive tells Angular to render the section only when the `selectedHero` is defined after it has been selected by clicking on a hero.

<div class="alert is-important">

Не забывайте о символе звездочки `*` перед `ngIf`. Это критически важная часть синтаксиса.

</div>

### Style the selected hero

To help identify the selected hero, you can use the `.selected` CSS class in the [styles you added earlier](#styles). To apply the `.selected` class to the `<li>` when the user clicks it, use class binding.

<div class="lightbox">

<img alt="Selected hero with dark background and light text that differentiates it from unselected list items" src="generated/images/guide/toh/heroes-list-selected.png">

</div>

Angular's [class binding](guide/class-binding) can add and remove a CSS class conditionally. Add `[class.some-css-class]="some-condition"` to the element you want to style.

Add the following `[class.selected]` binding to the `<button>` in the `HeroesComponent` template:

<code-example header="heroes.component.html (toggle the 'selected' CSS class)" path="toh-pt2/src/app/heroes/heroes.component.1.html" region="class-selected"></code-example>

When the current row hero is the same as the `selectedHero`, Angular adds the `selected` CSS class. When the two heroes are different, Angular removes the class.

The finished `<li>` looks like this:

<code-example header="heroes.component.html (герой элемента списка)" path="toh-pt2/src/app/heroes/heroes.component.html" region="li"></code-example>.

<a id="final-code-review"></a>

## Окончательный обзор кода

Здесь находятся файлы кода, обсуждаемые на этой странице, включая стили `HeroesComponent`.

<code-tabs> <code-pane header="src/app/mock-heroes.ts" path="toh-pt2/src/app/mock-heroes.ts"></code-pane>
<code-pane header="src/app/heroes/heroes.component.ts" path="toh-pt2/src/app/heroes/heroes.component.ts"></code-pane>
<code-pane header="src/app/heroes/heroes.component.html" path="toh-pt2/src/app/heroes/heroes.component.html"></code-pane>
<code-pane header="src/app/heroes/heroes.component.css" path="toh-pt2/src/app/heroes/heroes.component.css"></code-pane>
</code-tabs>

## Резюме

-   Приложение Tour of Heroes отображает список героев с подробным представлением.

-   Пользователь может выбрать героя и просмотреть его подробную информацию.

-   Вы использовали `*ngFor` для отображения списка.

-   Вы использовали `*ngIf` для условного включения или исключения блока HTML.

-   Вы можете переключить класс стиля CSS с помощью привязки `class`.

:date: 23.05.2022
