---
description: "Ресурс встраивает асинхронные данные в код на сигналах и оставляет синхронное чтение результата."
---

# Асинхронная реактивность через ресурсы {: #async-reactivity-with-resources}

:date: 30.09.2026

Все API сигналов синхронны: `signal`, `computed`, `input` и остальные. Приложению часто нужны данные, которые появляются асинхронно. `Resource` встраивает такие данные в код на сигналах и оставляет синхронный доступ к результату.

`Resource` подходит для любой асинхронной операции, но чаще всего им запрашивают данные с сервера. В примере ниже ресурс загружает данные пользователя.

Проще всего создать `Resource` функцией `resource`.

```ts
import {computed, resource, Signal} from '@angular/core';

const userId: Signal<string> = getUserId();

const userResource = resource({
  // Define a reactive computation.
  // The params value recomputes whenever any read signals change.
  params: () => ({id: userId()}),

  // Define an async loader that retrieves data.
  // The resource calls this function every time the `params` value changes.
  loader: ({params}) => fetchUser(params),
});

// Create a computed signal based on the result of the resource's loader function.
const firstName = computed(() => {
  if (userResource.hasValue()) {
    // `hasValue` serves 2 purposes:
    // - It acts as type guard to strip `undefined` from the type
    // - It protects against reading a throwing `value` when the resource is in error state
    return userResource.value().firstName;
  }

  // fallback in case the resource value is `undefined` or if the resource is in error state
  return undefined;
});
```

Функция `resource` принимает объект `ResourceOptions` с двумя главными свойствами: `params` и `loader`.

Свойство `params` задаёт реактивное вычисление параметра. Когда меняется сигнал, прочитанный в этом вычислении, ресурс производит новое значение параметра, как это делает `computed`.

