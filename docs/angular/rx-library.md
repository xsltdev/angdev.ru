---
description: Реактивное программирование — парадигма асинхронного программирования, связанная с потоками данных и распространением изменений
---

# Библиотека RxJS

:date: 28.02.2022

Реактивное программирование — парадигма асинхронного программирования, связанная с потоками данных и распространением изменений ([Wikipedia](https://en.wikipedia.org/wiki/Reactive_programming)). RxJS (Reactive Extensions for JavaScript) — это библиотека для реактивного программирования с использованием наблюдаемых значений, облегчающая создание асинхронного кода или кода, основанного на обратных вызовах. См. ([RxJS Docs](https://rxjs.dev/guide/overview)).

RxJS предоставляет реализацию типа `Observable`, которая необходима до тех пор, пока этот тип не станет частью языка и пока браузеры не будут его поддерживать. Библиотека также предоставляет служебные функции для создания и работы с наблюдаемыми значениями. Эти утилиты могут быть использованы для:

-   Преобразования существующего кода для асинхронных операций в наблюдаемые значения
-   Итерации значений в потоке
-   Сопоставления значений с различными типами
-   Фильтрации потоков
-   Компоновка нескольких потоков

## Функции создания наблюдаемых значений

RxJS предлагает ряд функций, которые можно использовать для создания новых наблюдаемых значений. Эти функции могут упростить процесс создания наблюдаемых значений из таких элементов, как события, таймеры и промисы. Например:

```ts title="Создание наблюдаемого значения из промиса"
import { from, Observable } from 'rxjs';

// Create an Observable out of a promise
const data = from(fetch('/api/endpoint'));
// Subscribe to begin listening for async result
data.subscribe({
    next(response) {
        console.log(response);
    },
    error(err) {
        console.error('Error: ' + err);
    },
    complete() {
        console.log('Completed');
    },
});
```

---

```ts title="Создание наблюдаемого значения из счетчика"
import { interval } from 'rxjs';

// Create an Observable that will publish a value on an interval
const secondsCounter = interval(1000);
// Subscribe to begin publishing values
const subscription = secondsCounter.subscribe((n) =>
    console.log(
        `It's been ${n + 1} seconds since subscribing!`
    )
);
```

---

```ts title="Создание наблюдаемого значения из события"
import { fromEvent } from 'rxjs';

const el = document.getElementById('my-element')!;

// Create an Observable that will publish mouse movements
const mouseMoves = fromEvent<MouseEvent>(el, 'mousemove');

// Subscribe to start listening for mouse-move events
const subscription = mouseMoves.subscribe((evt) => {
    // Log coords of mouse movements
    console.log(`Coords: ${evt.clientX} X ${evt.clientY}`);

    // When the mouse is over the upper-left of the screen,
    // unsubscribe to stop listening for mouse movements
    if (evt.clientX < 40 && evt.clientY < 40) {
        subscription.unsubscribe();
    }
});
```

---

```ts title="Создайте наблюдаемое значение, создающее AJAX-запрос"
import { Observable } from 'rxjs';
import { ajax } from 'rxjs/ajax';

// Create an Observable that will create an AJAX request
const apiData = ajax('/api/data');
// Subscribe to create the request
apiData.subscribe((res) =>
    console.log(res.status, res.response)
);
```

## Операторы

Операторы — это функции, построенные на основе наблюдаемых значений и позволяющие выполнять сложные манипуляции с коллекциями. Например, в RxJS определены такие операторы, как `map()`, `filter()`, `concat()` и `flatMap()`.

Операторы принимают параметры конфигурации и возвращают функцию, принимающую исходное наблюдаемое значение. При выполнении возвращаемой функции оператор наблюдает излучаемые исходным наблюдаемым значения, преобразует их и возвращает новое наблюдаемое значение, состоящее из этих преобразованных значений. Приведем простой пример:

```ts
import { of } from 'rxjs';
import { map } from 'rxjs/operators';

const nums = of(1, 2, 3);

const squareValues = map((val: number) => val * val);
const squaredNums = squareValues(nums);

squaredNums.subscribe((x) => console.log(x));

// Logs
// 1
// 4
// 9
```

Для соединения операторов между собой можно использовать _трубы_. Пайпы позволяют объединить несколько функций в одну. Функция `пайп()` принимает в качестве аргументов функции, которые необходимо объединить, и возвращает новую функцию, которая при выполнении запускает составленные функции в последовательности.

Набор операторов, применяемых к наблюдаемому значению, является рецептом &mdash; то есть набором инструкций для получения интересующих вас значений. Сам по себе рецепт ничего не делает. Для получения результата через рецепт необходимо вызвать `subscribe()`.

Приведем пример:

```ts
import { of, pipe } from 'rxjs';
import { filter, map } from 'rxjs/operators';

const nums = of(1, 2, 3, 4, 5);

// Create a function that accepts an Observable.
const squareOddVals = pipe(
    filter((n: number) => n % 2 !== 0),
    map((n) => n * n)
);

// Create an Observable that will run the filter and map functions
const squareOdd = squareOddVals(nums);

