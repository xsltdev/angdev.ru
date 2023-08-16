---
description: Приложение Angular использует отдельные компоненты для определения и управления различными аспектами приложения
---

# Введение в компоненты и шаблоны

Компонент _компонента_ управляет участком экрана, называемым _вид_. Он состоит из класса TypeScript, шаблона HTML и таблицы стилей CSS. Класс TypeScript определяет взаимодействие

шаблона HTML и отрисованной структуры DOM, а таблица стилей описывает его внешний вид.

Приложение Angular использует отдельные компоненты для определения и управления различными аспектами приложения. Например, приложение может включать компоненты для описания:

-   корень приложения с навигационными ссылками

-   Список героев

-   Редактор героев

В следующем примере класс `HeroListComponent` включает:

-   Свойство `heroes`, которое содержит массив героев.

-   Свойство `selectedHero`, которое содержит последнего героя, выбранного пользователем.

-   Метод `selectHero()` устанавливает свойство `selectedHero`, когда пользователь щелкает мышью, чтобы выбрать героя из списка.

Компонент инициализирует свойство `heroes` с помощью сервиса `HeroService`, который является TypeScript [свойством параметра](https://www.typescriptlang.org/docs/handbook/2/classes.html#parameter-properties) на конструкторе. Система инъекции зависимостей Angular предоставляет компоненту сервис `HeroService`.

<code-example header="src/app/hero-list.component.ts (class)" path="architecture/src/app/hero-list.component.ts" region="class"></code-example>.

Angular создает, обновляет и уничтожает компоненты по мере того, как пользователь перемещается по приложению. Ваше приложение может предпринимать действия в каждый момент этого жизненного цикла с помощью необязательных [lifecycle hooks](lifecycle-hooks.md), таких как `ngOnInit()`.

## Метаданные компонента

<div class="lightbox">

<img alt="Metadata" class="left" src="generated/images/guide/architecture/metadata.png">

</div>

Декоратор `@Component` идентифицирует класс, расположенный непосредственно под ним, как класс компонента и определяет его метаданные. В приведенном ниже примере кода видно, что `HeroListComponent` - это просто класс, без каких-либо специальных обозначений или синтаксиса Angular.
Он не является компонентом, пока вы не пометите его как компонент с помощью декоратора `@Component`.

Метаданные компонента указывают Angular, где взять основные строительные блоки, необходимые для создания и представления компонента и его вида. В частности, он связывает _шаблон_ с компонентом, либо непосредственно со встроенным кодом, либо по ссылке.

Вместе компонент и его шаблон описывают _вид_.

Помимо содержания шаблона или указания на него, метаданные `@Component` определяют, например, как на компонент можно ссылаться в HTML и какие службы ему требуются.

Вот пример основных метаданных для `HeroListComponent`.

<code-example header="src/app/hero-list.component.ts (metadata)" path="architecture/src/app/hero-list.component.ts" region="metadata"></code-example>

Этот пример показывает некоторые из наиболее полезных опций конфигурации `@Component`:

| Параметры конфигурации | Подробности | |:--- |:--- |:--- |

| `selector` | CSS-селектор, который указывает Angular создать и вставить экземпляр этого компонента везде, где он найдет соответствующий тег в HTML шаблона. Например, если HTML приложения содержит `<app-hero-list></app-hero-list>`, то Angular вставляет экземпляр представления `HeroListComponent` между этими тегами. |

| `templateUrl` | Относительный к модулю адрес HTML-шаблона этого компонента. В качестве альтернативы, вы можете указать HTML-шаблон в строке, как значение свойства `template`. Этот шаблон определяет _хостовое представление_ компонента. |

| `providers` | Массив [providers](glossary.md#provider) для сервисов, которые требуются компоненту. В примере это указывает Angular, как предоставить экземпляр `HeroService`, который конструктор компонента использует для получения списка героев для отображения. |

## Шаблоны и представления

<div class="lightbox">

<img alt="Template" class="left" src="generated/images/guide/architecture/template.png">

</div>

Вы определяете вид компонента с помощью сопутствующего шаблона. Шаблон - это форма HTML, которая указывает Angular, как отобразить компонент.

Представления обычно организованы иерархически, что позволяет изменять или показывать и скрывать целые разделы пользовательского интерфейса или страницы как единое целое. Шаблон, непосредственно связанный с компонентом, определяет _хост-вид_ этого компонента.

Компонент также может определять _иерархию представлений_, которая содержит _вложенные представления_, размещенные в других компонентах.

<div class="lightbox">

<img alt="Component tree" class="left" src="generated/images/guide/architecture/component-tree.png">

</div>

Иерархия представлений может включать представления из компонентов одного и того же NgModule и из компонентов разных NgModules.

## Синтаксис шаблонов

Шаблон выглядит как обычный HTML, за исключением того, что он также содержит синтаксис Angular [template syntax](template-syntax.md), который изменяет HTML на основе логики вашего приложения и состояния данных приложения и DOM. Ваш шаблон может использовать _привязки данных_ для координации данных приложения и DOM, _трубы_ для преобразования данных перед их отображением и _директивы_ для применения логики приложения к тому, что отображается.

Например, вот шаблон для компонента `HeroListComponent` учебника.

<code-example header="src/app/hero-list.component.html" path="architecture/src/app/hero-list.component.html" ></code-example>.

Этот шаблон использует типичные элементы HTML, такие как `<h2>` и `<p>`. Он также включает элементы синтаксиса шаблона Angular, `*ngFor`, `{{hero.name}}`, `(click)`, `[hero]` и `<app-hero-detail>`. Элементы синтаксиса шаблона указывают Angular, как вывести HTML на экран, используя программную логику и данные.

-   Директива `*ngFor` указывает Angular на итерацию списка.

-   `{{герой.имя}}`, `(клик)` и `[герой]` связывают данные программы с DOM и обратно, реагируя на ввод пользователя.

    Подробнее о [связывании данных](#data-binding) см. ниже.

-   Тег элемента `<app-hero-detail>` в примере представляет новый компонент, `HeroDetailComponent`.

    Компонент `HeroDetailComponent` определяет часть `hero-detail` визуализированной DOM-структуры, заданной компонентом `HeroListComponent`.

    Обратите внимание, как эти пользовательские компоненты смешиваются с родным HTML.

### Привязка данных

Без фреймворка вы были бы ответственны за введение значений данных в элементы управления HTML и превращение ответов пользователя в действия и обновления значений. Написание такой логики вручную утомительно, чревато ошибками и является кошмаром для чтения, что может подтвердить любой опытный программист на JavaScript.

Angular поддерживает _двустороннее связывание данных_, механизм для координации частей шаблона с частями компонента. Добавьте разметку привязки данных в HTML шаблона, чтобы указать Angular, как соединить обе стороны.

На следующей диаграмме показаны четыре формы разметки привязки данных. Каждая форма имеет направление: к DOM, из DOM или и то, и другое.

<div class="lightbox">

<img alt="Data Binding" class="left" src="generated/images/guide/architecture/databinding.png">

</div>

Этот пример из шаблона `HeroListComponent` использует три таких формы.

<code-example header="src/app/hero-list.component.html (binding)" path="architecture/src/app/hero-list.component.1.html" region="binding"></code-example>

| Data bindings | Details | |:--- |:--- |

| `[hero]` [property binding](property-binding.md) | Passes the value of `selectedHero` from the parent `HeroListComponent` to the `hero` property of the child `HeroDetailComponent`. |

| `(click)` [event binding](user-input.md#binding-to-user-input-events) | Calls the component's `selectHero` method when the user clicks a hero's name. |

| `{{hero.name}}` [interpolation](interpolation.md) | Displays the component's `hero.name` property value within the `<button>` element. |

Two-way data binding (used mainly in [template-driven forms](forms.md)) combines property and event binding in a single notation. Here's an example from the `HeroDetailComponent` template that uses two-way data binding with the `ngModel` directive.

<code-example header="src/app/hero-detail.component.html (ngModel)" path="architecture/src/app/hero-detail.component.html" region="ngModel"></code-example>.

При двустороннем связывании значение свойства данных поступает в поле ввода из компонента, как при связывании свойств. Изменения пользователя также возвращаются в компонент, сбрасывая свойство на последнее значение, как при привязке к событию.

Angular обрабатывает _все_ привязки данных один раз для каждого цикла событий JavaScript, начиная с корня дерева компонентов приложения и заканчивая всеми дочерними компонентами.

<div class="lightbox">

<img alt="Data Binding" class="left" src="generated/images/guide/architecture/component-databinding.png">

</div>

Привязка данных играет важную роль в коммуникации между шаблоном и его компонентом, а также важна для коммуникации между родительскими и дочерними компонентами.

<div class="lightbox">

<img alt="Parent/Child binding" class="left" src="generated/images/guide/architecture/parent-child-binding.png">

</div>

### Трубы

Трубы Angular позволяют объявлять преобразования отображения-значения в HTML шаблона. Класс с декоратором `@Pipe` определяет функцию, которая преобразует входные значения в выходные значения для отображения в представлении.

Angular определяет различные трубы, такие как [date](api/common/DatePipe) и [currency](api/common/CurrencyPipe). Полный список см. в [Pipes API list](api?type=pipe). Вы также можете определить новые трубы.

Чтобы указать преобразование значений в шаблоне HTML, используйте оператор [pipe operator (`|`)](pipes.md).

<code-example format="html" language="html">

{{interpolated_value &verbar; pipe_name}}

</code-example>

Вы можете объединять трубы в цепочку, отправляя вывод одной функции трубы для преобразования другой функцией трубы. Труба также может принимать аргументы, которые управляют тем, как она выполняет преобразование.
Например, вы можете передать желаемый формат в функцию pipe `date`.

<code-example format="html" language="html">

&lt;!-- Формат по умолчанию: вывод 'Jun 15, 2015'--&gt; &lt;p&gt;Сегодня {{today &verbar; date}}&lt;/p&gt;

&lt;!-- fullDate format: output 'Monday, June 15, 2015'--&gt; &lt;p&gt;The date is {{today &verbar; date:'fullDate'}}&lt;/p&gt;

&lt;!-- формат shortTime: output '9:43 AM'--&gt; &lt;p&gt;The time is {{today &verbar; date:'shortTime'}}&lt;/p&gt;

</code-example>

### Директивы

<div class="lightbox">

<img alt="Directives" class="left" src="generated/images/guide/architecture/directive.png">

</div>

Шаблоны Angular являются _динамическими_. Когда Angular рендерит их, он преобразует DOM в соответствии с инструкциями, заданными _директивами_.
Директива - это класс с декоратором `@Directive()`.

Компонент технически является директивой. Однако компоненты настолько характерны и важны для приложений Angular, что Angular определяет декоратор `@Component()`, который расширяет декоратор `@Directive()` с функциями, ориентированными на шаблоны.

Помимо компонентов, есть еще два вида директив: _структурные_ и _атрибутивные_. Angular определяет ряд директив обоих типов, и вы можете определить свои собственные с помощью декоратора `@Directive()`.

Как и для компонентов, метаданные для директивы связывают декорированный класс с элементом `selector`, который используется для вставки в HTML. В шаблонах директивы обычно появляются в теге элемента как атрибуты, либо по имени, либо как цель присваивания или привязки.

#### Структурные директивы

_Структурные директивы_ изменяют макет путем добавления, удаления и замены элементов в DOM. В примере шаблона используются две встроенные структурные директивы для добавления логики приложения к тому, как отображается представление.

<code-example header="src/app/hero-list.component.html (structural)" path="architecture/src/app/hero-list.component.1.html" region="structural"></code-example>

| Directives | Details | |:--- |:--- |

| [`*ngFor`](built-in-directives.md#ngFor) | An _iterative_, which tells Angular to create one `<li>` per hero in the `heroes` list. |

| [`*ngIf`](built-in-directives.md#ngIf) | A _conditional_, which includes the `HeroDetail` component only if a selected hero exists. |

#### Attribute directives

_Attribute directives_ alter the appearance or behavior of an existing element. In templates they look like regular HTML attributes, hence the name.

The `ngModel` directive, which implements two-way data binding, is an example of an attribute directive. `ngModel` modifies the behavior of an existing element \(typically `<input>`\) by setting its display value property and responding to change events.

<code-example header="src/app/hero-detail.component.html (ngModel)" path="architecture/src/app/hero-detail.component.html" region="ngModel"></code-example>.

Angular включает предопределенные директивы, которые изменяют:

-   Структуру макета, например [ngSwitch](built-in-directives.md#ngSwitch), и

-   Аспекты элементов и компонентов DOM, такие как [ngStyle](built-in-directives.md#ngstyle) и [ngClass](built-in-directives.md#ngClass).

<div class="alert is-helpful">

Узнайте больше в руководствах [Attribute Directives](attribute-directives.md) и [Structural Directives](structural-directives.md).

</div>

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
