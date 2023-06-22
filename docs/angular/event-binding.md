# Привязка к событиям

Привязка событий позволяет вам прослушивать и реагировать на действия пользователя, такие как нажатие клавиш, движение мыши, щелчки и прикосновения.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

## Предварительные условия

-   [Основы компонентов](guide/architecture-components)

-   [Основы шаблонов](guide/glossary#template)

-   [Синтаксис связывания](guide/binding-syntax)

-   [Шаблонные утверждения](guide/template-statements)

## Привязка к событиям

Для привязки к событию используется синтаксис привязки событий Angular. Этот синтаксис состоит из имени целевого события в круглых скобках слева от знака равенства и цитируемого шаблонного утверждения справа.

Создайте следующий пример; имя целевого события - `click`, а оператор шаблона - `onSave()`.

<code-example language="html" header="Event binding syntax">
 &lt;button (click)="onSave()"&gt;Save&lt;/button&gt;
</code-example>

Привязка событий прослушивает события нажатия кнопки и вызывает метод компонента `onSave()` всякий раз, когда происходит нажатие.

<div class="lightbox">
   <img src='generated/images/guide/template-syntax/syntax-diagram.svg' alt="Syntax diagram">
</div>

### Определение цели события

Чтобы определить цель события, Angular проверяет, совпадает ли имя целевого события со свойством события известной директивы.

Создайте следующий пример: (Angular проверяет, является ли `myClick` событием пользовательской директивы `ClickDirective`)

<code-example path="event-binding/src/app/app.component.html" region="custom-directive" header="src/app/app.component.html"></code-example>.

Если имя целевого события `myClick` не соответствует выходному свойству `ClickDirective`, Angular вместо этого привяжется к событию `myClick` на базовом элементе DOM.

## Привязка к пассивным событиям

Это продвинутая техника, которая не нужна для большинства приложений. Она может оказаться полезной, если вы хотите оптимизировать часто повторяющиеся события, вызывающие проблемы с производительностью.

Angular также поддерживает пассивные слушатели событий. Например, чтобы сделать событие прокрутки пассивным, выполните следующие действия.

1. Создайте файл `zone-flags.ts` в каталоге `src`.

2. Добавьте в этот файл следующую строку.

    ``typescript

    (window as any)['__zone_symbol__PASSIVE_EVENTS'] = ['scroll'];

    ```

    ```

3. В файле `src/polyfills.ts`, перед импортом zone.js, импортируйте только что созданные `zone-flags`.

    ```typescript
    import './zone-flags';

    import 'zone.js'; // Включено с помощью Angular CLI.
    ```

После этих шагов, если вы добавите слушателей событий для события `scroll`, слушатели будут `пассивными`.

## Привязка к событиям клавиатуры

Вы можете привязываться к событиям клавиатуры, используя синтаксис привязки Angular. Вы можете указать клавишу или код, которые вы хотите привязать к событиям клавиатуры. Поля `key` и `code` являются встроенной частью объекта события клавиатуры браузера. По умолчанию привязка событий предполагает, что вы хотите использовать поле `key` в событии клавиатуры. Вы также можете использовать поле `code`.

Комбинации клавиш можно разделять символом `.` (точка). Например, `keydown.enter` позволит вам привязать события к клавише `enter`. Вы также можете использовать клавиши-модификаторы, такие как `shift`, `alt`, `control` и `командные` клавиши Mac. В следующем примере показано, как привязать событие клавиатуры к `keydown.shift.t`.

```typescript
    <input (keydown.shift.t)="onKeydown($event)" />
```

В зависимости от операционной системы некоторые комбинации клавиш могут создавать специальные символы вместо ожидаемого сочетания клавиш. Например, macOS создает специальные символы, когда вы используете клавиши option и shift вместе. Если вы привяжетесь к `keydown.shift.alt.t`, в macOS эта комбинация создаст символ `ˇ` вместо `t`, что не соответствует привязке и не вызовет обработчик событий. Для привязки к `keydown.shift.alt.t` на macOS используйте поле событий клавиатуры `code`, чтобы получить правильное поведение, например `keydown.code.shiftleft.altleft.keyt`, как показано в этом примере.

```typescript
    <input (keydown.code.shiftleft.altleft.keyt)="onKeydown($event)" />
```

Поле `код` является более конкретным, чем поле `ключ`. Поле `key` всегда сообщает `shift`, тогда как поле `code` указывает `leftshift` или `rightshift`. При использовании поля `code` вам может понадобиться добавить отдельные привязки, чтобы уловить все нужные вам типы поведения. Использование поля `code` позволяет избежать необходимости обрабатывать поведение, специфичное для ОС, например, поведение `shift + option` в macOS.

Для получения дополнительной информации посетите полное руководство по [key](https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_key_values) и [code](https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_code_values), которое поможет вам создать свои строки событий.

## Что дальше

-   Для получения дополнительной информации о том, как работает привязка событий, смотрите [Как работает привязка событий](guide/event-binding-concepts).

-   [Связывание свойств](руководство/property-binding)

-   [Интерполяция текста](руководство/интерполяция)

-   [Двустороннее связывание](guide/two-way-binding)

:date: 10.05.2022