// Subscribe to run the combined functions
squareOdd.subscribe((x) => console.log(x));
```

Функция `pipe()` также является методом RxJS `Observable`, поэтому для определения той же операции используется более короткая форма:

```ts
import { of } from 'rxjs';
import { filter, map } from 'rxjs/operators';

const squareOdd = of(1, 2, 3, 4, 5).pipe(
    filter((n) => n % 2 !== 0),
    map((n) => n * n)
);

// Subscribe to get values
squareOdd.subscribe((x) => console.log(x));
```

### Общие операторы

RxJS предоставляет множество операторов, но только некоторые из них используются часто. Список операторов и примеры их использования можно найти в [RxJS API Documentation](https://rxjs.dev/api).

!!!note ""

    Для Angular-приложений мы предпочитаем использовать не цепочку, а комбинацию операторов с пайпами. Цепочка используется во многих примерах RxJS.

| Область        | Операторы                                                                 |
| :------------- | :------------------------------------------------------------------------ |
| Создание       | `from`, `fromEvent`, `of`                                                 |
| Комбинирование | `combineLatest`, `concat`, `merge`, `startWith` , `withLatestFrom`, `zip` |
| Фильтрация     | `debounceTime`, `distinctUntilChanged`, `filter`, `take`, `takeUntil`     |
| Трансформация  | `bufferTime`, `concatMap`, `map`, `mergeMap`, `scan`, `switchMap`         |
| Утилита        | `tap`                                                                     |
| Мультикастинг  | `share`                                                                   |

## Обработка ошибок

В дополнение к обработчику `error()`, предоставляемому по подписке, RxJS предоставляет оператор `catchError`, позволяющий обрабатывать известные ошибки в рецепте наблюдаемого значения.

Например, предположим, что у вас есть наблюдаемое значение, которое выполняет API-запрос и сопоставляется с ответом сервера. Если сервер возвращает ошибку или значение не существует, то выдается ошибка. Если вы поймаете эту ошибку и предоставите значение по умолчанию, ваш поток продолжит обрабатывать значения, а не будет выходить из строя.

Вот пример использования оператора `catchError` для этого:

```ts
import { Observable, of } from 'rxjs';
import { ajax } from 'rxjs/ajax';
import { map, catchError } from 'rxjs/operators';

// Return "response" from the API. If an error happens,
// return an empty array.
const apiData = ajax('/api/data').pipe(
    map((res: any) => {
        if (!res.response) {
            throw new Error('Value expected!');
        }
        return res.response;
    }),
    catchError(() => of([]))
);

apiData.subscribe({
    next(x: T) {
        console.log('data: ', x);
    },
    error() {
        console.log(
            'errors already caught... will not run'
        );
    },
});
```

### Повторное выполнение неудачного наблюдаемого значения

Если оператор `catchError` обеспечивает простой путь восстановления, то оператор `retry` позволяет повторить неудачный запрос.

Используйте оператор `retry` перед оператором `catchError`. Он переподписывается на исходное наблюдаемое значение, которое затем может повторно выполнить всю последовательность действий, приведших к ошибке. Если она включает в себя HTTP-запрос, то будет повторно выполнен этот HTTP-запрос.

Ниже приводится преобразование предыдущего примера для повторного выполнения запроса перед отлавливанием ошибки:

```ts
import { Observable, of } from 'rxjs';
import { ajax } from 'rxjs/ajax';
import { map, retry, catchError } from 'rxjs/operators';

const apiData = ajax('/api/data').pipe(
    map((res: any) => {
        if (!res.response) {
            console.log('Error occurred.');
            throw new Error('Value expected!');
        }
        return res.response;
    }),
    retry(3), // Retry up to 3 times before failing
    catchError(() => of([]))
);

apiData.subscribe({
    next(x: T) {
        console.log('data: ', x);
    },
    error() {
        console.log(
            'errors already caught... will not run'
        );
    },
});
```

!!!note ""

    Не повторяйте **аутентификационные** запросы, поскольку они должны инициироваться только действиями пользователя. Мы не хотим блокировать учетные записи пользователей повторными запросами на вход в систему, которые пользователь не инициировал.

## Соглашения об именовании наблюдаемых значений

Поскольку приложения Angular в основном пишутся на TypeScript, вы обычно знаете, что переменная имеет наблюдаемое значение. Хотя фреймворк Angular не применяет соглашение об именовании наблюдаемых значений, часто можно встретить названия наблюдаемых значений с завершающим знаком "\$".

Это может быть полезно при сканировании кода в поисках наблюдаемых значений. Кроме того, если вы хотите, чтобы свойство хранило самое последнее значение наблюдаемого значения, удобно использовать одно и то же имя со знаком "\$" или без него.

Например:

```ts
import { Component } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
    selector: 'app-stopwatch',
    templateUrl: './stopwatch.component.html',
})
export class StopwatchComponent {
    stopwatchValue = 0;
    stopwatchValue$!: Observable<number>;

    start() {
        this.stopwatchValue$.subscribe(
            (num) => (this.stopwatchValue = num)
        );
    }
}
```

## Ссылки

-   [The RxJS library](https://angular.io/guide/rx-library)
