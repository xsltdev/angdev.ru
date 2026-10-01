---
description: Синглтон-сервис — это сервис, для которого в приложении существует только один экземпляр
---

# Синглтонные сервисы

:date: 28.02.2022

**Синглтон-сервис** — это сервис, для которого в приложении существует только один экземпляр.

Пример приложения, использующего синглтон-сервис, описанный на этой странице, приведен в [живом примере](https://angular.io/generated/live-examples/ngmodules/stackblitz.html), демонстрирующем все документированные возможности NgModules.

## Предоставление однопользовательского сервиса

В Angular существует два способа сделать сервис синглтоном:

-   Установить свойство `providedIn` в `@Injectable()` в значение `"root"`.
-   Включить сервис в `AppModule` или в модуль, который импортируется только `AppModule`.

### Использование `providedIn` {#providedIn}

Начиная с версии Angular 6.0, предпочтительным способом создания синглтонного сервиса является установка значения `providedIn` в `root` для декоратора сервиса `@Injectable()`. Это указывает Angular на то, что сервис должен быть предоставлен в корне приложения.

```ts
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class UserService {}
```

Более подробную информацию о сервисах см. в главе [Services](toh-pt4.md) учебника [Tour of Heroes](toh.md).

### Массив NgModule `providers`

В приложениях, построенных на базе Angular версий, предшествующих 6.0, сервисы регистрируются в массивах NgModule `providers` следующим образом:

```ts
@NgModule({
  // …
  providers: [UserService],
  // …
})
```

Если бы этот NgModule был корневым `AppModule`, то `UserService` был бы синглтоном и был бы доступен во всем приложении. Хотя вы можете увидеть его в таком виде, использование свойства `providedIn` декоратора `@Injectable()` для самого сервиса предпочтительнее, начиная с версии Angular 6.0, поскольку оно делает ваши сервисы древовидными.

## Шаблон `forRoot()` {#forRoot}

Как правило, `providedIn` нужен только для предоставления сервисов, а `forRoot()`/`forChild()` — для маршрутизации. Однако понимание того, как работает `forRoot()` для того, чтобы убедиться, что сервис является синглтоном, поможет вам в разработке на более глубоком уровне.

Если в модуле определены как провайдеры, так и декларации (компоненты, директивы, пайпы), то загрузка модуля в несколько функциональных модулей приведет к дублированию регистрации сервиса. Это может привести к появлению нескольких экземпляров сервиса, и сервис перестанет вести себя как синглтон.

Существует несколько способов предотвратить это:

-   Использовать синтаксис [`providedIn`](singleton-services.md#providedIn) вместо регистрации сервиса в модуле.
-   Выделяйте сервисы в отдельный модуль.
-   Определите в модуле методы `forRoot()` и `forChild()`.

!!!note ""

    Существует два примера приложений, в которых можно увидеть этот сценарий: более продвинутый [NgModules live example](https://angular.io/generated/live-examples/ngmodules/stackblitz.html), содержащий `forRoot()` и `forChild()` в модулях маршрутизации и `GreetingModule`, и более простой [Lazy Loading live example](https://angular.io/generated/live-examples/lazy-loading-ngmodules/stackblitz.html). Вводное пояснение приведено в руководстве [Lazy Loading Feature Modules](lazy-loading-ngmodules.md).

Используйте `forRoot()` для отделения провайдеров от модуля, чтобы импортировать этот модуль в корневой модуль с `providers` и дочерние модули без `providers`.

1.  Создайте в модуле статический метод `forRoot()`.
2.  Поместите провайдеры в метод `forRoot()`.

```ts
static forRoot(config: UserServiceConfig): ModuleWithProviders<GreetingModule> {
  return {
    ngModule: GreetingModule,
    providers: [
      {provide: UserServiceConfig, useValue: config }
    ]
  };
}
```

### `forRoot()` и `Router` {#forRoot-router}

Модуль `RouterModule` предоставляет сервис `Router`, а также директивы маршрутизатора, такие как `RouterOutlet` и `routerLink`. Корневой модуль приложения импортирует `RouterModule`, чтобы у приложения был `Router` и компоненты корневого приложения могли получить доступ к директивам маршрутизатора. Любые функциональные модули также должны импортировать `RouterModule`, чтобы их компоненты могли помещать директивы маршрутизатора в свои шаблоны.

Если бы в `RouterModule` не было `forRoot()`, то каждый функциональный модуль инстанцировал бы новый экземпляр `Router`, что привело бы к поломке приложения, поскольку `Router` может быть только один. При использовании метода `forRoot()` корневой модуль приложения импортирует `RouterModule.forRoot(...)` и получает `Router`, а все функциональные модули импортируют `RouterModule.forChild(...)`, который не инстанцирует другой `Router`.

!!!note ""

    Если у вас есть модуль, в котором есть и провайдеры, и декларации, вы _можете_ использовать эту технику для их разделения, и вы можете встретить этот паттерн в старых приложениях.

    Однако, начиная с версии Angular 6.0, наилучшей практикой предоставления сервисов является использование свойства `@Injectable()` `providedIn`.

### Как работает `forRoot()`

`forRoot()` принимает объект конфигурации сервиса и возвращает [ModuleWithProviders](https://angular.io/api/core/ModuleWithProviders), который представляет собой простой объект со следующими свойствами:

| Свойства    | Детали                                  |
| :---------- | :-------------------------------------- |
| `ngModule`  | В данном примере класс `GreetingModule` |
| `providers` | Настроенные провайдеры                  |

В [live example](https://angular.io/generated/live-examples/ngmodules/stackblitz.html) корневой `AppModule` импортирует `GreetingModule` и добавляет `providers` в провайдеры `AppModule`. В частности, Angular накапливает все импортированные провайдеры перед добавлением элементов, перечисленных в `@NgModule.providers`. Такая последовательность гарантирует, что все, что вы явно добавите в провайдеры `AppModule`, будет иметь приоритет над провайдерами импортированных модулей.

В примере импортируется `GreetingModule` и его метод `forRoot()` используется один раз, в `AppModule`. Такая однократная регистрация позволяет избежать многократного использования.

Можно также добавить метод `forRoot()` в `GreetingModule`, который настраивает приветствие `UserService`.

В следующем примере необязательный, инжектируемый `UserServiceConfig` расширяет приветствие `UserService`. Если существует `UserServiceConfig`, то `UserService` устанавливает имя пользователя из этого конфига.

```ts
constructor(@Optional() config?: UserServiceConfig) {
  if (config) { this._userName = config.userName; }
}
```

Вот `forRoot()`, который принимает объект `UserServiceConfig`:

```ts
static forRoot(config: UserServiceConfig): ModuleWithProviders<GreetingModule> {
  return {
    ngModule: GreetingModule,
    providers: [
      {provide: UserServiceConfig, useValue: config }
    ]
  };
}
```

И, наконец, вызвать его в списке `imports` модуля `AppModule`. В приведенном ниже фрагменте другие части файла опущены. Полный текст файла см. в [живом примере](https://angular.io/generated/live-examples/ngmodules/stackblitz.html) или перейдите к следующему разделу этого документа.

```ts
import { GreetingModule } from './greeting/greeting.module';
@NgModule({
  imports: [
    GreetingModule.forRoot({userName: 'Miss Marple'}),
  ],
})
```

Приложение отображает в качестве пользователя "Мисс Марпл", а не "Шерлока Холмса" по умолчанию.

Не забудьте импортировать `GreetingModule` как Javascript-импорт в верхней части файла и не добавляйте его более чем в один список `@NgModule` `imports`.

## Предотвращение повторного импорта `GreetingModule`

Только корневой `AppModule` должен импортировать `GreetingModule`. Если лениво загруженный модуль импортирует и его, то приложение может сгенерировать [множественные экземпляры](ngmodule-faq.md#q-why-bad) сервиса.

Для защиты от повторного импортирования `GreetingModule` лениво загружаемым модулем добавьте следующий конструктор `GreetingModule`.

```ts
constructor(@Optional() @SkipSelf() parentModule?: GreetingModule) {
  if (parentModule) {
    throw new Error(
      'GreetingModule is already loaded. Import it in the AppModule only');
  }
}
```

Конструктор указывает Angular на необходимость инжектировать `GreetingModule` в себя. Инъекция была бы круговой, если бы Angular искал `GreetingModule` в _текущем_ инжекторе, но декоратор `@SkipSelf()` означает "искать `GreetingModule` в инжекторе-предке, выше меня в иерархии инжекторов".

По умолчанию инжектор выбрасывает ошибку, если не может найти запрашиваемый провайдер. Декоратор `@Optional()` означает, что не найти сервис — это нормально. Инжектор возвращает `null`, параметр `parentModule` равен null, и конструктор завершается без проблем.

Совсем другое дело, если вы неправильно импортируете `GreetingModule` в лениво загружаемый модуль, например `CustomersModule`.

Angular создает лениво загружаемый модуль со своим собственным инжектором, дочерним по отношению к корневому инжектору. `@SkipSelf()` заставляет Angular искать `GreetingModule` в родительском инжекторе, которым на этот раз является корневой инжектор. Конечно же, он находит экземпляр, импортированный корневым `AppModule`. Теперь `parentModule` существует, и конструктор выбрасывает ошибку.

Вот два файла целиком для справки:

=== "app.module.ts"

    ```ts
    import { BrowserModule } from '@angular/platform-browser';
    import { NgModule } from '@angular/core';

    /* App Root */
    import { AppComponent } from './app.component';

    /* Feature Modules */
    import { ContactModule } from './contact/contact.module';
    import { GreetingModule } from './greeting/greeting.module';

    /* Routing Module */
    import { AppRoutingModule } from './app-routing.module';

    @NgModule({
    	imports: [
    		BrowserModule,
    		ContactModule,
    		GreetingModule.forRoot({ userName: 'Miss Marple' }),
    		AppRoutingModule,
    	],
    	declarations: [AppComponent],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "greeting.module.ts"

    ```ts
    import {
    	ModuleWithProviders,
    	NgModule,
    	Optional,
    	SkipSelf,
    } from '@angular/core';

    import { CommonModule } from '@angular/common';

    import { GreetingComponent } from './greeting.component';
    import { UserServiceConfig } from './user.service';

    @NgModule({
    	imports: [CommonModule],
    	declarations: [GreetingComponent],
    	exports: [GreetingComponent],
    })
    export class GreetingModule {
    	constructor(
    		@Optional()
    		@SkipSelf()
    		parentModule?: GreetingModule
    	) {
    		if (parentModule) {
    			throw new Error(
    				'GreetingModule is already loaded. Import it in the AppModule only'
    			);
    		}
    	}

    	static forRoot(
    		config: UserServiceConfig
    	): ModuleWithProviders<GreetingModule> {
    		return {
    			ngModule: GreetingModule,
    			providers: [
    				{
    					provide: UserServiceConfig,
    					useValue: config,
    				},
    			],
    		};
    	}
    }
    ```

## Подробнее о NgModules

Вам также может быть интересно:

-   [Sharing Modules](sharing-ngmodules.md), в котором подробно рассматриваются концепции, изложенные на этой странице
-   [Lazy Loading Modules](lazy-loading-ngmodules.md)
-   [FAQ по NgModule](ngmodule-faq.md)

## Ссылки

-   [Singleton services](https://angular.io/guide/singleton-services)
