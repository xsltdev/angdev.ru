# Оптимизация размера клиентского приложения с помощью облегченных инъекционных маркеров

:date: 28.02.2022

На этой странице представлен концептуальный обзор техники инъекции зависимостей, которая рекомендуется разработчикам библиотек. Проектирование вашей библиотеки с использованием _легких инъекционных маркеров_ помогает оптимизировать размер пакета клиентских приложений, использующих вашу библиотеку.

Вы можете управлять структурой зависимостей среди ваших компонентов и инжектируемых сервисов для оптимизации размера пакета, используя [tree-shakable providers](architecture-services.md#introduction-to-services-and-dependency-injection). Обычно это гарантирует, что если предоставленный компонент или сервис никогда не будет использоваться приложением, компилятор сможет удалить его код из пакета.

Из-за того, как Angular хранит инъекционные маркеры, возможно, что такой неиспользуемый компонент или сервис все равно окажется в связке. На этой странице описан шаблон проектирования инъекции зависимостей, который поддерживает правильное встряхивание дерева с помощью облегченных инъекционных маркеров.

Шаблон проектирования облегченных инъекционных маркеров особенно важен для разработчиков библиотек. Он гарантирует, что когда приложение использует только некоторые из возможностей вашей библиотеки, неиспользуемый код может быть исключен из пакета клиентского приложения.

Когда приложение использует вашу библиотеку, могут существовать некоторые сервисы, предоставляемые вашей библиотекой, которые клиентское приложение не использует. В этом случае разработчик приложения должен ожидать, что этот сервис будет разнесен по деревьям и не будет способствовать увеличению размера скомпилированного приложения.

Поскольку разработчик приложения не может знать о проблеме tree-shaking в библиотеке или устранить ее, ответственность за это лежит на разработчике библиотеки.

Чтобы предотвратить сохранение неиспользуемых компонентов, ваша библиотека должна использовать облегченный шаблон проектирования инъекционных токенов.

## Когда маркеры сохраняются

Чтобы лучше объяснить условие, при котором происходит сохранение маркера, рассмотрим библиотеку, которая предоставляет компонент library-card. Этот компонент содержит тело и может содержать необязательный заголовок.

```html
<lib-card>
    <lib-header>…</lib-header>
</lib-card>
```

В вероятной реализации компонент `<lib-card>` использует `@ContentChild()` или `@ContentChildren()` для получения `<lib-header>` и `<lib-body>`, как показано ниже.

```ts
@Component({
  selector: 'lib-header',
  …,
})
class LibHeaderComponent {}

@Component({
  selector: 'lib-card',
  …,
})
class LibCardComponent {
  @ContentChild(LibHeaderComponent)
  header: LibHeaderComponent|null = null;
}
```

Поскольку `<lib-header>` является необязательным, элемент может появиться в шаблоне в своей минимальной форме, `<lib-card></lib-card>`. В этом случае `<lib-header>` не используется, и можно было бы ожидать, что он будет в виде дерева, но этого не происходит.
Это происходит потому, что `LibCardComponent` фактически содержит две ссылки на `LibHeaderComponent`.

```ts
@ContentChild(LibHeaderComponent) header: LibHeaderComponent;
```

-   Одна из этих ссылок находится в позиции _type_ — то есть, она указывает `LibHeaderComponent` как тип: `header: LibHeaderComponent;`.

-   Другая ссылка находится в позиции _value_ — то есть LibHeaderComponent является значением декоратора параметров `@ContentChild()`: `@ContentChild(LibHeaderComponent)`.

Компилятор по-разному обрабатывает ссылки на маркеры в этих позициях.

-   Компилятор стирает ссылки _type position_ после преобразования из TypeScript, поэтому они не влияют на дрожание деревьев.

-   Компилятор должен сохранять ссылки _value position_ во время выполнения, что предотвращает древовидное дрожание компонента.

В примере компилятор сохраняет маркер `LibHeaderComponent`, который встречается в позиции значения. Это предотвращает перетряхивание дерева ссылающегося компонента, даже если разработчик приложения фактически нигде не использует `<lib-header>`. Если код, шаблон и стили `LibHeaderComponent`` в совокупности становятся слишком большими, включение их без необходимости может значительно увеличить размер клиентского приложения.

## Когда использовать облегченный шаблон инъекционного маркера

Проблема "дрожащего дерева" возникает, когда компонент используется в качестве маркера инъекции. Это может произойти в двух случаях.

-   Маркер используется в позиции значения [content query](lifecycle-hooks.md#using-aftercontent-hooks 'Подробнее об использовании content queries.').

-   Маркер используется в качестве спецификатора типа для инъекции конструктора.

В следующем примере оба использования маркера `OtherComponent` приводят к сохранению `OtherComponent`, предотвращая его от перетряхивания дерева, когда он не используется.

```ts
class MyComponent {
    constructor(@Optional() other: OtherComponent) {}

    @ContentChild(OtherComponent)
    other: OtherComponent | null;
}
```

Хотя маркеры, используемые только в качестве спецификаторов типов, удаляются при преобразовании в JavaScript, все маркеры, используемые для инъекции зависимостей, необходимы во время выполнения. Они эффективно изменяют `constructor(@Optional() other: OtherComponent)` на `constructor(@Optional() @Inject(OtherComponent) other)`.
Теперь маркер находится в позиции значения и заставляет шейкер дерева сохранять ссылку.

!!!note ""

    Для всех сервисов библиотека должна использовать [tree-shakable providers](architecture-services.md#introduction-to-services-and-dependency-injection), предоставляя зависимости на корневом уровне, а не в конструкторах компонентов.

## Использование облегченных инъекционных маркеров

Шаблон проектирования облегченных инъекционных маркеров заключается в использовании небольшого абстрактного класса в качестве инъекционного маркера и предоставлении фактической реализации на более позднем этапе. Абстрактный класс сохраняется, а не встряхивается в дерево, но он мал и не оказывает существенного влияния на размер приложения.

Следующий пример показывает, как это работает для `LibHeaderComponent`.

```ts
abstract class LibHeaderToken {}

@Component({
  selector: 'lib-header',
  providers: [
    {provide: LibHeaderToken, useExisting: LibHeaderComponent}
  ]
  …,
})
class LibHeaderComponent extends LibHeaderToken {}

@Component({
  selector: 'lib-card',
  …,
})
class LibCardComponent {
  @ContentChild(LibHeaderToken) header: LibHeaderToken|null = null;
}
```

В этом примере реализация `LibCardComponent` больше не ссылается на `LibHeaderComponent` ни в позиции типа, ни в позиции значения. Это позволяет полностью перетряхнуть дерево `LibHeaderComponent`.
Сохраняется `LibHeaderToken`, но это только объявление класса, без конкретной реализации.

Он мал и не оказывает существенного влияния на размер приложения, если сохраняется после компиляции.

Вместо этого сам `LibHeaderComponent` реализует абстрактный класс `LibHeaderToken`. Вы можете смело использовать этот токен в качестве провайдера в определении компонента, что позволит Angular правильно инжектировать конкретный тип.

Подводя итог, можно сказать, что паттерн облегченной инъекции токенов состоит из следующего.

1.  Легкий инжектируемый токен, который представлен в виде абстрактного класса.

2.  Определение компонента, реализующего абстрактный класс.

3.  Инъекция облегченного шаблона с использованием `@ContentChild()` или `@ContentChildren()`.

4.  Провайдер в реализации маркера инъекции легковесного паттерна, который связывает маркер инъекции легковесного паттерна с реализацией.

### Использование маркера облегченной инъекции для определения API.

Компоненту, инжектирующему легкий инжектируемый маркер, может понадобиться вызвать метод в инжектированном классе. Теперь маркер является абстрактным классом. Поскольку инжектируемый компонент реализует этот класс, вы должны также объявить абстрактный метод в абстрактном классе легкого инжектируемого маркера.

Реализация метода со всеми его накладными расходами кода находится в инжектируемом компоненте, который может быть встряхнут деревом.

Это позволяет родителю общаться с дочерним компонентом, если он присутствует, безопасным для типов образом.

Например, `LibCardComponent` теперь запрашивает `LibHeaderToken`, а не `LibHeaderComponent`. Следующий пример показывает, как шаблон позволяет `LibCardComponent` взаимодействовать с `LibHeaderComponent` без фактического обращения к `LibHeaderComponent`.

```ts
abstract class LibHeaderToken {
  abstract doSomething(): void;
}

@Component({
  selector: 'lib-header',
  providers: [
    {provide: LibHeaderToken, useExisting: LibHeaderComponent}
  ]
  …,
})
class LibHeaderComponent extends LibHeaderToken {
  doSomething(): void {
    // Concrete implementation of `doSomething`
  }
}

@Component({
  selector: 'lib-card',
  …,
})
class LibCardComponent implement AfterContentInit {
  @ContentChild(LibHeaderToken)
  header: LibHeaderToken|null = null;

  ngAfterContentInit(): void {
    this.header && this.header.doSomething();
  }
}
```

В этом примере родительский компонент запрашивает маркер, чтобы получить дочерний компонент, и сохраняет полученную ссылку на компонент, если она присутствует. Перед вызовом метода в дочернем компоненте родительский компонент проверяет, присутствует ли дочерний компонент.
Если дочерний компонент был встряхнут, то на него нет ссылки во время выполнения, и вызов его метода невозможен.

### Именование вашего легковесного маркера инъекции

Легкие инъекционные маркеры полезны только для компонентов. Руководство по стилю Angular предлагает называть компоненты с помощью суффикса "Component".

Пример "LibHeaderComponent" следует этому соглашению.

Вы должны поддерживать связь между компонентом и его токеном, но при этом различать их. Рекомендуемый стиль — использовать базовое имя компонента с суффиксом "`Token`" для названия ваших облегченных инъекционных токенов: "`LibHeaderToken`".
