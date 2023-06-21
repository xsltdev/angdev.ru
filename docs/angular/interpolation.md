# Отображение значений с помощью интерполяции

## Предварительные условия

-   [Основы компонентов](guide/architecture-components)

-   [Основы шаблонов](guide/glossary#template)

-   [Синтаксис связывания](guide/binding-syntax)

<!--todo: needs a level 2 heading for info below -->

Интерполяция - это вставка выражений в размеченный текст. По умолчанию интерполяция использует двойные фигурные скобки `{{` и `}}` в качестве разделителей.

Чтобы проиллюстрировать работу интерполяции, рассмотрим компонент Angular, содержащий переменную `currentCustomer`:

<code-example path="interpolation/src/app/app.component.ts" region="customer"></code-example>.

Используйте интерполяцию для отображения значения этой переменной в соответствующем шаблоне компонента:

<code-example path="interpolation/src/app/app.component.html" region="interpolation-example1"></code-example>.

Angular заменяет `currentCustomer` строковым значением соответствующего свойства компонента. В данном случае это значение `Maria`.

В следующем примере Angular оценивает свойства `title` и `itemImageUrl` для отображения текста заголовка и изображения.

<code-example path="interpolation/src/app/app.component.html" region="component-property"></code-example>

## Что дальше

-   [Привязка свойств](guide/property-binding)

-   [Связывание событий](guide/event-binding)

:date: 14.04.2022
