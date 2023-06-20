# Что такое Angular?

Эта тема поможет вам понять Angular: что такое Angular, какие преимущества он дает и чего можно ожидать, когда вы начнете создавать свои приложения.

Angular - это платформа разработки, построенная на [TypeScript](https://scriptdev.ru/). Как платформа, Angular включает в себя:

-   компонентный фреймворк для создания масштабируемых веб-приложений
-   набор хорошо интегрированных библиотек, которые охватывают широкий спектр функций, включая маршрутизацию, управление формами, взаимодействие клиент-сервер и т.д.
-   Набор инструментов для разработчиков, которые помогут вам разрабатывать, собирать, тестировать и обновлять код.

Используя Angular, вы получаете преимущества платформы, которая может масштабироваться от проектов для одного разработчика до приложений корпоративного уровня. Angular разработан таким образом, чтобы сделать обновление максимально простым, поэтому вы сможете воспользоваться преимуществами последних разработок с минимальными усилиями.

Самое главное, что экосистема Angular состоит из разнообразной группы, включающей более 1,7 миллиона разработчиков, авторов библиотек и создателей контента.

<iframe width="100%" height="600" src="https://stackblitz.com/edit/4qrdjg?embed=1&amp;file=src%2Fapp%2Fapp.component.html&amp;theme=light"></iframe>

## Angular applications: The essentials

This section explains the core ideas behind Angular. Understanding these ideas can help you design and build your applications more effectively.

### Components

Components are the building blocks that compose an application. A component includes a TypeScript class with a `@Component()` decorator, an HTML template, and styles.

The `@Component()` decorator specifies the following Angular-specific information:

-   A CSS selector that defines how the component is used in a template. HTML elements in your template that match this selector become instances of the component.
-   An HTML template that instructs Angular how to render the component
-   An optional set of CSS styles that define the appearance of the template's HTML elements

The following is a minimal Angular component.

```ts
import { Component } from '@angular/core';

@Component({
    selector: 'hello-world',
    template: `
        <h2>Hello World</h2>
        <p>This is my first component!</p>
    `,
})
export class HelloWorldComponent {
    // The code in this class drives the component's behavior.
}
```

To use this component, you write the following in a template:

```html
<hello-world></hello-world>
```

When Angular renders this component, the resulting DOM looks like this:

```html
<hello-world>
    <h2>Hello World</h2>
    <p>This is my first component!</p>
</hello-world>
```

Angular's component model offers strong encapsulation and an intuitive application structure. Components also make your application painless to unit test and can improve the general readability of your code.

For more information on what to do with components, see the [Components](component-overview.md) section.

### Шаблоны

Каждый компонент имеет HTML-шаблон, который определяет способ отображения этого компонента. Вы определяете этот шаблон либо в строке, либо по пути к файлу.

Angular добавляет элементы синтаксиса, расширяющие HTML, чтобы вы могли вставлять динамические значения из вашего компонента. Angular автоматически обновляет рендеринг DOM при изменении состояния вашего компонента.
Одним из применений этой возможности является вставка динамического текста, как показано в следующем примере.

```html
<p>{{ message }}</p>
```

Значение для `message` берется из класса компонента:

```ts
import { Component } from '@angular/core';

@Component({
    selector: 'hello-world-interpolation',
    templateUrl:
        './hello-world-interpolation.component.html',
})
export class HelloWorldInterpolationComponent {
    message = 'Hello, World!';
}
```

Когда приложение загружает компонент и его шаблон, пользователь видит следующее:

```html
<p>Hello, World!</p>
```

Обратите внимание на использование двойных фигурных скобок - они указывают Angular интерполировать содержимое внутри них.

Angular также поддерживает привязки свойств, чтобы помочь вам установить значения для свойств и атрибутов элементов HTML и передать значения логике представления вашего приложения.

```html
<p [id]="sayHelloId" [style.color]="fontColor">
    You can set my color in the component!
</p>
```

Обратите внимание на использование квадратных скобок - этот синтаксис указывает на то, что вы привязываете свойство или атрибут к значению в классе компонента.

Объявление слушателей событий для прослушивания и реагирования на действия пользователя, такие как нажатие клавиш, движение мыши, щелчки и прикосновения. Вы объявляете слушатель событий, указывая имя события в круглых скобках:

```html
<button
    type="button"
    [disabled]="canClick"
    (click)="sayMessage()"
>
    Trigger alert message
</button>
```

В предыдущем примере вызывается метод, который определен в классе компонента:

```ts
sayMessage() {
  alert(this.message);
}
```

Ниже приведен комбинированный пример интерполяции, привязки свойств и привязки событий в шаблоне Angular:

=== "hello-world-bindings.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'hello-world-bindings',
    	templateUrl: './hello-world-bindings.component.html',
    })
    export class HelloWorldBindingsComponent {
    	fontColor = 'blue';
    	sayHelloId = 1;
    	canClick = false;
    	message = 'Hello, World';

    	sayMessage() {
    		alert(this.message);
    	}
    }
    ```

=== "hello-world-bindings.component.html"

    ```html
    <button
    	type="button"
    	[disabled]="canClick"
    	(click)="sayMessage()"
    >
    	Trigger alert message
    </button>

    <p [id]="sayHelloId" [style.color]="fontColor">
    	You can set my color in the component!
    </p>

    <p>My color is {{ fontColor }}</p>
    ```

Добавьте возможности в ваши шаблоны с помощью [директив](built-in-directives.md). Наиболее популярными директивами в Angular являются `*ngIf` и `*ngFor`. Используйте директивы для выполнения различных задач, например, для динамического изменения структуры DOM.

А также создавайте собственные пользовательские директивы для создания великолепного пользовательского опыта.

Следующий код является примером директивы [`*ngIf`](https://angular.io/api/common/NgIf).

=== "hello-world-ngif.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'hello-world-ngif',
    	templateUrl: './hello-world-ngif.component.html',
    })
    export class HelloWorldNgIfComponent {
    	message = "I'm read only!";
    	canEdit = false;

    	onEditClick() {
    		this.canEdit = !this.canEdit;
    		if (this.canEdit) {
    			this.message = 'You can edit me!';
    		} else {
    			this.message = "I'm read only!";
    		}
    	}
    }
    ```

