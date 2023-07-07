# Многоразовые анимации

:date: 11.10.2022

В этой теме приведены примеры создания многократно используемых анимаций.

## Предварительные условия

Прежде чем продолжить изучение этой темы, вы должны быть знакомы со следующим:

-   [Введение в анимации Angular](animations.md)
-   [Переход и триггеры](transition-and-triggers.md)

## Создание многократно используемых анимаций

Чтобы создать многократно используемую анимацию, используйте функцию `animation()` для определения анимации в отдельном файле `.ts` и объявите это определение анимации как экспортную переменную `const`. Затем вы можете импортировать и повторно использовать эту анимацию в любом из компонентов вашего приложения с помощью функции [`useAnimation()`](https://angular.io/api/animations/useAnimation).

```ts
import {
    animation,
    style,
    animate,
    trigger,
    transition,
    useAnimation,
} from '@angular/animations';

export const transitionAnimation = animation([
    style({
        height: '{{ height }}',
        opacity: '{{ opacity }}',
        backgroundColor: '{{ backgroundColor }}',
    }),
    animate('{{ time }}'),
]);
```

В предыдущем фрагменте кода `transitionAnimation` сделан многократно используемым путем объявления его как переменной экспорта.

!!!note ""

    Вводы `height`, `opacity`, `backgroundColor` и `time` заменяются во время выполнения.

Вы также можете экспортировать часть анимации. Например, в следующем фрагменте экспортируется анимация `trigger`.

```ts
import {
    animation,
    style,
    animate,
    trigger,
    transition,
    useAnimation,
} from '@angular/animations';

export const triggerAnimation = trigger('openClose', [
    transition('open => closed', [
        useAnimation(transitionAnimation, {
            params: {
                height: 0,
                opacity: 1,
                backgroundColor: 'red',
                time: '1s',
            },
        }),
    ]),
]);
```

С этого момента вы можете импортировать многократно используемые переменные анимации в класс вашего компонента. Например, следующий фрагмент кода импортирует переменную `transitionAnimation` и использует ее с помощью функции `useAnimation()`.

```ts
import { Component } from '@angular/core';
import {
    transition,
    trigger,
    useAnimation,
} from '@angular/animations';
import { transitionAnimation } from './animations';

@Component({
    selector: 'app-open-close-reusable',
    animations: [
        trigger('openClose', [
            transition('open => closed', [
                useAnimation(transitionAnimation, {
                    params: {
                        height: 0,
                        opacity: 1,
                        backgroundColor: 'red',
                        time: '1s',
                    },
                }),
            ]),
        ]),
    ],
    templateUrl: 'open-close.component.html',
    styleUrls: ['open-close.component.css'],
});
```

## Больше об анимации Angular

Вам также может быть интересно следующее:

-   [Введение в анимации Angular](animations.md)
-   [Переход и триггеры](transition-and-triggers.md)
-   [Сложные анимационные последовательности](complex-animation-sequences.md)
-   [Анимации перехода по маршруту](route-animations.md)
