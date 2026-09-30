---
description: "Отложенная реакция на сигнал пока экспериментальна: её можно пробовать, но до стабильной версии поведение может измениться."
---

# Задержка сигналов через `debounced` {: #debouncing-signals-with-debounced}

:date: 30.09.2026

!!! warning ""

    `debounced` — [экспериментальная](https://angular.dev/reference/releases#experimental) возможность. Её уже можно пробовать, но до стабильной версии поведение может измениться.

`debounced` откладывает реакцию на значение сигнала, пока оно не перестанет меняться. Функция возвращает `Resource`, чьё значение — это отложенное значение исходного сигнала.

```ts
import {debounced, resource, signal} from '@angular/core';

@Component({
  template: `
    <input (input)="query.set($event.target.value)" />

    @if (results.isLoading()) {
      <p>Searching…</p>
    }
    @for (item of results.value(); track item.id) {
      <li>{{ item.name }}</li>
    }
  `,
})
export class Search {
  query = signal('');

  debouncedQuery = debounced(this.query, 300);

  results = resource({
    params: () => this.debouncedQuery.value(),
    loader: ({params}) => fetchResults(params),
  });
}
```

`debounced` принимает исходный сигнал и паузу в миллисекундах. У полученного ресурса `value()` всегда хранит последнее установившееся значение, а `status()` показывает, ждёт ли ресурс новое.

## Статус во время задержки {: #status-during-debounce}

Пока идёт отсчёт таймера, `status()` равен `'loading'`, а `value()` возвращает прежнее полученное значение. Когда таймер истекает, ресурс устанавливается в `'resolved'`. Если исходный сигнал выбрасывает исключение, ресурс сразу переходит в `'error'`, таймер не запускается.

Полный список статусов и то, что при них возвращает `value()`, — в разделе [Статус ресурса](resource.md#resource-status).

## Своя функция ожидания {: #custom-wait-function}

Вместо миллисекунд можно передать функцию, которая возвращает `Promise<void>`. Ресурс завершается, когда завершается промис. Если исходный сигнал изменится до завершения промиса, Angular отбрасывает прежний промис и начинает новый.

```ts
debouncedQuery = debounced(query, (value, lastSnapshot) => {
  // Retry immediately after an error rather than making the user wait again.
  if (lastSnapshot.status === 'error') return;
  // Short queries get a longer delay—the user is likely still typing.
  const ms = value.length < 3 ? 500 : 200;
  return new Promise<void>((resolve) => setTimeout(resolve, ms));
});
```

Тип `DebounceTimer` описан в справочнике API.

## Равенство {: #equality}

По умолчанию `debounced` сравнивает значения через `Object.is`.

Если стандартная проверка идентичности слишком строгая, задайте свою функцию равенства параметром `equal`:

```ts
debouncedFilter = debounced(filter, 200, {
  equal: (a, b) => a.category === b.category && a.minPrice === b.minPrice,
});
```

## Контекст инъекции {: #injection-context}

`debounced` вызывают только внутри [контекста инъекции](https://angular.dev/guide/di/dependency-injection-context). Когда инжектор уничтожается, Angular сам уничтожает отложенный ресурс и отменяет таймер, который ещё не сработал.

Чтобы вызвать `debounced` вне контекста инъекции, передайте `Injector` явно в параметрах:

```ts
@Service()
export class SearchService {
  private injector = inject(Injector);

  createDebouncedQuery(query: Signal<string>): Resource<string> {
    return debounced(query, 300, {injector: this.injector});
  }
}
```


---

Источник: [https://angular.dev/guide/signals/debounced](https://angular.dev/guide/signals/debounced)
