---
description: Приведем несколько примеров областей, в которых наблюдаемые значения особенно полезны
---

# Практическое использование наблюдаемых значений

:date: 28.02.2022

Приведем несколько примеров областей, в которых наблюдаемые значения особенно полезны.

## Предложения с опережением типа

Наблюдаемые значения могут упростить реализацию предложений с заголовочными типами. Как правило, для этого необходимо выполнить ряд отдельных задач:

-   Прослушать данные, поступающие на вход
-   Обрезать значение (удалить пробелы) и убедиться, что оно имеет минимальную длину
-   Отставание (чтобы не посылать API-запросы на каждое нажатие клавиши, а дождаться паузы в нажатиях)
-   Не отправлять запрос, если значение остается неизменным (например, быстро нажимается символ, затем backspace)
-   Отменять текущие AJAX-запросы, если их результаты будут аннулированы обновленными результатами.

Написать все это на JavaScript может быть довольно сложно. С помощью наблюдаемых значений можно использовать простую серию операторов RxJS:

```ts
import { fromEvent, Observable } from 'rxjs';
import { ajax } from 'rxjs/ajax';
import {
    debounceTime,
    distinctUntilChanged,
    filter,
    map,
    switchMap,
} from 'rxjs/operators';

const searchBox = document.getElementById(
    'search-box'
) as HTMLInputElement;

const typeahead = fromEvent(searchBox, 'input').pipe(
    map((e) => (e.target as HTMLInputElement).value),
    filter((text) => text.length > 2),
    debounceTime(10),
    distinctUntilChanged(),
    switchMap((searchTerm) =>
        ajax(`/api/endpoint?search=${searchTerm}`)
    )
);

typeahead.subscribe((data) => {
    // Handle the data from the API
});
```

## Экспоненциальный откат

Экспоненциальный откат - это метод, при котором повторные попытки выполнения запроса к API выполняются после неудачи, причем время между попытками увеличивается после каждой последующей неудачи, а максимальное количество попыток, после которых запрос считается неудачным. Это может быть довольно сложно реализовать с помощью промисов и других методов отслеживания вызовов AJAX. С помощью наблюдаемых значений это очень просто:

```ts
import { timer } from 'rxjs';
import { ajax } from 'rxjs/ajax';
import { retry } from 'rxjs/operators';

export function backoff(
    maxTries: number,
    initialDelay: number
) {
    return retry({
        count: maxTries,
        delay: (error, retryCount) =>
            timer(initialDelay * retryCount ** 2),
    });
}

ajax('/api/endpoint')
    .pipe(backoff(3, 250))
    .subscribe(function handleData(data) {
        /* ... */
    });
```

## Ссылки

-   [Practical observable usage](https://angular.io/guide/practical-observable-usage)
