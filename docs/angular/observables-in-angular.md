# Наблюдаемые значения в Angular

:date: 28.02.2022

Angular использует наблюдаемые значения в качестве интерфейса для обработки множества распространенных асинхронных операций. Например:

-   Модуль HTTP использует наблюдаемые значения для обработки AJAX-запросов и ответов
-   Модули Router и Forms используют наблюдаемые значения для прослушивания и реагирования на события, связанные с вводом данных пользователем

## Передача данных между компонентами

Angular предоставляет класс `EventEmitter`, который используется при публикации значений из компонента через декоратор [`@Output()`](inputs-outputs.md#output). `EventEmitter` расширяет [RxJS `Subject`](https://rxjs.dev/api/index/class/Subject), добавляя метод `emit()`, чтобы можно было отправлять произвольные значения. Когда вы вызываете `emit()`, он передает переданное значение методу `next()` любого подписанного наблюдателя.

Хороший пример использования можно найти в документации [EventEmitter](https://angular.io/api/core/EventEmitter). Здесь приведен пример компонента, который прослушивает события открытия и закрытия:

```ts
<app-zippy (open)="onOpen($event)" (close)="onClose($event)"></app-zippy>
```

Вот определение компонента:

```ts
@Component({
    selector: 'app-zippy',
    template: `
        <div class="zippy">
            <button type="button" (click)="toggle()">
                Toggle
            </button>
            <div [hidden]="!visible">
                <ng-content></ng-content>
            </div>
        </div>
    `,
})
export class ZippyComponent {
    visible = true;
    @Output() open = new EventEmitter<any>();
    @Output() close = new EventEmitter<any>();

    toggle() {
        this.visible = !this.visible;
        if (this.visible) {
            this.open.emit(null);
        } else {
            this.close.emit(null);
        }
    }
}
```

## HTTP

Angular `HttpClient` возвращает наблюдаемые значения из вызовов HTTP-методов. Например, `http.get('/api')` возвращает наблюдаемое значение. Это дает ряд преимуществ по сравнению с HTTP API, основанными на промисах:

-   Наблюдаемые значения не изменяют ответ сервера (как это может происходить при цепочке вызовов `.then()` на промисах).

    Вместо этого можно использовать ряд операторов для преобразования значений по мере необходимости.

-   HTTP-запросы можно отменить с помощью метода `unsubscribe()`.
-   Запросы могут быть настроены на получение обновлений о событиях выполнения
-   Неудачные запросы могут быть легко повторены

## Асинхронный пайп

[AsyncPipe](https://angular.io/api/common/AsyncPipe) подписывается на наблюдаемое значение или промис и возвращает последнее выданное им значение. Когда выдается новое значение, пайп помечает компонент для проверки на изменения.

В следующем примере наблюдаемое значение `time` привязывается к представлению компонента. Наблюдаемое значение постоянно обновляет представление текущим временем.

```ts
@Component({
    selector: 'async-observable-pipe',
    template: `<div>
        <code>observable|async</code>: Time:
        {{ time | async }}
    </div>`,
})
export class AsyncObservablePipeComponent {
    time = new Observable<string>((observer) => {
        setInterval(
            () => observer.next(new Date().toString()),
            1000
        );
    });
}
```

## Router

[`Router.events`](https://angular.io/api/router/Router#events) предоставляет события в виде наблюдаемых значений. Вы можете использовать оператор `filter()` из RxJS для поиска интересующих вас событий и подписки на них, чтобы принимать решения, основанные на последовательности событий в процессе навигации. Приведем пример:

```ts
import { Router, NavigationStart } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({
    selector: 'app-routable',
    template: 'Routable1Component template',
})
export class Routable1Component implements OnInit {
    navStart: Observable<NavigationStart>;

    constructor(router: Router) {
        // Create a new Observable that publishes only the NavigationStart event
        this.navStart = router.events.pipe(
            filter((evt) => evt instanceof NavigationStart)
        ) as Observable<NavigationStart>;
    }

    ngOnInit() {
        this.navStart.subscribe(() =>
            console.log('Navigation Started!')
        );
    }
}
```

[ActivatedRoute](https://angular.io/api/router/ActivatedRoute) — это инжектируемый сервис маршрутизатора, использующий наблюдаемые значения для получения информации о пути маршрута и параметрах. Например, `ActivatedRoute.url` содержит наблюдаемое значение, сообщающее о пути или путях маршрута. Вот пример:

```ts
import { ActivatedRoute } from '@angular/router';

@Component({
    selector: 'app-routable',
    template: 'Routable2Component template',
})
export class Routable2Component implements OnInit {
    constructor(private activatedRoute: ActivatedRoute) {}

    ngOnInit() {
        this.activatedRoute.url.subscribe((url) =>
            console.log('The URL changed to: ' + url)
        );
    }
}
```

## Реактивные формы

Реактивные формы имеют свойства, использующие наблюдаемые значения для отслеживания значений элементов управления формой. Свойства [`FormControl`](https://angular.io/api/forms/FormControl) `valueChanges` и `statusChanges` содержат наблюдаемые значения, вызывающие события изменения. Подписка на наблюдаемое значение свойства элемента управления формой позволяет задействовать прикладную логику в классе компонента. Например:

```ts
import { FormGroup } from '@angular/forms';

@Component({
    selector: 'my-component',
    template: 'MyComponent Template',
})
export class MyComponent implements OnInit {
    nameChangeLog: string[] = [];
    heroForm!: FormGroup;

    ngOnInit() {
        this.logNameChange();
    }
    logNameChange() {
        const nameControl = this.heroForm.get('name');
        nameControl?.valueChanges.forEach((value: string) =>
            this.nameChangeLog.push(value)
        );
    }
}
```

## Ссылки

-   [Observables in Angular](https://angular.io/guide/observables-in-angular)
