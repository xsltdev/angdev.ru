# Добавить сервисы

Компонент `HeroesComponent` в Туре Героев получает и отображает поддельные данные.

Рефакторинг `HeroesComponent` сосредоточен на поддержке представления и облегчении юнит-тестирования с помощью имитационного сервиса.

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, см. в <live-example></live-example>.

</div>

## Почему сервисы

Компоненты не должны получать или сохранять данные напрямую и уж точно не должны представлять заведомо ложные данные. Они должны сосредоточиться на представлении данных и делегировать доступ к ним сервису.

В этом руководстве создается `HeroService`, который все классы приложения могут использовать для получения героев. Вместо того чтобы создавать сервис с помощью ключевого слова [`new`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/new), используйте [_dependency injection_](dependency-injection.md), который поддерживает Angular, чтобы внедрить его в конструктор `HeroesComponent`.

Сервисы - это отличный способ обмена информацией между классами, которые _не знают друг друга_. Создайте следующий `MessageService` и инжектируйте его в эти два места.

-   Inject в `HeroService`, который использует сервис для отправки сообщения

-   Вставьте в `MessagesComponent`, который отображает это сообщение, а также отображает ID, когда пользователь нажимает на героя.

## Создайте `HeroService`.

Запустите `ng generate` для создания сервиса под названием `hero`.

<code-example format="shell" language="shell">

генерировать героя службы

</code-example>

Команда генерирует скелет класса `HeroService` в `src/app/hero.service.ts` следующим образом:

<code-example header="src/app/hero.service.ts (новый сервис)" path="toh-pt4/src/app/hero.service.1.ts" region="new"></code-example>.

### `@Injectable()` сервисы

Обратите внимание, что новый сервис импортирует символ Angular `Injectable` и аннотирует класс декоратором `@Injectable()`. Это отмечает класс как участвующий в системе _инъекции зависимостей_. Класс `HeroService` будет предоставлять инжектируемый сервис, и он также может иметь свои собственные инжектируемые зависимости.

Пока у него нет никаких зависимостей.

Декоратор `@Injectable()` принимает объект метаданных для сервиса, так же, как декоратор `@Component()` для ваших классов компонентов.

### Получение данных героя

Сервис `HeroService` может получать данные героя откуда угодно, например, из веб-сервиса, локального хранилища или имитируемого источника данных.

Удаление доступа к данным из компонентов означает, что вы можете в любой момент изменить свое мнение о реализации, не трогая никаких компонентов. Они не знают, как работает сервис.

Реализация в _этом_ учебнике продолжает предоставлять _макет героев_.

Импортируйте `Hero` и `HEROES`.

<code-example header="src/app/hero.service.ts" path="toh-pt4/src/app/hero.service.ts" region="import-heroes"></code-example>.

Добавьте метод `getHeroes`, чтобы вернуть _макет героев_.

<code-example header="src/app/hero.service.ts" path="toh-pt4/src/app/hero.service.1.ts" region="getHeroes"></code-example>.

<a id="provide"></a>

## Предоставьте `HeroService`.

Вы должны сделать `HeroService` доступным для системы инъекции зависимостей, прежде чем Angular сможет _инжектировать_ его в `HeroesComponent`, зарегистрировав _провайдера_. Провайдер - это то, что может создавать или предоставлять услугу. В данном случае он инстанцирует класс `HeroService` для предоставления услуги.

Чтобы убедиться, что `HeroService` может предоставить эту услугу, зарегистрируйте его с помощью _инжектора_. Инжектор\_ - это объект, который выбирает и внедряет провайдера там, где это требуется приложению.

По умолчанию `ng generate service` регистрирует провайдера с _корневым инжектором_ для вашего сервиса, включая метаданные провайдера, это `providedIn: 'root'` в декораторе `@Injectable()`.

<code-example format="typescript" language="typescript">

@Injectable({ providedIn: 'root',
})

</code-example>

Когда вы предоставляете сервис на корневом уровне, Angular создает единственный, общий экземпляр `HeroService` и внедряет его в любой класс, который его запрашивает. Регистрация провайдера в метаданных `@Injectable` также позволяет Angular оптимизировать приложение, удаляя сервис, если он не используется.

<div class="alert is-helpful">

Чтобы узнать больше о провайдерах, смотрите раздел [Провайдеры](providers.md). Чтобы узнать больше об инжекторах, см. руководство [Dependency Injection guide](dependency-injection.md).

</div>

Теперь `HeroService` готов к подключению к `HeroesComponent`.

<div class="alert is-important">

