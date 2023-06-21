# Двустороннее связывание

Двустороннее связывание дает компонентам вашего приложения возможность обмениваться данными. Используйте двустороннюю привязку для прослушивания событий и обновления значений одновременно между родительским и дочерним компонентами.

<div class="alert is-helpful">

Смотрите <live-example></live-example> для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

</div>

## Предварительные условия

Чтобы получить максимальную отдачу от двустороннего связывания, вы должны иметь базовое представление о следующих концепциях:

-   [Связывание свойств](руководство/связывание свойств)

-   [Связывание событий](guide/event-binding)

-   [Входы и выходы](guide/inputs-outputs)

Двустороннее связывание объединяет связывание свойств с связыванием событий:

| Связывание | Подробности | |:--- |:--- |:--- |

| [Property binding](guide/property-binding) | Устанавливает определенное свойство элемента. |

| [Event binding](guide/event-binding) | Слушает событие изменения элемента. |

## Добавление двусторонней привязки данных

Синтаксис двустороннего связывания данных в Angular представляет собой комбинацию квадратных скобок и круглых скобок, `[()]`. Синтаксис `[()]` сочетает скобки привязки свойств, `[]`, со скобками привязки событий, `()`, следующим образом.

<code-example header="src/app/app.component.html" path="two-way-binding/src/app/app.component.html" region="two-way-syntax"></code-example>.

## Как работает двустороннее связывание

Чтобы двустороннее связывание данных работало, свойство `@Output()` должно использовать шаблон `inputChange`, где `input` - это имя свойства `@Input()`. Например, если свойством `@Input()` является `size`, то свойство `@Output()` должно быть `sizeChange`.

Следующий `sizerComponent` имеет свойство значения `size` и событие `sizeChange`. Свойство `size` является `@Input()`, поэтому данные могут поступать в `sizerComponent`.

Событие `sizeChange` - это `@Output()`, которое позволяет данным выходить из `sizerComponent` в родительский компонент.

Далее есть два метода, `dec()` для уменьшения размера шрифта и `inc()` для увеличения размера шрифта. Эти два метода используют `resize()` для изменения значения свойства `size` в пределах ограничений min/max, а также для эмиссии события, передающего новое значение `size`.

<code-example header="src/app/sizer.component.ts" path="two-way-binding/src/app/sizer/sizer.component.ts" region="sizer-component"></code-example>

Шаблон `sizerComponent` имеет две кнопки, каждая из которых привязывает событие click к методам `inc()` и `dec()`. Когда пользователь нажимает на одну из кнопок, `sizerComponent` вызывает соответствующий метод.

Оба метода, `inc()` и `dec()`, вызывают метод `resize()` с `+1` или `-1`, который в свою очередь вызывает событие `sizeChange` с новым значением размера.

<code-example header="src/app/sizer.component.html" path="two-way-binding/src/app/sizer/sizer.component.html"></code-example>.

В шаблоне `AppComponent`, `fontSizePx` двусторонне связан с `SizerComponent`.

<code-example header="src/app/app.component.html" path="two-way-binding/src/app/app.component.html" region="two-way-1"></code-example>

В `AppComponent`, `fontSizePx` устанавливает начальное значение `SizerComponent.size`, задавая значение `16`.

<code-example header="src/app/app.component.ts" path="two-way-binding/src/app/app/app.component.ts" region="font-size"></code-example>.

Нажатие на кнопки обновляет `AppComponent.fontSizePx`. Измененное значение `AppComponent.fontSizePx` обновляет привязку стиля, что делает отображаемый текст больше или меньше.

Синтаксис двусторонней привязки является сокращением для комбинации привязки свойств и привязки событий. Привязка `SizerComponent` как отдельная привязка свойств и привязка событий выглядит следующим образом.

<code-example header="src/app/app.component.html (expanded)" path="two-way-binding/src/app/app/app.component.html" region="two-way-2"></code-example>.

Переменная `$event` содержит данные события `SizerComponent.sizeChange`. Angular присваивает значение `$event` событию `AppComponent.fontSizePx`, когда пользователь нажимает на кнопки.

<div class="callout is-helpful">

<header>Two-way binding in forms</header>

Поскольку ни один встроенный элемент HTML не следует шаблону событий `x` value и `xChange`, для двустороннего связывания с элементами формы требуется `NgModel`. Для получения дополнительной информации о том, как использовать двустороннее связывание в формах, смотрите Angular [NgModel](guide/built-in-directives#ngModel).

</div>

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
