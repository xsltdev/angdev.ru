# Разрешение загрязнения зоны

:date: 4.05.2022

**Zone.js** — это сигнальный механизм, который Angular использует для обнаружения изменений состояния приложения. Он фиксирует асинхронные операции, такие как `setTimeout`, сетевые запросы и слушатели событий. Angular планирует обнаружение изменений на основе сигналов от Zone.js.

В некоторых случаях запланированные [задачи](https://developer.mozilla.org/docs/Web/API/HTML_DOM_API/Microtask_guide#tasks) или [микрозадачи](https://developer.mozilla.org/docs/Web/API/HTML_DOM_API/Microtask_guide#microtasks) не вносят никаких изменений в модель данных, что делает запуск обнаружения изменений ненужным. Общими примерами являются:

-   `requestAnimationFrame`, `setTimeout` или `setInterval`.
-   Планирование задач или микрозадач сторонними библиотеками.

В этом разделе рассказывается о том, как определить такие условия и как запускать код вне зоны Angular, чтобы избежать ненужных вызовов обнаружения изменений.

## Выявление ненужных вызовов обнаружения изменений

Вы можете обнаружить ненужные вызовы обнаружения изменений с помощью Angular DevTools. Часто они появляются в виде последовательных полос на временной шкале профилировщика с источником `setTimeout`, `setInterval`, `requestAnimationFrame` или обработчиком события. Если в вашем приложении вызовы этих API ограничены, вызов обнаружения изменений обычно вызван сторонней библиотекой.

![Angular DevTools profiler preview showing Zone pollution](zone-pollution.png)

На изображении выше показана серия вызовов обнаружения изменений, вызванных обработчиками событий, связанных с элементом. Это распространенная проблема при использовании сторонних, неродных компонентов Angular, которые не изменяют поведение `NgZone` по умолчанию.

## Запускать задачи вне `NgZone`.

В таких случаях вы можете указать Angular не вызывать обнаружение изменений для задач, запланированных данным элементом кода, используя `NgZone`.

```ts
import { Component, NgZone, OnInit } from '@angular/core';
@Component(/* ... */)
class AppComponent implements OnInit {
    constructor(private ngZone: NgZone) {}
    ngOnInit() {
        this.ngZone.runOutsideAngular(
            () => setInterval(pollForUpdates),
            500
        );
    }
}
```

Предыдущий фрагмент предписывает Angular вызывать `setInterval` вне Angular Zone и пропускать обнаружение изменений после выполнения `pollForUpdates`.

Сторонние библиотеки часто вызывают ненужные циклы обнаружения изменений, поскольку они не были разработаны с учетом Zone.js. Избегайте этих лишних циклов, вызывая API библиотеки вне зоны Angular:

```ts
import { Component, NgZone, OnInit } from '@angular/core';
import * as Plotly from 'plotly.js-dist-min';

@Component(/* ... */)
class AppComponent implements OnInit {
    constructor(private ngZone: NgZone) {}
    ngOnInit() {
        this.ngZone.runOutsideAngular(() => {
            Plotly.newPlot('chart', data);
        });
    }
}
```

Запуск `Plotly.newPlot('chart', data);` внутри `runOutsideAngular` инструктирует фреймворк, что он не должен запускать обнаружение изменений после выполнения задач, запланированных логикой инициализации.

Например, если `Plotly.newPlot('chart', data)` добавляет слушателей событий к элементу DOM, Angular не запускает обнаружение изменений после выполнения их обработчиков.
