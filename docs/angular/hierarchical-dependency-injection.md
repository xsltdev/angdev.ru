# Иерархические инжекторы

Инжекторы в Angular имеют правила, которые вы можете использовать для достижения желаемой видимости инжекторов в ваших приложениях. Понимая эти правила, вы можете определить, в каком NgModule, Component или Directive вам следует объявить провайдер.

<div class="alert is-helpful">

**NOTE**:<br /> This topic uses the following pictographs.

| html entities | pictographs | |:--- |:--- |

| <code>&#x1F33A;</code> | red hibiscus \(`🌺`\) |

| <code>&#x1F33B;</code> | sunflower \(`🌻`\) |

| <code>&#x1F337;</code> | tulip \(`🌷`\) |

| <code>&#x1F33F;</code> | fern \(`🌿`\) |

| <code>&#x1F341;</code> | maple leaf \(`🍁`\) |

| <code>&#x1F433;</code> | whale \(`🐳`\) |

| <code>&#x1F436;</code> | dog \(`🐶`\) |

| <code>&#x1F994;</code> | hedgehog \(`🦔`\) |

</div>

Приложения, которые вы создаете с помощью Angular, могут стать довольно большими, и одним из способов управления этой сложностью является разделение приложения на множество небольших хорошо инкапсулированных модулей, которые сами по себе разделены на четко определенное дерево компонентов.

На вашей странице могут быть разделы, которые работают совершенно независимо от остальной части приложения, со своими локальными копиями служб и других зависимостей, которые им необходимы. Некоторые из сервисов, которые используют эти разделы приложения, могут быть общими с другими частями приложения или с родительскими компонентами, которые находятся дальше по дереву компонентов, в то время как другие зависимости должны быть частными.

С помощью иерархической инъекции зависимостей вы можете изолировать разделы приложения и предоставить им свои собственные частные зависимости, не разделяемые с остальной частью приложения, или заставить родительские компоненты разделять определенные зависимости только с дочерними компонентами, но не с остальной частью дерева компонентов, и так далее. Иерархическая инъекция зависимостей позволяет вам обмениваться зависимостями между различными частями приложения только тогда, когда и если это необходимо.

## Типы иерархий инжекторов

Инжекторы в Angular имеют правила, которые вы можете использовать для достижения желаемой видимости инжекторов в ваших приложениях.

Понимая эти правила, вы можете определить, в каком

NgModule, Component или Directive вы должны объявить провайдер.

Angular имеет две иерархии инжекторов:

| Иерархии инжекторов | Подробности | | |:--- |:--- |:---.

| Иерархия `ModuleInjector` | Настройте `ModuleInjector` в этой иерархии, используя аннотацию `@NgModule()` или `@Injectable()`. |

| Иерархия `ElementInjector` | Создается неявно в каждом элементе DOM. По умолчанию `ElementInjector` пуст, если вы не настроили его в свойстве `providers` в `@Directive()` или `@Component()`. |

<a id="register-providers-injectable"></a>

### `ModuleInjector`

Инжектор модулей можно настроить одним из двух способов, используя:

-   Свойство `@Injectable()` `providedIn` для ссылки на `@NgModule()`, или `root`.

-   Массив `@NgModule()` `providers`.

<div class="callout is-helpful">

<header>Tree-shaking and &commat;Injectable()</header>

Использование свойства `@Injectable()` `providedIn` предпочтительнее, чем использование массива `@NgModule()` `providers`. Используя `@Injectable()` `providedIn`, инструменты оптимизации могут выполнять древовидную встряску, которая удаляет сервисы, не используемые вашим приложением. Это приводит к уменьшению размера пакета.

