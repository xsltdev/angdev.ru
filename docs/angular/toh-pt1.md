# Редактор героев

Теперь у приложения есть базовый заголовок. Далее создайте новый компонент для отображения информации о герое и поместите этот компонент в оболочку приложения.

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, см. в <live-example></live-example>.

</div>

## Создание компонента heroes

Используйте `ng generate` для создания нового компонента с именем `heroes`.

<code-example format="shell" language="shell">

ng generate component heroes

</code-example>

`ng generate` создает новый каталог `src/app/heroes/` и генерирует три файла `HeroesComponent` вместе с тестовым файлом.

Файл класса `HeroesComponent` выглядит следующим образом:

<code-example header="app/heroes/heroes.component.ts (initial version)" path="toh-pt1/src/app/heroes/heroes.component.ts" region="v1"></code-example

Вы всегда импортируете символ `Component` из библиотеки ядра Angular и аннотируете класс компонента с помощью `@Component`.

`@Component` - это функция-декоратор, которая определяет метаданные Angular для компонента.

Функция `ng generate` создала три свойства метаданных:

| Properties | Details | | :------------ | :-------------------------------------------------- |.

| `selector` | Селектор CSS элементов компонента. |

| | `templateUrl` | Расположение файла шаблона компонента. |

| | `styleUrls` | Расположение частных стилей CSS компонента. |

<a id="selector"></a>

