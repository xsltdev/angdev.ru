# Переходы и триггеры анимации

:date: 11.10.2022

В этом руководстве подробно рассматриваются специальные состояния перехода, такие как `*` подстановочный знак и `void`. В нем показано, как эти специальные состояния используются для элементов, входящих и выходящих из представления. В этом разделе также рассматриваются триггеры анимации, обратные вызовы анимации и анимация на основе последовательности с использованием ключевых кадров.

## Предопределенные состояния и сопоставление подстановочных знаков

В Angular состояния перехода могут быть определены явно через функцию `state()` или с помощью предопределенных `*` подстановочных знаков и `void` состояний.

### Состояние подстановочного знака

Звездочка `*` или _wildcard_ соответствует любому состоянию анимации. Это полезно для определения переходов, которые применяются независимо от начального или конечного состояния HTML-элемента.

Например, переход `open => *` применяется, когда состояние элемента меняется с открытого на любое другое.

![wildcard state expressions](wildcard-state-500.png)

Ниже приведен еще один пример кода, использующий состояние с подстановочным знаком вместе с предыдущим примером, использующим состояния `открыто` и `закрыто`. Вместо определения каждой пары переходов из состояния в состояние, любой переход в `закрытое` занимает 1 секунду, а любой переход в `открытое` — 0,5 секунды.

Это позволяет добавлять новые состояния без необходимости включать отдельные переходы для каждого из них.

```ts
animations: [
  trigger('openClose', [
    // ...
    state('open', style({
      height: '200px',
      opacity: 1,
      backgroundColor: 'yellow'
    })),
    state('closed', style({
      height: '100px',
      opacity: 0.8,
      backgroundColor: 'blue'
    })),
    transition('* => closed', [
      animate('1s')
    ]),
    transition('* => open', [
      animate('0.5s')
    ]),
  ]),
],
```

Используйте синтаксис двойной стрелки для указания переходов из состояния в состояние в обоих направлениях.

```ts
transition('open <=> closed', [
  animate('0.5s')
]),
```

### Использование состояния подстановочного знака с несколькими состояниями перехода

В примере с кнопкой с двумя состояниями подстановочный знак не так полезен, потому что есть только два возможных состояния, `открыто` и `закрыто`. В целом, используйте подстановочный знак состояния, когда элемент имеет несколько потенциальных состояний, в которые он может перейти.

Если кнопка может переходить из состояния `открыто` в состояние `закрыто` или что-то вроде `в процессе`, использование подстановочного знака может сократить объем необходимой кодировки.

![wildcard state with 3 states](wildcard-3-states.png)

```ts
animations: [
    trigger('openClose', [
        // ...
        state(
            'open',
            style({
                height: '200px',
                opacity: 1,
                backgroundColor: 'yellow',
            })
        ),
        state(
            'closed',
            style({
                height: '100px',
                opacity: 0.8,
                backgroundColor: 'blue',
            })
        ),
        transition('open => closed', [animate('1s')]),
        transition('closed => open', [animate('0.5s')]),
        transition('* => closed', [animate('1s')]),
        transition('* => open', [animate('0.5s')]),
        transition('open <=> closed', [animate('0.5s')]),
        transition('* => open', [
            animate('1s', style({ opacity: '*' })),
        ]),
        transition('* => *', [animate('1s')]),
    ]),
];
```

Переход `* => *` применяется, когда происходит изменение между двумя состояниями.

Переходы сопоставляются в том порядке, в котором они определены. Таким образом, вы можете применять другие переходы поверх перехода `* => *`.

Например, определите изменения стиля или анимации, которые будут применяться только к `открыто => закрыто`, а затем используйте `* => *` в качестве запасного варианта для пар состояний, которые иначе не называются.

Для этого перечислите более конкретные переходы _перед_ `* => *`.

### Использовать подстановочные знаки в стилях

Используйте подстановочный знак `*` со стилем, чтобы указать анимации использовать любое текущее значение стиля и анимировать в соответствии с ним. Wildcard — это запасное значение, которое используется, если анимируемое состояние не объявлено в триггере.

```ts
transition ('* => open', [
  animate ('1s',
    style ({ opacity: '*' }),
  ),
]),
```

