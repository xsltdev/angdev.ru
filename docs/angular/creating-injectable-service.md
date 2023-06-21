# Создание инжектируемой службы

Сервис - это широкая категория, охватывающая любые ценности, функции или возможности, необходимые приложению. Обычно сервис - это класс с узкой, четко определенной целью. Компонент - это один из типов классов, который может использовать DI.

Angular отличает компоненты от сервисов для повышения модульности и возможности повторного использования. Отделяя функции компонента, связанные с представлением, от других видов обработки, вы можете сделать свои классы компонентов компактными и эффективными.

В идеале задача компонента - обеспечить удобство работы пользователя и не более того. Компонент должен представлять свойства и методы для связывания данных, чтобы быть посредником между представлением (отображаемым шаблоном) и логикой приложения (которая часто включает в себя некоторое понятие модели).

Компонент может делегировать определенные задачи сервисам, например, получение данных с сервера, проверку пользовательского ввода или ведение журнала непосредственно в консоли. Определяя такие задачи обработки в классе инжектируемого сервиса, вы делаете эти задачи доступными для любого компонента. Вы также можете сделать свое приложение более адаптируемым, внедряя различных поставщиков одного и того же вида услуг в зависимости от обстоятельств.

Angular не навязывает эти принципы. Angular помогает вам следовать этим принципам, упрощая разделение логики приложения на сервисы и делая эти сервисы доступными для компонентов через DI.

## Примеры сервисов

Вот пример класса сервиса, который ведет журнал в консоль браузера.

<code-example header="src/app/logger.service.ts (class)" path="architecture/src/app/logger.service.ts" region="class"></code-example>.

Сервисы могут зависеть от других сервисов. Например, вот `HeroService`, который зависит от сервиса `Logger`, а также использует `BackendService` для получения героев.

Этот сервис, в свою очередь, может зависеть от сервиса `HttpClient` для асинхронного получения героев с сервера.

<code-example header="src/app/hero.service.ts (class)" path="architecture/src/app/hero.service.ts" region="class"></code-example>

## Создание инжектируемого сервиса

Angular CLI предоставляет команду для создания нового сервиса. В следующем примере вы добавляете новый сервис в ваше приложение, которое было создано ранее с помощью команды `ng new`.

Чтобы создать новый класс `HeroService` в папке `src/app/heroes`, выполните следующие шаги:

1. Выполните эту команду [Angular CLI](cli):

<code-example language="sh">
 ng generate service heroes/hero
</code-example>

Эта команда создает следующую службу по умолчанию `HeroService`.

<code-example path="dependency-injection/src/app/heroes/hero.service.0.ts" header="src/app/heroes/hero.service.ts (CLI-generated)">
 </code-example>

Декоратор `@Injectable()` указывает, что Angular может использовать этот класс в системе DI. Метаданные `providedIn: 'root'` означают, что `HeroService` виден во всем приложении.

2. Добавьте метод `getHeroes()`, который возвращает героев из `mock.heroes.ts` для получения имитационных данных героев:

<code-example path="dependency-injection/src/app/heroes/hero.service.3.ts" header="src/app/heroes/hero.service.ts">
 </code-example>

Для ясности и удобства сопровождения рекомендуется определять компоненты и сервисы в отдельных файлах.

## Инжектирование сервисов

Чтобы внедрить сервис в качестве зависимости в компонент, вы можете использовать функцию `constructor()` компонента и указать в аргументе конструктора тип зависимости. Следующий пример указывает `HeroService` в конструкторе `HeroListComponent`. Тип `heroService` - `HeroService`. Angular распознает `HeroService` как зависимость, поскольку этот класс был ранее аннотирован декоратором `@Injectable`.

<code-example header="src/app/heroes/hero-list.component (подпись конструктора)" path="dependency-injection/src/app/heroes/hero-list.component.ts" region="ctor-signature">
</code-example>

## Инжектирование сервисов в другие сервисы

Когда сервис зависит от другого сервиса, следуйте той же схеме, что и при инъекции в компонент. В следующем примере `HeroService` зависит от сервиса `Logger`, чтобы сообщать о своих действиях.

Сначала импортируйте службу `Logger`. Затем внедрите службу `Logger` в `конструктор()` службы `HeroService`, указав `private logger: Logger`.

Здесь `constructor()` указывает тип `Logger` и хранит экземпляр `Logger` в приватном поле `logger`.

В следующих вкладках кода представлены сервис `Logger` и две версии `HeroService`. Первая версия `HeroService` не зависит от сервиса `Logger`. Переработанная вторая версия зависит от службы `Logger`.

<code-tabs>

  <code-pane header="src/app/heroes/hero.service (v2)" path="dependency-injection/src/app/heroes/hero.service.2.ts">
   </code-pane>

  <code-pane header="src/app/heroes/hero.service (v1)" path="dependency-injection/src/app/heroes/hero.service.1.ts">
   </code-pane>

<code-pane header="src/app/logger.service" path="dependency-injection/src/app/logger.service.ts">
  </code-pane>

</code-tabs>

В этом примере метод `getHeroes()` использует службу `Logger`, записывая в журнал сообщение при получении героев.

## Что дальше

-   [Как настроить зависимости в DI](guide/dependency-injection-providers)

-   [Как использовать `InjectionTokens` для предоставления и инъекции значений, отличных от сервисов/классов](guide/dependency-injection-providers#configuring-dependency-providers)

-   [Dependency Injection in Action](guide/dependency-injection-in-action)

@ просмотрено 2022-08-02
