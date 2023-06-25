# Тестирование сервисов

Чтобы проверить, что ваши сервисы работают так, как вы задумали, вы можете написать тесты специально для них.

<div class="alert is-helpful">

Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, <live-example name="testing" noDownload>запустите его в браузере</live-example> или <live-example name="testing" downloadOnly>скачайте и запустите его локально</live-example>.

</div>

Сервисы часто являются самыми гладкими файлами для модульного тестирования. Вот несколько синхронных и асинхронных модульных тестов `ValueService`, написанных без помощи утилит тестирования Angular.

<code-example header="app/demo/demo.spec.ts" path="testing/src/app/demo/demo.spec.ts" region="ValueService"></code-example>.

<a id="services-with-dependencies"></a>

## Сервисы с зависимостями

Сервисы часто зависят от других сервисов, которые Angular инжектирует в конструктор. Во многих случаях вы можете создать и _инжектировать_ эти зависимости вручную при вызове конструктора сервиса.

Простым примером является `MasterService`:

<code-example header="app/demo/demo.ts" path="testing/src/app/demo/demo.ts" region="MasterService"></code-example>.

`MasterService` делегирует свой единственный метод, `getValue`, инжектированному `ValueService`.

Вот несколько способов проверить это.

<code-example header="app/demo/demo.spec.ts" path="testing/src/app/demo/demo.spec.ts" region="MasterService"></code-example>.

Первый тест создает `ValueService` с `new` и передает его в конструктор `MasterService`.

Однако инжектирование реального сервиса редко работает хорошо, поскольку большинство зависимых сервисов сложно создавать и контролировать.

