---
description: Компонент HeroesComponent в Туре Героев получает и отображает поддельные данные
---

# Добавить сервисы

:date: 28.02.2022

Компонент `HeroesComponent` в Туре Героев получает и отображает поддельные данные.

Рефакторинг `HeroesComponent` сосредоточен на поддержке представления и облегчении юнит-тестирования с помощью имитационного сервиса.

!!!note ""

    Пример приложения, которое описывается на этой странице, см.:

    -   [Живой пример](https://angular.io/generated/live-examples/toh-pt4/stackblitz.html)
    -   [Скачать](https://angular.io/generated/zips/toh-pt4/toh-pt4.zip)

## Почему сервисы

Компоненты не должны получать или сохранять данные напрямую и уж точно не должны представлять заведомо ложные данные. Они должны сосредоточиться на представлении данных и делегировать доступ к ним сервису.

В этом руководстве создается `HeroService`, который все классы приложения могут использовать для получения героев. Вместо того чтобы создавать сервис с помощью ключевого слова [`new`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/new), используйте [_dependency injection_](dependency-injection.md), который поддерживает Angular, чтобы внедрить его в конструктор `HeroesComponent`.

Сервисы — это отличный способ обмена информацией между классами, которые _не знают друг друга_. Создайте следующий `MessageService` и инжектируйте его в эти два места.

-   Inject в `HeroService`, который использует сервис для отправки сообщения

-   Вставьте в `MessagesComponent`, который отображает это сообщение, а также отображает ID, когда пользователь нажимает на героя.

## Создайте `HeroService`

Запустите `ng generate` для создания сервиса под названием `hero`.

```shell
ng generate service hero
```

Команда генерирует скелет класса `HeroService` в `src/app/hero.service.ts` следующим образом:

```ts
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class HeroService {
    constructor() {}
}
```

### `@Injectable()` сервисы

Обратите внимание, что новый сервис импортирует символ Angular `Injectable` и аннотирует класс декоратором `@Injectable()`. Это отмечает класс как участвующий в системе _инъекции зависимостей_. Класс `HeroService` будет предоставлять инжектируемый сервис, и он также может иметь свои собственные инжектируемые зависимости.

Пока у него нет никаких зависимостей.

Декоратор `@Injectable()` принимает объект метаданных для сервиса, так же, как декоратор `@Component()` для ваших классов компонентов.

### Получение данных героя

Сервис `HeroService` может получать данные героя откуда угодно, например, из веб-сервиса, локального хранилища или имитируемого источника данных.

Удаление доступа к данным из компонентов означает, что вы можете в любой момент изменить свое мнение о реализации, не трогая никаких компонентов. Они не знают, как работает сервис.

Реализация в _этом_ учебнике продолжает предоставлять _макет героев_.

Импортируйте `Hero` и `HEROES`.

```ts
import { Hero } from './hero';
import { HEROES } from './mock-heroes';
```

Добавьте метод `getHeroes`, чтобы вернуть _макет героев_.

```ts
getHeroes(): Hero[] {
  return HEROES;
}
```

## Предоставьте `HeroService` {#provide}

Вы должны сделать `HeroService` доступным для системы инъекции зависимостей, прежде чем Angular сможет _инжектировать_ его в `HeroesComponent`, зарегистрировав _провайдера_. Провайдер — это то, что может создавать или предоставлять услугу. В данном случае он инстанцирует класс `HeroService` для предоставления услуги.

Чтобы убедиться, что `HeroService` может предоставить эту услугу, зарегистрируйте его с помощью _инжектора_. Инжектор — это объект, который выбирает и внедряет провайдера там, где это требуется приложению.

По умолчанию `ng generate service` регистрирует провайдера с _корневым инжектором_ для вашего сервиса, включая метаданные провайдера, это `providedIn: 'root'` в декораторе `@Injectable()`.

```ts
@Injectable({
  providedIn: 'root',
})
```

Когда вы предоставляете сервис на корневом уровне, Angular создает единственный, общий экземпляр `HeroService` и внедряет его в любой класс, который его запрашивает. Регистрация провайдера в метаданных `@Injectable` также позволяет Angular оптимизировать приложение, удаляя сервис, если он не используется.

!!!note ""

    Чтобы узнать больше о провайдерах, смотрите раздел [Провайдеры](providers.md). Чтобы узнать больше об инжекторах, см. руководство [Dependency Injection guide](dependency-injection.md).

Теперь `HeroService` готов к подключению к `HeroesComponent`.

!!!warning ""

    Это промежуточный пример кода, который позволяет вам предоставлять и использовать `HeroService`. На данном этапе код отличается от `HeroService` в [финальном обзоре кода](#final-code-review).

## Обновление `HeroesComponent`

Откройте файл класса `HeroesComponent`.

Удалите импорт `HEROES`, потому что он вам больше не понадобится. Вместо этого импортируйте `HeroService`.

```ts
import { HeroService } from '../hero.service';
```

Замените определение свойства `heroes` объявлением.

```ts
heroes: Hero[] = [];
```

### Инжектируйте `HeroService` {#inject}

Добавьте приватный параметр `heroService` типа `HeroService` в конструктор.

```ts
constructor(private heroService: HeroService) {}
```

Параметр одновременно определяет частное свойство `heroService` и идентифицирует его как место инъекции `HeroService`.

Когда Angular создает `HeroesComponent`, система [Dependency Injection](dependency-injection.md) устанавливает параметр `heroService` в синглтон экземпляра `HeroService`.

### Добавьте `getHeroes()`

Создайте метод для получения героев из сервиса.

```ts
getHeroes(): void {
  this.heroes = this.heroService.getHeroes();
}
```

### Вызовите его в `ngOnInit()` {#oninit}

Хотя вы можете вызвать `getHeroes()` в конструкторе, это не лучшая практика.

Оставьте конструктор для минимальной инициализации, например, для подключения параметров конструктора к свойствам. Конструктор не должен _делать ничего_.

Он определенно не должен вызывать функцию, которая делает HTTP-запросы к удаленному серверу, как это сделала бы _реальная_ служба данных.

Вместо этого вызовите `getHeroes()` внутри [_ngOnInit lifecycle hook_](lifecycle-hooks.md) и позвольте Angular вызвать `ngOnInit()` в подходящее время _после_ создания экземпляра `HeroesComponent`.

```ts
ngOnInit(): void {
  this.getHeroes();
}
```

### Посмотрите, как это работает

После обновления браузера приложение должно работать как прежде, показывая список героев и подробное представление героя, когда вы нажимаете на имя героя.

## Наблюдаемые данные

Метод `HeroService.getHeroes()` имеет _синхронную подпись_, что подразумевает, что `HeroService` может получать героев синхронно. Компонент `HeroesComponent` потребляет результат `getHeroes()`, как если бы герои могли быть получены синхронно.

```ts
this.heroes = this.heroService.getHeroes();
```

Этот подход не будет работать в реальном приложении, использующем асинхронные вызовы. Сейчас он работает, потому что ваш сервис синхронно возвращает _макет героев_.

Если `getHeroes()` не может немедленно вернуться с данными о героях, он не должен быть синхронным, потому что это заблокирует браузер в ожидании возврата данных.

У `HeroService.getHeroes()` должна быть какая-то _асинхронная подпись_.

В этом руководстве `HeroService.getHeroes()` возвращает `Observable`, чтобы можно было использовать метод Angular `HttpClient.get` для получения героев

и чтобы [`HttpClient.get()`](understanding-communicating-with-http.md) возвращал `Observable`.

### Observable `HeroService`

`Observable` является одним из ключевых классов в [библиотеке RxJS](../rxjs/about.md).

В [учебнике по HTTP](toh-pt6.md) вы можете увидеть, как методы Angular `HttpClient` возвращают объекты RxJS `Observable`. Этот учебник имитирует получение данных с сервера с помощью функции RxJS `of()`.

Откройте файл `HeroService` и импортируйте символы `Observable` и `of` из RxJS.

```ts
import { Observable, of } from 'rxjs';
```

Замените метод `getHeroes()` на следующий:

```ts
getHeroes(): Observable<Hero[]> {
  const heroes = of(HEROES);
  return heroes;
}
```

`of(HEROES)` возвращает `Observable<Hero[]>`, который выдает _единственное значение_, массив подражаемых героев.

!!!note ""

    В [HTTP tutorial](toh-pt6.md) показано, как вызвать `HttpClient.get<Hero[]>()`, который также возвращает `Observable<Hero[]>`, выдающий _единственное значение_, массив героев из тела HTTP-ответа.

### Подписаться в `HeroesComponent`

Метод `HeroService.getHeroes` раньше возвращал `Hero[]`. Теперь он возвращает `Observable<Hero[]>`.

Вам нужно настроить свое приложение для работы с этим изменением в `HeroesComponent`.

Найдите метод `getHeroes` и замените его следующим кодом. новый код показан рядом с текущей версией для сравнения.

=== "heroes.component.ts (Observable)"

```ts
getHeroes(): void {
  this.heroService.getHeroes()
      .subscribe(heroes => this.heroes = heroes);
}
```

=== "heroes.component.ts (Original)"

```ts
getHeroes(): void {
  this.heroes = this.heroService.getHeroes();
}
```

Критическим отличием является `Observable.subscribe()`.

В предыдущей версии массив героев присваивается свойству `heroes` компонента. Присвоение происходит _синхронно_, как будто сервер может вернуть героев мгновенно или браузер может заморозить пользовательский интерфейс в ожидании ответа сервера.

Это _не работает_, когда `HeroService` действительно делает запросы к удаленному серверу.

Новая версия ждет, пока `Observable` не выдаст массив героев, что может произойти сейчас или через несколько минут. Метод `subscribe()` передает массив героев в обратный вызов,

который устанавливает свойство компонента `heroes`.

Этот асинхронный подход _работает_, когда `HeroService` запрашивает героев с сервера.

## Показать сообщения

Этот раздел поможет вам сделать следующее:

-   Добавление компонента `MessagesComponent`, который отображает сообщения приложения в нижней части экрана.
-   Создание инжектируемого, общеприкладного `MessageService` для отправки сообщений на экран
-   Инжектирование `MessageService` в `HeroService`.
-   Отображение сообщения, когда `HeroService` успешно получает героев

### Создайте `MessagesComponent`

Используйте `ng generate` для создания `MessagesComponent`.

```shell
ng generate component messages
```

`ng generate` создает файлы компонента в каталоге `src/app/messages` и объявляет `MessagesComponent` в `AppModule`.

Отредактируйте шаблон `AppComponent` для отображения `MessagesComponent`.

```html
<h1>{{title}}</h1>
<app-heroes></app-heroes>
<app-messages></app-messages>
```

Вы должны увидеть параграф по умолчанию из `MessagesComponent` в нижней части страницы.

### Создайте `MessageService`

Используйте `ng generate` для создания `MessageService` в `src/app`.

```shell
ng generate service message
```

Откройте `MessageService` и замените его содержимое на следующее.

```ts
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class MessageService {
    messages: string[] = [];

    add(message: string) {
        this.messages.push(message);
    }

    clear() {
        this.messages = [];
    }
}
```

Сервис раскрывает свой кэш `messages` и два метода:

-   Один для `add()` сообщения в кэш.
-   Другой — для `clear()` кэша.

### Вставьте его в `HeroService` {#inject-message-service}

В `HeroService` импортируйте `MessageService`.

```ts
import { MessageService } from './message.service';
```

Отредактируйте конструктор с параметром, который объявляет приватное свойство `messageService`. Angular инжектирует синглтон `MessageService` в это свойство при создании `HeroService`.

```ts
constructor(private messageService: MessageService) { }
```

!!!note ""

    Это пример типичного сценария _сервис в сервисе_, в котором вы вводите `MessageService` в `HeroService`, который вводится в `HeroesComponent`.

### Отправка сообщения из `HeroService`

Отредактируйте метод `getHeroes()` для отправки сообщения при получении героев.

```ts
getHeroes(): Observable<Hero[]> {
  const heroes = of(HEROES);
  this.messageService.add('HeroService: fetched heroes');
  return heroes;
}
```

### Отображение сообщения от `HeroService`

Компонент `MessagesComponent` должен отображать все сообщения, включая сообщение, отправленное `HeroService` при получении героев.

Откройте `MessagesComponent` и импортируйте `MessageService`.

```ts
import { MessageService } from '../message.service';
```

Отредактируйте конструктор с параметром, который объявляет **публичное** свойство `messageService`. Angular инжектирует синглтон `MessageService` в это свойство при создании `MessagesComponent`.

```ts
constructor(public messageService: MessageService) {}
```

Свойство `messageService` **должно быть public**, потому что вы собираетесь привязать его к шаблону.

!!!warning ""

    Angular привязывается только к _публичным_ свойствам компонентов.

### Привязка к `MessageService`

Замените шаблон `MessagesComponent`, созданный `ng generate`, на следующий.

```html
<div *ngIf="messageService.messages.length">
    <h2>Messages</h2>
    <button
        type="button"
        class="clear"
        (click)="messageService.clear()"
    >
        Clear messages
    </button>
    <div *ngFor="let message of messageService.messages">
        {{message}}
    </div>
</div>
```

Этот шаблон напрямую связывается с `messageService` компонента.

|                                           | Подробности                                                                       |
| :---------------------------------------- | :-------------------------------------------------------------------------------- |
| `*ngIf`                                   | Отображать область сообщений только в том случае, если есть сообщения для показа. |
| `*ngFor`                                  | Представляет список сообщений в повторяющихся элементах `<div>`.                  |
| Angular [event binding](event-binding.md) | Связывает событие нажатия кнопки с `MessageService.clear()`.                      |

Сообщения выглядят лучше после добавления частных CSS-стилей в `messages.component.css`, как указано в одной из вкладок ["final code review"](#final-code-review) ниже.

## Добавление сервиса MessageService в компонент HeroesComponent

В следующем примере показано, как отобразить историю каждого нажатия пользователем на героя. Это поможет при переходе к следующему разделу [Routing](toh-pt5.md).

```ts
import { Component, OnInit } from '@angular/core';

import { Hero } from '../hero';
import { HeroService } from '../hero.service';
import { MessageService } from '../message.service';

@Component({
    selector: 'app-heroes',
    templateUrl: './heroes.component.html',
    styleUrls: ['./heroes.component.css'],
})
export class HeroesComponent implements OnInit {
    selectedHero?: Hero;

    heroes: Hero[] = [];

    constructor(
        private heroService: HeroService,
        private messageService: MessageService
    ) {}

    ngOnInit(): void {
        this.getHeroes();
    }

    onSelect(hero: Hero): void {
        this.selectedHero = hero;
        this.messageService.add(
            `HeroesComponent: Selected hero id=${hero.id}`
        );
    }

    getHeroes(): void {
        this.heroService
            .getHeroes()
            .subscribe((heroes) => (this.heroes = heroes));
    }
}
```

Обновите браузер, чтобы увидеть список героев, и прокрутите страницу вниз, чтобы увидеть сообщения от HeroService. Каждый раз, когда вы нажимаете на героя, появляется новое сообщение для записи выбора.

Используйте кнопку **Очистить сообщения**, чтобы очистить историю сообщений.

## Окончательный обзор кода {#final-code-review}

Вот файлы кода, обсуждаемые на этой странице.

=== "src/app/hero.service.ts"

    ```ts
    import { Injectable } from '@angular/core';

    import { Observable, of } from 'rxjs';

    import { Hero } from './hero';
    import { HEROES } from './mock-heroes';
    import { MessageService } from './message.service';

    @Injectable({
    	providedIn: 'root',
    })
    export class HeroService {
    	constructor(private messageService: MessageService) {}

    	getHeroes(): Observable<Hero[]> {
    		const heroes = of(HEROES);
    		this.messageService.add(
    			'HeroService: fetched heroes'
    		);
    		return heroes;
    	}
    }
    ```

=== "src/app/message.service.ts"

    ```ts
    import { Injectable } from '@angular/core';

    @Injectable({
    	providedIn: 'root',
    })
    export class MessageService {
    	messages: string[] = [];

    	add(message: string) {
    		this.messages.push(message);
    	}

    	clear() {
    		this.messages = [];
    	}
    }
    ```

=== "src/app/heroes/heroes.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';

    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';
    import { MessageService } from '../message.service';

    @Component({
    	selector: 'app-heroes',
    	templateUrl: './heroes.component.html',
    	styleUrls: ['./heroes.component.css'],
    })
    export class HeroesComponent implements OnInit {
    	selectedHero?: Hero;

    	heroes: Hero[] = [];

    	constructor(
    		private heroService: HeroService,
    		private messageService: MessageService
    	) {}

    	ngOnInit(): void {
    		this.getHeroes();
    	}

    	onSelect(hero: Hero): void {
    		this.selectedHero = hero;
    		this.messageService.add(
    			`HeroesComponent: Selected hero id=${hero.id}`
    		);
    	}

    	getHeroes(): void {
    		this.heroService
    			.getHeroes()
    			.subscribe((heroes) => (this.heroes = heroes));
    	}
    }
    ```

=== "src/app/messages/messages.component.ts"

    ```ts
    import { Component } from '@angular/core';
    import { MessageService } from '../message.service';

    @Component({
    	selector: 'app-messages',
    	templateUrl: './messages.component.html',
    	styleUrls: ['./messages.component.css'],
    })
    export class MessagesComponent {
    	constructor(public messageService: MessageService) {}
    }
    ```

=== "src/app/messages/messages.component.html"

    ```html
    <div *ngIf="messageService.messages.length">
    	<h2>Messages</h2>
    	<button
    		type="button"
    		class="clear"
    		(click)="messageService.clear()"
    	>
    		Clear messages
    	</button>
    	<div *ngFor="let message of messageService.messages">
    		{{message}}
    	</div>
    </div>
    ```

=== "src/app/messages/messages.component.css"

    ```css
    /* MessagesComponent's private CSS styles */
    h2 {
    	color: #a80000;
    	font-family: Arial, Helvetica, sans-serif;
    	font-weight: lighter;
    }

    .clear {
    	color: #333;
    	background-color: #eee;
    	margin-bottom: 12px;
    	padding: 1rem;
    	border-radius: 4px;
    	font-size: 1rem;
    }
    .clear:hover {
    	color: white;
    	background-color: #42545c;
    }
    ```

=== "src/app/app.module.ts"

    ```ts
    import { BrowserModule } from '@angular/platform-browser';
    import { NgModule } from '@angular/core';
    import { FormsModule } from '@angular/forms';
    import { AppComponent } from './app.component';
    import { HeroesComponent } from './heroes/heroes.component';
    import { HeroDetailComponent } from './hero-detail/hero-detail.component';
    import { MessagesComponent } from './messages/messages.component';

    @NgModule({
    	declarations: [
    		AppComponent,
    		HeroesComponent,
    		HeroDetailComponent,
    		MessagesComponent,
    	],
    	imports: [BrowserModule, FormsModule],
    	providers: [
    		// no need to place any providers due to the `providedIn` flag...
    	],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "src/app/app.component.html"

    ```html
    <h1>{{title}}</h1>
    <app-heroes></app-heroes>
    <app-messages></app-messages>
    ```

## Резюме

-   Вы рефакторизовали доступ к данным в классе `HeroService`.
-   Вы зарегистрировали `HeroService` как _провайдера_ своего сервиса на корневом уровне, чтобы его можно было внедрить в любое место приложения.
-   Вы использовали [Angular Dependency Injection](dependency-injection.md), чтобы внедрить его в компонент.
-   Вы придали методу `HeroService` `get data` асинхронную сигнатуру.
-   Вы открыли для себя `Observable` и библиотеку RxJS `Observable`.
-   Вы использовали RxJS `of()` для возврата `Observable<Hero[]>`, наблюдаемой модели героев.
-   Хук жизненного цикла компонента `ngOnInit` вызывает метод `HeroService`, а не конструктор.
-   Вы создали `MessageService` для свободно связанного взаимодействия между классами.
-   Внедренный в компонент `HeroService` создается вместе с другим внедренным сервисом, `MessageService`.

## Ссылки

-   [Add services](https://angular.io/tutorial/tour-of-heroes/toh-pt4)