=== "hello-world-ngif.component.html"

    ```html
    <h2>Hello World: ngIf!</h2>

    <button type="button" (click)="onEditClick()">
    	Make text editable!
    </button>

    <div *ngIf="canEdit; else noEdit">
    	<p>You can edit the following paragraph.</p>
    </div>

    <ng-template #noEdit>
    	<p>
    		The following paragraph is read only. Try clicking
    		the button!
    	</p>
    </ng-template>

    <p [contentEditable]="canEdit">{{ message }}</p>
    ```

Angular's declarative templates let you cleanly separate your application's logic from its presentation. Templates are based on standard HTML, for ease in building, maintaining, and updating.

For more information on templates, see the [Templates](template-syntax.md) section.

### Dependency injection

Dependency injection lets you declare the dependencies of your TypeScript classes without taking care of their instantiation. Instead, Angular handles the instantiation for you.

This design pattern lets you write more testable and flexible code.

Understanding dependency injection is not critical to start using Angular, but it is strongly recommended as a best practice. Many aspects of Angular take advantage of it to some degree.

To illustrate how dependency injection works, consider the following example. The first file, `logger.service.ts`, defines a `Logger` class.

This class contains a `writeCount` function that logs a number to the console.

```ts
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class Logger {
    writeCount(count: number) {
        console.warn(count);
    }
}
```

Next, the `hello-world-di.component.ts` file defines an Angular component. This component contains a button that uses the `writeCount` function of the Logger class.

To access that function, the `Logger` service is injected into the `HelloWorldDI` class by adding `private logger: Logger` to the constructor.

```ts
import { Component } from '@angular/core';
import { Logger } from '../logger.service';

@Component({
    selector: 'hello-world-di',
    templateUrl: './hello-world-di.component.html',
})
export class HelloWorldDependencyInjectionComponent {
    count = 0;

    constructor(private logger: Logger) {}

    onLogMe() {
        this.logger.writeCount(this.count);
        this.count++;
    }
}
```

For more information about dependency injection and Angular, see the [Dependency injection in Angular](dependency-injection.md) section.

## Angular CLI

The Angular CLI is the fastest, straightforward, and recommended way to develop Angular applications. The Angular CLI makes some tasks trouble-free.

For example:

| Команда       | Подробности                                                                    |
| :------------ | :----------------------------------------------------------------------------- |
| `ng build`    | Компилирует приложение Angular в выходной каталог.                             |
| `ng serve`    | Собирает и обслуживает ваше приложение, перестраивая его при изменении файлов. |
| `ng generate` | Генерирует или изменяет файлы на основе схемы.                                 |
| `ng test`     | Запускает модульные тесты для данного проекта.                                 |
| `ng e2e`      | Собирает и обслуживает приложение Angular, затем запускает сквозные тесты.     |

The Angular CLI is a valuable tool for building out your applications.

## First-party libraries

The section, Angular applications: the essentials, provides a brief overview of a couple of the key architectural elements that are used when building Angular applications. The many benefits of Angular really become clear when your application grows and you want to add functions such as site navigation or user input.

Use the Angular platform to incorporate one of the many first-party libraries that Angular provides.

Some of the libraries available to you include:

| Библиотека                             | Подробности                                                                                                                                                                                      |
| :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Angular Router](router.md)            | Расширенная навигация и маршрутизация на стороне клиента на основе компонентов Angular. Поддерживает ленивую загрузку, вложенные маршруты, пользовательское сопоставление путей и многое другое. |
| [Angular Forms](forms-overview.md)     | Единая система участия и проверки форм.                                                                                                                                                          |
| [Angular HttpClient](http.md)          | Надежный HTTP-клиент, способный обеспечить более продвинутое взаимодействие клиент-сервер.                                                                                                       |
| [Angular Animations](animations.md)    | Богатая система для управления анимацией на основе состояния приложения.                                                                                                                         |
| [Angular PWA](service-worker-intro.md) | Инструменты для создания прогрессивных веб-приложений \(PWA\), включая сервисный работник и манифест веб-приложения.                                                                             |
| [Angular Schematics](schematics.md)    | Автоматизированные инструменты для создания лесов, рефакторинга и обновления, которые упрощают разработку в больших масштабах.                                                                   |

Эти библиотеки расширяют возможности вашего приложения, позволяя вам сосредоточиться на функциях, которые делают ваше приложение уникальным. Добавляйте эти библиотеки, зная, что они разработаны для безупречной интеграции и обновления одновременно с фреймворком Angular.

Эти библиотеки необходимы только тогда, когда они могут помочь вам добавить функции в ваше приложение или решить конкретную проблему.

## Следующие шаги

Эта тема дает вам краткий обзор того, что такое Angular, какие преимущества он предоставляет и чего ожидать, когда вы начнете создавать свои приложения.

Чтобы увидеть Angular в действии, посмотрите учебник [Getting Started](start.md). В этом учебнике используется [stackblitz.com](https://stackblitz.com), чтобы вы могли изучить рабочий пример Angular без каких-либо требований к установке.

Для дальнейшего изучения возможностей Angular рекомендуем следующие разделы:

-   [Понимание Angular](understanding-angular-overview.md)
-   [Гайд разработчика Angular](developer-guide-overview.md)