Селектор [CSS элемента](https://developer.mozilla.org/docs/Web/CSS/Type_selectors), `'app-heroes'`, соответствует имени HTML элемента, который идентифицирует этот компонент в шаблоне родительского компонента.

Всегда `экспортируйте` класс компонента, чтобы вы могли `импортировать` его в другое место &hellip; например, в `AppModule`.

### Добавить свойство `герой`

Добавьте свойство `hero` в `HeroesComponent` для героя по имени `Windstorm`.

<code-example header="heroes.component.ts (свойство героя)" path="toh-pt1/src/app/heroes/heroes.component.ts" region="add-hero"></code-example>.

### Показать героя

Откройте файл шаблона `heroes.component.html`. Удалите текст по умолчанию, созданный `ng generate`, и замените его привязкой данных к новому свойству `hero`.

<code-example header="heroes.component.html" path="toh-pt1/src/app/heroes/heroes.component.1.html" region="show-hero-1"></code-example>.

## Показать представление `HeroesComponent`

Чтобы отобразить `HeroesComponent`, вы должны добавить его в шаблон оболочки `AppComponent`.

Помните, что `app-heroes` является [селектором элемента](#selector) для `HeroesComponent`. Добавьте элемент `<app-heroes>` в файл шаблона `AppComponent`, чуть ниже заголовка.

<code-example header="src/app/app.component.html" path="toh-pt1/src/app/app/app.component.html"></code-example>.

Если `ng serve` все еще запущен, браузер должен обновиться и отобразить заголовок приложения и имя героя.

## Создание интерфейса `героя

Настоящий герой - это больше, чем имя.

Создайте интерфейс `Hero` в собственном файле в каталоге `src/app`. Дайте ему свойства `id` и `name`.

<code-example path="toh-pt1/src/app/hero.ts" header="src/app/hero.ts"></code-example>.

Вернитесь к классу `HeroesComponent` и импортируйте интерфейс `Hero`.

Переделайте свойство `hero` компонента так, чтобы оно имело тип `Hero`. Инициализируйте его с `id` равным `1` и именем `Windstorm`.

Измененный файл класса `HeroesComponent` должен выглядеть следующим образом:

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt1/src/app/heroes/heroes.component.ts"></code-example>.

Страница больше не отображается должным образом, потому что вы изменили героя со строки на объект.

## Показать объект героя

Обновите привязку в шаблоне, чтобы объявить имя героя и показать и `id`, и `name` в подробном отображении, как показано ниже:

<code-example header="heroes.component.html (шаблон HeroesComponent)" path="toh-pt1/src/app/heroes/heroes.component.1.html" region="show-hero-2"></code-example>.

Браузер обновляется и отображает информацию о герое.

## Форматирование с помощью `UppercasePipe`

Отредактируйте привязку `hero.name` следующим образом:

<code-example header="src/app/heroes/heroes.component.html" path="toh-pt1/src/app/heroes/heroes.component.html" region="pipe"></code-example>

The browser refreshes and now the hero's name is displayed in capital letters.

The word `uppercase` in the interpolation binding after the pipe <code>&verbar;</code> character, activates the built-in `UppercasePipe`.

[Pipes](guide/pipes) are a good way to format strings, currency amounts, dates, and other display data. Angular ships with several built-in pipes and you can create your own.

## Edit the hero

Users should be able to edit the hero's name in an `<input>` text box.

The text box should both _display_ the hero's `name` property and _update_ that property as the user types. That means data flows from the component class _out to the screen_ and from the screen _back to the class_.

To automate that data flow, set up a two-way data binding between the `<input>` form element and the `hero.name` property.

### Two-way binding

Refactor the details area in the `HeroesComponent` template so it looks like this:

<code-example header="src/app/heroes/heroes.component.html (шаблон HeroesComponent)" path="toh-pt1/src/app/heroes/heroes.component.1.html" region="name-input"></code-example>.

`[(ngModel)]` - это синтаксис двустороннего связывания данных Angular.

Здесь он связывает свойство `hero.name` с текстовым полем HTML, чтобы данные могли поступать _в обоих направлениях_. Данные могут поступать из свойства `hero.name` в текстовое поле и из текстового поля обратно в `hero.name`.

### Отсутствующий `FormsModule`.

Обратите внимание, что приложение перестало работать, когда вы добавили `[(ngModel)]`.

Чтобы увидеть ошибку, откройте средства разработки браузера и найдите в консоли сообщение вида

<code-example format="output" hideCopy language="shell">

Ошибки разбора шаблона: Невозможно привязать к 'ngModel', так как это неизвестное свойство 'input'.

</code-example>

Хотя `ngModel` является действительной директивой Angular, она не доступна по умолчанию.

Она относится к дополнительному модулю `FormsModule`, и вы должны _оптировать_ ее использование.

## `AppModule`

Angular необходимо знать, как части вашего приложения сочетаются друг с другом и какие другие файлы и библиотеки требуются приложению. Эта информация называется _метаданные_.

Часть метаданных находится в декораторах `@Component`, которые вы добавили в классы компонентов. Другие важные метаданные находятся в декораторах [`@NgModule`](guide/ngmodules).

Самый важный декоратор `@NgModule` аннотирует класс верхнего уровня **AppModule**.

При создании проекта `ng new` создал класс `AppModule` в `src/app/app.module.ts`. Именно здесь вы _входите_ в `FormsModule`.

### Импортируйте `FormsModule`.

Откройте `app.module.ts` и импортируйте символ `FormsModule` из библиотеки `@angular/forms`.

<code-example path="toh-pt1/src/app/app.module.ts" header="app.module.ts (импорт символа FormsModule)" region="formsmodule-js-import"></code-example>.

Добавьте `FormsModule` в массив `imports` в `@NgModule`. Массив `imports` содержит список внешних модулей, которые необходимы приложению.

<code-example header="app.module.ts (@NgModule imports)" path="toh-pt1/src/app/app.module.ts" region="ng-imports"></code-example>.

Когда браузер обновится, приложение должно снова работать. Вы можете отредактировать имя героя и увидеть изменения, отраженные сразу же в `<h2>` над текстовым полем.

### Объявление `HeroesComponent`.

Каждый компонент должен быть объявлен в _только одном_ [NgModule](guide/ngmodules).

Вы не объявили `HeroesComponent`. Почему приложение сработало?

Оно заработало, потому что `ng generate` объявил `HeroesComponent` в `AppModule`, когда создавал этот компонент.

Откройте `src/app/app.module.ts` и найдите импортированный `HeroesComponent` в самом верху.

<code-example path="toh-pt1/src/app/app.module.ts" header="src/app/app.module.ts" region="heroes-import"></code-example>.

Компонент `HeroesComponent` объявлен в массиве `@NgModule.declarations`.

<code-example header="src/app/app.module.ts" path="toh-pt1/src/app/app/app.module.ts" region="declarations"></code-example>

<div class="alert is-helpful">

`AppModule` объявляет оба компонента приложения, `AppComponent` и `HeroesComponent`.

</div>

## Окончательный обзор кода

Вот файлы кода, обсуждаемые на этой странице.

<code-tabs> <code-pane header="src/app/heroes/heroes.component.ts" path="toh-pt1/src/app/heroes/heroes.component.ts"></code-pane>
<code-pane header="src/app/heroes/heroes.component.html" path="toh-pt1/src/app/heroes/heroes.component.html"></code-pane>
<code-pane header="src/app/app.module.ts" path="toh-pt1/src/app/app.module.ts"></code-pane>
<code-pane header="src/app/app.component.ts" path="toh-pt1/src/app/app.component.ts"></code-pane>
<code-pane header="src/app/app.component.html" path="toh-pt1/src/app/app.component.html"></code-pane>
<code-pane header="src/app/hero.ts" path="toh-pt1/src/app/hero.ts"></code-pane>
</code-tabs>

## Резюме

-   Вы использовали `ng generate` для создания второго `HeroesComponent`.

-   Вы отобразили `HeroesComponent`, добавив его в оболочку `AppComponent`.

-   Вы применили `UppercasePipe` для форматирования имени.

-   Вы использовали двустороннее связывание данных с помощью директивы `ngModel`.

-   Вы узнали о модуле `AppModule`.

-   Вы импортировали `FormsModule` в `AppModule`, чтобы Angular распознал и применил директиву `ngModel`.

-   Вы узнали о важности объявления компонентов в `AppModule`.

:date: 28.02.2022
