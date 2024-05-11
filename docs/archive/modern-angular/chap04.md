# Элементы Angular с автономными компонентами

Начиная с версии Angular 14.2, появилась возможность использовать автономные компоненты в качестве элементов Angular. В этой главе я покажу вам, как работает эта новая возможность.

[Исходный код](https://github.com/manfredsteyer/standalone-components-elements)

## Предоставление автономного компонента {#leanpub-auto-providing-a-standalone-component}

Автономный компонент, который я буду использовать здесь, — это простая кнопка переключения под названием `ToggleComponent`:

```ts
import {
    Component,
    EventEmitter,
    Input,
    Output,
    ViewEncapsulation,
} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-toggle',
    standalone: true,
    imports: [],
    template: `
        <div
            class="toggle"
            [class.active]="active"
            (click)="toggle()"
        >
            <slot>Toggle!</slot>
        </div>
    `,
    styles: [
        `
            .toggle {
                padding: 10px;
                border: solid black 1px;
                cursor: pointer;
                display: inline;
            }

            .active {
                background-color: lightsteelblue;
            }
        `,
    ],
    encapsulation: ViewEncapsulation.ShadowDom,
})
export class ToggleComponent {
    @Input() active = false;
    @Output() change = new EventEmitter<boolean>();

    toggle(): void {
        this.active = !this.active;
        this.change.emit(this.active);
    }
}
```

Установив инкапсуляцию на `ViewEncapsulation.ShadowDom`, я заставляю браузер использовать "настоящий" Shadow DOM вместо эмулированного аналога Angular. Однако это также означает, что нам придется использовать API `slot` браузера для проецирования контента, а не `ng-content` Angular.

## Установка Angular Elements {#leanpub-auto-installing-angular-elements}

Хотя Angular Elements предоставляется непосредственно командой Angular, CLI не устанавливает его. Следовательно, мы должны сделать это вручную:

```sh
npm i @angular/elements
```

В былые времена `@angular/elements` также поддерживал `ng add`. Эта поддержка сопровождалась схемой добавления необходимого полифилла. Однако в настоящее время все браузеры, поддерживаемые Angular, могут работать с веб-компонентами нативно. Таким образом, необходимость в таком полифилле отпала, и поддержка `ng add` была удалена несколько версий назад.

## Загрузка с Angular Elements {#leanpub-auto-bootstrapping-with-angular-elements}

Теперь давайте загрузим наше приложение и представим `ToggleComponent` как веб-компонент (пользовательский элемент) с помощью Angular Elements. Для этого мы можем использовать функцию `createApplication`, добавленную в Angular 14.2:

```ts title="main.ts"
import { createCustomElement } from '@angular/elements';
import { createApplication } from '@angular/platform-browser';
import { ToggleComponent } from './app/toggle/toggle.component';

(async () => {
    const app = await createApplication({
        providers: [
            /* your global providers here */
        ],
    });

    const toogleElement = createCustomElement(
        ToggleComponent,
        {
            injector: app.injector,
        }
    );

    customElements.define('my-toggle', toogleElement);
})();
```

Мы можем передать массив с провайдерами в `createApplication`. Это позволит предоставлять сервисы вроде `HttpClient` через корневую область приложения. В общем случае эта опция нужна, когда мы хотим настроить этих провайдеров, например, с помощью метода `forRoot` или функции `provideXYZ`. Во всех остальных случаях предпочтительнее просто использовать древовидные провайдеры (`providedIn: 'root'`).

Результатом `createApplication` является новый `ApplicationRef`. Мы можем передать его инжектор вместе с `ToggleComponent` в `createCustomElement`. В результате мы получим пользовательский элемент, который можно зарегистрировать в браузере с помощью `customElements.define`.

Обратите внимание, что текущий API не позволяет установить собственный экземпляр зоны, как, например, зона `noop`. Вместо этого команда Angular хочет сконцентрироваться на новых функциях для обнаружения изменений без зон в будущем.

## Побочное замечание: загрузка нескольких компонентов {#leanpub-auto-side-note-bootstrapping-multiple-components}

Показанный API также позволяет создавать несколько пользовательских элементов:

```ts
const element1 = createCustomElement(ThisComponent, {
    injector: app.injector,
});

const element2 = createCustomElement(ThatComponent, {
    injector: app.injector,
});
```

Помимо работы с пользовательскими элементами, `ApplicationRef` позволяет загружать несколько компонентов в качестве приложений Angular:

```ts
app.injector.get(NgZone).run(() => {
    app.bootstrap(ToggleComponent, 'my-a');
    app.bootstrap(ToggleComponent, 'my-b');
});
```

При загрузке компонента таким образом можно переписать используемый селектор. Обратите внимание, что для обнаружения изменений необходимо вызывать `bootstrap` внутри зоны.

Изначально загрузка нескольких компонентов осуществлялась путем размещения нескольких компонентов в массиве `bootstrap` вашего `AppModule`. Однако функция `bootstrapApplication`, используемая для загрузки автономных компонентов, не позволяет этого сделать, поскольку целью было предоставить простой API для наиболее распространенного случая использования.

## Вызов элемента Angular {#leanpub-auto-calling-an-angular-element}

Чтобы вызвать наш элемент Angular, нам нужно просто поместить соответствующий тег в наш `index.html`:

```html
<h1>Standalone Angular Element Demo</h1>
<my-toggle id="myToggle">Click me!</my-toggle>
```

Поскольку пользовательский элемент воспринимается браузером как обычный узел DOM, мы можем использовать традиционные вызовы DOM для установки событий и присвоения значений свойствам:

```html
<script>
    const myToggle = document.getElementById('myToggle');

    myToggle.addEventListener('change', (event) => {
        console.log('active', event.detail);
    });

    setTimeout(() => {
        myToggle.active = true;
    }, 3000);
</script>
```

## Вызов веб-компонента в компоненте Angular {#leanpub-auto-calling-a-web-component-in-an-angular-component}

Если мы вызываем веб-компонент в компоненте Angular, мы можем напрямую привязать к нему данные, используя скобки для свойств и круглые скобки для событий. Это работает независимо от того, был ли веб-компонент создан в Angular или нет.

Чтобы продемонстрировать это, предположим, что у нас есть следующий AppComponent:

```ts
import {
    Component,
    CUSTOM_ELEMENTS_SCHEMA,
} from '@angular/core';

@Component({
    selector: 'app-root',
    standalone: true,
    schemas: [CUSTOM_ELEMENTS_SCHEMA],
    template: `
        <h2>Root Component</h2>
        <my-toggle
            [active]="active"
            (change)="change($event)"
        >
            Hello!
        </my-toggle>
    `,
})
export class AppComponent {
    active = false;
    change(event: Event) {
        const customEvent = event as CustomEvent<boolean>;
        console.log('active', customEvent.detail);
    }
}
```

Этот автономный компонент вызывает наш веб-компонент `my-toggle`. Хотя компилятор Angular знает обо всех возможных компонентах Angular, он не знает о веб-компонентах. Следовательно, при виде тега `my-toggle` он будет выдавать ошибку. Чтобы избежать этого, нам нужно зарегистрировать схему `CUSTOM_ELEMENTS_SCHEMA`.

Раньше мы делали это со всеми NgModules, которые хотели использовать вместе с веб-компонентами. Теперь мы можем напрямую зарегистрировать эту схему в автономных компонентах. Технически это просто отключает проверки компилятора относительно возможных имен тегов. Это двоичная схема — проверки либо включены, либо выключены — и нет способа напрямую сообщить компилятору о доступных веб-компонентах.

Чтобы этот компонент появился на нашей странице, нам нужно его загрузить:

```ts title="main.ts"
/* ... */
// Register web components ...
/* ... */

app.injector.get(NgZone).run(() => {
    app.bootstrap(AppComponent);
});
```

Также нам нужно добавить элемент для AppComponent в index.html:

```html
<app-root></app-root>
```

## Бонус: компиляция самодостаточного бандла {#leanpub-auto-bonus-compiling-self-contained-bundle}

Теперь предположим, что мы предоставляем только пользовательский элемент и не загружаем наш `AppComponent`. Чтобы использовать этот пользовательский элемент в других приложениях, нам нужно скомпилировать его в самодостаточный бандл. В то время как традиционный сборщик на основе webpack создает несколько пакетов, например, основной пакет и пакет времени выполнения, новый `ApplicationBuilder` на основе esbuild (см. главу _esbuild и новый Application Builder_) просто дает нам один пакет для нашего исходного кода и еще один для полифиллов.

Результирующие пакеты выглядят следующим образом:

```
      948 favicon.ico
      703 index.html
  100 177 main.43BPAPVS.js
   33 916 polyfills.M7XCYQVG.js
        0 styles.VFXLKGBH.css
```

Если вы используете свой веб-компонент на другом сайте, например, на CMS, просто ссылайтесь там на основной пакет и добавьте соответствующий тег. Также ссылайтесь на полифиллы. Однако при использовании нескольких таких пакетов необходимо убедиться, что полифиллы загружаются только один раз.

## Заключение {#leanpub-auto-conclusion-3}

Как побочный продукт автономных компонентов, Angular предоставляет упрощенный способ использования элементов Angular: Мы начинаем с создания `ApplicationRef`, чтобы получить `Injector`. Наряду с автономным компонентом мы передаем этот инжектор в Angular Elements. В результате мы получаем веб-компонент, который можно зарегистрировать в браузере.
