---
description: Observables обеспечивают поддержку передачи сообщений между частями приложения. Они часто используются в Angular и служат для обработки событий, асинхронного программирования и работы с несколькими значениями
---

# Использование observables для передачи значений

:date: 28.02.2022

Observables обеспечивают поддержку передачи сообщений между частями приложения. Они часто используются в Angular и служат для обработки событий, асинхронного программирования и работы с несколькими значениями.

Паттерн наблюдателя — это паттерн проектирования программного обеспечения, в котором объект, называемый _субъектом_, ведет список своих зависимых объектов, называемых _наблюдателями_, и автоматически уведомляет их об изменении состояния. Этот паттерн похож (но не идентичен) на паттерн [publish/subscribe](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern).

Observables являются декларативными &mdash; то есть вы определяете функцию для публикации значений, но она не выполняется до тех пор, пока на нее не подпишется потребитель. Подписавшийся потребитель получает уведомления до тех пор, пока функция не завершится, или пока он не откажется от подписки.

Observables может передавать несколько значений любого типа &mdash; литералы, сообщения или события, в зависимости от контекста. API для получения значений одинаково, независимо от того, синхронно или асинхронно они передаются. Поскольку логика установки и удаления обрабатывается observables, код приложения должен быть озабочен только подпиской на потребление значений и отменой подписки. Будь то поток нажатий клавиш, HTTP-ответ или интервальный таймер, интерфейс для прослушивания значений и прекращения прослушивания одинаков.

Благодаря этим преимуществам observables широко используются в Angular, а также при разработке приложений.

## Основные способы использования и термины

В качестве издателя вы создаете экземпляр `Observable`, который определяет функцию _subscriber_. Именно эта функция выполняется, когда потребитель вызывает метод `subscribe()`. Функция подписчика определяет, как получать или генерировать значения или сообщения для публикации.

Чтобы запустить созданный observables и начать получать уведомления, необходимо вызвать его метод `subscribe()`, передав ему _observer_. Это объект JavaScript, определяющий обработчики получаемых уведомлений. Вызов `subscribe()` возвращает объект `Subscription`, имеющий метод `unsubscribe()`, который вызывается для прекращения получения уведомлений.

Приведем пример, демонстрирующий базовую модель использования, в котором показано, как observables можно использовать для предоставления обновлений геолокации.

```ts
// Create an Observable that will start listening to geolocation updates
// when a consumer subscribes.
const locations = new Observable((observer) => {
    let watchId: number;

    // Simple geolocation API check provides values to publish
    if ('geolocation' in navigator) {
        watchId = navigator.geolocation.watchPosition(
            (position: GeolocationPosition) => {
                observer.next(position);
            },
            (error: GeolocationPositionError) => {
                observer.error(error);
            }
        );
    } else {
        observer.error('Geolocation not available');
    }

    // When the consumer unsubscribes, clean up data ready for next subscription.
    return {
        unsubscribe() {
            navigator.geolocation.clearWatch(watchId);
        },
    };
});

// Call subscribe() to start listening for updates.
const locationsSubscription = locations.subscribe({
    next(position) {
        console.log('Current Position: ', position);
    },
    error(msg) {
        console.log('Error Getting Location: ', msg);
    },
});

// Stop listening for location after 10 seconds
setTimeout(() => {
    locationsSubscription.unsubscribe();
}, 10000);
```

## Определение наблюдателей

Обработчик для получения уведомлений от observables реализует интерфейс `Observer`.
Он представляет собой объект, определяющий методы обратного вызова для обработки трех типов уведомлений, которые может посылать observables:

| Тип уведомления | Подробности                                                                                                                                                          |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `next`          | Требуется. Обработчик для каждого доставленного значения. Вызывается ноль или более раз после начала выполнения.                                                     |
| `error`         | Необязательно. Обработчик уведомления об ошибке. Ошибка останавливает выполнение экземпляра observables.                                                             |
| `complete`      | Необязательно. Обработчик уведомления о завершении выполнения. Отложенные значения могут продолжать доставляться следующему обработчику после завершения выполнения. |