Tree-shaking особенно полезен для библиотеки, поскольку приложение, использующее библиотеку, может не иметь необходимости в ее инжектировании. Подробнее о [tree-shakable providers](guide/architecture-services#providing-services) читайте в [Introduction to services and dependency injection](guide/architecture-services).

</div>

`ModuleInjector` конфигурируется свойствами `@NgModule.providers` и `NgModule.imports`. `ModuleInjector` - это уплощение всех массивов провайдеров, которые можно получить, рекурсивно следуя за `NgModule.imports`.

Дочерние иерархии `ModuleInjector` создаются при ленивой загрузке других `@NgModules`.

Предоставляйте сервисы с помощью свойства `providedIn` из `@Injectable()` следующим образом:

<code-example format="typescript" language="typescript">

import { Injectable } from '&commat;angular/core';

&commat;Injectable({ providedIn: 'root' // &lt;- предоставляет этот сервис в корне ModuleInjector

})

export class ItemService {

name = 'phone';

}

</code-example>

Декоратор `@Injectable()` идентифицирует класс сервиса. Свойство `providedIn` настраивает определенный `ModuleInjector`, здесь `root`, что делает сервис доступным в `root` `ModuleInjector`.

#### Инжектор платформы

Есть еще два инжектора над `root`, дополнительный `ModuleInjector` и `NullInjector()`.

Рассмотрим, как Angular загружает приложение, используя следующее в файле `main.ts`:

<code-example format="javascript" language="javascript">

platformBrowserDynamic().bootstrapModule(AppModule).then(ref =&gt; {&hellip;})

</code-example>

Метод `bootstrapModule()` создает дочерний инжектор инжектора платформы, который конфигурируется `AppModule`. Это `корневой` `ModuleInjector`.

Метод `platformBrowserDynamic()` создает инжектор, настроенный `PlatformModule`, который содержит специфические для платформы зависимости. Это позволяет нескольким приложениям совместно использовать конфигурацию платформы.

Например, браузер имеет только одну строку URL, независимо от того, сколько приложений у вас запущено.

Вы можете настроить дополнительные провайдеры на уровне платформы, предоставив `extraProviders` с помощью функции `platformBrowser()`.

Следующим родительским инжектором в иерархии является `NullInjector()`, который является вершиной дерева. Если вы забрались так далеко вверх по дереву, что ищете сервис в `NullInjector()`, вы получите ошибку, если только не использовали `@Optional()`, потому что в конечном итоге все заканчивается на `NullInjector()` и он возвращает ошибку или, в случае `@Optional()`, `null`.

Более подробную информацию о `@Optional()` смотрите в разделе [`@Optional()`](guide/hierarchical-dependency-injection#optional) этого руководства.

Следующая диаграмма представляет отношения между `корневым` `ModuleInjector` и его родительскими инжекторами, как описано в предыдущих параграфах.

<div class="lightbox">

<img alt="NullInjector, ModuleInjector, root injector" src="generated/images/guide/dependency-injection/injectors.svg">

</div>

Хотя имя `root` является специальным псевдонимом, другие иерархии `ModuleInjector` не имеют псевдонимов. У вас есть возможность создавать иерархии `ModuleInjector` всякий раз, когда создается динамически загружаемый компонент, например, Router, который будет создавать дочерние иерархии `ModuleInjector`.

Все запросы направляются к корневому инжектору, независимо от того, настроили ли вы его с помощью метода `bootstrapModule()` или зарегистрировали все провайдеры с `root` в своих собственных сервисах.

<div class="callout is-helpful">

<header>&commat;Injectable() vs. &commat;NgModule()</header>

Если вы настраиваете провайдера для всего приложения в `@NgModule()` из `AppModule`, он переопределяет провайдера, настроенного для `root` в метаданных `@Injectable()`. Вы можете сделать это, чтобы сконфигурировать провайдера не по умолчанию для сервиса, который совместно используется несколькими приложениями.

Вот пример случая, когда в конфигурацию маршрутизатора компонента включена стратегия размещения не по умолчанию [location strategy](guide/router#location-strategy) путем перечисления его провайдера в списке `providers` модуля `AppModule`.

<code-example header="src/app/app.module.ts (providers)" path="dependency-injection-in-action/src/app/app/app.module.ts" region="providers"></code-example>

</div>

### `ElementInjector`

Angular создает иерархии `ElementInjector` неявно для каждого элемента DOM.

Предоставление сервиса в декораторе `@Component()` с помощью свойства `providers` или `viewProviders` настраивает `ElementInjector`. Например, следующий `TestComponent` конфигурирует `ElementInjector`, предоставляя сервис следующим образом:

<code-example format="typescript" language="typescript">

&commat;Component({ &hellip;
провайдеры: [{ { provide: ItemService, useValue: { name: 'lamp' } }]

})

export class TestComponent

</code-example>

<div class="alert is-helpful">

**NOTE**: <br /> See the [resolution rules](guide/hierarchical-dependency-injection#resolution-rules) section to understand the relationship between the `ModuleInjector` tree and the `ElementInjector` tree.

</div>

Когда вы предоставляете услуги в компоненте, эта услуга доступна через `ElementInjector` в данном экземпляре компонента. Он также может быть виден в дочерних компонентах/директивах на основании правил видимости, описанных в разделе [Правила разрешения](guide/hierarchical-dependency-injection#resolution-rules).

Когда экземпляр компонента уничтожается, уничтожается и экземпляр сервиса.

#### `@Директива()` и `@Компонент()`.

Компонент - это особый тип директивы, а это значит, что так же, как `@Directive()` имеет свойство `providers`, `@Component()` тоже имеет его. Это означает, что директивы, как и компоненты, могут настраивать провайдеров, используя свойство `providers`.

Когда вы настраиваете провайдера для компонента или директивы с помощью свойства `providers`, этот провайдер принадлежит `ElementInjector` этого компонента или директивы.

Компоненты и директивы на одном и том же элементе имеют общий инжектор.

<a id="resolution-rules"></a>

## Правила разрешения

При разрешении токена для компонента/директивы, Angular разрешает его в два этапа:

1.  По отношению к родителям в иерархии `ElementInjector`.

2.  По отношению к родителям в иерархии `ModuleInjector`.

Когда компонент объявляет зависимость, Angular пытается удовлетворить эту зависимость с помощью собственного `ElementInjector`. Если инжектору компонента не хватает провайдера, он передает запрос вверх к `ElementInjector` своего родительского компонента.

Запросы продолжают передаваться до тех пор, пока Angular не найдет инжектор, способный обработать запрос, или пока не закончатся иерархии предков `ElementInjector`.

Если Angular не находит провайдера ни в одной иерархии `ElementInjector`, он возвращается к элементу, откуда пришел запрос, и ищет его в иерархии `ModuleInjector`. Если Angular все еще не находит провайдера, он выдает ошибку.

Если вы зарегистрировали провайдера для одного и того же DI-токена на разных уровнях, то для разрешения зависимости Angular использует первый встреченный провайдер. Если, например, провайдер зарегистрирован локально в компоненте, которому нужен сервис,

Angular не будет искать другого провайдера той же услуги.

## Модификаторы разрешения

Поведение Angular при разрешении может быть изменено с помощью `@Optional()`, `@Self()`, `@SkipSelf()` и `@Host()`. Импортируйте каждый из них из `@angular/core` и используйте каждый в конструкторе класса компонента, когда вы внедряете свой сервис.

Рабочее приложение, демонстрирующее модификаторы разрешения, которые рассматриваются в этом разделе, смотрите в <live-example name="resolution-modifiers">примере модификаторов разрешения</live-example>.

### Типы модификаторов

Модификаторы разрешения делятся на три категории:

-   Что делать, если Angular не находит то, что вы ищете, то есть `@Optional()`.

-   Где начать поиск, то есть `@SkipSelf()`.

-   Где остановить поиск, `@Host()` и `@Self()`.

По умолчанию Angular всегда начинает с текущего `Injector` и продолжает поиск по всему пути вверх. Модификаторы позволяют изменять начальное, или _self_, местоположение и конечное местоположение.

Кроме того, вы можете комбинировать все модификаторы, кроме `@Host()` и `@Self()` и, конечно, `@SkipSelf()` и `@Self()`.

<a id="optional"></a>

### `@Optional()`

`@Optional()` позволяет Angular считать сервис, который вы вводите, необязательным. Таким образом, если он не может быть разрешен во время выполнения, Angular разрешает его как `null`, а не выдает ошибку.

В следующем примере сервис `OptionalService` не предоставляется ни в сервисе, ни в `@NgModule()`, ни в классе компонента, поэтому он недоступен нигде в приложении.

<code-example header="src/app/optional/optional.component.ts" path="resolution-modifiers/src/app/optional/optional.component.ts" region="optional-component"></code-example>.

### `@Self()`

Используйте `@Self()`, чтобы Angular просматривал `ElementInjector` только для текущего компонента или директивы.

Хорошим вариантом использования `@Self()` является внедрение сервиса, но только если он доступен для текущего элемента хоста. Чтобы избежать ошибок в этой ситуации, комбинируйте `@Self()` с `@Optional()`.

Например, в следующем `SelfComponent` обратите внимание на инжектированный `LeafService` в конструкторе.

<code-example header="src/app/self-no-data/self-no-data.component.ts" path="resolution-modifiers/src/app/self-no-data/self-no-data.component.ts" region="self-no-data-component"></code-example>

In this example, there is a parent provider and injecting the service will return the value, however, injecting the service with `@Self()` and `@Optional()` will return `null` because `@Self()` tells the injector to stop searching in the current host element.

Another example shows the component class with a provider for `FlowerService`. In this case, the injector looks no further than the current `ElementInjector` because it finds the `FlowerService` and returns the tulip <code>&#x1F337;</code>.

<code-example header="src/app/self/self.component.ts" path="resolution-modifiers/src/app/self/self.component.ts" region="self-component"></code-example>

### `@SkipSelf()`

`@SkipSelf()` is the opposite of `@Self()`. With `@SkipSelf()`, Angular starts its search for a service in the parent `ElementInjector`, rather than in the current one.

So if the parent `ElementInjector` were using the fern <code>&#x1F33F;</code> value for `emoji`, but you had maple leaf <code>&#x1F341;</code> in the component's `providers` array, Angular would ignore maple leaf <code>&#x1F341;</code> and use fern <code>&#x1F33F;</code>.

To see this in code, assume that the following value for `emoji` is what the parent component were using, as in this service:

<code-example header="src/app/leaf.service.ts" path="resolution-modifiers/src/app/leaf.service.ts" region="leafservice"></code-example>

Imagine that in the child component, you had a different value, maple leaf <code>&#x1F341;</code> but you wanted to use the parent's value instead. This is when you'd use `@SkipSelf()`:

<code-example header="src/app/skipself/skipself.component.ts" path="resolution-modifiers/src/app/skipself/skipself.component.ts" region="skipself-component"></code-example>

In this case, the value you'd get for `emoji` would be fern <code>&#x1F33F;</code>, not maple leaf <code>&#x1F341;</code>.

#### `@SkipSelf()` with `@Optional()`

Use `@SkipSelf()` with `@Optional()` to prevent an error if the value is `null`. In the following example, the `Person` service is injected in the constructor.

`@SkipSelf()` tells Angular to skip the current injector and `@Optional()` will prevent an error should the `Person` service be `null`.

<code-example format="typescript" language="typescript">

class Person { constructor(&commat;Optional() &commat;SkipSelf() parent?: Person) {}
}

</code-example>

### `@Host()`

`@Host()` позволяет вам назначить компонент последней остановкой в дереве инжекторов при поиске провайдеров. Даже если есть экземпляр сервиса дальше по дереву, Angular не будет продолжать поиск.

Используйте `@Host()` следующим образом:

<code-example header="src/app/host/host.component.ts" path="resolution-modifiers/src/app/host/host.component.ts" region="host-component"></code-example>

Since `HostComponent` has `@Host()` in its constructor, no matter what the parent of `HostComponent` might have as a `flower.emoji` value, the `HostComponent` will use tulip <code>&#x1F337;</code>.

## Logical structure of the template

When you provide services in the component class, services are visible within the `ElementInjector` tree relative to where and how you provide those services.

Understanding the underlying logical structure of the Angular template will give you a foundation for configuring services and in turn control their visibility.

Components are used in your templates, as in the following example:

<code-example format="html" language="html">

&lt;app-root&gt; &lt;app-child&gt;&lt;/app-child&gt;
&lt;/app-root&gt;

</code-example>

<div class="alert is-helpful">

**NOTE**: <br /> Usually, you declare the components and their templates in separate files.
For the purposes of understanding how the injection system works, it is useful to look at them from the point of view of a combined logical tree.

The term _logical_ distinguishes it from the render tree, which is your application's DOM tree.

To mark the locations of where the component templates are located, this guide uses the `<#VIEW>` pseudo-element, which doesn't actually exist in the render tree and is present for mental model purposes only.

</div>

Ниже приведен пример того, как деревья представлений `<app-root>` и `<app-child>` объединяются в одно логическое дерево:

<code-example format="html" language="html">

&lt;app-root&gt; &lt;#VIEW&gt;
&lt;app-child&gt;

     &lt;#VIEW&gt;

       &hellip;content goes here&hellip;

     &lt;/#VIEW&gt;

    &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

Понимание идеи демаркации `<#VIEW>` особенно важно, когда вы настраиваете сервисы в классе компонента.

## Предоставление сервисов в `@Компонент()`

То, как вы предоставляете сервисы с помощью декоратора `@Component()`\ (или `@Directive()`\), определяет их видимость. В следующих разделах демонстрируются `providers` и `viewProviders`, а также способы изменения видимости сервисов с помощью `@SkipSelf()` и `@Host()`.

Класс компонента может предоставлять услуги двумя способами:

| Массивы | Детали | | |:--- |:--- |:--- |.

| С помощью массива `providers` | <code-example format="typescript" language="typescript"> &commat;Component({ &NewLine;&nbsp; &hellip; &NewLine;&nbsp; providers: [ &NewLine;&nbsp;&nbsp;&nbsp;&nbsp; {provide: FlowerService, useValue: {emoji: '&#x1F33A;'}} &NewLine;&nbsp; ] &NewLine;}) </code-example> |

| С массивом `viewProviders` | <code-example format="typescript" language="typescript"> &commat;Component({ &NewLine;&nbsp; &hellip; &NewLine;&nbsp;viewProviders: [ &NewLine;&nbsp;&nbsp;&nbsp;&nbsp; {provide: AnimalService, useValue: {emoji: '&#x1F436;'}} &NewLine;&nbsp; ] &NewLine;}) </code-example> |

Чтобы понять, как `providers` и `viewProviders` по-разному влияют на видимость сервиса, в следующих разделах шаг за шагом строится <live-example name="providers-viewproviders"></live-example> и сравнивается использование `providers` и `viewProviders` в коде и логическом дереве.

<div class="alert is-helpful">

**NOTE**: <br /> In the logical tree, you'll see `@Provide`, `@Inject`, and `@NgModule`, which are not real HTML attributes but are here to demonstrate what is going on under the hood.

| Angular service attribute | Details | |:--- |:--- |

| <code-example format="typescript" hideCopy language="typescript"> &commat;Inject(Token)=&gt;Value </code-example> | Demonstrates that if `Token` is injected at this location in the logical tree its value would be `Value`. |

| <code-example format="typescript" hideCopy language="typescript"> &commat;Provide(Token=Value) </code-example> | Demonstrates that there is a declaration of `Token` provider with value `Value` at this location in the logical tree. |

| <code-example format="typescript" hideCopy language="typescript"> &commat;NgModule(Token) </code-example> | Demonstrates that a fallback `NgModule` injector should be used at this location. |

</div>

### Example app structure

The example application has a `FlowerService` provided in `root` with an `emoji` value of red hibiscus <code>&#x1F33A;</code>.

<code-example header="src/app/flower.service.ts" path="providers-viewproviders/src/app/flower.service.ts" region="flowerservice"></code-example>.

Рассмотрим приложение, в котором есть только `AppComponent` и `ChildComponent`. Самый базовый визуализированный вид будет выглядеть как вложенные HTML-элементы, как показано ниже:

<code-example format="html" language="html">

&lt;app-root&gt; &lt;!-- Селектор AppComponent --&gt; &lt;app-child&gt; &lt;!-- Селектор ChildComponent --&gt;
&lt;/app-child&gt;

&lt;/app-root&gt;

</code-example>

Однако за кулисами Angular использует логическое представление представления следующим образом при разрешении инъекционных запросов:

<code-example format="html" language="html">

&lt;app-root&gt; &lt;!-- Селектор AppComponent --&gt; &lt;#VIEW&gt;
&lt;app-child&gt; &lt;!-- Селектор ChildComponent --&gt;

            &lt;#VIEW&gt;

            &lt;/#VIEW&gt;

        &lt;/app-child&gt;

    &lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

Здесь `<#VIEW>` представляет собой экземпляр шаблона. Обратите внимание, что каждый компонент имеет свой собственный `<#VIEW>`.

Знание этой структуры может помочь вам понять, как вы предоставляете и внедряете свои службы, и дать вам полный контроль над видимостью служб.

Теперь рассмотрим, что `<app-root>` инжектирует `FlowerService`:

<code-example header="src/app/app.component.ts" path="providers-viewproviders/src/app/app.component.1.ts" region="injection"></code-example>

Добавьте привязку к шаблону `<app-root>` для визуализации результата:

<code-example header="src/app/app.component.html" path="providers-viewproviders/src/app/app/app.component.html" region="binding-flower"></code-example>

Вывод в представлении будет следующим:

<code-example format="output" hideCopy language="shell">

Emoji от FlowerService: &#x1F33A;

</code-example>

В логическом дереве это будет представлено следующим образом:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(FlowerService) flower=&gt;"&#x1F33A;"&gt;
&lt;#VIEW&gt;

    &lt;p&gt;Emoji из FlowerService: {{flower.emoji}} (&#x1F33A;)&lt;/p&gt;

    &lt;app-child&gt;

      &lt;#VIEW&gt;

      &lt;/#VIEW&gt;

    &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

Когда `<app-root>` запрашивает `FlowerService`, задача инжектора - разрешить токен `FlowerService`. Разрешение токена происходит в два этапа:

1.  Инжектор определяет начальное местоположение в логическом дереве и конечное местоположение поиска.

    Инжектор начинает с начального места и ищет токен на каждом уровне логического дерева.

    Если маркер найден, он возвращается.

1.  Если токен не найден, инжектор ищет ближайшего родителя `@NgModule()` для передачи запроса.

В примере ограничения следующие:

1.  Начинается с `<#VIEW>`, принадлежащего `<app-root>` и заканчивается `<app-root>`.

    -   Обычно начальная точка поиска находится в точке внедрения.

        Однако в данном случае `<app-root>` `@Component` являются особенными, поскольку они также включают свои собственные `viewProviders`, поэтому поиск начинается с `<#VIEW>`, принадлежащего `<app-root>`.

        Это не относится к директиве, сопоставленной в том же месте.

    -   Конечное местоположение совпадает с местоположением самого компонента, поскольку он является самым верхним компонентом в этом приложении.

1.  Модуль `AppModule` действует как запасной инжектор, когда инжектируемый токен не может быть найден в иерархии `ElementInjector`.

### Использование массива `providers`.

Теперь в классе `ChildComponent` добавьте провайдер для `FlowerService`, чтобы продемонстрировать более сложные правила разрешения в последующих разделах:

<code-example header="src/app/child.component.ts" path="providers-viewproviders/src/app/child/child.component.1.ts" region="flowerservice"></code-example>.

Теперь, когда `FlowerService` предоставлен в декораторе `@Component()`, когда `<app-child>` запрашивает сервис, инжектору достаточно посмотреть до `ElementInjector` в `<app-child>`. Ему не придется продолжать поиск дальше по дереву инжекторов.

Следующим шагом будет добавление привязки к шаблону `ChildComponent`.

<code-example header="src/app/child.component.html" path="providers-viewproviders/src/app/child/child.component.html" region="flower-binding"></code-example>.

Чтобы отобразить новые значения, добавьте `<app-child>` в нижнюю часть шаблона `AppComponent`, чтобы представление также отображало подсолнух:

<code-example format="output" hideCopy language="shell">

Детский компонент Emoji из FlowerService: &#x1F33B;

</code-example>

В логическом дереве это представлено следующим образом:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(FlowerService) flower=&gt;"&#x1F33A;"&gt;
&lt;#VIEW&gt;

    &lt;p&gt;Emoji из FlowerService: {{flower.emoji}} (&#x1F33A;)&lt;/p&gt;

    &lt;app-child &commat;Provide(FlowerService="&#x1F33B;")

               &commat;Inject(FlowerService)=&gt;"&#x1F33B;"&gt; &lt;!-- поиск заканчивается здесь --&gt;

      &lt;#VIEW&gt; &lt;!-- поиск начинается здесь --&gt;

        &lt;h2&gt;Родительский компонент&lt;/h2&gt;

        &lt;p&gt;Emoji от FlowerService: {{flower.emoji}} (&#x1F33B;)&lt;/p&gt;

      &lt;/#VIEW&gt;

    &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

When `<app-child>` requests the `FlowerService`, the injector begins its search at the `<#VIEW>` belonging to `<app-child>` \(`<#VIEW>` is included because it is injected from `@Component()`\) and ends with `<app-child>`. In this case, the `FlowerService` is resolved in the `providers` array with sunflower <code>&#x1F33B;</code> of the `<app-child>`.
The injector doesn't have to look any further in the injector tree.

It stops as soon as it finds the `FlowerService` and never sees the red hibiscus <code>&#x1F33A;</code>.

<a id="use-view-providers"></a>

### Использование массива `viewProviders`

Используйте массив `viewProviders` как еще один способ предоставления сервисов в декораторе `@Component()`. Использование `viewProviders` делает сервисы видимыми в `<#VIEW>`.

<div class="is-helpful alert">

Шаги те же, что и при использовании массива `providers`, за исключением использования массива `viewProviders`.

Для получения пошаговых инструкций продолжите этот раздел. Если вы можете настроить его самостоятельно, перейдите к [Изменение доступности сервиса](guide/hierarchical-dependency-injection#modify-visibility).

</div>

The example application features a second service, the `AnimalService` to demonstrate `viewProviders`.

First, create an `AnimalService` with an `emoji` property of whale <code>&#x1F433;</code>:

<code-example header="src/app/animal.service.ts" path="providers-viewproviders/src/app/animal.service.ts" region="animal-service"></code-example>.

Следуя той же схеме, что и в случае с `FlowerService`, внедрите `AnimalService` в класс `AppComponent`:

<code-example header="src/app/app.component.ts" path="providers-viewproviders/src/app/app.component.ts" region="inject-animal-service"></code-example>

<div class="alert is-helpful">

**NOTE**: <br /> You can leave all the `FlowerService` related code in place as it will allow a comparison with the `AnimalService`.

</div>

Add a `viewProviders` array and inject the `AnimalService` in the `<app-child>` class, too, but give `emoji` a different value. Here, it has a value of dog <code>&#x1F436;</code>.

<code-example header="src/app/child.component.ts" path="providers-viewproviders/src/app/child/child.component.ts" region="provide-animal-service"></code-example>.

Добавьте привязки к шаблонам `ChildComponent` и `AppComponent`. В шаблоне `ChildComponent` добавьте следующую привязку:

<code-example header="src/app/child.component.html" path="providers-viewproviders/src/app/child/child.component.html" region="animal-binding"></code-example>.

Кроме того, добавьте то же самое в шаблон `AppComponent`:

<code-example header="src/app/app.component.html" path="providers-viewproviders/src/app/app.component.html" region="binding-animal"></code-example>

Теперь вы должны увидеть оба значения в браузере:

<code-example format="output" hideCopy language="shell">

AppComponent Emoji из AnimalService: &#x1F433;

Child Component Emoji из AnimalService: &#x1F436;

</code-example>

Логическое дерево для этого примера `viewProviders` выглядит следующим образом:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(AnimalService) animal=&gt;"&#x1F433;"&gt;
&lt;#VIEW&gt;

    &lt;app-child&gt;

      &lt;#VIEW &commat;Provide(AnimalService="&#x1F436;")

            &commat;Inject(AnimalService=&gt;"&#x1F436;")&gt;

       &lt;!-- ^^ использование viewProviders означает, что AnimalService доступен в &lt;#VIEW&gt;--&gt;

       &lt;p&gt;Эмодзи из AnimalService: {{animal.emoji}} (&#x1F436;)&lt;/p&gt;

      &lt;/#VIEW&gt;

    &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

Just as with the `FlowerService` example, the `AnimalService` is provided in the `<app-child>` `@Component()` decorator. This means that since the injector first looks in the `ElementInjector` of the component, it finds the `AnimalService` value of dog <code>&#x1F436;</code>.
It doesn't need to continue searching the `ElementInjector` tree, nor does it need to search the `ModuleInjector`.

### `providers` vs. `viewProviders`

To see the difference between using `providers` and `viewProviders`, add another component to the example and call it `InspectorComponent`. `InspectorComponent` will be a child of the `ChildComponent`.

In `inspector.component.ts`, inject the `FlowerService` and `AnimalService` in the constructor:

<code-example header="src/app/inspector/inspector.component.ts" path="providers-viewproviders/src/app/inspector/inspector.component.ts" region="injection"></code-example>.

Вам не нужен массив `providers` или `viewProviders`. Далее, в `inspector.component.html`, добавьте ту же разметку, что и в предыдущих компонентах:

<code-example header="src/app/inspector/inspector.component.html" path="providers-viewproviders/src/app/inspector/inspector.component.html" region="binding"></code-example>.

Не забудьте добавить `InspectorComponent` в массив `AppModule` `declarations`.

<code-example header="src/app/app.module.ts" path="providers-viewproviders/src/app/app.module.ts" region="appmodule"></code-example>

Далее, убедитесь, что ваш `child.component.html` содержит следующее:

<code-example header="src/app/child/child.component.html" path="providers-viewproviders/src/app/child/child.component.html" region="child-component"></code-example>.

Первые две строки с привязками остались от предыдущих шагов. Новые части - это `<ng-content>` и `<app-inspector>`.

`<ng-content>` позволяет вам проектировать контент, а `<app-inspector>` внутри шаблона `ChildComponent` делает `InspectorComponent` дочерним компонентом `ChildComponent`.

Далее, добавьте следующее в `app.component.html`, чтобы воспользоваться преимуществами проекции содержимого.

<code-example header="src/app/app.component.html" path="providers-viewproviders/src/app/app.component.html" region="content-projection"></code-example>

Теперь браузер отображает следующее, опуская предыдущие примеры для краткости:

<code-example format="output" hideCopy language="shell">

//&hellip;Опуская предыдущие примеры. К этому разделу относится следующее.

Проекция содержимого: это происходит из содержимого. Не видит щенка, потому что щенок объявлен только внутри представления.

Emoji из FlowerService: &#x1F33B; Emoji из AnimalService: &#x1F433;

Emoji из FlowerService: &#x1F33B; Emoji из AnimalService: &#x1F436;

</code-example>

These four bindings demonstrate the difference between `providers` and `viewProviders`. Since the dog <code>&#x1F436;</code> is declared inside the `<#VIEW>`, it isn't visible to the projected content.
Instead, the projected content sees the whale <code>&#x1F433;</code>.

The next section though, where `InspectorComponent` is a child component of `ChildComponent`, `InspectorComponent` is inside the `<#VIEW>`, so when it asks for the `AnimalService`, it sees the dog <code>&#x1F436;</code>.

The `AnimalService` in the logical tree would look like this:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(AnimalService) animal=&gt;"&#x1F433;"&gt;
&lt;#VIEW&gt;

    &lt;app-child&gt;

      &lt;#VIEW &commat;Provide(AnimalService="&#x1F436;")

            &commat;Inject(AnimalService=&gt;"&#x1F436;")&gt;

        &lt;!-- ^^ использование viewProviders означает, что AnimalService доступен в &lt;#VIEW&gt;--&gt;

        &lt;p&gt;Эмодзи из AnimalService: {{animal.emoji}} (&#x1F436;)&lt;/p&gt;

        &lt;div class="container"&gt;
           &lt;h3&gt;Content projection&lt;/h3&gt;
          &lt;app-inspector &commat;Inject(AnimalService) animal=&gt;"&#x1F433;"&gt;
            &lt;p&gt;Emoji from AnimalService: {{animal.emoji}} (&#x1F433;)&lt;/p&gt;
          &lt;/app-inspector&gt;
        &lt;/div&gt;

      &lt;/#VIEW&gt;
      &lt;app-inspector&gt;
        &lt;#VIEW&gt;
          &lt;p&gt;Emoji from AnimalService: {{animal.emoji}} (&#x1F436;)&lt;/p&gt;
        &lt;/#VIEW&gt;
      &lt;/app-inspector&gt;
    &lt;/app-child&gt;

&lt;/#VIEW&gt; &lt;/app-root&gt;

</code-example>

The projected content of `<app-inspector>` sees the whale <code>&#x1F433;</code>, not the dog <code>&#x1F436;</code>, because the dog <code>&#x1F436;</code> is inside the `<app-child>` `<#VIEW>`. The `<app-inspector>` can only see the dog <code>&#x1F436;</code> if it is also within the `<#VIEW>`.

<a id="modify-visibility"></a>

## Изменение видимости сервиса

В этом разделе описывается, как ограничить область видимости начального и конечного `ElementInjector` с помощью декораторов видимости `@Host()`, `@Self()` и `@SkipSelf()`.

### Видимость предоставляемых лексем

Декораторы видимости влияют на то, где в дереве логики начинается и заканчивается поиск маркера инъекции. Для этого размещайте декораторы видимости в точке инъекции, то есть в `constructor()`, а не в точке объявления.

Чтобы изменить, где инжектор начинает искать `FlowerService`, добавьте `@SkipSelf()` в объявление `<app-child>` `@Inject` для `FlowerService`. Это объявление находится в конструкторе `<app-child>`, как показано в `child.component.ts`:

<code-example format="typescript" language="typescript">

constructor(&commat;SkipSelf() public flower : FlowerService) { }

</code-example>

With `@SkipSelf()`, the `<app-child>` injector doesn't look to itself for the `FlowerService`. Instead, the injector starts looking for the `FlowerService` at the `ElementInjector` or the `<app-root>`, where it finds nothing.
Then, it goes back to the `<app-child>` `ModuleInjector` and finds the red hibiscus <code>&#x1F33A;</code> value, which is available because the `<app-child>` `ModuleInjector` and the `<app-root>` `ModuleInjector` are flattened into one `ModuleInjector`.

Thus, the UI renders the following:

<code-example format="output" hideCopy language="shell">

Emoji от FlowerService: &#x1F33A;

</code-example>

В логическом дереве эта же идея может выглядеть следующим образом:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(FlowerService) flower=&gt;"&#x1F33A;"&gt;
&lt;#VIEW&gt;

    &lt;app-child &commat;Provide(FlowerService="&#x1F33B;")&gt;

      &lt;#VIEW &commat;Inject(FlowerService, SkipSelf)=&gt;"&#x1F33A;"&gt;

        &lt;!-- При SkipSelf инжектор обращается к следующему инжектору по дереву --&gt;

      &lt;/#VIEW&gt;

    &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

Though `<app-child>` provides the sunflower <code>&#x1F33B;</code>, the application renders the red hibiscus <code>&#x1F33A;</code> because `@SkipSelf()` causes the current injector to skip itself and look to its parent.

If you now add `@Host()` \(in addition to the `@SkipSelf()`\) to the `@Inject` of the `FlowerService`, the result will be `null`. This is because `@Host()` limits the upper bound of the search to the `<#VIEW>`.

Here's the idea in the logical tree:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(FlowerService) flower=&gt;"&#x1F33A;"&gt;
&lt;#VIEW&gt; &lt;!-- завершите поиск здесь с помощью null--&gt;

    &lt;app-child &commat;Provide(FlowerService="&#x1F33B;")&gt; &lt;!-- начать поиск здесь --&gt;

      &lt;#VIEW &commat;Inject(FlowerService, &commat;SkipSelf, &commat;Host, &commat;Optional)=&gt;null&gt;

      &lt;/#VIEW&gt;

      &lt;/app-parent&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

Здесь сервисы и их значения одинаковы, но `@Host()` не позволяет инжектору искать `<#VIEW>` для `FlowerService`, поэтому он не находит его и возвращает `null`.

<div class="alert is-helpful">

**NOTE**: <br /> The example application uses `@Optional()` so the application does not throw an error, but the principles are the same.

</div>

### `@SkipSelf()` and `viewProviders`

The `<app-child>` currently provides the `AnimalService` in the `viewProviders` array with the value of dog <code>&#x1F436;</code>. Because the injector has only to look at the `ElementInjector` of the `<app-child>` for the `AnimalService`, it never sees the whale <code>&#x1F433;</code>.

As in the `FlowerService` example, if you add `@SkipSelf()` to the constructor for the `AnimalService`, the injector won't look in the `ElementInjector` of the current `<app-child>` for the `AnimalService`.

<code-example format="typescript" language="typescript">

export class ChildComponent {

// добавить &commat;SkipSelf() constructor(&commat;SkipSelf() public animal : AnimalService) { }

}

</code-example>

Instead, the injector will begin at the `<app-root>` `ElementInjector`. Remember that the `<app-child>` class provides the `AnimalService` in the `viewProviders` array with a value of dog <code>&#x1F436;</code>:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'app-child',
&hellip;

viewProviders:

[{ provide: AnimalService, useValue: { emoji: '&#x1F436;' } }]]

})

</code-example>

Логическое дерево выглядит следующим образом с `@SkipSelf()` в `<app-child>`:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(AnimalService=&gt;"&#x1F433;")&gt;
&lt;#VIEW&gt;&lt;!-- поиск начинается здесь --&gt;

    &lt;app-child&gt;

      &lt;#VIEW &commat;Provide(AnimalService="&#x1F436;")

             &commat;Inject(AnimalService, SkipSelf=&gt;"&#x1F433;")&gt;

        &lt;!-Добавить &commat;SkipSelf --&gt;

      &lt;/#VIEW&gt;

    &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

With `@SkipSelf()` in the `<app-child>`, the injector begins its search for the `AnimalService` in the `<app-root>` `ElementInjector` and finds whale <code>&#x1F433;</code>.

### `@Host()` and `viewProviders`

If you add `@Host()` to the constructor for `AnimalService`, the result is dog <code>&#x1F436;</code> because the injector finds the `AnimalService` in the `<app-child>` `<#VIEW>`. Here is the `viewProviders` array in the `<app-child>` class and `@Host()` in the constructor:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'app-child',
&hellip;

viewProviders:

[{ provide: AnimalService, useValue: { emoji: '&#x1F436;' } }]]

}) export class ChildComponent {

constructor(&commat;Host() public animal : AnimalService) { }

}

</code-example>

`@Host()` заставляет инжектор искать, пока он не встретит край `<#VIEW>`.

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(AnimalService=&gt;"&#x1F433;")&gt;
&lt;#VIEW&gt;

    &lt;app-child&gt;

      &lt;#VIEW &commat;Provide(AnimalService="&#x1F436;")

             &commat;Inject(AnimalService, &commat;Host=&gt;"&#x1F436;")&gt; &lt;!-- &commat;Host останавливает поиск здесь --&gt;

      &lt;/#VIEW&gt;

    &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

Добавьте массив `viewProviders` с третьим животным, ежом <code>&#x1F994;</code>, в метаданные `app.component.ts` `@Component()`:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'app-root',
templateUrl: './app.component.html',

styleUrls: [ './app.component.css' ],

viewProviders: [{ provide: AnimalService, useValue: { emoji: '&#x1F994;' } } }]

})

</code-example>

Затем добавьте `@SkipSelf()` вместе с `@Host()` в конструктор для `Animal Service` в `child.component.ts`. Вот `@Host()` и `@SkipSelf()` в конструкторе `<app-child>`:

<code-example format="typescript" language="typescript">

export class ChildComponent {

constructor( &commat;Host() &commat;SkipSelf() public animal : AnimalService) { }

}

</code-example>

Когда `@Host()` и `SkipSelf()` были применены к `FlowerService`, который находится в массиве `providers`, результат был `null`, потому что `@SkipSelf()` начинает поиск в инжекторе `<app-child>`, но `@Host()` прекращает поиск в `<#VIEW>` &mdash; где нет `FlowerService` В логическом дереве видно, что `FlowerService` виден в `<app-child>`, а не в его `<#VIEW>`.

Однако `AnimalService`, который предоставляется в массиве `AppComponent` `viewProviders`, виден.

Представление логического дерева показывает, почему это так:

<code-example format="html" language="html">

&lt;app-root &commat;NgModule(AppModule) &commat;Inject(AnimalService=&gt;"&#x1F433;")&gt;
&lt;#VIEW &commat;Provide(AnimalService="&#x1F994;")

         &commat;Inject(AnimalService, &commat;Optional)=&gt;"&#x1F994;"&gt;

    &lt;!-- ^^&commat;SkipSelf() начинается здесь, &commat;Host() останавливается здесь^^ --&gt;

    &lt;app-child&gt;

      &lt;#VIEW &commat;Provide(AnimalService="&#x1F436;")

             &commat;Inject(AnimalService, &commat;SkipSelf, &commat;Host, &commat;Optional)=&gt;"&#x1F994;"&gt;

               &lt;!-- Добавить &commat;SkipSelf ^^--&gt;

      &lt;/#VIEW&gt;

      &lt;/app-child&gt;

&lt;/#VIEW&gt;

&lt;/app-root&gt;

</code-example>

`@SkipSelf()`, causes the injector to start its search for the `AnimalService` at the `<app-root>`, not the `<app-child>`, where the request originates, and `@Host()` stops the search at the `<app-root>` `<#VIEW>`. Since `AnimalService` is provided by way of the `viewProviders` array, the injector finds hedgehog <code>&#x1F994;</code> in the `<#VIEW>`.

<a id="component-injectors"></a>

## Примеры использования `ElementInjector`

Возможность настраивать один или несколько провайдеров на разных уровнях открывает полезные возможности. Чтобы посмотреть на следующие сценарии в работающем приложении, смотрите <live-example>примеры использования героев</live-example>.

### Сценарий: изоляция сервисов

Архитектурные причины могут заставить вас ограничить доступ к службе доменом приложения, к которому она принадлежит. Например, пример руководства включает `VillainsListComponent`, который отображает список злодеев.

Он получает этих злодеев из службы `VillainsService`.

Если бы вы указали `VillainsService` в корневом `AppModule`\ (где вы зарегистрировали `HeroesService`\), это сделало бы `VillainsService` видимым везде в приложении, включая рабочие процессы _Hero_. Если бы вы позже изменили `VillainsService`, вы могли бы сломать что-нибудь в компоненте героя.

Вместо этого вы можете предоставить `VillainsService` в метаданных `providers` компонента `VillainsListComponent` следующим образом:

<code-example header="src/app/villains-list.component.ts (metadata)" path="hierarchical-dependency-injection/src/app/villains-list.component.ts" region="metadata"></code-example>.

Предоставляя `VillainsService` в метаданных `VillainsListComponent` и нигде больше, сервис становится доступным только в `VillainsListComponent` и его дереве подкомпонентов.

`VillainService` является синглтоном по отношению к `VillainsListComponent`, потому что именно там он объявлен. Пока `VillainsListComponent` не будет уничтожен, он будет тем же самым экземпляром `VillainService`, но если есть несколько экземпляров `VillainsListComponent`, то каждый экземпляр `VillainsListComponent` будет иметь свой собственный экземпляр `VillainService`.

### Сценарий: несколько сеансов редактирования

Многие приложения позволяют пользователям работать над несколькими открытыми задачами одновременно. Например, в приложении для подготовки налогов специалист может работать над несколькими налоговыми декларациями, переключаясь с одной на другую в течение дня.

Чтобы продемонстрировать этот сценарий, представьте внешний компонент `HeroListComponent`, который отображает список супергероев.

Чтобы открыть налоговую декларацию героя, специалист по подготовке документов щелкает на имени героя, что открывает компонент для редактирования этой декларации. Налоговая декларация каждого выбранного героя открывается в отдельном компоненте, и несколько деклараций могут быть открыты одновременно.

Каждый компонент налоговой декларации имеет следующие характеристики:

-   Является собственным сеансом редактирования налоговой декларации.

-   Может изменять налоговую декларацию, не затрагивая декларацию в другом компоненте.

-   Имеет возможность сохранить изменения в своей налоговой декларации или отменить их

<div class="lightbox">

<img alt="Heroes in action" src="generated/images/guide/dependency-injection/hid-heroes-anim.gif">

</div>

Предположим, что `HeroTaxReturnComponent` имеет логику для управления и восстановления изменений. Это была бы простая задача для героической налоговой декларации.
В реальном мире, с богатой моделью данных налоговой декларации, управление изменениями было бы сложным.

Вы можете делегировать это управление вспомогательной службе, как это сделано в данном примере.

Служба `HeroTaxReturnService` кэширует одну `HeroTaxReturn`, отслеживает изменения в этой декларации, может сохранять или восстанавливать ее. Он также делегирует полномочия синглтону приложения `HeroService`, который он получает путем инъекции.

<code-example header="src/app/hero-tax-return.service.ts" path="hierarchical-dependency-injection/src/app/hero-tax-return.service.ts"></code-example>.

Вот `HeroTaxReturnComponent`, который использует `HeroTaxReturnService`.

<code-example header="src/app/hero-tax-return.component.ts" path="hierarchical-dependency-injection/src/app/hero-tax-return.component.ts"></code-example>.

Данные _tax-return-to-edit_ поступают через свойство `@Input()`, которое реализовано с помощью геттеров и сеттеров. Сеттер инициализирует собственный экземпляр компонента `HeroTaxReturnService` входящим возвратом.

Геттер всегда возвращает то, что, по словам службы, является текущим состоянием героя.

Компонент также просит службу сохранить и восстановить эту налоговую декларацию.

Это не будет работать, если служба является синглтоном всего приложения. Каждый компонент будет использовать один и тот же экземпляр службы, и каждый компонент будет перезаписывать налоговую декларацию, принадлежащую другому герою.

Чтобы предотвратить это, настройте инжектор компонента `HeroTaxReturnComponent` на предоставление сервиса, используя свойство `providers` в метаданных компонента.

<code-example header="src/app/hero-tax-return.component.ts (providers)" path="hierarchical-dependency-injection/src/app/hero-tax-return.component.ts" region="providers"></code-example>.

У `HeroTaxReturnComponent` есть свой собственный провайдер `HeroTaxReturnService`. Вспомните, что каждый компонент _экземпляр_ имеет свой инжектор.

Предоставление сервиса на уровне компонента гарантирует, что _каждый_ экземпляр компонента получает частный экземпляр сервиса. Это гарантирует, что ни одна налоговая декларация не будет перезаписана.

<div class="alert is-helpful">

Остальная часть кода сценария опирается на другие возможности и приемы Angular, о которых вы можете узнать в других разделах документации. Вы можете ознакомиться с ним и загрузить его из <live-example></live-example>.

</div>

### Scenario: specialized providers

Another reason to provide a service again at another level is to substitute a _more specialized_ implementation of that service, deeper in the component tree.

For example, consider a `Car` component that includes tire service information and depends on other services to provide more details about the car.

The root injector, marked as \(A\), uses _generic_ providers for details about `CarService` and `EngineService`.

1. `Car` component \(A\). Component \(A\) displays tire service data about a car and specifies generic services to provide more information about the car.

2. Child component \(B\). Component \(B\) defines its own, _specialized_ providers for `CarService` and `EngineService` that have special capabilities suitable for what's going on in component \(B\).

3. Child component \(C\) as a child of Component \(B\). Component \(C\) defines its own, even _more specialized_ provider for `CarService`.

<div class="lightbox">

<img alt="car components" src="generated/images/guide/dependency-injection/car-components.png">

</div>

Behind the scenes, each component sets up its own injector with zero, one, or more providers defined for that component itself.

When you resolve an instance of `Car` at the deepest component \(C\), its injector produces:

-   An instance of `Car` resolved by injector \(C\)
-   An `Engine` resolved by injector \(B\)
-   Its `Tires` resolved by the root injector \(A\).

<div class="lightbox">

<img alt="car injector tree" src="generated/images/guide/dependency-injection/injector-tree.png">

</div>

## More on dependency injection

For more information on Angular dependency injection, see the [DI Providers](guide/dependency-injection-providers) and [DI in Action](guide/dependency-injection-in-action) guides.

<!-- links -->

<!-- external links -->

<!-- end links -->

@reviewed 2022-02-28
