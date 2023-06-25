# API утилиты для тестирования

На этой странице описаны наиболее полезные функции тестирования Angular.

Утилиты тестирования Angular включают `TestBed`, `ComponentFixture` и несколько функций, которые управляют тестовой средой. Классы [`TestBed`](#testbed-api-summary) и [`ComponentFixture`](#component-fixture-api-summary) рассматриваются отдельно.

Вот краткое описание отдельных функций в порядке их вероятной полезности:

| Function | Details | | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `waitForAsync` | Runs the body of a test \(`it`\) or setup \(`beforeEach`\) function within a special _async test zone_. See [waitForAsync](guide/testing-components-scenarios#waitForAsync). |
| `fakeAsync` | Runs the body of a test \(`it`\) within a special _fakeAsync test zone_, enabling a linear control flow coding style. See [fakeAsync](guide/testing-components-scenarios#fake-async). |
| `tick` | Simulates the passage of time and the completion of pending asynchronous activities by flushing both _timer_ and _micro-task_ queues within the _fakeAsync test zone_. <div class="alert is-helpful"> The curious, dedicated reader might enjoy this lengthy blog post, ["_Tasks, microtasks, queues and schedules_"](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules). </div> Accepts an optional argument that moves the virtual clock forward by the specified number of milliseconds, clearing asynchronous activities scheduled within that timeframe. See [tick](guide/testing-components-scenarios#tick). |
| `inject` | Injects one or more services from the current `TestBed` injector into a test function. It cannot inject a service provided by the component itself. See discussion of the [debugElement.injector](guide/testing-components-scenarios#get-injected-services). |
| `discardPeriodicTasks` | When a `fakeAsync()` test ends with pending timer event _tasks_ \(queued `setTimeOut` and `setInterval` callbacks\), the test fails with a clear error message. <br /> In general, a test should end with no queued tasks. When pending timer tasks are expected, call `discardPeriodicTasks` to flush the _task_ queue and avoid the error. |
| `flushMicrotasks` | When a `fakeAsync()` test ends with pending _micro-tasks_ such as unresolved promises, the test fails with a clear error message. <br /> In general, a test should wait for micro-tasks to finish. When pending microtasks are expected, call `flushMicrotasks` to flush the _micro-task_ queue and avoid the error. |
| `ComponentFixtureAutoDetect` | A provider token for a service that turns on [automatic change detection](guide/testing-components-scenarios#automatic-change-detection). |
| `getTestBed` | Gets the current instance of the `TestBed`. Usually unnecessary because the static class methods of the `TestBed` class are typically sufficient. The `TestBed` instance exposes a few rarely used members that are not available as static methods. |

<a id="testbed-class-summary"></a>

## Краткое описание класса `TestBed`

Класс `TestBed` является одной из основных утилит тестирования Angular. Его API довольно большой и может быть подавляющим, пока вы не изучите его понемногу.

Прочитайте сначала начальную часть этого руководства, чтобы получить основы, прежде чем пытаться освоить весь API.

Определение модуля, передаваемое в `configureTestingModule`, является подмножеством свойств метаданных `@NgModule`.

<code-example format="javascript" language="javascript">

type TestModuleMetadata = { providers?: any[];
декларации?: любые[];

импорты?: any[];

схемы? Array&lt;SchemaMetadata | any[]&gt;;

};

</code-example>

<a id="metadata-override-object"></a>

Каждый метод переопределения принимает `MetadataOverride<T>`, где `T` - это тип метаданных, соответствующий методу, то есть параметр `@NgModule`, `@Component`, `@Directive` или `@Pipe`.

<code-example format="javascript" language="javascript">

type MetadataOverride&lt;T&gt; = { add? Partial&lt;T&gt;;
remove? Partial&lt;T&gt;;

set?: Partial&lt;T&gt;;

};

</code-example>

<a id="testbed-methods"></a> <a id="testbed-api-summary"></a>

API `TestBed` состоит из статических методов класса, которые либо обновляют, либо ссылаются на _глобальный_ экземпляр `TestBed`.

Внутри, все статические методы охватывают методы текущего экземпляра `TestBed`, который также возвращается функцией `getTestBed()`.

Вызывайте методы `TestBed` \_в рамках `beforeEach()`, чтобы обеспечить новый старт перед каждым отдельным тестом.

Ниже приведены наиболее важные статические методы в порядке их вероятной полезности.

| Methods | Details | | :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `configureTestingModule` | The testing shims \(`karma-test-shim`, `browser-test-shim`\) establish the [initial test environment](guide/testing) and a default testing module. The default testing module is configured with basic declaratives and some Angular service substitutes that every tester needs. <br /> Call `configureTestingModule` to refine the testing module configuration for a particular set of tests by adding and removing imports, declarations \(of components, directives, and pipes\), and providers. |
| `compileComponents` | Compile the testing module asynchronously after you've finished configuring it. You **must** call this method if _any_ of the testing module components have a `templateUrl` or `styleUrls` because fetching component template and style files is necessarily asynchronous. See [compileComponents](guide/testing-components-scenarios#compile-components). <br /> After calling `compileComponents`, the `TestBed` configuration is frozen for the duration of the current spec. |
| `createComponent<T>` | Create an instance of a component of type `T` based on the current `TestBed` configuration. After calling `createComponent`, the `TestBed` configuration is frozen for the duration of the current spec. |
| `overrideModule` | Replace metadata for the given `NgModule`. Recall that modules can import other modules. The `overrideModule` method can reach deeply into the current testing module to modify one of these inner modules. |
| `overrideComponent` | Replace metadata for the given component class, which could be nested deeply within an inner module. |
| `overrideDirective` | Replace metadata for the given directive class, which could be nested deeply within an inner module. |
| `overridePipe` | Replace metadata for the given pipe class, which could be nested deeply within an inner module. |

| <a id="testbed-inject"></a>
`inject` | Retrieve a service from the current `TestBed` injector. The `inject` function is often adequate for this purpose. But `inject` throws an error if it can't provide the service. <br /> What if the service is optional? <br /> The `TestBed.inject()` method takes an optional second parameter, the object to return if Angular can't find the provider \(`null` in this example\): <code-example header="app/demo/demo.testbed.spec.ts" path="testing/src/app/demo/demo.testbed.spec.ts" region="testbed-get-w-null"></code-example> After calling `TestBed.inject`, the `TestBed` configuration is frozen for the duration of the current spec. |

|

<a id="testbed-initTestEnvironment"></a>

`initTestEnvironment` | Initialize the testing environment for the entire test run. <br /> The testing shims \(`karma-test-shim`, `browser-test-shim`\) call it for you so there is rarely a reason for you to call it yourself. <br /> Call this method _exactly once_. To change this default in the middle of a test run, call `resetTestEnvironment` first. <br /> Specify the Angular compiler factory, a `PlatformRef`, and a default Angular testing module. Alternatives for non-browser platforms are available in the general form `@angular/platform-<platform_name>/testing/<platform_name>`. |

| `resetTestEnvironment` | Сброс начального тестового окружения, включая модуль тестирования по умолчанию. |

Несколько методов экземпляра `TestBed` не покрываются статическими методами _класса_ `TestBed`. Они нужны редко.

<a id="component-fixture-api-summary"></a>

## Фикстура `ComponentFixture`

Функция `TestBed.createComponent<T>` создает экземпляр компонента `T` и возвращает сильно типизированную `ComponentFixture` для этого компонента.

Свойства и методы `ComponentFixture` предоставляют доступ к компоненту, его DOM-представлению и аспектам его Angular-окружения.

<a id="component-fixture-properties"></a>

### `свойства `компонентной фикстуры`

Вот наиболее важные свойства для тестировщиков, в порядке вероятной полезности.

| Properties | Details | | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `componentInstance` | The instance of the component class created by `TestBed.createComponent`. |

| `debugElement` | The `DebugElement` associated with the root element of the component. <br /> The `debugElement` provides insight into the component and its DOM element during test and debugging. It's a critical property for testers. The most interesting members are covered [below](#debug-element-details). |

| `nativeElement` | The native DOM element at the root of the component. |

| `changeDetectorRef` | The `ChangeDetectorRef` for the component. <br /> The `ChangeDetectorRef` is most valuable when testing a component that has the `ChangeDetectionStrategy.OnPush` method or the component's change detection is under your programmatic control. |

<a id="component-fixture-methods"></a>

### `методы компонентной фикстуры`

Методы _fixture_ заставляют Angular выполнять определенные задачи на дереве компонентов. Вызывайте эти методы, чтобы вызвать поведение Angular в ответ на имитацию действий пользователя.

Вот наиболее полезные методы для тестировщиков.

| Methods | Details | | :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `detectChanges` | Trigger a change detection cycle for the component. <br /> Call it to initialize the component \(it calls `ngOnInit`\) and after your test code, change the component's data bound property values. Angular can't see that you've changed `personComponent.name` and won't update the `name` binding until you call `detectChanges`. <br /> Runs `checkNoChanges` afterwards to confirm that there are no circular updates unless called as `detectChanges(false)`; |
| `autoDetectChanges` | Set this to `true` when you want the fixture to detect changes automatically. <br /> When autodetect is `true`, the test fixture calls `detectChanges` immediately after creating the component. Then it listens for pertinent zone events and calls `detectChanges` accordingly. When your test code modifies component property values directly, you probably still have to call `fixture.detectChanges` to trigger data binding updates. <br /> The default is `false`. Testers who prefer fine control over test behavior tend to keep it `false`. |
| `checkNoChanges` | Do a change detection run to make sure there are no pending changes. Throws an exceptions if there are. |
| `isStable` | If the fixture is currently _stable_, returns `true`. If there are async tasks that have not completed, returns `false`. |
| `whenStable` | Returns a promise that resolves when the fixture is stable. <br /> To resume testing after completion of asynchronous activity or asynchronous change detection, hook that promise. See [whenStable](guide/testing-components-scenarios#when-stable). |
| `destroy` | Trigger component destruction. |

<a id="debug-element-details"></a>

#### `DebugElement`

Элемент `DebugElement` предоставляет важную информацию о DOM-представлении компонента.

Из `DebugElement` корневого компонента теста, возвращаемого `fixture.debugElement`, вы можете пройтись \(и запросить\) по всем поддеревьям элементов и компонентов компонента.

Вот наиболее полезные члены `DebugElement` для тестировщиков, в примерном порядке полезности:

| Members | Details | | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `nativeElement` | The corresponding DOM element in the browser |
| `query` | Calling `query(predicate: Predicate<DebugElement>)` returns the first `DebugElement` that matches the [predicate](#query-predicate) at any depth in the subtree. |
| `queryAll` | Calling `queryAll(predicate: Predicate<DebugElement>)` returns all `DebugElements` that matches the [predicate](#query-predicate) at any depth in subtree. |
| `injector` | The host dependency injector. For example, the root element's component instance injector. |
| `componentInstance` | The element's own component instance, if it has one. |
| `context` | An object that provides parent context for this element. Often an ancestor component instance that governs this element. <br /> When an element is repeated within `*ngFor`, the context is an `NgForOf` whose `$implicit` property is the value of the row instance value. For example, the `hero` in `*ngFor="let hero of heroes"`. |
| `children` | The immediate `DebugElement` children. Walk the tree by descending through `children`. <div class="alert is-helpful"> `DebugElement` also has `childNodes`, a list of `DebugNode` objects. `DebugElement` derives from `DebugNode` objects and there are often more nodes than elements. Testers can usually ignore plain nodes. </div> |
| `parent` | The `DebugElement` parent. Null if this is the root element. |
| `name` | The element tag name, if it is an element. |
| `triggerEventHandler` | Triggers the event by its name if there is a corresponding listener in the element's `listeners` collection. The second parameter is the _event object_ expected by the handler. See [triggerEventHandler](guide/testing-components-scenarios#trigger-event-handler). <br /> If the event lacks a listener or there's some other problem, consider calling `nativeElement.dispatchEvent(eventObject)`. |
| `listeners` | The callbacks attached to the component's `@Output` properties and/or the element's event properties. |
| `providerTokens` | This component's injector lookup tokens. Includes the component itself plus the tokens that the component lists in its `providers` metadata. |
| `source` | Where to find this element in the source component template. |
| `references` | Dictionary of objects associated with template local variables \(for example, `#foo`\), keyed by the local variable name. |

<a id="query-predicate"></a>

Методы `DebugElement.query(predicate)` и `DebugElement.queryAll(predicate)` принимают предикат, который фильтрует поддерево исходного элемента на предмет соответствия `DebugElement`.

Предикат - это любой метод, который принимает `DebugElement` и возвращает _истинное_ значение. Следующий пример находит все `DebugElements` со ссылкой на локальную переменную шаблона с именем "content":

<code-example header="app/demo/demo.testbed.spec.ts" path="testing/src/app/demo/demo.testbed.spec.ts" region="custom-predicate"></code-example>.

Класс Angular `By` имеет три статических метода для общих предикатов:

| Статический метод | Подробности | | :------------------------ | :------------------------------------------------------------------------- |.

| `By.all` | Возвращает все элементы |

| `By.css(selector)` | Возвращает элементы с соответствующими CSS-селекторами |

| `By.directive(directive)` | Возвращает элементы, которые Angular сопоставил с экземпляром класса директивы | `By.directive(directive)` | Возвращает элементы, которые Angular сопоставил с экземпляром класса директивы.

<code-example header="app/hero/hero-list.component.spec.ts" path="testing/src/app/hero/hero-list.component.spec.ts" region="by"></code-example>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
