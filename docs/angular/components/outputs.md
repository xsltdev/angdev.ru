---
description: "Как компонент порождает пользовательские события и как на них подписаться из шаблона и из кода."
---

# Пользовательские события через output {: #custom-events-with-outputs}

:date: 30.09.2026

!!! tip ""

    Этот материал предполагает, что вы уже прочитали [руководство по основам](../essentials/overview.md). Если Angular для вас в новинку, начните с него.

Компонент Angular задаёт пользовательское событие, записав в свойство результат функции `output`:

```ts
@Component({
  /*...*/
})
export class ExpandablePanel {
  panelClosed = output<void>();
}
```

```html
<expandable-panel (panelClosed)="savePanelState()" />
```

Функция `output` возвращает `OutputEmitterRef`. Событие порождают методом `emit` у `OutputEmitterRef`:

```ts
this.panelClosed.emit();
```

Свойства, инициализированные функцией `output`, Angular называет **output**. Через них порождают пользовательские события, по смыслу близкие к нативным событиям браузера вроде `click`.

**Пользовательские события Angular не всплывают по DOM.**

**Имена output чувствительны к регистру.**

При наследовании класса компонента **output наследуются дочерним классом.**

Функция `output` имеет особый смысл для компилятора Angular. **Вызывать `output` можно только в инициализаторах свойств компонента и директивы.**

## Передача данных события {: #emitting-event-data}

В `emit` можно передать данные события:

```ts
// You can emit primitive values.
this.valueChanged.emit(7);

// You can emit custom event objects
this.thumbDropped.emit({
  pointerX: 123,
  pointerY: 456,
});
```

В обработчике события в шаблоне данные доступны через переменную `$event`:

```html
<custom-slider (valueChanged)="logValue($event)" />
```

Родительский компонент принимает данные так:

```ts
@Component({
 /*...*/
})
export class App {
  logValue(value: number) {
    ...
  }
}
```

## Свои имена выходных событий {: #customizing-output-names}

Функция `output` принимает параметр, которым событию в шаблоне задают другое имя:

```ts
@Component(/* ... */)
export class CustomSlider {
  changed = output({alias: 'valueChanged'});
}
```

```html
<custom-slider (valueChanged)="saveVolume()" />
```

На обращение к свойству в коде TypeScript псевдоним не влияет.

Псевдонимы output лучше не плодить, но они уместны, когда свойство переименовывают и оставляют старое имя, либо когда нужно уйти от столкновения с именем нативного события DOM.

## Программная подписка на output {: #subscribing-to-outputs-programmatically}

Если компонент создаётся динамически, на его output можно подписаться из кода экземпляра. У типа `OutputRef` есть метод `subscribe`:

```ts
const someComponentRef: ComponentRef<SomeComponent> = viewContainerRef.createComponent(/*...*/);

someComponentRef.instance.someEventProperty.subscribe((eventData) => {
  console.log(eventData);
});
```

Angular сам снимает подписки на события, когда уничтожает компонент, на который подписались. Подписку можно снять и вручную: `subscribe` возвращает `OutputRefSubscription` с методом `unsubscribe`:

```ts
const eventSubscription = someComponent.someEventProperty.subscribe((eventData) => {
  console.log(eventData);
});

// ...

eventSubscription.unsubscribe();
```

## Выбор имён событий {: #choosing-event-names}

Не выбирайте имена output, которые совпадают с событиями DOM-элементов вроде `HTMLElement`. Из-за совпадения непонятно, принадлежит привязка компоненту или DOM-элементу.

Префиксы, как у селекторов компонентов, output не нужны. На одном элементе живёт только один компонент, поэтому нестандартные свойства относятся к нему.

Имена output всегда пишите в [camelCase](https://en.wikipedia.org/wiki/Camel_case). Не начинайте имя с `on`.

## Output и RxJS {: #using-outputs-with-rxjs}

Как связать output с RxJS, описано в [Совместимость RxJS с output компонентов и директив](https://angular.dev/ecosystem/rxjs-interop/output-interop).

## Объявление output декоратором `@Output` {: #declaring-outputs-with-the-output-decorator}

!!! tip ""

    Команда Angular рекомендует в новых проектах функцию `output`, но исходный API на декораторе `@Output` по-прежнему полностью поддерживается.

Пользовательское событие можно задать и так: свойство с новым `EventEmitter` и декоратор `@Output`:

```ts
@Component(/* ... */)
export class ExpandablePanel {
  @Output() panelClosed = new EventEmitter<void>();
}
```

Событие порождают методом `emit` у `EventEmitter`.

### Псевдонимы декоратора `@Output` {: #aliases-with-the-output-decorator}

Декоратор `@Output` принимает параметр, которым событию в шаблоне задают другое имя:

```ts
@Component(/* ... */)
export class CustomSlider {
  @Output('valueChanged') changed = new EventEmitter<number>();
}
```

```html
<custom-slider (valueChanged)="saveVolume()" />
```

На обращение к свойству в коде TypeScript псевдоним не влияет.

## Выходные события в декораторе `@Component` {: #specify-outputs-in-the-component-decorator}

Помимо декоратора `@Output`, выходные события можно перечислить в свойстве `outputs` декоратора `@Component`. Это удобно, когда компонент наследует свойство базового класса:

```ts
// `CustomSlider` inherits the `valueChanged` property from `BaseSlider`.
@Component({
  /*...*/
  outputs: ['valueChanged'],
})
export class CustomSlider extends BaseSlider {}
```

Псевдоним в списке `outputs` задают после двоеточия в строке:

```ts
// `CustomSlider` inherits the `valueChanged` property from `BaseSlider`.
@Component({
  /*...*/
  outputs: ['valueChanged: volumeChanged'],
})
export class CustomSlider extends BaseSlider {}
```

---

Источник: [https://angular.dev/guide/components/outputs](https://angular.dev/guide/components/outputs)