Это промежуточный пример кода, который позволяет вам предоставлять и использовать `HeroService`. На данном этапе код отличается от `HeroService` в [финальном обзоре кода](#final-code-review).

</div>

## Обновление `HeroesComponent`.

Откройте файл класса `HeroesComponent`.

Удалите импорт `HEROES`, потому что он вам больше не понадобится. Вместо этого импортируйте `HeroService`.

<code-example header="src/app/heroes/heroes.component.ts (import HeroService)" path="toh-pt4/src/app/heroes/heroes.component.ts" region="hero-service-import"></code-example>.

Замените определение свойства `heroes` объявлением.

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt4/src/app/heroes/heroes.component.ts" region="heroes"></code-example>.

<a id="inject"></a>

### Инжектируйте `HeroService`.

Добавьте приватный параметр `heroService` типа `HeroService` в конструктор.

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt4/src/app/heroes/heroes.component.1.ts" region="ctor"></code-example>.

Параметр одновременно определяет частное свойство `heroService` и идентифицирует его как место инъекции `HeroService`.

Когда Angular создает `HeroesComponent`, система [Dependency Injection](dependency-injection.md) устанавливает параметр `heroService` в синглтон экземпляра `HeroService`.

### Добавьте `getHeroes()`.

Создайте метод для получения героев из сервиса.

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt4/src/app/heroes/heroes.component.1.ts" region="getHeroes"></code-example>.

<a id="oninit"></a>

### Вызовите его в `ngOnInit()`.

Хотя вы можете вызвать `getHeroes()` в конструкторе, это не лучшая практика.

Оставьте конструктор для минимальной инициализации, например, для подключения параметров конструктора к свойствам. Конструктор не должен _делать ничего_.

Он определенно не должен вызывать функцию, которая делает HTTP-запросы к удаленному серверу, как это сделала бы _реальная_ служба данных.

Вместо этого вызовите `getHeroes()` внутри [_ngOnInit lifecycle hook_](lifecycle-hooks.md) и позвольте Angular вызвать `ngOnInit()` в подходящее время _после_ создания экземпляра `HeroesComponent`.

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt4/src/app/heroes/heroes.component.ts" region="ng-on-init"></code-example>.

### Посмотрите, как это работает

После обновления браузера приложение должно работать как прежде, показывая список героев и подробное представление героя, когда вы нажимаете на имя героя.

## Наблюдаемые данные

Метод `HeroService.getHeroes()` имеет _синхронную подпись_, что подразумевает, что `HeroService` может получать героев синхронно. Компонент `HeroesComponent` потребляет результат `getHeroes()`, как если бы герои могли быть получены синхронно.

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt4/src/app/heroes/heroes.component.1.ts" region="get-heroes"></code-example>.

Этот подход не будет работать в реальном приложении, использующем асинхронные вызовы. Сейчас он работает, потому что ваш сервис синхронно возвращает _макет героев_.

Если `getHeroes()` не может немедленно вернуться с данными о героях, он не должен быть синхронным, потому что это заблокирует браузер в ожидании возврата данных.

У `HeroService.getHeroes()` должна быть какая-то _асинхронная подпись_.

В этом руководстве `HeroService.getHeroes()` возвращает `Observable`, чтобы можно было использовать метод Angular `HttpClient.get` для получения героев

и чтобы [`HttpClient.get()`](http.md) возвращал `Observable`.

### Observable `HeroService`.

`Observable` является одним из ключевых классов в [библиотеке RxJS](https://rxjs.dev).

В [учебнике по HTTP](toh-pt6.md) вы можете увидеть, как методы Angular `HttpClient` возвращают объекты RxJS `Observable`. Этот учебник имитирует получение данных с сервера с помощью функции RxJS `of()`.

Откройте файл `HeroService` и импортируйте символы `Observable` и `of` из RxJS.

<code-example header="src/app/hero.service.ts (Observable imports)" path="toh-pt4/src/app/hero.service.ts" region="import-observable"></code-example>.

Замените метод `getHeroes()` на следующий:

<code-example header="src/app/hero.service.ts" path="toh-pt4/src/app/hero.service.ts" region="getHeroes-1"></code-example>

`of(HEROES)` возвращает `Observable<Hero[]>`, который выдает _единственное значение_, массив подражаемых героев.

<div class="alert is-helpful">

В [HTTP tutorial](toh-pt6.md) показано, как вызвать `HttpClient.get<Hero[]>()`, который также возвращает `Observable<Hero[]>`, выдающий _единственное значение_, массив героев из тела HTTP-ответа.

</div>

### Подписаться в `HeroesComponent`.

Метод `HeroService.getHeroes` раньше возвращал `Hero[]`. Теперь он возвращает `Observable<Hero[]>`.

Вам нужно настроить свое приложение для работы с этим изменением в `HeroesComponent`.

Найдите метод `getHeroes` и замените его следующим кодом. новый код показан рядом с текущей версией для сравнения.

<code-tabs> <code-pane header="heroes.component.ts (Observable)" path="toh-pt4/src/app/heroes/heroes.component.ts" region="getHeroes"></code-pane>
<code-pane header="heroes.component.ts (Original)" path="toh-pt4/src/app/heroes/heroes.component.1.ts" region="getHeroes"></code-pane>
</code-tabs>

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

### Создайте `MessagesComponent`.

Используйте `ng generate` для создания `MessagesComponent`.

<code-example format="shell" language="shell">

ng генерировать сообщения компонентов

</code-example>

`ng generate` создает файлы компонента в каталоге `src/app/messages` и объявляет `MessagesComponent` в `AppModule`.

Отредактируйте шаблон `AppComponent` для отображения `MessagesComponent`.

<code-example header="src/app/app.component.html" path="toh-pt4/src/app/app/app.component.html"></code-example>.

Вы должны увидеть параграф по умолчанию из `MessagesComponent` в нижней части страницы.

### Создайте `MessageService`.

Используйте `ng generate` для создания `MessageService` в `src/app`.

<code-example format="shell" language="shell">

ng генерировать служебное сообщение

</code-example>

Откройте `MessageService` и замените его содержимое на следующее.

<code-example header="src/app/message.service.ts" path="toh-pt4/src/app/message.service.ts"></code-example>.

Сервис раскрывает свой кэш `messages` и два метода:

-   Один для `добавления()` сообщения в кэш.

-   Другой - для `очистки()` кэша.

<a id="inject-message-service"></a>

### Вставьте его в `HeroService`.

В `HeroService` импортируйте `MessageService`.

<code-example header="src/app/hero.service.ts (import MessageService)" path="toh-pt4/src/app/hero.service.ts" region="import-message-service"></code-example>.

Отредактируйте конструктор с параметром, который объявляет приватное свойство `messageService`. Angular инжектирует синглтон `MessageService` в это свойство при создании `HeroService`.

<code-example header="src/app/hero.service.ts" path="toh-pt4/src/app/hero.service.ts" region="ctor"></code-example>

<div class="alert is-helpful">

Это пример типичного сценария _сервис в сервисе_, в котором вы вводите `MessageService` в `HeroService`, который вводится в `HeroesComponent`.

</div>

### Отправка сообщения из `HeroService`.

Отредактируйте метод `getHeroes()` для отправки сообщения при получении героев.

<code-example header="src/app/hero.service.ts" path="toh-pt4/src/app/hero.service.ts" region="getHeroes"></code-example>.

### Отображение сообщения от `HeroService`.

Компонент `MessagesComponent` должен отображать все сообщения, включая сообщение, отправленное `HeroService` при получении героев.

Откройте `MessagesComponent` и импортируйте `MessageService`.

<code-example header="src/app/messages/messages.component.ts (import MessageService)" path="toh-pt4/src/app/messages/messages.component.ts" region="import-message-service"></code-example>.

Отредактируйте конструктор с параметром, который объявляет **публичное** свойство `messageService`. Angular инжектирует синглтон `MessageService` в это свойство при создании `MessagesComponent`.

<code-example header="src/app/messages/messages.component.ts" path="toh-pt4/src/app/messages/messages.component.ts" region="ctor"></code-example

Свойство `messageService` **должно быть public**, потому что вы собираетесь привязать его к шаблону.

<div class="alert is-important">

Angular привязывается только к _публичным_ свойствам компонентов.

</div>

### Привязка к `MessageService`.

Замените шаблон `MessagesComponent`, созданный `ng generate`, на следующий.

<code-example header="src/app/messages/messages.component.html" path="toh-pt4/src/app/messages/messages.component.html"></code-example>

This template binds directly to the component's `messageService`.

| | Details | | :------------------------------------------- | :------------------------------------------------------------- |

| `*ngIf` | Only displays the messages area if there are messages to show. |

| `*ngFor` | Presents the list of messages in repeated `<div>` elements. |

| Angular [event binding](event-binding.md) | Binds the button's click event to `MessageService.clear()`. |

The messages look better after you add the private CSS styles to `messages.component.css` as listed in one of the ["final code review"](#final-code-review) tabs below.

## Add MessageService to HeroesComponent

The following example shows how to display a history of each time the user clicks on a hero. This helps when you get to the next section on [Routing](toh-pt5.md).

<code-example header="src/app/heroes/heroes.component.ts" path="toh-pt4/src/app/heroes/heroes.component.ts"></code-example>.

Обновите браузер, чтобы увидеть список героев, и прокрутите страницу вниз, чтобы увидеть сообщения от HeroService. Каждый раз, когда вы нажимаете на героя, появляется новое сообщение для записи выбора.

Используйте кнопку **Очистить сообщения**, чтобы очистить историю сообщений.

<a id="final-code-review"></a>

## Окончательный обзор кода

Вот файлы кода, обсуждаемые на этой странице.

<code-tabs> <code-pane header="src/app/hero.service.ts" path="toh-pt4/src/app/hero.service.ts"></code-pane>
<code-pane header="src/app/message.service.ts" path="toh-pt4/src/app/message.service.ts"></code-pane>
<code-pane header="src/app/heroes/heroes.component.ts" path="toh-pt4/src/app/heroes/heroes.component.ts"></code-pane>
<code-pane header="src/app/messages/messages.component.ts" path="toh-pt4/src/app/messages/messages.component.ts"></code-pane>
<code-pane header="src/app/messages/messages.component.html" path="toh-pt4/src/app/messages/messages.component.html"></code-pane>
<code-pane header="src/app/messages/messages.component.css" path="toh-pt4/src/app/messages/messages.component.css"></code-pane>
<code-pane header="src/app/app.module.ts" path="toh-pt4/src/app/app.module.ts"></code-pane>
<code-pane header="src/app/app.component.html" path="toh-pt4/src/app/app.component.html"></code-pane>
</code-tabs>

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

:дата: 28.02.2022