Объект наблюдателя может определять любую комбинацию этих обработчиков. Если обработчик для какого-либо типа уведомления не задан, то наблюдатель игнорирует уведомления этого типа.

## Подписка

Экземпляр `Observable` начинает публиковать значения только тогда, когда на него кто-то подписывается. Подписка осуществляется вызовом метода `subscribe()` экземпляра с передачей объекта наблюдателя для получения уведомлений.

!!!note ""

    Для того чтобы показать, как работает подписка, нам необходимо создать новую observables. Существует конструктор, который используется для создания новых экземпляров, но для иллюстрации мы можем воспользоваться некоторыми методами из библиотеки RxJS, которые создают простые observables часто используемых типов:

    | Методы RxJS      | Подробности                                                                                                                   |
    | :--------------- | :---------------------------------------------------------------------------------------------------------------------------- |
    | `of(...items)`   | Возвращает экземпляр `Observable`, который синхронно доставляет значения, указанные в качестве аргументов.                    |
    | `from(iterable)` | Преобразует свой аргумент в экземпляр `Observables`. Этот метод обычно используется для преобразования массива в observables. |

Приведем пример создания и подписки на простую observables с наблюдателем, который записывает полученное сообщение в консоль:

```ts
// Create simple observable that emits three values
const myObservable = of(1, 2, 3);

// Create observer object
const myObserver = {
    next: (x: number) =>
        console.log('Observer got a next value: ' + x),
    error: (err: Error) =>
        console.error('Observer got an error: ' + err),
    complete: () =>
        console.log('Observer got a complete notification'),
};

// Execute with the observer object
myObservable.subscribe(myObserver);

// Logs:
// Observer got a next value: 1
// Observer got a next value: 2
// Observer got a next value: 3
// Observer got a complete notification
```

В качестве альтернативы метод `subscribe()` может принимать определения функций обратного вызова в строке, для обработчиков `next`, `error` и `complete`. Например, следующий вызов `subscribe()` аналогичен вызову, задающему предопределенный наблюдатель:

```ts
myObservable.subscribe(
    (x) => console.log('Observer got a next value: ' + x),
    (err) => console.error('Observer got an error: ' + err),
    () =>
        console.log('Observer got a complete notification')
);
```

В любом случае требуется обработчик `next`. Обработчики `error` и `complete` являются необязательными.

!!!note ""

    Функция `next()` может принимать, например, строки сообщений, или объекты событий, числовые значения, или структуры, в зависимости от контекста. В общем случае мы называем данные, публикуемые observables, _потоком_. Любой тип значений может быть представлен с помощью observables, а сами значения публикуются в виде потока.

## Создание observables

Для создания потока observables любого типа используйте конструктор `Observable`. В качестве аргумента конструктор принимает функцию-подписчика, которая должна запускаться при выполнении метода `ubscribe()` наблюдаемой. Функция-подписчик получает объект `Observer` и может публиковать значения в метод `next()` наблюдателя.

Например, для создания observables, эквивалентных `of(1, 2, 3)`, описанным выше, можно поступить следующим образом:

```ts title="Создание observables с помощью конструктора"
// This function runs when subscribe() is called
function sequenceSubscriber(observer: Observer<number>) {
    // synchronously deliver 1, 2, and 3, then complete
    observer.next(1);
    observer.next(2);
    observer.next(3);
    observer.complete();

    // unsubscribe function doesn't need to do anything in this
    // because values are delivered synchronously
    return { unsubscribe() {} };
}

// Create a new Observable that will deliver the above sequence
const sequence = new Observable(sequenceSubscriber);

// execute the Observable and print the result of each notification
sequence.subscribe({
    next(num) {
        console.log(num);
    },
    complete() {
        console.log('Finished sequence');
    },
});

// Logs:
// 1
// 2
// 3
// Finished sequence
```

Если пойти еще дальше, то можно создать observables, которые публикуют события.
В этом примере функция подписчика определена inline.

