---
description: Провайдер — это инструкция системе Dependency Injection о том, как получить значение для зависимости
---

# Предоставление зависимостей в модулях

:date: 28.02.2022

Провайдер — это инструкция системе [Dependency Injection](dependency-injection.md) о том, как получить значение для зависимости. Чаще всего эти зависимости представляют собой сервисы, которые вы создаете и предоставляете.

Последний пример приложения, использующего провайдер, который описывается на этой странице, приведен в [живом примере](https://angular.io/generated/live-examples/providers/stackblitz.html).

## Предоставление сервиса

Если у вас уже есть приложение, созданное с помощью [Angular CLI](https://angular.io/cli), вы можете создать сервис с помощью команды [`ng generate`](https://angular.io/cli/generate) CLI в корневом каталоге проекта. Замените _User_ на имя вашего сервиса.

```shell
ng generate service User
```

Эта команда создает следующий скелет `UserService`:

```ts
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class UserService {}
```

Теперь вы можете внедрить `UserService` в любое место вашего приложения.

Сам сервис представляет собой класс, сгенерированный CLI и декорированный с помощью `@Injectable()`. По умолчанию этот декоратор имеет свойство `providedIn`, которое создает провайдера для сервиса. В данном случае `providedIn: 'root'` указывает, что Angular должен предоставлять сервис в корневом инжекторе.

## Область видимости провайдера

Когда вы добавляете провайдер в корневой инжектор приложения, он становится доступным во всем приложении. Кроме того, эти провайдеры доступны всем классам в приложении, если они имеют маркер поиска.

Вы всегда должны предоставлять свой сервис в корневом инжекторе, за исключением случаев, когда вы хотите, чтобы сервис был доступен только в том случае, если потребитель импортирует определенный `@NgModule`.

## `providedIn` и NgModules

Также можно указать, что сервис должен предоставляться в определенном `@NgModule`. Например, если вы не хотите, чтобы `UserService` был доступен приложениям, если они не импортируют созданный вами `UserModule`, вы можете указать, что сервис должен предоставляться в этом модуле:

```ts
import { Injectable } from '@angular/core';
import { UserModule } from './user.module';

@Injectable({
    providedIn: UserModule,
})
export class UserService {}
```

В приведенном примере показан предпочтительный способ предоставления сервиса в модуле. Этот способ предпочтителен, так как позволяет встряхнуть дерево сервиса, если в него ничего не внедряется. Если в сервисе невозможно указать, какой модуль должен его предоставлять, можно также объявить провайдера сервиса внутри модуля:

```ts
import { NgModule } from '@angular/core';

import { UserService } from './user.service';

@NgModule({
    providers: [UserService],
})
export class UserModule {}
```

## Ограничение области действия провайдера путем ленивой загрузки модулей

В базовом приложении, создаваемом с помощью CLI, модули загружаются с нетерпением, что означает, что все они загружаются при запуске приложения. Angular использует систему инжекторов для обеспечения доступности между модулями. В приложении, загружаемом с нетерпением, инжектор корневого приложения делает доступными все провайдеры всех модулей во всем приложении.

Такое поведение обязательно меняется при использовании ленивой загрузки. Ленивая загрузка — это загрузка модулей только тогда, когда они нужны; например, при маршрутизации. Они не загружаются сразу, как модули с нетерпеливой загрузкой. Это означает, что любые сервисы, перечисленные в массивах провайдеров, будут недоступны, поскольку корневой инжектор не знает об этих модулях.

Когда Angular router лениво загружает модуль, он создает новый инжектор. Этот инжектор является дочерним по отношению к инжектору корневого приложения. Представьте себе дерево инжекторов: есть один корневой инжектор, а затем дочерние инжекторы для каждого лениво загруженного модуля. Этот дочерний инжектор заполняется всеми провайдерами, специфичными для модуля, если таковые имеются. Разрешение поиска для каждого провайдера происходит в соответствии с [правилами иерархической инъекции зависимостей](hierarchical-dependency-injection.md#resolution-rules).

Любой компонент, созданный в контексте лениво загруженного модуля, например, при навигации по маршрутизатору, получает свой собственный локальный экземпляр дочерних сервисов, а не экземпляр в инжекторе корневого приложения. Компоненты во внешних модулях продолжают получать экземпляры, созданные для корневого инжектора приложения.

Хотя можно предоставлять сервисы с помощью ленивой загрузки модулей, не все сервисы могут быть лениво загружены. Например, некоторые модули работают только в корневом модуле, такие как Router. Router работает с объектом глобального расположения в браузере.

Начиная с 9-й версии Angular, можно предоставлять новый экземпляр сервиса с каждым лениво загруженным модулем. Следующий код добавляет эту функциональность в `UserService`.

```ts
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'any',
})
export class UserService {}
```

При использовании `providedIn: 'any'` все загружаемые с нетерпением модули имеют один экземпляр; однако модули, загружаемые с нетерпением, получают свой собственный уникальный экземпляр, как показано на следующей диаграмме.

![any-provider-scope](any-provider.svg)

## Ограничение области действия провайдера с помощью компонентов

Другим способом ограничения области действия провайдера является добавление сервиса, который вы хотите ограничить, в массив `providers` компонента. Провайдеры компонентов и провайдеры NgModule независимы друг от друга. Этот способ удобен, когда требуется нетерпеливо загрузить модуль, которому нужен отдельный сервис. Предоставление сервиса в компоненте ограничивает его действие только этим компонентом и его потомками. Другие компоненты того же модуля не могут получить к нему доступ.

```ts
@Component({
  /* . . . */
  providers: [UserService]
})
```

## Предоставление сервисов в модулях и компонентах

Как правило, в корневом модуле следует предоставлять сервисы, необходимые всему приложению, а в лениво загружаемых модулях — расширять область применения сервисов.

Маршрутизатор работает на корневом уровне, поэтому если поместить провайдеры в компонент, даже `AppComponent`, то лениво загружаемые модули, которые полагаются на маршрутизатор, не смогут их увидеть.

Регистрируйте провайдер в компоненте, когда необходимо ограничить экземпляр сервиса компонентом и его деревом компонентов, то есть его дочерними компонентами. Например, компонент редактирования пользователя `UserEditorComponent`, которому необходима частная копия кэширующего `UserService`, должен зарегистрировать `UserService` в `UserEditorComponent`. Тогда каждый новый экземпляр `UserEditorComponent` получит свой собственный кэшированный экземпляр сервиса.

<a id="singleton-services"></a>
<a id="component-child-injectors"></a>

## Иерархия инжекторов и экземпляры сервисов

Сервисы являются синглтонами в области видимости инжектора, что означает, что в данном инжекторе существует не более одного экземпляра сервиса.

Angular DI имеет [иерархическую систему инъекций](hierarchical-dependency-injection.md), что означает, что вложенные инжекторы могут создавать свои собственные экземпляры сервисов. Всякий раз, когда Angular создает новый экземпляр компонента, у которого `providers` указан в `@Component()`, он также создает новый дочерний инжектор для этого экземпляра. Аналогично, когда новый модуль NgModule лениво загружается во время выполнения, Angular может создать для него инжектор с собственными провайдерами.

Дочерние модули и инжекторы компонентов независимы друг от друга и создают свои собственные отдельные экземпляры предоставляемых сервисов. Когда Angular уничтожает экземпляр NgModule или компонента, он также уничтожает этот инжектор и экземпляры сервисов этого инжектора.

Более подробная информация приведена в разделе [Иерархические инжекторы](hierarchical-dependency-injection.md).

## Подробнее о NgModules

Вам также могут быть интересны:

-   [Singleton Services](singleton-services.md), в котором подробно рассматриваются концепции, изложенные на этой странице
-   [Lazy Loading Modules](lazy-loading-ngmodules.md)
-   [Провайдеры зависимостей](dependency-injection-providers.md)
-   [FAQ по NgModule](ngmodule-faq.md)

## Ссылки

-   [Providing dependencies in modules](https://angular.io/guide/providers)