### Состояние пустоты

Используйте состояние `void` для настройки переходов для элемента, который входит или выходит со страницы. Смотрите [Анимация входа и выхода из представления](#enter-leave-view).

### Объединить состояния подстановочного знака и пустоты

Комбинируйте состояния wildcard и void в переходе, чтобы вызвать анимацию входа и выхода со страницы:

-   Переход `* => void` применяется, когда элемент покидает представление, независимо от того, в каком состоянии он находился до выхода.
-   Переход `void => *` применяется, когда элемент входит в представление, независимо от того, в каком состоянии он находится при входе.
-   Подстановочный знак состояния `*` соответствует _любому_ состоянию, включая `void`.

## Анимация входа и выхода из представления

В этом разделе показано, как анимировать элементы, входящие или выходящие со страницы.

Добавьте новое поведение:

-   Когда вы добавляете героя в список героев, он влетает на страницу слева.
-   Когда вы удаляете героя из списка, он вылетает справа.

```ts
animations: [
    trigger('flyInOut', [
        state('in', style({ transform: 'translateX(0)' })),
        transition('void => *', [
            style({ transform: 'translateX(-100%)' }),
            animate(100),
        ]),
        transition('* => void', [
            animate(
                100,
                style({ transform: 'translateX(100%)' })
            ),
        ]),
    ]),
];
```

В предыдущем коде вы применили состояние `void`, когда HTML-элемент не прикреплен к представлению.

## Псевдонимы :enter и :leave {: #enter-leave-view}

`:enter` и `:leave` являются псевдонимами для переходов `void => *` и `* => void`. Эти псевдонимы используются несколькими функциями анимации.

```ts
transition ( ':enter', [ … ] );  // alias for void => *
transition ( ':leave', [ … ] );  // alias for * => void
```

Сложнее нацелиться на элемент, который входит в представление, поскольку он еще не находится в DOM. Используйте псевдонимы `:enter` и `:leave` для адресации HTML-элементов, которые вставляются или удаляются из представления.

### Используйте `*ngIf` и `*ngFor` с :enter и :leave

Переход `:enter` выполняется, когда на странице размещаются любые представления `*ngIf` или `*ngFor`, а `:leave` выполняется, когда эти представления удаляются со страницы.

!!!warning ""

    Поведение при входе/выходе иногда может сбивать с толку.
    В качестве эмпирического правила считайте, что любой элемент, добавляемый в DOM с помощью Angular, проходит через переход `:enter`. Только элементы, которые Angular непосредственно удаляет из DOM, проходят через переход `:leave`. Например, представление элемента удаляется из DOM, потому что его родитель удаляется из DOM.

В этом примере есть специальный триггер для анимации входа и выхода под названием `myInsertRemoveTrigger`. HTML-шаблон содержит следующий код.

```html
<div
    @myInsertRemoveTrigger
    *ngIf="isShown"
    class="insert-remove-container"
>
    <p>The box is inserted</p>
</div>
```

В файле компонента переход `:enter` устанавливает начальную непрозрачность 0. Затем он анимируется, чтобы изменить эту непрозрачность на 1, когда элемент вставляется в представление.

```ts
trigger('myInsertRemoveTrigger', [
  transition(':enter', [
    style({ opacity: 0 }),
    animate('100ms', style({ opacity: 1 })),
  ]),
  transition(':leave', [
    animate('100ms', style({ opacity: 0 }))
  ])
]),
```

Обратите внимание, что в этом примере не нужно использовать `state()`.

## Переход :increment и :decrement

Функция `transition()` принимает другие значения селектора, `:increment` и `:decrement`. Используйте их для запуска перехода, когда числовое значение увеличивается или уменьшается.

!!!note ""

    В следующем примере используются методы `query()` и `stagger()`.
    Более подробную информацию об этих методах можно найти на странице [сложные последовательности](complex-animation-sequences.md#complex-sequence).

```ts
trigger('filterAnimation', [
  transition(':enter, * => 0, * => -1', []),
  transition(':increment', [
    query(':enter', [
      style({ opacity: 0, width: 0 }),
      stagger(50, [
        animate('300ms ease-out', style({ opacity: 1, width: '*' })),
      ]),
    ], { optional: true })
  ]),
  transition(':decrement', [
    query(':leave', [
      stagger(50, [
        animate('300ms ease-out', style({ opacity: 0, width: 0 })),
      ]),
    ])
  ]),
]),
```

## Булевы значения в переходах

Если триггер содержит булево значение в качестве значения привязки, то это значение может быть сопоставлено с помощью выражения `transition()`, которое сравнивает `true` и `false`, или `1` и `0`.

```html
<div
    [@openClose]="isOpen ? true : false"
    class="open-close-container"
></div>
```

В приведенном выше фрагменте кода HTML-шаблон связывает элемент `<div>` с триггером `openClose` с выражением состояния `isOpen` и возможными значениями `true` и `false`. Этот шаблон является альтернативой практике создания двух именованных состояний, таких как `open` и `close`.

Внутри метаданных `@Component` в свойстве `animations:`, когда состояние оценивается как `true`, высота связанного HTML-элемента является стилем подстановки или значением по умолчанию. В этом случае анимация использует ту высоту, которую элемент уже имел до начала анимации.

Когда элемент `закрыт`, он анимируется до высоты 0, что делает его невидимым.

```ts
animations: [
  trigger('openClose', [
    state('true', style({ height: '*' })),
    state('false', style({ height: '0px' })),
    transition('false <=> true', animate(500))
  ])
],
```

## Несколько триггеров анимации

Вы можете определить более одного триггера анимации для компонента. Прикрепите триггеры анимации к разным элементам, и отношения "родитель-потомок" между элементами будут влиять на то, как и когда запускается анимация.

### Анимация родительского и дочернего элементов

При каждом запуске анимации в Angular родительская анимация всегда получает приоритет, а дочерние анимации блокируются. Чтобы запустить дочернюю анимацию, родительская анимация должна запросить каждый из элементов, содержащих дочерние анимации. Затем она разрешает запуск анимации с помощью функции `animateChild()`.

#### Отключение анимации на элементе HTML

Специальная привязка управления анимацией `@.disabled` может быть размещена на элементе HTML для отключения анимации на этом элементе, а также на любых вложенных элементах. При значении true привязка `@.disabled` предотвращает отрисовку всех анимаций.

Следующий пример кода показывает, как использовать эту функцию.

=== "src/app/open-close.component.html"

```html
<div [@.disabled]="isDisabled">
    <div
        [@childAnimation]="isOpen ? 'open' : 'closed'"
        class="open-close-container"
    >
        <p>
            The box is now {{ isOpen ? 'Open' : 'Closed' }}!
        </p>
    </div>
</div>
```

=== "src/app/open-close.component.ts"

```ts
@Component({
    animations: [
        trigger('childAnimation', [
            // ...
        ]),
    ],
})
export class OpenCloseChildComponent {
    isDisabled = false;
    isOpen = false;
}
```

Когда привязка `@.disabled` истинна, триггер `@childAnimation` не срабатывает.

Когда у элемента в HTML-шаблоне отключена анимация с помощью привязки `@.disabled`, анимация отключается и у всех внутренних элементов. Вы не можете выборочно отключить несколько анимаций на одном элементе.

Выборочная дочерняя анимация все еще может быть запущена на отключенном родительском элементе одним из следующих способов:

-   Родительская анимация может использовать функцию `query()` для сбора внутренних элементов, расположенных в отключенных областях шаблона HTML.

    Эти элементы все равно могут анимироваться.

-   Дочерняя анимация может быть запрошена родительской, а затем анимирована с помощью функции `animateChild()`.

#### Отключить все анимации

Чтобы отключить все анимации в приложении Angular, поместите привязку хоста `@.disabled` на самый верхний компонент Angular.

```ts
@Component({
    selector: 'app-root',
    templateUrl: 'app.component.html',
    styleUrls: ['app.component.css'],
    animations: [slideInAnimation],
})
export class AppComponent {
    @HostBinding('@.disabled')
    public animationsDisabled = false;
}
```

!!!note ""

    Отключение анимации во всем приложении полезно при сквозном тестировании (E2E).

## Обратные вызовы анимации

Функция анимации `trigger()` испускает _обратные вызовы_, когда она начинается и когда она завершается. В следующем примере представлен компонент, содержащий триггер `openClose`.

```ts
@Component({
    selector: 'app-open-close',
    animations: [
        trigger('openClose', [
            // ...
        ]),
    ],
    templateUrl: 'open-close.component.html',
    styleUrls: ['open-close.component.css'],
})
export class OpenCloseComponent {
    onAnimationEvent(event: AnimationEvent) {}
}
```

В шаблоне HTML событие анимации передается обратно через `$event`, как `@triggerName.start` и `@triggerName.done`, где `triggerName` — имя используемого триггера. В данном примере триггер `openClose` выглядит следующим образом.

```html
<div
    [@openClose]="isOpen ? 'open' : 'closed'"
    (@openClose.start)="onAnimationEvent($event)"
    (@openClose.done)="onAnimationEvent($event)"
    class="open-close-container"
></div>
```

Потенциальное использование обратных вызовов анимации может быть связано с медленным вызовом API, таким как поиск в базе данных. Например, кнопка **InProgress** может быть настроена на зацикленную анимацию, пока завершается работа внутренней системы.

По завершении текущей анимации можно вызвать другую анимацию. Например, кнопка переходит из состояния `в процессе` в состояние `закрыто`, когда вызов API завершен.

Анимация может повлиять на конечного пользователя, чтобы он _воспринимал_ операцию как более быструю, даже если это не так.

Обратные вызовы могут служить в качестве инструмента отладки, например, в сочетании с `console.warn()` для просмотра хода выполнения приложения в JavaScript-консоли разработчика браузера. Следующий фрагмент кода создает вывод журнала консоли для исходного примера — кнопки с двумя состояниями `открыто` и `закрыто`.

```ts
export class OpenCloseComponent {
    onAnimationEvent(event: AnimationEvent) {
        // openClose is trigger name in this example
        console.warn(
            `Animation Trigger: ${event.triggerName}`
        );

        // phaseName is "start" or "done"
        console.warn(`Phase: ${event.phaseName}`);

        // in our example, totalTime is 1000 (number of milliseconds in a second)
        console.warn(`Total time: ${event.totalTime}`);

        // in our example, fromState is either "open" or "closed"
        console.warn(`From: ${event.fromState}`);

        // in our example, toState either "open" or "closed"
        console.warn(`To: ${event.toState}`);

        // the HTML element itself, the button in this case
        console.warn(`Element: ${event.element}`);
    }
}
```

## Ключевые кадры {: #keyframes}

Чтобы создать анимацию с несколькими последовательно выполняемыми шагами, используйте _ключевые кадры_.

Функция Angular `keyframe()` позволяет изменять несколько стилей в пределах одного временного сегмента. Например, кнопка, вместо того чтобы исчезать, может менять цвет несколько раз в течение одного 2-секундного отрезка времени.

![keyframes](keyframes-500.png)

Код для этого изменения цвета может выглядеть следующим образом.

```ts
transition('* => active', [
    animate(
        '2s',
        keyframes([
            style({ backgroundColor: 'blue' }),
            style({ backgroundColor: 'red' }),
            style({ backgroundColor: 'orange' }),
        ])
    ),
]);
```

### Offset

Ключевые кадры включают `Offset`, которое определяет точку в анимации, где происходит каждое изменение стиля. Смещение — это относительная величина от нуля до единицы, обозначающая начало и конец анимации. Они должны применяться к каждому из ключевых кадров, если используются хотя бы один раз.

Определение смещений для ключевых кадров необязательно. Если вы их не зададите, то равномерно расположенные смещения будут назначены автоматически.

Например, три ключевых кадра без заданных смещений получают смещения 0, 0,5 и 1.

Указание смещения 0,8 для среднего перехода в предыдущем примере может выглядеть следующим образом.

![keyframes with offset](keyframes-offset-500.png)

Код с указанными смещениями будет выглядеть следующим образом.

```ts
transition('* => active', [
  animate('2s', keyframes([
    style({ backgroundColor: 'blue', offset: 0}),
    style({ backgroundColor: 'red', offset: 0.8}),
    style({ backgroundColor: '#754600', offset: 1.0})
  ]))
]),
transition('* => inactive', [
  animate('2s', keyframes([
    style({ backgroundColor: '#754600', offset: 0}),
    style({ backgroundColor: 'red', offset: 0.2}),
    style({ backgroundColor: 'blue', offset: 1.0})
  ]))
]),
```

Вы можете комбинировать ключевые кадры с `duration`, `delay` и `easing` в рамках одной анимации.

### Ключевые кадры с пульсацией

Используйте ключевые кадры для создания эффекта пульсации в анимации, определяя стили с определенным смещением на протяжении всей анимации.

Вот пример использования ключевых кадров для создания эффекта пульсации:

-   Исходные состояния `open` и `closed` с оригинальными изменениями высоты, цвета и непрозрачности, происходящими в течение 1 секунды.
-   Последовательность ключевых кадров, вставленная в середине, которая заставляет кнопку пульсировать неравномерно в течение того же 1 секунды.

![keyframes with irregular pulsation](keyframes-pulsation.png)

Фрагмент кода для этой анимации может выглядеть следующим образом.

```ts
trigger('openClose', [
    state(
        'open',
        style({
            height: '200px',
            opacity: 1,
            backgroundColor: 'yellow',
        })
    ),
    state(
        'close',
        style({
            height: '100px',
            opacity: 0.5,
            backgroundColor: 'green',
        })
    ),
    // ...
    transition('* => *', [
        animate(
            '1s',
            keyframes([
                style({ opacity: 0.1, offset: 0.1 }),
                style({ opacity: 0.6, offset: 0.2 }),
                style({ opacity: 1, offset: 0.5 }),
                style({ opacity: 0.2, offset: 0.7 }),
            ])
        ),
    ]),
]);
```

### Анимируемые свойства и единицы

Поддержка анимации в Angular основана на веб-анимации, поэтому вы можете анимировать любое свойство, которое браузер считает анимируемым. Сюда входят позиции, размеры, трансформации, цвета, границы и многое другое.

W3C поддерживает список анимируемых свойств на странице [CSS Transitions](https://www.w3.org/TR/css-transitions-1).

Для свойств с числовым значением определите единицу измерения, указав значение в виде строки в кавычках с соответствующим суффиксом:

-   50 пикселей: `'50px'`
-   Относительный размер шрифта: `'3em'`
-   Процент: `'100%'`

Вы также можете указать значение в виде числа. В таких случаях Angular принимает единицу измерения по умолчанию — пиксели, или `px`. Выразить 50 пикселей как `50` — то же самое, что сказать `'50px'`.

!!!note ""

    Строка `"50"` вместо этого не будет считаться действительной

### Автоматическое вычисление свойств с помощью подстановочных знаков

Иногда значение свойства размерного стиля не известно до момента выполнения. Например, элементы часто имеют ширину и высоту, которые зависят от их содержимого или размера экрана.

Эти свойства часто сложно анимировать с помощью CSS.

В таких случаях можно использовать специальный подстановочный знак `*` в свойстве `style()`. Значение этого конкретного свойства стиля вычисляется во время выполнения и затем вставляется в анимацию.

В следующем примере есть триггер `shrinkOut`, который используется, когда элемент HTML покидает страницу. Анимация берет высоту элемента перед его уходом и анимируется от этой высоты до нуля.

```ts
animations: [
    trigger('shrinkOut', [
        state('in', style({ height: '*' })),
        transition('* => void', [
            style({ height: '*' }),
            animate(250, style({ height: 0 })),
        ]),
    ]),
];
```

### Краткое описание ключевых кадров

Функция `keyframes()` в Angular позволяет задать несколько промежуточных стилей в рамках одного перехода. Необязательное `offset` может быть использовано для определения точки в анимации, в которой должно произойти изменение каждого стиля.

## Подробнее об анимации в Angular

Вам также может быть интересно следующее:

-   [Введение в анимации Angular](animations.md)
-   [Сложные анимационные последовательности](complex-animation-sequences.md)
-   [Многоразовые анимации](reusable-animations.md)
-   [Анимации перехода по маршруту](route-animations.md)