```ts title="Создание с помощью пользовательской функции fromEvent"
function fromEvent<T extends keyof HTMLElementEventMap>(
    target: HTMLElement,
    eventName: T
) {
    return new Observable<HTMLElementEventMap[T]>(
        (observer) => {
            const handler = (e: HTMLElementEventMap[T]) =>
                observer.next(e);

            // Add the event handler to the target
            target.addEventListener(eventName, handler);

            return () => {
                // Detach the event handler from the target
                target.removeEventListener(
                    eventName,
                    handler
                );
            };
        }
    );
}
```

Теперь вы можете использовать эту функцию для создания observables, которые публикуют события нажатия клавиш:

```ts
const ESC_CODE = 'Escape';
const nameInput = document.getElementById(
    'name'
) as HTMLInputElement;

const subscription = fromEvent(
    nameInput,
    'keydown'
).subscribe((e: KeyboardEvent) => {
    if (e.code === ESC_CODE) {
        nameInput.value = '';
    }
});
```

## Мультикастинг

Типичный observables создает новое, независимое исполнение для каждого подписавшегося наблюдателя. Когда один наблюдатель подписывается, observables подключает обработчик события и передает значения этому наблюдателю. Когда на него подписывается второй наблюдатель, наблюдаемый подключает новый обработчик событий и передает значения этому второму наблюдателю в отдельном выполнении.

Иногда вместо того, чтобы начинать независимое выполнение для каждого подписчика, необходимо, чтобы каждый подписчик получал одни и те же значения &mdash; даже если значения уже начали выдаваться. Это может произойти, например, с observables кликов на объекте документа.

Многоадресная рассылка — это практика рассылки по списку нескольких подписчиков за одно выполнение. При использовании многоадресных observables вы не регистрируете несколько слушателей на документе, а используете первый слушатель и рассылаете значения каждому подписчику.

При создании observables вы должны определить, как вы хотите использовать эту observables и хотите ли вы передавать ее значения многократно.

Рассмотрим пример, который считает от 1 до 3 с задержкой в одну секунду после каждого выданного числа.

```ts
function sequenceSubscriber(observer: Observer<number>) {
    const seq = [1, 2, 3];
    let clearTimer: VoidFunction | undefined;

    // Will run through an array of numbers, emitting one value
    // per second until it gets to the end of the array.
    function doInSequence(arr: number[], idx: number) {
        const timeout = setTimeout(() => {
            observer.next(arr[idx]);
            if (idx === arr.length - 1) {
                observer.complete();
            } else {
                doInSequence(arr, ++idx);
            }
        }, 1000);
        clearTimer = () => clearTimeout(timeout);
    }

    doInSequence(seq, 0);

    // Unsubscribe should clear the timeout to stop execution
    return {
        unsubscribe() {
            clearTimer?.();
        },
    };
}

// Create a new Observable that will deliver the above sequence
const sequence = new Observable(sequenceSubscriber);

sequence.subscribe({
    next(num) {
        console.log(num);
    },
    complete() {
        console.log('Finished sequence');
    },
});

// Logs:
// (at 1 second): 1
// (at 2 seconds): 2
// (at 3 seconds): 3
// (at 3 seconds): Finished sequence
```

Обратите внимание, что если подписаться дважды, то будет два отдельных потока, каждый из которых будет выдавать значения каждую секунду. Выглядит это примерно так:

```ts
// Subscribe starts the clock, and will emit after 1 second
sequence.subscribe({
    next(num) {
        console.log('1st subscribe: ' + num);
    },
    complete() {
        console.log('1st sequence finished.');
    },
});

// After 1/2 second, subscribe again.
setTimeout(() => {
    sequence.subscribe({
        next(num) {
            console.log('2nd subscribe: ' + num);
        },
        complete() {
            console.log('2nd sequence finished.');
        },
    });
}, 500);

// Logs:
// (at 1 second): 1st subscribe: 1
// (at 1.5 seconds): 2nd subscribe: 1
// (at 2 seconds): 1st subscribe: 2
// (at 2.5 seconds): 2nd subscribe: 2
// (at 3 seconds): 1st subscribe: 3
// (at 3 seconds): 1st sequence finished
// (at 3.5 seconds): 2nd subscribe: 3
// (at 3.5 seconds): 2nd sequence finished
```

Изменение observables для многоадресной рассылки может выглядеть следующим образом:

