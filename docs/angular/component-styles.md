# Стили компонентов

Стилизация приложений Angular осуществляется с помощью стандартного CSS. Это означает, что вы можете применять все, что знаете о таблицах стилей CSS, селекторах, правилах и медиа-запросах непосредственно в приложениях Angular.

Кроме того, Angular может объединять _компонентные стили_ с компонентами, обеспечивая более модульную конструкцию, чем обычные таблицы стилей.

На этой странице описано, как загрузить и применить эти компонентные стили.

Запустите [пример](https://angular.io/generated/live-examples/component-styles/stackblitz.html) в Stackblitz и загрузите оттуда код.

## Использование стилей компонентов

Для каждого написанного вами компонента Angular вы можете определить не только HTML-шаблон, но и CSS-стили, которые будут сочетаться с этим шаблоном, указывая любые селекторы, правила и медиа-запросы, которые вам необходимы.

Один из способов сделать это — установить свойство `styles` в метаданных компонента. Свойство `styles` принимает массив строк, содержащих код CSS.

Обычно вы задаете одну строку, как в следующем примере:

```ts title=""
@Component({
    selector: 'app-root',
    template: `
        <h1>Tour of Heroes</h1>
        <app-hero-main [hero]="hero"></app-hero-main>
    `,
    styles: ['h1 { font-weight: normal; }'],
})
export class HeroAppComponent {
    /* . . . */
}
```

## Лучшие практики стилизации компонентов

!!!note ""

    Информацию о том, как Angular привязывает стили к конкретным компонентам, смотрите в [View Encapsulation](view-encapsulation.md).

Стили компонента следует рассматривать как частные детали реализации этого компонента. При использовании общего компонента вы не должны переопределять стили компонента так же, как не должны обращаться к закрытым членам класса TypeScript.

Хотя стандартная инкапсуляция стилей Angular не позволяет стилям компонентов влиять на другие компоненты, глобальные стили влияют на все компоненты на странице.

Сюда входит `::ng-deep`, который повышает стиль компонента до глобального стиля.

### Авторизация компонента для поддержки настройки

Как автор компонента, вы можете явно спроектировать компонент для поддержки настройки одним из четырех различных способов.

**1. Использовать пользовательские свойства CSS (рекомендуется)**

Вы можете определить поддерживаемый API настройки для вашего компонента, определив его стили с помощью CSS Custom Properties, альтернативно известных как CSS Variables. Любой пользователь вашего компонента может использовать этот API, определяя значения для этих свойств, настраивая окончательный вид компонента на отображаемой странице.

Хотя это требует определения пользовательского свойства для каждой точки настройки, это создает четкий контракт API, который работает во всех режимах инкапсуляции стилей.

**2. Объявление глобального CSS с помощью `@mixin`**

Хотя эмулированная инкапсуляция стилей Angular предотвращает выход стилей за пределы компонента, она не предотвращает влияние глобального CSS на всю страницу. Хотя потребители компонентов должны избегать прямой перезаписи внутренних CSS компонентов, вы можете предложить поддерживаемый API настройки через препроцессор CSS, например Sass.

Например, компонент может предлагать один или несколько поддерживаемых миксинов для настройки различных аспектов внешнего вида компонента. Хотя этот подход использует глобальные стили в своей реализации, он позволяет автору компонента поддерживать миксины в актуальном состоянии с учетом изменений в частной структуре DOM компонента и CSS-классах.

**3. Настройка с помощью CSS `::part`**

Если ваш компонент использует [Shadow DOM](https://developer.mozilla.org/docs/Web/Web_Components/Using_shadow_DOM), вы можете применить атрибут `part` для указания элементов в шаблоне вашего компонента. Это позволит потребителям компонента создавать произвольные стили, нацеленные на эти конкретные элементы с помощью [псевдоэлемента `::part`](https://developer.mozilla.org/docs/Web/CSS/::part).

Хотя это позволяет вам ограничить элементы в вашем шаблоне, которые потребители могут настраивать, это не ограничивает настраиваемые свойства CSS.

**4. Предоставление API TypeScript**

Вы можете определить TypeScript API для настройки стилей, используя привязки шаблона для обновления классов и стилей CSS. Это не рекомендуется, поскольку дополнительные затраты JavaScript на этот API стилей требуют гораздо больших затрат производительности, чем CSS.

## Специальные селекторы

Компонентные стили имеют несколько специальных _селекторов_ из мира теневых DOM стилей (описанных на странице [CSS Scoping Module Level 1](https://www.w3.org/TR/css-scoping-1) на сайте [W3C](https://www.w3.org)). В следующих разделах описаны эти селекторы.

### :host

Каждый компонент ассоциируется с элементом, который соответствует селектору компонента. Этот элемент, в который выводится шаблон, называется _хост-элементом_.

Селектор псевдокласса `:host` можно использовать для создания стилей, нацеленных на сам элемент host, а не на элементы внутри него.

```ts title="src/app/host-selector-example.component.ts"
@Component({
    selector: 'app-main',
    template: `
        <h1>It Works!</h1>
        <div>Start editing to see some magic happen :)</div>
    `,
})
export class HostSelectorExampleComponent {}
```

Создание следующего стиля будет нацелено на элемент host компонента. Любое правило, примененное к этому селектору, будет влиять на главный элемент и все его потомки (в данном случае, выделение курсивом всего содержащегося текста).

```css title="src/app/hero-details.component.css"
:host {
    font-style: italic;
}
```

Селектор `:host` нацелен только на основной элемент компонента. Любые стили в блоке `:host` дочернего компонента _не_ будут влиять на родительские компоненты.

Используйте форму _функции_ для условного применения стилей хоста, включив другой селектор в круглые скобки после `:host`.

В этом примере содержимое хоста также становится жирным, когда к элементу хоста применяется CSS-класс `active`.

```css title="src/app/hero-details.component.css"
:host {
    font-style: italic;
}

:host(.active) {
    font-weight: bold;
}
```

Селектор `:host` также можно комбинировать с другими селекторами. Добавьте селекторы за `:host` для выбора дочерних элементов, например, используя `:host h2` для выбора всех элементов `<h2>` внутри представления компонента.

!!!note ""

    Вы не должны добавлять селекторы (кроме `:host-context`) перед селектором `:host` для стилизации компонента на основе внешнего контекста представления компонента. Такие селекторы не привязаны к представлению компонента и будут выбирать внешний контекст, но это не встроенное поведение.

    Вместо этого используйте селектор `:host-context`.

### :host-context

Иногда полезно применять стили к элементам в шаблоне компонента на основе некоторого условия в элементе, который является предком элемента-хоста. Например, класс темы CSS может быть применен к элементу документа `<body>`, и вы хотите изменить внешний вид вашего компонента в зависимости от этого.

Используйте селектор псевдокласса `:host-context()`, который работает так же, как и функциональная форма `:host()`. Селектор `:host-context()` ищет CSS-класс в любом предке элемента-хоста компонента, вплоть до корня документа.

Селектор `:host-context()` полезен только в сочетании с другим селектором.

В следующем примере весь текст внутри компонента выделяется курсивом, но только в том случае, если какой-то _предшественник_ элемента-хоста имеет CSS-класс `active`.

```css title="src/app/hero-details.component.css"
:host-context(.active) {
    font-style: italic;
}
```

!!!note ""

    Будет затронут только элемент-хозяин и его потомки, но не предок с назначенным классом `active`.

### (устаревшие) `/deep/`, `>>>` и `::ng-deep`.

Стили компонента обычно применяются только к HTML в собственном шаблоне компонента.

Применение псевдокласса `::ng-deep` к любому CSS-правилу полностью отключает инкапсуляцию просмотра для этого правила. Любой стиль с примененным `::ng-deep` становится глобальным стилем.

Чтобы распространить указанный стиль на текущий компонент и все его потомки, обязательно включите селектор `:host` перед `::ng-deep`.

Если комбинатор `::ng-deep` используется без селектора псевдокласса `:host`, стиль может распространиться на другие компоненты.

Следующий пример нацелен на все элементы `<h3>`, начиная с основного элемента и заканчивая этим компонентом и всеми его дочерними элементами в DOM.

```css title="src/app/hero-details.component.css"
:host ::ng-deep h3 {
    font-style: italic;
}
```

Комбинатор `/deep/` также имеет псевдонимы `>>>` и `::ng-deep`.

!!!warning ""

    Используйте `/deep/`, `>>>` и `::ng-deep` только с _эмулированной_ инкапсуляцией представления. Emulated — это стандартная и наиболее часто используемая инкапсуляция представления.

    Для получения дополнительной информации смотрите раздел [Инкапсуляция представления](view-encapsulation.md).

!!!warning ""

    Комбинатор потомков, пронизывающий тень, устарел и [его поддержка удаляется из основных браузеров](https://www.chromestatus.com/feature/6750456638341120) и инструментов. В связи с этим мы планируем отказаться от поддержки в Angular (для всех трех `/deep/`, `>>>`, и `::ng-deep`).

    До тех пор `::ng-deep` следует предпочесть для более широкой совместимости с инструментами.

## Загрузка стилей компонента

Существует несколько способов добавить стили в компонент:

-   Путем установки метаданных `styles` или `styleUrls`.
-   Встраивание в HTML шаблона
-   С помощью импорта CSS

К каждому из этих способов загрузки применимы правила описания, описанные ранее.

### Стили в метаданных компонента

Добавьте свойство массива `styles` к декоратору `@Component`.

Каждая строка в массиве определяет некоторый CSS для этого компонента.

```ts title="src/app/hero-app.component.ts (CSS inline)"
@Component({
    selector: 'app-root',
    template: `
        <h1>Tour of Heroes</h1>
        <app-hero-main [hero]="hero"></app-hero-main>
    `,
    styles: ['h1 { font-weight: normal; }'],
})
export class HeroAppComponent {
    /* . . . */
}
```

!!!danger "Напоминание"

    Эти стили применяются _только к этому компоненту_. Они _не наследуются_ ни компонентами, вложенными в шаблон, ни содержимым, проецируемым в компонент.

Команда Angular CLI `ng generate component` определяет пустой массив `styles`, когда вы создаете компонент с флагом `--inline-style`.

```shell
ng generate component hero-app --inline-style
```

### Файлы стилей в метаданных компонента

Загружайте стили из внешних CSS файлов, добавляя свойство `styleUrls` в декоратор компонента `@Component`:

=== "src/app/hero-app.component.ts (CSS in file)"

    ```ts
    @Component({
    	selector: 'app-root',
    	template: `
    		<h1>Tour of Heroes</h1>
    		<app-hero-main [hero]="hero"></app-hero-main>
    	`,
    	styleUrls: ['./hero-app.component.css'],
    })
    export class HeroAppComponent {
    	/* . . . */
    }
    ```

=== "src/app/hero-app.component.css"

    ```css
    h1 {
    	font-weight: normal;
    }
    ```

!!!danger "Напоминание"

    Стили в файле стилей применяются _только к этому компоненту_. Они _не наследуются_ ни компонентами, вложенными в шаблон, ни содержимым, проецируемым в компонент.

!!!info ""

    Вы можете указать более одного файла стилей или даже комбинацию `styles` и `styleUrls`.

Когда вы используете команду Angular CLI `ng generate component` без флага `--inline-style`, она создает для вас пустой файл стилей и ссылается на этот файл в сгенерированных `styleUrls` компонента.

```shell
ng generate component hero-app
```

### Встраиваемые стили шаблона

Встраивайте стили CSS непосредственно в HTML-шаблон, помещая их в теги `<style>`.

```ts title="src/app/hero-controls.component.ts"
@Component({
  selector: 'app-hero-controls',
  template: `
    <style>
      button {
        background-color: white;
        border: 1px solid #777;
      }
    </style>
    <h3>Controls</h3>
    <button type="button" (click)="activate()">Activate</button>
  `
})
```

### Теги ссылок шаблонов

Вы также можете вписать теги `<link>` в HTML-шаблон компонента.

```ts title=""
@Component({
  selector: 'app-hero-team',
  template: `
    <!-- We must use a relative URL so that the AOT compiler can find the stylesheet -->
    <link rel="stylesheet" href="../assets/hero-team.component.css">
    <h3>Team</h3>
    <ul>
      <li *ngFor="let member of hero.team">
        {{member}}
      </li>
    </ul>`
})
```

!!!danger ""

    При сборке с помощью CLI обязательно включите связанный файл стилей в число активов, которые будут скопированы на сервер, как описано в руководстве [Assets configuration guide](workspace-config.md#assets-configuration).

    После включения CLI включает таблицу стилей независимо от того, является ли URL-адрес href тега ссылки относительным к корню приложения или к файлу компонента.

### CSS @imports

Импортируйте файлы CSS в файлы CSS, используя стандартное правило CSS `@import`. Подробности смотрите в [`@import`](https://developer.mozilla.org/en/docs/Web/CSS/@import) на сайте [MDN](https://developer.mozilla.org).

В этом случае URL является относительным к файлу CSS, в который вы импортируете.

```css title="src/app/hero-details.component.css (excerpt)"
/* The AOT compiler needs the `./` to show that this is local */
@import './hero-details-box.css';
```

### Внешние и глобальные файлы стилей

При сборке с помощью CLI, вы должны настроить `angular.json` на включение _всех внешних активов_, включая внешние файлы стилей.

Зарегистрируйте **глобальные** файлы стилей в секции `styles`, которая по умолчанию предварительно сконфигурирована с глобальным файлом `styles.css`.

См. руководство [Конфигурация стилей](workspace-config.md#styles-and-scripts-configuration), чтобы узнать больше.

### Файлы стилей, не относящиеся к CSS

Если вы собираете с помощью CLI, вы можете записать файлы стилей в [sass](https://sass-lang.com) или [less](https://lesscss.org), и указать эти файлы в метаданных `@Component.styleUrls` с соответствующими расширениями (`.scss`, `.less`), как в следующем примере:

```ts
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
…
```

В процессе сборки CLI запускается соответствующий препроцессор CSS.

При генерации файла компонента с помощью `ng generate component`, CLI по умолчанию создает пустой файл стилей CSS (`.css`). Настройте CLI по умолчанию на предпочтительный препроцессор CSS, как описано в руководстве [Workspace configuration guide](workspace-config.md#generation-schematics).

:date: 28.02.2022