Вместо этого высмеивайте зависимость, используйте фиктивное значение или создайте [spy](https://jasmine.github.io/tutorials/your_first_suite#section-Spies) на соответствующем методе сервиса.

<div class="alert is-helpful">

Предпочитает шпионов, так как они, как правило, лучший способ поиздеваться над службами.

</div>

Эти стандартные методы тестирования отлично подходят для модульного тестирования сервисов в изоляции.

Однако вы почти всегда внедряете сервисы в классы приложения, используя инъекцию зависимостей Angular, и у вас должны быть тесты, отражающие эту модель использования. Утилиты тестирования Angular позволяют легко исследовать поведение внедренных сервисов.

## Тестирование сервисов с помощью `TestBed`.

Ваше приложение полагается на Angular [dependency injection (DI)](guide/dependency-injection) для создания сервисов. Когда у сервиса есть зависимый сервис, DI находит или создает этот зависимый сервис.

А если у этого зависимого сервиса есть свои собственные зависимости, DI находит или создает и их.

Как _потребитель_ сервиса, вы не беспокоитесь ни о чем из этого. Вас не волнует порядок аргументов конструктора или то, как они создаются.

Как _тестер_ сервисов, вы должны, по крайней мере, думать о первом уровне зависимостей сервисов, но вы _можете_ позволить Angular DI сделать создание сервиса и разобраться с порядком аргументов конструктора, если используете утилиту тестирования `TestBed` для предоставления и создания сервисов.

<a id="testbed"></a>

## Angular `TestBed`

`TestBed` является наиболее важной из утилит тестирования Angular. В `TestBed` создается динамически конструируемый модуль Angular _test_, который эмулирует модуль Angular [@NgModule](guide/ngmodules).

Метод `TestBed.configureTestingModule()` принимает объект метаданных, который может иметь большинство свойств [@NgModule](guide/ngmodules).

Чтобы протестировать сервис, вы задаете свойство метаданных `providers` с массивом сервисов, которые вы будете тестировать или имитировать.

<code-example header="app/demo/demo.testbed.spec.ts (provide ValueService in beforeEach)" path="testing/src/app/demo/demo.testbed.spec.ts" region="value-service-before-each"></code-example>.

Затем внедрите его внутрь теста, вызвав `TestBed.inject()` с классом сервиса в качестве аргумента.

<div class="alert is-helpful">

**NOTE**: <br /> `TestBed.get()` was deprecated as of Angular version 9.
To help minimize breaking changes, Angular introduces a new function called `TestBed.inject()`, which you should use instead.

For information on the removal of `TestBed.get()`, see its entry in the [Deprecations index](guide/deprecations#index).

</div>

<code-example path="testing/src/app/demo/demo.testbed.spec.ts" region="value-service-inject-it"></code-example>.

Или внутри `beforeEach()`, если вы предпочитаете инжектировать сервис как часть вашей установки.

<code-example path="testing/src/app/demo/demo.testbed.spec.ts" region="value-service-inject-before-each"> </code-example>.

При тестировании сервиса с зависимостью, предоставьте макет в массиве `providers`.

В следующем примере имитатором является объект spy.

<code-example path="testing/src/app/demo/demo.testbed.spec.ts" region="master-service-before-each"></code-example>.

Тест потребляет этого шпиона тем же способом, что и ранее.

<code-example path="testing/src/app/demo/demo.testbed.spec.ts" region="master-service-it"></code-example>.

<a id="no-before-each"></a>

## Тестирование без `beforeEach()`

Большинство тестовых наборов в этом руководстве вызывают `beforeEach()` для установки предварительных условий для каждого теста `it()` и полагаются на `TestBed` для создания классов и внедрения сервисов.

Существует и другая школа тестирования, которая никогда не вызывает `beforeEach()` и предпочитает создавать классы явно, а не использовать `TestBed`.

Вот как можно переписать один из тестов `MasterService` в этом стиле.

Начните с размещения повторно используемого, подготовительного кода в функции _setup_ вместо `beforeEach()`.

<code-example header="app/demo/demo.spec.ts (setup)" path="testing/src/app/demo/demo.spec.ts" region="no-before-each-setup"></code-example>.

Функция `setup()` возвращает литерал объекта с переменными, такими как `masterService`, на которые может ссылаться тест. Вы не определяете _полуглобальные_ переменные\(например, `let masterService: MasterService`\) в теле `describe()`.

Затем каждый тест вызывает `setup()` в своей первой строке, прежде чем продолжить шаги, которые манипулируют объектом тестирования и утверждают ожидания.

<code-example path="testing/src/app/demo/demo.spec.ts" region="no-before-each-test"></code-example>.

Обратите внимание, как тест использует [_деструктурирующее назначение_](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) для извлечения необходимых ему переменных настройки.

<code-example path="testing/src/app/demo/demo.spec.ts" region="no-before-each-setup-call"></code-example>.

Многие разработчики считают этот подход более чистым и явным, чем традиционный стиль `beforeEach()`.

Хотя это руководство по тестированию следует традиционному стилю, и по умолчанию [CLI схемы](https://github.com/angular/angular-cli) генерируют тестовые файлы с `beforeEach()` и `TestBed`, не стесняйтесь использовать _этот альтернативный подход_ в ваших собственных проектах.

## Тестирование HTTP-сервисов

Сервисы данных, выполняющие HTTP-вызовы к удаленным серверам, обычно инжектируют и делегируют службу Angular [`HttpClient`](guide/http) для XHR-вызовов.

Вы можете протестировать сервис данных с инжектированным `HttpClient` шпионом, как вы тестировали бы любой сервис с зависимостью.

<code-example header="app/model/hero.service.spec.ts (тесты со шпионами)" path="testing/src/app/model/hero.service.spec.ts" region="test-with-spies"></code-example>.

<div class="alert is-important">

Методы `HeroService` возвращают `Observables`. Вы должны _подписаться_ на наблюдаемую переменную, чтобы \(a\) вызвать ее выполнение и \(b\) подтвердить успех или неудачу метода.

Метод `subscribe()` принимает обратный вызов успеха \(`next`\) и отказа \(`error`\). Убедитесь, что вы предоставили _обои_ обратные вызовы, чтобы перехватить ошибки.

Пренебрежение этим приводит к асинхронной не пойманной наблюдаемой ошибке, которую программа запуска тестов, скорее всего, отнесет к совершенно другому тесту.

</div>

## `HttpClientTestingModule`.

Расширенные взаимодействия между сервисом данных и `HttpClient` могут быть сложными и их трудно имитировать с помощью шпионов.

Модуль `HttpClientTestingModule` может сделать эти сценарии тестирования более управляемыми.

Хотя _пример кода_, сопровождающий данное руководство, демонстрирует `HttpClientTestingModule`, эта страница отсылает к [Http guide](guide/http#testing-http-requests), где подробно рассматривается тестирование с помощью `HttpClientTestingModule`.

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