Свойство `loader` задаёт `ResourceLoader` — асинхронную функцию, которая получает состояние. Ресурс вызывает её каждый раз, когда вычисление `params` даёт новое значение, и передаёт это значение в загрузчик. Подробнее — ниже, в разделе [Загрузчики ресурсов](#resource-loaders).

У `Resource` есть сигнал `value`: в нём результат загрузчика.

## Загрузчики ресурсов {: #resource-loaders}

При создании ресурса указывают `ResourceLoader`. Это асинхронная функция: она принимает один аргумент, объект `ResourceLoaderParams`, и возвращает значение.

У объекта `ResourceLoaderParams` три свойства: `params`, `previous` и `abortSignal`.

| Свойство | Описание |
| --- | --- |
| `params` | Значение вычисления `params` у ресурса. |
| `previous` | Объект со свойством `status`, в котором лежит предыдущий `ResourceStatus`. |
| `abortSignal` | [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal). Подробности — в разделе [Отмена запросов](#aborting-requests) ниже. |

Если вычисление `params` вернуло `undefined`, загрузчик не запускается, а статус ресурса становится `'idle'`.

### Потоковые ресурсы {: #streaming-resources}

Некоторые асинхронные источники со временем отдают несколько значений, а не один результат. Например, WebSocket, Server-Sent Events (SSE) и слушатели `onSnapshot` в Firestore.

Для таких источников, которые обновляются непрерывно, берите `stream`. В отличие от `loader`, который для каждого запроса завершается один раз, `stream` возвращает сигнал, и его значение может обновляться и дальше, когда приходят новые данные.

`loader` — для разовой асинхронной операции, например запроса к HTTP-эндпоинту.

```ts
const userUpdates = signal({value: 'Alice'});

const userResource = resource({
  stream: () => userUpdates,
});

// Later, when new data arrives:
userUpdates.set({value: 'Bob'});
```

### Отмена запросов {: #aborting-requests}

Если вычисление `params` меняется, пока ресурс загружается, незавершённая загрузка отменяется.

На отмену отвечают через `abortSignal` из `ResourceLoaderParams`. Например, встроенный `fetch` принимает `AbortSignal`:

```ts
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params, abortSignal}): Promise<User> => {
    // fetch cancels any outstanding HTTP requests when the given `AbortSignal`
    // indicates that the request has been aborted.
    return fetch(`users/${params.id}`, {signal: abortSignal});
  },
});
```

Подробнее об отмене запроса через `AbortSignal` — в статье [`AbortSignal` на MDN](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal).

### Перезагрузка {: #reloading}

Загрузчик ресурса можно запустить из кода методом `reload`.

```ts
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params}) => fetchUser(params),
});

// ...

userResource.reload();
```

## Статус ресурса {: #resource-status}

У объекта ресурса есть сигнальные свойства: по ним читают состояние асинхронного загрузчика.

| Свойство | Описание |
| --- | --- |
| `value` | Последнее значение ресурса или `undefined`, если значение ещё не получено. |
| `hasValue` | Есть ли у ресурса значение. |
| `error` | Последняя ошибка загрузчика ресурса или `undefined`, если ошибки не было. |
| `isLoading` | Выполняется ли загрузчик ресурса сейчас. |
| `status` | Конкретный `ResourceStatus` ресурса, как описано ниже. |

Сигнал `status` даёт конкретный `ResourceStatus`: состояние ресурса строковой константой.

| Статус | `value()` | Описание |
| --- | --- | --- |
| `'idle'` | `undefined` | У ресурса нет корректного запроса, загрузчик не запускался. |
| `'error'` | `undefined` | Загрузчик столкнулся с ошибкой. |
| `'loading'` | `undefined` | Загрузчик работает, потому что изменилось значение `params`. |
| `'reloading'` | Предыдущее значение | Загрузчик работает, потому что вызван метод `reload` ресурса. |
| `'resolved'` | Полученное значение | Загрузчик завершился. |
| `'local'` | Значение, заданное локально | Значение ресурса задано локально через `.set()` или `.update()`. |

По статусу в интерфейсе условно показывают, например, индикатор загрузки и текст ошибки.

## Кэширование данных `resource` при серверном рендеринге {: #caching-resource-data-with-ssr}

При отрисовке на сервере загрузчик ресурса выполняется один раз и формирует исходный HTML. При гидратации браузер обычно запускает тот же загрузчик ещё раз.

Чтобы переиспользовать серверный результат, задайте ресурсу `id`. Angular сохраняет полученное значение в `TransferState` на сервере и на клиенте по нему инициализирует ресурс в состоянии `'resolved'`.

```ts
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params}) => fetchUser(params),
  id: 'user-unique-id',
});
```

Значение `id` должно быть уникальным внутри приложения и совпадать на сервере и клиенте, чтобы Angular нашёл кэш того ресурса, который его запросил.

!!! warning ""

    Кэш сериализуется в HTML страницы. Не ставьте `id` ресурсам с данными того пользователя, который запустил серверный рендеринг, особенно если этот HTML кэшируют или отдают нескольким пользователям.

## Цепочка ресурсов {: #chaining-resources}

Иногда один ресурс зависит от результата другого. Эту зависимость описывают функцией `chain` из объекта контекста `params`.

```ts
import {resource} from '@angular/core';

const userResource = resource({
  params: () => ({id: getUserId()}),
  loader: ({params}) => fetchUser(params),
});

const companyResource = resource({
  params: ({chain}) => chain(userResource)?.companyId,
  loader: ({params: companyId}) => fetchCompany(companyId),
});
```

Здесь `companyResource` зависит от `companyId` пользователя, а он известен только после загрузки `userResource`. Вызов `chain(userResource)` читает значение `userResource` и сам переносит его статус на `companyResource`:

-   Если `userResource` в состоянии **idle**, `companyResource` тоже становится `idle`.
-   Если `userResource` загружается или перезагружается (**loading** или **reloading**), `companyResource` входит в состояние `loading`, и его загрузчик не запускается. Пока идёт `reloading`, `chain` не возвращает ранее полученное значение.
-   Если `userResource` в состоянии **ошибки** (`error`), `companyResource` тоже переходит в `error`.
-   Если `userResource` получен или задан локально (**resolved** или **local**), `chain` возвращает текущее значение, и `companyResource` берёт его как свои `params`.

Когда `chain` переносит статус `userResource` (`idle`, `loading`, `reloading` или `error`), функция `params` на этом останавливается. Когда `userResource` в состоянии `resolved` или `local`, `chain` возвращает его значение, и это значение само может быть `undefined`. Пример учитывает это через `chain(userResource)?.companyId`: значение `undefined` даёт `params`, равные `undefined`, и `companyResource` становится `idle`.

!!! info ""

    Передавайте значение из цепочки напрямую как значение `params`, а не оборачивайте его в объект. Значение `params` вроде `{companyId: undefined}` всё равно считается заданным: загрузчик запустится с `companyId`, равным `undefined`, и ресурс не перейдёт в `idle`.

### Цепочка и прямое чтение значения {: #chaining-vs-reading-resource-values-directly}

Может показаться удобным прочитать значение ресурса прямо в `params`:

```ts
const companyResource = resource({
  params: () => {
    const user = userResource.value(); // may be undefined
    return user ? {companyId: user.companyId} : undefined;
  },
  loader: ({params}) => fetchCompany(params.companyId),
});
```

Это работает, но `undefined` из `params` переводит ресурс в `idle` и не показывает настоящий статус ресурса выше по цепочке. `chain` лучше: он честно повторяет состояния `loading` и `error`.

Берите `chain` только тогда, когда зависимый ресурс сам делает асинхронную работу и ей нужно значение верхнего ресурса. Если значение нужно лишь синхронно вывести из ресурса, используйте `computed`.

## Реактивная загрузка данных через `httpResource` {: #reactive-data-fetching-with-httpresource}

[`httpResource`](https://angular.dev/guide/http/http-resource) — обёртка над `HttpClient`: статус запроса и ответ доступны как сигналы. Запросы идут через HTTP-стек Angular, в том числе через перехватчики.

## Композиция ресурсов через снимки {: #resource-composition-with-snapshots}

`ResourceSnapshot` — структурированный снимок текущего состояния ресурса. У каждого ресурса есть свойство `snapshot`, сигнал с этим состоянием.

```ts
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params}) => fetchUser(params),
});

const userSnapshot = userResource.snapshot;
```

В снимке есть `status` и либо `value`, либо `error`.

### Сборка ресурсов из снимков {: #composing-resources-with-snapshots}

Новые ресурсы собирают из снимков функцией `resourceFromSnapshots`. Так поведение ресурса меняют через сигнальные API, например `computed` и `linkedSignal`.

```ts
import {linkedSignal, resourceFromSnapshots, Resource, ResourceSnapshot} from '@angular/core';

function withPreviousValue<T>(input: Resource<T>): Resource<T> {
  const derived = linkedSignal<ResourceSnapshot<T>, ResourceSnapshot<T>>({
    source: input.snapshot,
    computation: (snap, previous) => {
      if (snap.status === 'loading' && previous && previous.value.status !== 'error') {
        // When the input resource enters loading state, we keep the value
        // from its previous state, if any.
        return {status: 'loading' as const, value: previous.value.value};
      }

      // Otherwise we simply forward the state of the input resource.
      return snap;
    },
  });

  return resourceFromSnapshots(derived);
}

@Component({
  /*... */
})
export class AwesomeProfile {
  userId = input.required<number>();
  user = withPreviousValue(httpResource(() => `/user/${this.userId()}`));
  // When userId changes, user.value() keeps the old user data until the new one loads
}
```


---

Источник: [https://angular.dev/guide/signals/resource](https://angular.dev/guide/signals/resource)
