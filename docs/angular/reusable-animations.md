# Многоразовые анимации

В этой теме приведены примеры создания многократно используемых анимаций.

## Предварительные условия

Прежде чем продолжить изучение этой темы, вы должны быть знакомы со следующим:

-   [Введение в анимации Angular](руководство/анимации)

-   [Переход и триггеры](guide/transition-and-triggers)

## Создание многократно используемых анимаций

Чтобы создать многократно используемую анимацию, используйте функцию [`animation()`](api/animations/animation) для определения анимации в отдельном файле `.ts` и объявите это определение анимации как экспортную переменную `const`. Затем вы можете импортировать и повторно использовать эту анимацию в любом из компонентов вашего приложения с помощью функции [`useAnimation()`](api/animations/useAnimation).

<code-example header="src/app/animations.ts" path="animations/src/app/animations.1.ts" region="animation-const"></code-example>.

В предыдущем фрагменте кода `transitionAnimation` сделан многократно используемым путем объявления его как переменной экспорта.

<div class="alert is-helpful">

**NOTE**: <br /> The `height`, `opacity`, `backgroundColor`, and `time` inputs are replaced during runtime.

</div>

Вы также можете экспортировать часть анимации. Например, в следующем фрагменте экспортируется анимация `trigger`.

<code-example header="src/app/animations.1.ts" path="animations/src/app/animations.1.ts" region="trigger-const"></code-example>.

С этого момента вы можете импортировать многократно используемые переменные анимации в класс вашего компонента. Например, следующий фрагмент кода импортирует переменную `transitionAnimation` и использует ее с помощью функции `useAnimation()`.

<code-example header="src/app/open-close.component.ts" path="animations/src/app/open-close.component.3.ts" region="reusable"></code-example>.

## Больше об анимации Angular

Вам также может быть интересно следующее:

-   [Введение в анимации Angular](руководство/анимации)

-   [Переход и триггеры](guide/transition-and-triggers)

-   [Сложные анимационные последовательности](руководство/complex-animation-sequences)

-   [Анимации перехода по маршруту](guide/route-animations)

:date: 11.10.2022
