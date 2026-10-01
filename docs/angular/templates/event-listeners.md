---
description: "Обработчик события на элементе шаблона задают именем события в круглых скобках и выражением, которое выполняется при каждом срабатывании."
---

# Добавление обработчиков событий {: #adding-event-listeners}

:date: 30.09.2026

Angular позволяет задать обработчик события на элементе шаблона: имя события указывают в круглых скобках вместе с выражением, которое выполняется при каждом срабатывании события.

## Прослушивание нативных событий {: #listening-to-native-events}

Чтобы добавить обработчик события к элементу HTML, имя события оборачивают круглыми скобками `()` и указывают выражение обработчика.

```ts
@Component({
  template: `
    <input type="text" (keyup)="updateField()" />
  `,
  ...
})
export class App{
  updateField(): void {
    console.log('Field is updated!');
  }
}
```

В этом примере Angular вызывает `updateField` каждый раз, когда элемент `<input>` порождает событие `keyup`.

Обработчики можно добавить для любых нативных событий, например `click`, `keydown`, `mouseover`. Полный список — в статье [все доступные события элементов на MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element#events).

## Доступ к аргументу события {: #accessing-the-event-argument}

В каждом обработчике события шаблона Angular предоставляет переменную `$event` со ссылкой на объект события.

```ts
@Component({
  template: `
    <input type="text" (keyup)="updateField($event)" />
  `,
  ...
})
export class App {
  updateField(event: KeyboardEvent): void {
    console.log(`The user pressed: ${event.key}`);
  }
}
```

## Модификаторы клавиш {: #using-key-modifiers}

Чтобы поймать событие клавиатуры для конкретной клавиши, часто пишут код вроде такого:

```ts
@Component({
  template: `
    <input type="text" (keyup)="updateField($event)" />
  `,
  ...
})
export class App {
  updateField(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      console.log('The user pressed enter in the text field.');
    }
  }
}
```

Это частый случай, поэтому Angular позволяет отфильтровать события, указав конкретную клавишу через точку (`.`). Код упрощается до такого:

```ts
@Component({
  template: `
    <input type="text" (keyup.enter)="updateField($event)" />
  `,
  ...
})
export class App{
  updateField(event: KeyboardEvent): void {
    console.log('The user pressed enter in the text field.');
  }
}
```

Можно добавить и дополнительные модификаторы клавиш:

```html
<!-- Matches shift and enter -->
<input type="text" (keyup.shift.enter)="updateField($event)" />
```

Angular поддерживает модификаторы `alt`, `control`, `meta` и `shift`.

Для событий клавиатуры можно указать key или code. Поля key и code — штатная часть объекта события клавиатуры в браузере. По умолчанию привязка события считает, что нужны [значения Key для событий клавиатуры](https://developer.mozilla.org/docs/Web/API/UI_Events/Keyboard_event_key_values).

Angular также позволяет указать [значения Code для событий клавиатуры](https://developer.mozilla.org/docs/Web/API/UI_Events/Keyboard_event_code_values) через встроенный суффикс `code`.

```html
<!-- Matches alt and left shift -->
<input type="text" (keydown.code.alt.shiftleft)="updateField($event)" />
```

Так проще одинаково обрабатывать события клавиатуры в разных операционных системах. Например, при клавише Alt на устройствах macOS свойство `key` сообщает клавишу по символу, уже изменённому клавишей Alt. Сочетание вроде Alt + S даёт значение `key`, равное `'ß'`. Свойство `code` при этом соответствует нажатой физической или виртуальной кнопке, а не полученному символу.

## Прослушивание глобальных целей {: #listening-on-global-targets}

Имя глобальной цели можно поставить префиксом события. Поддерживаются три глобальные цели: `window`, `document` и `body`.

```ts
@Component({
  /* ... */
  host: {
    '(window:click)': 'onWindowClick()',
    '(document:click)': 'onDocumentClick()',
    '(body:click)': 'onBodyClick()',
  },
})
export class MyView {}
```

## Отмена поведения события по умолчанию {: #preventing-event-default-behavior}

Если обработчик должен заменить штатное поведение браузера, используйте [метод `preventDefault`](https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault) объекта события:

```ts
@Component({
  template: `
    <a href="#overlay" (click)="showOverlay($event)">
  `,
  ...
})
export class App{
  showOverlay(event: PointerEvent): void {
    event.preventDefault();
    console.log('Show overlay without updating the URL!');
  }
}
```

Если выражение обработчика события даёт `false`, Angular сам вызывает `preventDefault()`, по аналогии с [нативными атрибутами обработчиков событий](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes#event_handler_attributes). _Всегда лучше вызывать `preventDefault` явно_: так намерение кода очевидно.

## Расширение обработки событий {: #extend-event-handling}

Систему событий Angular расширяют собственными плагинами событий, которые регистрируют через токен инъекции `EVENT_MANAGER_PLUGINS`.

### Реализация плагина событий {: #implementing-event-plugin}

Чтобы создать собственный плагин событий, расширьте класс `EventManagerPlugin` и реализуйте нужные методы.

```ts
import {Injectable} from '@angular/core';
import {EventManagerPlugin} from '@angular/platform-browser';

@Injectable()
export class DebounceEventPlugin extends EventManagerPlugin {
  constructor() {
    super(document);
  }

  // Define which events this plugin supports
  override supports(eventName: string) {
    return /debounce/.test(eventName);
  }

  // Handle the event registration
  override addEventListener(element: HTMLElement, eventName: string, handler: Function) {
    // Parse the event: e.g., "click.debounce.500"
    // event: "click", delay: 500
    const [event, method, delay = 300] = eventName.split('.');

    let timeoutId: number;

    const listener = (event: Event) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        handler(event);
      }, delay);
    };

    element.addEventListener(event, listener);

    // Return cleanup function
    return () => {
      clearTimeout(timeoutId);
      element.removeEventListener(event, listener);
    };
  }
}
```

Зарегистрируйте свой плагин через токен `EVENT_MANAGER_PLUGINS` в провайдерах приложения:

```ts
import {bootstrapApplication} from '@angular/platform-browser';
import {EVENT_MANAGER_PLUGINS} from '@angular/platform-browser';
import {App} from './app';
import {DebounceEventPlugin} from './debounce-event-plugin';

bootstrapApplication(App, {
  providers: [
    {
      provide: EVENT_MANAGER_PLUGINS,
      useClass: DebounceEventPlugin,
      multi: true,
    },
  ],
});
```

После регистрации собственный синтаксис событий работает и в шаблонах, и в свойстве `host`:

```ts
@Component({
  template: `
    <input
      type="text"
      (input.debounce.500)="onSearch($event.target.value)"
      placeholder="Search..."
    />
  `,
  ...
})
export class Search {
 onSearch(query: string): void {
    console.log('Searching for:', query);
  }
}
```

```ts
@Component({
  ...,
  host: {
    '(click.debounce.500)': 'handleDebouncedClick()',
  },
})
export class AwesomeCard {
  handleDebouncedClick(): void {
   console.log('Debounced click!');
  }
}
```


---

Источник: [https://angular.dev/guide/templates/event-listeners](https://angular.dev/guide/templates/event-listeners)
