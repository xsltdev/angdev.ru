# Жизненный цикл компонента

Экземпляр компонента имеет жизненный цикл, который начинается, когда Angular инстанцирует класс компонента и отображает представление компонента вместе с его дочерними представлениями. Жизненный цикл продолжается при обнаружении изменений, так как Angular проверяет, когда изменяются свойства, связанные с данными, и обновляет представление и экземпляр компонента по мере необходимости.

Жизненный цикл заканчивается, когда Angular уничтожает экземпляр компонента и удаляет его отрисованный шаблон из DOM.

Директивы имеют аналогичный жизненный цикл, поскольку Angular создает, обновляет и уничтожает экземпляры в процессе выполнения.

Ваше приложение может использовать методы [lifecycle hook] (guide/glossary#lifecycle-hook "Definition of lifecycle hook") для подключения к ключевым событиям жизненного цикла компонента или директивы для инициализации новых экземпляров, инициирования обнаружения изменений при необходимости, реагирования на обновления во время обнаружения изменений и очистки перед удалением экземпляров.

## Предварительные условия

Перед работой с крючками жизненного цикла необходимо иметь базовое представление о следующем:

-   [программирование на TypeScript](https://www.typescriptlang.org)

-   основы дизайна приложений Angular, описанные в [Концепции Angular] (руководство/архитектура "Введение в фундаментальные концепции дизайна приложений")

<a id="hooks-overview"></a>

## Реагирование на события жизненного цикла

Реагируйте на события жизненного цикла компонента или директивы, реализуя один или несколько интерфейсов _lifecycle hook_ в библиотеке Angular `core`. Эти хуки дают вам возможность действовать на экземпляр компонента или директивы в нужный момент, когда Angular создает, обновляет или уничтожает этот экземпляр.

Каждый интерфейс определяет прототип для одного метода хука, имя которого является именем интерфейса с префиксом `ng`. Например, интерфейс `OnInit` имеет хук-метод с именем `ngOnInit()`.

Если вы реализуете этот метод в классе вашего компонента или директивы, Angular вызовет его вскоре после первой проверки свойств ввода для этого компонента или директивы.

<code-example header="peek-a-boo.directive.ts (excerpt)" path="lifecycle-hooks/src/app/peek-a-boo.directive.ts" region="ngOnInit"></code-example>.

Вам не обязательно реализовывать все \(или любые\) крючки жизненного цикла, только те, которые вам нужны.

<a id="hooks-purpose-timing"></a>

### Последовательность событий жизненного цикла

После того как ваше приложение инстанцирует компонент или директиву, вызывая его конструктор, Angular вызывает реализованные вами методы hook в соответствующий момент жизненного цикла этого экземпляра.

Angular выполняет методы hook в следующей последовательности. Используйте их для выполнения следующих видов операций.

| Hook method | Purpose | Timing | |:--- |:--- |:--- |
| `ngOnChanges()` | Respond when Angular sets or resets data-bound input properties. The method receives a `SimpleChanges` object of current and previous property values. <br /> <div class="alert is-helpful"> **NOTE**: <br /> This happens frequently, so any operation you perform here impacts performance significantly. </div> See details in [Using change detection hooks](#onchanges) in this document. | Called before `ngOnInit()` \(if the component has bound inputs\) and whenever one or more data-bound input properties change. <br /> <div class="alert is-helpful"> **NOTE**: <br /> If your component has no inputs or you use it without providing any inputs, the framework will not call `ngOnChanges()`. </div> |

| `ngOnInit()` | Initialize the directive or component after Angular first displays the data-bound properties and sets the directive or component's input properties. See details in [Initializing a component or directive](#oninit) in this document. | Called once, after the first `ngOnChanges()`. `ngOnInit()` is still called even when `ngOnChanges()` is not \(which is the case when there are no template-bound inputs\). |

| `ngDoCheck()` | Detect and act upon changes that Angular can't or won't detect on its own. See details and example in [Defining custom change detection](#docheck) in this document. | Called immediately after `ngOnChanges()` on every change detection run, and immediately after `ngOnInit()` on the first run. |

| `ngAfterContentInit()` | Respond after Angular projects external content into the component's view, or into the view that a directive is in. <br /> See details and example in [Responding to changes in content](#aftercon

<a id="the-sample"></a>

### Набор примеров жизненного цикла

<live-example></live-example> демонстрирует использование крючков жизненного цикла через серию упражнений, представленных в виде компонентов под управлением корневого `AppComponent`. В каждом случае _родительский_ компонент служит испытательным стендом для _детского_ компонента, который иллюстрирует один или несколько методов крючков жизненного цикла.

В следующей таблице перечислены упражнения с краткими описаниями. Пример кода также используется для иллюстрации конкретных задач в следующих разделах.

| Компонент | Подробности | |:--- |:--- |:--- |
| [Peek-a-boo](#peek-a-boo) | Демонстрирует каждый хук жизненного цикла. Каждый метод хука записывает данные в экранный журнал. |

| [Spy](#spy) | Показывает, как использовать крючки жизненного цикла с пользовательской директивой. Директива `SpyDirective` реализует хуки `ngOnInit()` и `ngOnDestroy()` и использует их, чтобы наблюдать и сообщать, когда элемент входит или выходит из текущего представления. |

| [OnChanges](#onchanges) | Демонстрирует, как Angular вызывает хук `ngOnChanges()` каждый раз, когда изменяется одно из входных свойств компонента, и показывает, как интерпретировать объект `changes`, переданный в метод хука. |

| [DoCheck](#docheck) | Реализует метод `ngDoCheck()` с пользовательским обнаружением изменений. Посмотрите, как хук публикует изменения в журнале, чтобы узнать, как часто Angular вызывает этот хук. |

| [AfterView](#afterview) | Показывает, что Angular подразумевает под [view](guide/glossary#view 'Определение view.'). Демонстрирует хуки `ngAfterViewInit()` и `ngAfterViewChecked()`. |

| [AfterContent](#aftercontent) | Показывает, как проецировать внешнее содержимое в компонент и как отличать проецируемое содержимое от дочерних элементов представления компонента. Демонстрирует хуки `ngAfterContentInit()` и `ngAfterContentChecked()`. |

| [Counter](#counter) | Демонстрирует комбинацию компонента и директивы, каждая из которых имеет свои собственные крючки. |

<a id="oninit"></a>

## Initializing a component or directive

Use the `ngOnInit()` method to perform the following initialization tasks.

| Initialization tasks | Details | |:--- |:--- |

| Perform complex initializations outside of the constructor | Components should be cheap and safe to construct. You should not, for example, fetch data in a component constructor. You shouldn't worry that a new component will try to contact a remote server when created under test or before you decide to display it. <br /> An `ngOnInit()` is a good place for a component to fetch its initial data. For an example, see the [Tour of Heroes tutorial](tutorial/tour-of-heroes/toh-pt4#oninit). |

| Set up the component after Angular sets the input properties | Constructors should do no more than set the initial local variables to simple values. <br /> Keep in mind that a directive's data-bound input properties are not set until _after construction_. If you need to initialize the directive based on those properties, set them when `ngOnInit()` runs. <div class="alert is-helpful"> The `ngOnChanges()` method is your first opportunity to access those properties. Angular calls `ngOnChanges()` before `ngOnInit()`, but also many times after that. It only calls `ngOnInit()` once. </div> |

<a id="ondestroy"></a>

## Очистка при уничтожении экземпляра

Angular предоставляет несколько способов очистки при уничтожении экземпляра.

### `ngOnDestroy`.

Вы можете поместить логику очистки в `ngOnDestroy()`, логику, которая должна выполняться до того, как Angular уничтожит директиву.

Это место для освобождения ресурсов, которые не будут собраны автоматически. Если вы пренебрежете этим, то рискуете получить утечку памяти.

-   Отменить подписку на Observables и события DOM.

-   Остановите интервальные таймеры

-   Отмените регистрацию всех обратных вызовов, которые директива зарегистрировала в глобальных или прикладных службах.

Метод `ngOnDestroy()` также является временем для уведомления другой части приложения о том, что компонент уходит.

### DestroyRef

В дополнение к `ngOnDestroy()`, вы можете внедрить в Angular `DestroyRef` и зарегистрировать функции обратного вызова, которые будут вызываться при уничтожении окружающего контекста. Это может быть полезно для создания многократно используемых утилит, требующих очистки.

Зарегистрируйте обратный вызов с `DestroyRef`:

```ts @Component(...)
class Counter {
    count = 0;
    constructor() {
        // Start a timer to increment the counter every second.
        const id = setInterval(() => this.count++, 1000);

        // Stop the timer when the component is destroyed.
        const destroyRef = inject(DestroyRef);
        destroyRef.onDestroy(() => clearInterval(id));
    }
}
```

Как и `ngOnDestroy`, `DestroyRef` работает в любом сервисе, директиве, компоненте или трубе Angular.

### `takeUntilDestroyed`.

<div class="alert is-important">

`takeUntilDestroyed` доступен для [предварительного просмотра разработчиком](/guide/releases#developer-preview). Он готов к тому, чтобы вы попробовали, но он может измениться до того, как станет стабильным.

</div>

При использовании RxJS Observables в компонентах или директивах вы можете захотеть завершить работу всех наблюдаемых при уничтожении компонента или директивы. Пакет Angular `@angular/core/rxjs-interop` предоставляет оператор `takeUntilDestroyed` для упрощения этой распространенной задачи:

```ts data$ = http.get('...').pipe(takeUntilDestroyed());

```

По умолчанию `takeUntilDestroyed` должен быть вызван в контексте инъекции, чтобы он мог получить доступ к `DestroyRef`. Если контекст инъекции недоступен, вы можете явно указать `DestroyRef`.

## Общие примеры

Следующие примеры демонстрируют последовательность вызовов и относительную частоту различных событий жизненного цикла, а также то, как хуки можно использовать отдельно или вместе для компонентов и директив.

<a id="peek-a-boo"></a>

### Последовательность и частота всех событий жизненного цикла

Чтобы показать, как Angular вызывает хуки в ожидаемом порядке, `PeekABooComponent` демонстрирует все хуки в одном компоненте.

На практике вы редко, если вообще когда-либо, будете реализовывать все интерфейсы так, как это сделано в данном демонстрационном примере.

Следующий снимок отражает состояние журнала после того, как пользователь нажал кнопку **Create&hellip;**, а затем кнопку **Destroy&hellip;**.

<div class="lightbox">

<img alt="Peek-a-boo" src="generated/images/guide/lifecycle-hooks/peek-a-boo.png">

</div>

Последовательность сообщений журнала соответствует предписанному порядку вызова крючка:

| Порядок вызова крючка | Сообщение журнала | | |:--- |:--- |

| 1 | `OnChanges` | |

| 2 | `OnInit` | |

| 3 | `DoCheck'| |

| 4 | | `AfterContentInit` | |

| 5 | `AfterContentChecked` | |

| 6 | `AfterViewInit` | |

| 7 | `AfterViewChecked` | |

| 8 | `DoCheck` | |

| 9 | `AfterContentChecked` | |

| 10 | `AfterViewChecked` | |

| 11 | `OnDestroy` | |

<div class="alert is-helpful">

Обратите внимание, что журнал подтверждает, что входные свойства\(в данном случае свойство `name`\) не имеют присвоенных значений при построении. Входные свойства доступны методу `onInit()` для дальнейшей инициализации.

</div>

Если бы пользователь нажал кнопку _Update Hero_, в журнале было бы показано еще одно `OnChanges` и еще две тройки `DoCheck`, `AfterContentChecked` и `AfterViewChecked`. Обратите внимание, что эти три хука срабатывают _часто_, поэтому важно сохранить их логику как можно более компактной.

<a id="spy"></a>

### Use directives to watch the DOM

The `Spy` example demonstrates how to use the hook method for directives as well as components. The `SpyDirective` implements two hooks, `ngOnInit()` and `ngOnDestroy()`, to discover when a watched element is in the current view.

This template applies the `SpyDirective` to a `<div>` in the `ngFor` _hero_ repeater managed by the parent `SpyComponent`.

The example does not perform any initialization or clean-up. It just tracks the appearance and disappearance of an element in the view by recording when the directive itself is instantiated and destroyed.

A spy directive like this can provide insight into a DOM object that you cannot change directly. You can't access the implementation of a built-in `<div>`, or modify a third party component.

You do have the option to watch these elements with a directive.

The directive defines `ngOnInit()` and `ngOnDestroy()` hooks that log messages to the parent using an injected `LoggerService`.

<code-example header="src/app/spy.directive.ts" path="lifecycle-hooks/src/app/spy.directive.ts" region="spy-directive"></code-example>.

Примените шпиона к любому встроенному или компонентному элементу и убедитесь, что он инициализируется и уничтожается одновременно с этим элементом. Здесь он прикреплен к повторяющемуся герою `<p>`:

<code-example header="src/app/spy.component.html" path="lifecycle-hooks/src/app/spy.component.html" region="template"></code-example>.

Создание и уничтожение каждого шпиона отмечает появление и исчезновение присоединенного героя `<p>` записью в _Hook Log_. Добавление героя приводит к появлению нового героя `<p>`.

Шпионская функция `ngOnInit()` регистрирует это событие.

Кнопка _Reset_ очищает список `героев`. Angular удаляет все элементы героя `<p>` из DOM и одновременно уничтожает их шпионские директивы.

Метод `ngOnDestroy()` шпиона сообщает о его последних минутах.

<a id="counter"></a>

### Используйте крючки компонентов и директив вместе

В этом примере `CounterComponent` использует метод `ngOnChanges()` для регистрации изменений каждый раз, когда родительский компонент увеличивает свое входное свойство `counter`.

Этот пример применяет `SpyDirective` из предыдущего примера к журналу `CounterComponent`, чтобы следить за созданием и уничтожением записей журнала.

<a id="onchanges"></a>

## Использование крючков обнаружения изменений

Angular вызывает метод `ngOnChanges()` компонента или директивы всякий раз, когда обнаруживает изменения **_вводных свойств_**. Пример _onChanges_ демонстрирует это, отслеживая хук `OnChanges()`.

<code-example header="on-changes.component.ts (excerpt)" path="lifecycle-hooks/src/app/on-changes.component.ts" region="ng-on-changes"></code-example>.

Метод `ngOnChanges()` принимает объект, который сопоставляет каждое измененное имя свойства с объектом [SimpleChange](api/core/SimpleChange), содержащим текущее и предыдущее значения свойства. Этот хук перебирает измененные свойства и записывает их в журнал.

Пример компонента `OnChangesComponent` имеет два входных свойства: `герой` и `сила`.

<code-example header="src/app/on-changes.component.ts" path="lifecycle-hooks/src/app/on-changes.component.ts" region="inputs"></code-example>.

Хост `OnChangesParentComponent` привязывается к ним следующим образом.

<code-example header="src/app/on-changes-parent.component.html" path="lifecycle-hooks/src/app/on-changes-parent.component.html" region="on-changes"></code-example>.

Вот пример в действии, когда пользователь вносит изменения.

<div class="lightbox">

<img alt="OnChanges" src="generated/images/guide/lifecycle-hooks/on-changes-anim.gif">

</div>

Записи журнала появляются по мере изменения строкового значения свойства _power_. Заметьте, однако, что метод `ngOnChanges()` не перехватывает изменения `hero.name`.
Это происходит потому, что Angular вызывает хук только при изменении значения входного свойства.

В данном случае `hero` - это входное свойство, а значение свойства `hero` - это _ссылка на объект hero_.

Ссылка на объект не изменилась, когда изменилось значение его собственного свойства `name`.

<a id="afterview"></a>

### Responding to view changes

As Angular traverses the [view hierarchy](guide/glossary#view-hierarchy 'Definition of view hierarchy definition') during change detection, it needs to be sure that a change in a child does not attempt to cause a change in its own parent. Such a change would not be rendered properly, because of how [unidirectional data flow](guide/glossary#unidirectional-data-flow 'Definition') works.

If you need to make a change that inverts the expected data flow, you must trigger a new change detection cycle to allow that change to be rendered. The examples illustrate how to make such changes safely.

The _AfterView_ sample explores the `AfterViewInit()` and `AfterViewChecked()` hooks that Angular calls _after_ it creates a component's child views.

Here's a child view that displays a hero's name in an `<input>`:

<code-example header="ChildViewComponent" path="lifecycle-hooks/src/app/child-view.component.ts" region="child-view"></code-example>.

Компонент `AfterViewComponent` отображает это дочернее представление _в своем шаблоне_:

<code-example header="AfterViewComponent (template)" path="lifecycle-hooks/src/app/after-view.component.ts" region="template"></code-example>

Следующие хуки выполняют действия, основанные на изменении значений _в дочернем представлении_, которое можно получить только путем запроса дочернего представления с помощью свойства, украшенного [@ViewChild](api/core/ViewChild).

<code-example header="AfterViewComponent (выдержки из класса)" path="lifecycle-hooks/src/app/after-view.component.ts" region="hooks"></code-example>.

<a id="wait-a-tick"></a>

#### Ожидание перед обновлением представления

В этом примере метод `doSomething()` обновляет экран, когда имя героя превышает 10 символов, но ждет тик перед обновлением `comment`.

<code-example header="AfterViewComponent (doSomething)" path="lifecycle-hooks/src/app/after-view.component.ts" region="do-something"></code-example>.

Оба хука `AfterViewInit()` и `AfterViewChecked()` срабатывают после составления представления компонента. Если вы измените код таким образом, чтобы хук обновлял свойство компонента `comment`, связанное с данными, немедленно, вы увидите, что Angular выбрасывает ошибку.

Оператор `LoggerService.tick_then()` откладывает обновление журнала на один оборот цикла JavaScript браузера, что запускает новый цикл обнаружения изменений.

#### Пишите бережливые методы хуков, чтобы избежать проблем с производительностью.

Когда вы запускаете пример _AfterView_, обратите внимание, как часто Angular вызывает `AfterViewChecked()` - часто тогда, когда нет никаких изменений, представляющих интерес. Будьте внимательны к тому, как много логики или вычислений вы вкладываете в один из этих методов.

<div class="lightbox">

<img alt="AfterView" src="generated/images/guide/lifecycle-hooks/after-view-anim.gif">

</div>

<a id="aftercontent"></a> <a id="aftercontent-hooks"></a>

<a id="content-projection"></a>

### Реагирование на изменения проецируемого содержимого

_Проекция контента_ - это способ импортировать HTML-контент извне компонента и вставить его в шаблон компонента в определенном месте. Определить проекцию содержимого в шаблоне можно по следующим признакам.

-   HTML между тегами элементов компонента

-   Наличие тегов `<ng-content>` в шаблоне компонента

<div class="alert is-helpful">

Разработчики AngularJS знают эту технику как _transclusion_.

</div>

Пример _AfterContent_ исследует хуки `AfterContentInit()` и `AfterContentChecked()`, которые Angular вызывает _после_ того, как Angular проецирует внешний контент в компонент.

Рассмотрим эту вариацию на примере [предыдущего _AfterView_](#afterview). На этот раз вместо того, чтобы включать дочернее представление в шаблон, он импортирует содержимое из родительского хука `AfterContentComponent`.

Ниже приведен шаблон родителя.

<code-example header="AfterContentParentComponent (выдержка из шаблона)" path="lifecycle-hooks/src/app/after-content-parent.component.ts" region="parent-template"></code-example>.

Обратите внимание, что тег `<app-child>` находится между тегами `<after-content>`. Никогда не помещайте содержимое между тегами элементов компонента _если вы не собираетесь проецировать это содержимое в компонент_.

Теперь посмотрите на шаблон компонента.

<code-example header="AfterContentComponent (template)" path="lifecycle-hooks/src/app/after-content.component.ts" region="template"></code-example>.

Тег `<ng-content>` является _заместителем_ для внешнего содержимого. Он указывает Angular, куда вставить это содержимое.

В данном случае проектируемый контент - это `<app-child>` от родителя.

<div class="lightbox">

<img alt="Projected Content" src="generated/images/guide/lifecycle-hooks/projected-child-view.png">

</div>

#### Использование хуков AfterContent

Хуки _AfterContent_ похожи на хуки _AfterView_. Ключевое различие заключается в дочернем компоненте.

-   Хуки _AfterView_ касаются `ViewChildren`, дочерних компонентов, чьи теги элементов появляются _внутри_ шаблона компонента.

-   Хуки _AfterContent_ касаются `ContentChildren`, дочерних компонентов, которые Angular проецирует в компонент.

Следующие хуки _AfterContent_ выполняют действия, основанные на изменении значений в _дочерних компонентах контента_, которые можно получить только запросив их с помощью свойства, украшенного [@ContentChild](api/core/ContentChild).

<code-example header="AfterContentComponent (выдержки из класса)" path="lifecycle-hooks/src/app/after-content.component.ts" region="hooks"></code-example>.

<a id="no-unidirectional-flow-worries"></a>

<div class="callout is-helpful">

<header>No need to wait for content updates</header>

Метод `doSomething()` этого компонента немедленно обновляет свойство компонента `comment`, связанное с данными. Нет необходимости [задерживать обновление для обеспечения правильного рендеринга] (#wait-a-tick "Delaying updates").

Angular вызывает оба хука _AfterContent_ перед вызовом любого из хуков _AfterView_. Angular завершает композицию проектируемого контента _до_ завершения композиции представления этого компонента.

Между хуками `AfterContent...` и `AfterView...` есть небольшое окно, которое позволяет вам изменять представление хоста.

</div>

<a id="docheck"></a>

## Определение пользовательской проверки изменений

Чтобы отслеживать изменения, которые происходят там, где `ngOnChanges()` их не поймает, реализуйте собственную проверку изменений, как показано в примере _DoCheck_. Этот пример показывает, как использовать хук `ngDoCheck()` для обнаружения изменений, которые Angular не отлавливает самостоятельно, и принятия соответствующих мер.

Пример _DoCheck_ расширяет пример _OnChanges_ следующим хуком `ngDoCheck()`:

<code-example header="DoCheckComponent (ngDoCheck)" path="lifecycle-hooks/src/app/do-check.component.ts" region="ng-do-check"></code-example>.

Этот код проверяет определенные _значения, представляющие интерес_, фиксируя и сравнивая их текущее состояние с предыдущими значениями. Он записывает специальное сообщение в журнал, когда нет существенных изменений в `герое` или `силе`, чтобы вы могли видеть, как часто вызывается `DoCheck()`.

Результаты наглядны.

<div class="lightbox">

<img alt="DoCheck" src="generated/images/guide/lifecycle-hooks/do-check-anim.gif">

</div>

While the `ngDoCheck()` hook can detect when the hero's `name` has changed, it is an expensive hook. This hook is called with enormous frequency &mdash;after _every_ change detection cycle no matter where the change occurred.
It's called over twenty times in this example before the user can do anything.

Most of these initial checks are triggered by Angular's first rendering of _unrelated data elsewhere on the page_. Just moving the cursor into another `<input>` triggers a call.

Relatively few calls reveal actual changes to pertinent data.

If you use this hook, your implementation must be extremely lightweight or the user experience suffers.

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