```ts
function multicastSequenceSubscriber() {
    const seq = [1, 2, 3];
    // Keep track of each observer (one for every active subscription)
    const observers: Observer<unknown>[] = [];
    // Still a single timer because there will only ever be one
    // set of values being generated, multicasted to each subscriber
    let clearTimer: VoidFunction | undefined;

    // Return the subscriber function (runs when subscribe()
    // function is invoked)
    return (observer: Observer<unknown>) => {
        observers.push(observer);
        // When this is the first subscription, start the sequence
        if (observers.length === 1) {
            const multicastObserver: Observer<number> = {
                next(val) {
                    // Iterate through observers and notify all subscriptions
                    observers.forEach((obs) =>
                        obs.next(val)
                    );
                },
                error() {
                    /* Handle the error... */
                },
                complete() {
                    // Notify all complete callbacks
                    observers
                        .slice(0)
                        .forEach((obs) => obs.complete());
                },
            };
            doSequence(multicastObserver, seq, 0);
        }

        return {
            unsubscribe() {
                // Remove from the observers array so it's no longer notified
                observers.splice(
                    observers.indexOf(observer),
                    1
                );
                // If there's no more listeners, do cleanup
                if (observers.length === 0) {
                    clearTimer?.();
                }
            },
        };

        // Run through an array of numbers, emitting one value
        // per second until it gets to the end of the array.
        function doSequence(
            sequenceObserver: Observer<number>,
            arr: number[],
            idx: number
        ) {
            const timeout = setTimeout(() => {
                console.log('Emitting ' + arr[idx]);
                sequenceObserver.next(arr[idx]);
                if (idx === arr.length - 1) {
                    sequenceObserver.complete();
                } else {
                    doSequence(
                        sequenceObserver,
                        arr,
                        ++idx
                    );
                }
            }, 1000);
            clearTimer = () => clearTimeout(timeout);
        }
    };
}

// Create a new Observable that will deliver the above sequence
const multicastSequence = new Observable(
    multicastSequenceSubscriber()
);

// Subscribe starts the clock, and begins to emit after 1 second
multicastSequence.subscribe({
    next(num) {
        console.log('1st subscribe: ' + num);
    },
    complete() {
        console.log('1st sequence finished.');
    },
});

// After 1 1/2 seconds, subscribe again (should "miss" the first value).
setTimeout(() => {
    multicastSequence.subscribe({
        next(num) {
            console.log('2nd subscribe: ' + num);
        },
        complete() {
            console.log('2nd sequence finished.');
        },
    });
}, 1500);

// Logs:
// (at 1 second): Emitting 1
// (at 1 second): 1st subscribe: 1
// (at 2 seconds): Emitting 2
// (at 2 seconds): 1st subscribe: 2
// (at 2 seconds): 2nd subscribe: 2
// (at 3 seconds): Emitting 3
// (at 3 seconds): 1st subscribe: 3
// (at 3 seconds): 2nd subscribe: 3
// (at 3 seconds): 1st sequence finished
// (at 3 seconds): 2nd sequence finished
```

!!!note ""

    Многоадресные observables требуют немного больше настроек, но они могут быть полезны для некоторых приложений. Позже мы рассмотрим инструменты, упрощающие процесс многоадресной рассылки, позволяющие взять любую observables и сделать ее многоадресной.

## Обработка ошибок

Поскольку observables выдают значения асинхронно, try/catch не позволяет эффективно перехватывать ошибки. Вместо этого вы обрабатываете ошибки, указывая обратный вызов `error` на наблюдателе. Возникновение ошибки также приводит к тому, что observables очищает подписки и прекращает выдачу значений. Observables может либо выдавать значения (вызывая обратный вызов `next`), либо завершаться, вызывая обратный вызов `complete` или `error`.

```ts
myObservable.subscribe({
    next(num) {
        console.log('Next num: ' + num);
    },
    error(err) {
        console.log('Received an error: ' + err);
    },
});
```

Работа с ошибками (и, в частности, восстановление после ошибки) более подробно рассматривается в следующем разделе.

## Ссылки

-   [Using observables to pass values](https://angular.io/guide/observables)
