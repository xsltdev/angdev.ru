# Двустороннее связывание

Двустороннее связывание дает компонентам вашего приложения возможность обмениваться данными. Используйте двустороннюю привязку для прослушивания событий и обновления значений одновременно между родительским и дочерним компонентами.

!!!note ""

    Смотрите [код](https://angular.io/generated/live-examples/two-way-binding/stackblitz.html) для рабочего примера, содержащего фрагменты кода, приведенные в этом руководстве.

## Предварительные условия

Чтобы получить максимальную отдачу от двустороннего связывания, вы должны иметь базовое представление о следующих концепциях:

-   [Связывание свойств](property-binding.md)
-   [Связывание событий](event-binding.md)
-   [Входы и выходы](inputs-outputs.md)

Двустороннее связывание объединяет связывание свойств с связыванием событий:

| Связывание                              | Подробности                                   |
| :-------------------------------------- | :-------------------------------------------- |
| [Привязка свойств](property-binding.md) | Устанавливает определенное свойство элемента. |
| [Привязка событий](event-binding.md)    | Слушает событие изменения элемента.           |

## Добавление двусторонней привязки данных

Синтаксис двустороннего связывания данных в Angular представляет собой комбинацию квадратных скобок и круглых скобок, `[()]`. Синтаксис `[()]` сочетает скобки привязки свойств, `[]`, со скобками привязки событий, `()`, следующим образом.

```html
<app-sizer [(size)]="fontSizePx"></app-sizer>
```

## Как работает двустороннее связывание

Чтобы двустороннее связывание данных работало, свойство `@Output()` должно использовать шаблон `inputChange`, где `input` — это имя свойства `@Input()`. Например, если свойством `@Input()` является `size`, то свойство `@Output()` должно быть `sizeChange`.

Следующий `sizerComponent` имеет свойство значения `size` и событие `sizeChange`. Свойство `size` является `@Input()`, поэтому данные могут поступать в `sizerComponent`.

Событие `sizeChange` — это `@Output()`, которое позволяет данным выходить из `sizerComponent` в родительский компонент.

Далее есть два метода, `dec()` для уменьшения размера шрифта и `inc()` для увеличения размера шрифта. Эти два метода используют `resize()` для изменения значения свойства `size` в пределах ограничений min/max, а также для эмиссии события, передающего новое значение `size`.

```ts title="src/app/sizer.component.ts"
export class SizerComponent {
    @Input() size!: number | string;
    @Output() sizeChange = new EventEmitter<number>();

    dec() {
        this.resize(-1);
    }
    inc() {
        this.resize(+1);
    }

    resize(delta: number) {
        this.size = Math.min(
            40,
            Math.max(8, +this.size + delta)
        );
        this.sizeChange.emit(this.size);
    }
}
```

Шаблон `sizerComponent` имеет две кнопки, каждая из которых привязывает событие click к методам `inc()` и `dec()`. Когда пользователь нажимает на одну из кнопок, `sizerComponent` вызывает соответствующий метод.

Оба метода, `inc()` и `dec()`, вызывают метод `resize()` с `+1` или `-1`, который в свою очередь вызывает событие `sizeChange` с новым значением размера.

```html title="src/app/sizer.component.html"
<div>
    <button type="button" (click)="dec()" title="smaller">
        -
    </button>
    <button type="button" (click)="inc()" title="bigger">
        +
    </button>
    <span [style.font-size.px]="size"
        >FontSize: {{size}}px</span
    >
</div>
```

В шаблоне `AppComponent`, `fontSizePx` двусторонне связан с `SizerComponent`.

```html title="src/app/app.component.html"
<app-sizer [(size)]="fontSizePx"></app-sizer>
<div [style.font-size.px]="fontSizePx">Resizable Text</div>
```

В `AppComponent`, `fontSizePx` устанавливает начальное значение `SizerComponent.size`, задавая значение `16`.

```ts title="src/app/app.component.ts"
fontSizePx = 16;
```

Нажатие на кнопки обновляет `AppComponent.fontSizePx`. Измененное значение `AppComponent.fontSizePx` обновляет привязку стиля, что делает отображаемый текст больше или меньше.

Синтаксис двусторонней привязки является сокращением для комбинации привязки свойств и привязки событий. Привязка `SizerComponent` как отдельная привязка свойств и привязка событий выглядит следующим образом.

```html title="src/app/app.component.html (expanded)"
<app-sizer
    [size]="fontSizePx"
    (sizeChange)="fontSizePx=$event"
></app-sizer>
```

Переменная `$event` содержит данные события `SizerComponent.sizeChange`. Angular присваивает значение `$event` событию `AppComponent.fontSizePx`, когда пользователь нажимает на кнопки.

!!!note "Двустороннее связывание в формах"

    Поскольку ни один встроенный элемент HTML не следует шаблону событий `x` value и `xChange`, для двустороннего связывания с элементами формы требуется `NgModel`. Для получения дополнительной информации о том, как использовать двустороннее связывание в формах, смотрите Angular [NgModel](built-in-directives.md#ngModel).

:date: 28.02.2022
