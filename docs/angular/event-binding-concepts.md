---
description: При привязке событий Angular настраивает обработчик события для целевого события. Вы можете использовать привязку событий с собственными пользовательскими событиями
---

# Как работает привязка событий

:date: 28.02.2022

При привязке событий Angular настраивает обработчик события для целевого события. Вы можете использовать привязку событий с собственными пользовательскими событиями.

Когда компонент или директива вызывает событие, обработчик выполняет оператор шаблона. Шаблонный оператор выполняет действие в ответ на событие.

## Обработка событий

Обычно для обработки событий в метод, обрабатывающий событие, передается объект события `$event`. Объект `$event` часто содержит необходимую методу информацию, например, имя пользователя или URL-адрес изображения.

Целевое событие определяет форму объекта `$event`. Если целевое событие является собственным событием элемента DOM, то `$event` — это [DOM event object](https://developer.mozilla.org/docs/Web/Events), со свойствами `target` и `target.value`.

В следующем примере код устанавливает свойство `<input>` `value` путем привязки к свойству `name`.

```html
<input
    [value]="currentItem.name"
    (input)="currentItem.name=getValue($event)"
/>
```

В данном примере выполняются следующие действия:

1.  Код привязывается к событию `input` элемента `<input>`, что позволяет ему прослушивать изменения.
2.  Когда пользователь вносит изменения, компонент поднимает событие `input`.
3.  Привязка выполняет оператор в контексте, включающем объект события DOM, `$event`.
4.  Ангуляр извлекает измененный текст вызовом `getValue($event.target)` и обновляет свойство `name`.

Если событие принадлежит директиве или компоненту, то `$event` имеет ту форму, которую создает директива или компонент.

!!!note ""

    Тип `$event.target` в шаблоне только `EventTarget`.
    В методе `getValue()` цель приводится к `HTMLInputElement`, чтобы обеспечить безопасный для типа доступ к ее свойству `value`.

    ```ts
    getValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
    }
    ```

## Ссылки

-   [How event binding works](https://angular.io/guide/event-binding-concepts)
