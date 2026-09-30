---
description: "Откладываемые представления уменьшают начальный размер пакета: код, без которого страница может отрисоваться сразу, загружается позже."
---

# Отложенная загрузка через `@defer` {: #deferred-loading-with-defer}

:date: 30.09.2026

Откладываемые представления, они же блоки `@defer`, уменьшают начальный размер пакета приложения: загрузка кода, без которого страница может отрисоваться сразу, откладывается. Часто это ускоряет первую загрузку и улучшает Core Web Vitals (CWV), в первую очередь Largest Contentful Paint (LCP) и Time to First Byte (TTFB).

Чтобы воспользоваться этой возможностью, участок шаблона декларативно оборачивают блоком `@defer`:

```html
@defer {
  <large-component />
}
```

Код любых компонентов, директив и пайпов внутри блока `@defer` выносится в отдельный файл JavaScript и загружается только когда это нужно, уже после отрисовки остального шаблона.

Откладываемые представления поддерживают разные триггеры, параметры предзагрузки и вложенные блоки для заполнителя, загрузки и состояния ошибки.

## Какие зависимости откладываются? {: #which-dependencies-are-deferred}

При загрузке приложения можно отложить компоненты, директивы, пайпы и любые CSS-стили компонента.

Чтобы зависимости внутри блока `@defer` действительно откладывались, нужны два условия:

1.  **Они должны быть автономными.** Неавтономные зависимости отложить нельзя: они всё равно загружаются сразу, даже если стоят внутри блоков `@defer`.
1.  **На них нельзя ссылаться вне блоков `@defer` в том же файле.** Если ссылка есть вне блока `@defer` или в запросах ViewChild, зависимости загружаются сразу.

_Транзитивные_ зависимости компонентов, директив и пайпов, использованных в блоке `@defer`, не обязаны быть автономными: их по-прежнему можно объявить в `NgModule`, и они участвуют в отложенной загрузке.

Компилятор Angular порождает оператор [динамического импорта](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import) для каждого компонента, директивы и пайпа, использованных в блоке `@defer`. Основное содержимое блока отрисовывается после того, как все импорты разрешатся. Angular не гарантирует какой-либо порядок этих импортов.

## Как вести разные этапы отложенной загрузки {: #how-to-manage-different-stages-of-deferred-loading}

У блоков `@defer` есть несколько вложенных блоков, чтобы аккуратно провести разные этапы отложенной загрузки.

### `@defer` {: #defer}

Это основной блок: он задаёт участок содержимого с ленивой загрузкой. Сразу он не отрисовывается — отложенное содержимое загружается и отрисовывается, когда срабатывает указанный [триггер](#controlling-deferred-content-loading-with-triggers) или выполняется условие `when`.

По умолчанию блок `@defer` срабатывает, когда состояние браузера становится [idle](defer.md#idle).

```html
@defer {
  <large-component />
}
```

### Содержимое-заполнитель через `@placeholder` {: #show-placeholder-content-with-placeholder}

По умолчанию блоки `@defer` не отрисовывают содержимое, пока не сработают.

`@placeholder` — необязательный блок: он объявляет, что показывать, пока блок `@defer` не сработал.

```html
@defer {
  <large-component />
} @placeholder {
  <p>Placeholder content</p>
}
```

Блок необязателен, но некоторым триггерам для работы нужен либо `@placeholder`, либо [ссылочная переменная шаблона](variables.md#template-reference-variables). Подробнее — в разделе [Триггеры](#controlling-deferred-content-loading-with-triggers).

Когда загрузка завершена, Angular заменяет содержимое заполнителя основным содержимым. В секции заполнителя можно использовать что угодно: обычный HTML, компоненты, директивы и пайпы. Учтите: _зависимости блока заполнителя загружаются сразу_.

Блок `@placeholder` принимает необязательный параметр `minimum`: минимальное время, в течение которого заполнитель показывается после первой отрисовки его содержимого.

```html
@defer {
  <large-component />
} @placeholder (minimum 500ms) {
  <p>Placeholder content</p>
}
```

Параметр `minimum` задают в миллисекундах (ms) или секундах (s). Им можно убрать быстрое мерцание заполнителя, если отложенные зависимости приходят слишком быстро.

### Содержимое загрузки через `@loading` {: #show-loading-content-with-loading}

`@loading` — необязательный блок: он объявляет содержимое, которое показывается, пока загружаются отложенные зависимости. Когда загрузка запускается, он заменяет блок `@placeholder`.

```html
@defer {
  <large-component />
} @loading {
  <img alt="loading..." src="loading.gif" />
} @placeholder {
  <p>Placeholder content</p>
}
```

Его зависимости загружаются сразу (как у `@placeholder`).

Блок `@loading` принимает два необязательных параметра, чтобы убрать быстрое мерцание содержимого, когда отложенные зависимости приходят слишком быстро:

-   `minimum` — минимальное время, в течение которого показывается этот заполнитель
-   `after` — сколько ждать после начала загрузки, прежде чем показать шаблон загрузки

```html
@defer {
  <large-component />
} @loading (after 100ms; minimum 1s) {
  <img alt="loading..." src="loading.gif" />
}
```

Оба параметра задают в миллисекундах (ms) или секундах (s). Таймеры обоих параметров начинаются сразу после того, как загрузка запущена.

### Состояние ошибки через `@error`, если отложенная загрузка не удалась {: #show-error-state-when-deferred-loading-fails-with-error}

`@error` — необязательный блок: он показывается, если отложенная загрузка не удалась. Как у `@placeholder` и `@loading`, зависимости блока `@error` загружаются сразу.

```html
@defer {
  <large-component />
} @error {
  <p>Failed to load large component.</p>
}
```

## Управление загрузкой отложенного содержимого триггерами {: #controlling-deferred-content-loading-with-triggers}

**Триггеры** задают, когда Angular загружает и показывает отложенное содержимое.

Когда блок `@defer` срабатывает, он заменяет содержимое заполнителя содержимым с ленивой загрузкой.

Несколько триггеров событий разделяют точкой с запятой `;`, и они вычисляются как условия ИЛИ.

Есть два вида триггеров: `on` и `when`.

### `on` {: #on}

`on` задаёт условие, при котором срабатывает блок `@defer`.

Доступные триггеры:

| Триггер | Описание |
| ----------------------------- | ---------------------------------------------------------------------- |
| [`idle`](#idle) | Срабатывает, когда браузер простаивает. Поддерживает необязательный таймаут. |
| [`viewport`](#viewport) | Срабатывает, когда указанное содержимое входит в область просмотра |
| [`interaction`](#interaction) | Срабатывает, когда пользователь взаимодействует с указанным элементом |
| [`hover`](#hover) | Срабатывает, когда указатель мыши оказывается над указанной областью |
| [`immediate`](#immediate) | Срабатывает сразу после того, как отрисовка неотложенного содержимого закончилась |
| [`timer`](#timer) | Срабатывает через заданное время |

#### `idle` {: #idle}

Триггер `idle` загружает отложенное содержимое, когда браузер достигает состояния простоя, на основе requestIdleCallback. Для блока `@defer` это поведение по умолчанию.

Необязательно можно указать таймаут в миллисекундах: он передаётся в [`requestIdleCallback`](https://developer.mozilla.org/docs/Web/API/Window/requestIdleCallback). Если браузер не запланирует обратный вызов достаточно скоро, работа выполнится не позже указанного таймаута.

```html
<!-- @defer (on idle) -->
@defer {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}

<!-- With a 500ms timeout -->
@defer (on idle(500)) {
  <large-cmp />
}
```

##### Настройка поведения `idle` {: #customizing-idle-behavior}

Поведение триггера `idle` настраивают собственной реализацией `IdleService` и регистрацией через `provideIdleServiceWith` в провайдерах приложения.

```ts
@Service()
class CustomIdleService implements IdleService {
  requestOnIdle(callback: (deadline?: IdleDeadline) => void, options?: IdleRequestOptions) {
    // Custom idle scheduling logic can be implemented here.
  }

  cancelOnIdle(id: number) {
    // Implement custom idle cancellation here.
  }
}

bootstrapApplication(App, {
  providers: [provideIdleServiceWith(CustomIdleService)],
});
```

#### `viewport` {: #viewport}

Триггер `viewport` загружает отложенное содержимое, когда указанное содержимое входит в область просмотра, через [Intersection Observer API](https://developer.mozilla.org/docs/Web/API/Intersection_Observer_API). Наблюдаемым содержимым может быть содержимое `@placeholder` или явная ссылка на элемент.

По умолчанию `@defer` следит, когда заполнитель входит в область просмотра. У такого заполнителя должен быть один корневой элемент.

```html
@defer (on viewport) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Другой вариант — указать [ссылочную переменную шаблона](variables.md) в том же шаблоне, что и блок `@defer`: это элемент, за входом которого в область просмотра следят. Переменную передают параметром триггера viewport.

```html
<div #greeting>Hello!</div>
@defer (on viewport(greeting)) {
  <greetings-cmp />
}
```

Чтобы настроить параметры `IntersectionObserver`, триггер `viewport` принимает объектный литерал. Литерал поддерживает все свойства второго параметра `IntersectionObserver`, кроме `root`. При записи объектным литералом триггер передают через свойство `trigger`.

```html
<div #greeting>Hello!</div>

<!-- With options and a trigger -->
@defer (on viewport({trigger: greeting, rootMargin: '100px', threshold: 0.5})) {
  <greetings-cmp />
}

<!-- With options and an implied trigger -->
@defer (on viewport({rootMargin: '100px', threshold: 0.5})) {
  <greetings-cmp />
} @placeholder {
  <div>Implied trigger</div>
}
```

#### `interaction` {: #interaction}

Триггер `interaction` загружает отложенное содержимое, когда пользователь взаимодействует с указанным элементом через события `click` или `keydown`.

По умолчанию элементом взаимодействия служит заполнитель. У такого заполнителя должен быть один корневой элемент.

```html
@defer (on interaction) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Другой вариант — указать [ссылочную переменную шаблона](variables.md) в том же шаблоне, что и блок `@defer`: это элемент, за взаимодействиями с которым следят. Переменную передают параметром триггера interaction.

```html
<div #greeting>Hello!</div>
@defer (on interaction(greeting)) {
  <greetings-cmp />
}
```

#### `hover` {: #hover}

Триггер `hover` загружает отложенное содержимое, когда указатель мыши оказывается над областью срабатывания, через события `mouseover` и `focusin`.

По умолчанию элементом взаимодействия служит заполнитель. У такого заполнителя должен быть один корневой элемент.

```html
@defer (on hover) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Другой вариант — указать [ссылочную переменную шаблона](variables.md) в том же шаблоне, что и блок `@defer`: это элемент, над которым оказывается указатель. Переменную передают параметром триггера hover.

```html
<div #greeting>Hello!</div>
@defer (on hover(greeting)) {
  <greetings-cmp />
}
```

#### `immediate` {: #immediate}

Триггер `immediate` загружает отложенное содержимое сразу. Отложенный блок начинает загружаться, как только закончилась отрисовка всего остального неотложенного содержимого.

```html
@defer (on immediate) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

#### `timer` {: #timer}

Триггер `timer` загружает отложенное содержимое через заданное время.

```html
@defer (on timer(500ms)) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Параметр длительности задают в миллисекундах (`ms`) или секундах (`s`).

### `when` {: #when}

Триггер `when` принимает собственное условное выражение и загружает отложенное содержимое, когда условие становится истинным.

```html
@defer (when condition) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Это одноразовая операция: блок `@defer` не возвращается к заполнителю, если после истинного значения условие становится ложным.

## Предзагрузка данных через `prefetch` {: #prefetching-data-with-prefetch}

Помимо условия, которое решает, когда показывать отложенное содержимое, можно указать **триггер предзагрузки**. Он загружает JavaScript, связанный с блоком `@defer`, ещё до показа отложенного содержимого.

Предзагрузка даёт более тонкое поведение: ресурсы можно начать подгружать ещё до того, как пользователь увидел блок `@defer` или поработал с ним, но когда взаимодействие вероятно скоро. Тогда ресурсы окажутся на месте быстрее.

Триггер предзагрузки записывают так же, как основной триггер блока, но с ключевым словом `prefetch` впереди. Основной триггер блока и триггер предзагрузки разделяют точкой с запятой (`;`).

В примере ниже предзагрузка начинается, когда браузер переходит в простой, а содержимое блока отрисовывается только после взаимодействия пользователя с заполнителем.

```html
@defer (on interaction; prefetch on idle) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}

<!-- Prefetching with a 500ms idle timeout -->
@defer (on interaction; prefetch on idle(500)) {
  <large-cmp />
}
```

## Тестирование блоков `@defer` {: #testing-defer-blocks}

Angular даёт API TestBed, чтобы проще тестировать блоки `@defer` и переключать разные состояния в тестах. По умолчанию блоки `@defer` в тестах проигрываются так же, как блок `@defer` вёл бы себя в настоящем приложении. Чтобы проходить состояния вручную, в конфигурации TestBed переключите поведение блока `@defer` на `Manual`.

```ts
it('should render a defer block in different states', async () => {
  // configures the defer block behavior to start in "paused" state for manual control.
  TestBed.configureTestingModule({deferBlockBehavior: DeferBlockBehavior.Manual});
  @Component({
    // ...
    template: `
      @defer {
        <large-component />
      } @placeholder {
        Placeholder
      } @loading {
        Loading...
      }
    `,
  })
  class ExampleA {}
  // Create component fixture.
  const componentFixture = TestBed.createComponent(ExampleA);
  // Retrieve the list of all defer block fixtures and get the first block.
  const deferBlockFixture = (await componentFixture.getDeferBlocks())[0];
  // Renders placeholder state by default.
  expect(componentFixture.nativeElement.innerHTML).toContain('Placeholder');
  // Render loading state and verify rendered output.
  await deferBlockFixture.render(DeferBlockState.Loading);
  expect(componentFixture.nativeElement.innerHTML).toContain('Loading');
  // Render final state and verify the output.
  await deferBlockFixture.render(DeferBlockState.Complete);
  expect(componentFixture.nativeElement.innerHTML).toContain('large works!');
});
```

## Работает ли `@defer` с `NgModule`? {: #does-defer-work-with-ngmodule}

Блоки `@defer` совместимы и с автономными компонентами, директивами и пайпами, и с теми, что основаны на NgModule. При этом **отложить можно только автономные компоненты, директивы и пайпы**. Зависимости на основе NgModule не откладываются и попадают в пакет, который загружается сразу.

## Совместимость блоков `@defer` и Hot Module Reload (HMR) {: #compatibility-between-defer-blocks-and-hot-module-reload-hmr}

Когда активна Hot Module Replacement (HMR), все чанки блоков `@defer` запрашиваются сразу, и настроенные триггеры не действуют. Чтобы вернуть обычное поведение триггеров, отключите HMR, запустив приложение с флагом `--no-hmr`.

## Как `@defer` работает с серверным рендерингом (SSR) и статической генерацией сайта (SSG)? {: #how-does-defer-work-with-server-side-rendering-ssr-and-static-site-generation-ssg}

По умолчанию при отрисовке приложения на сервере (и при SSR, и при SSG) блоки `@defer` всегда отрисовывают свой `@placeholder` (или ничего, если заполнитель не задан), а триггеры не вызываются. На клиенте содержимое `@placeholder` гидратируется, и триггеры включаются.

Чтобы отрисовать основное содержимое блоков `@defer` на сервере (и при SSR, и при SSG), включите [инкрементальную гидратацию](https://angular.dev/guide/incremental-hydration) и настройте триггеры `hydrate` для нужных блоков.

## Barrel-файлы и ленивые чанки {: #barrel-files-and-lazy-chunks}

Если `@defer` используется, а в результате сборки нет отдельного ленивого чанка, проверьте, как импортируется отложенный компонент. Частая причина — импорт через barrel-файл (`index.ts`): сборщики видят barrel как один модуль и держат все его экспорты вместе, поэтому компонент попадает в основной пакет независимо от `@defer`.

_index.ts_

```ts
export {HeavyComponent} from './heavy.component';
export {OtherComponent} from './other.component';
```

_parent.component.ts_

```ts
import {HeavyComponent} from './index'; // pulls in OtherComponent too

@Component({
  imports: [HeavyComponent],
  template: `@defer {
    <heavy-component />
  }`,
})
export class ParentComponent {}
```

Исправление простое: импортируйте напрямую из собственного файла компонента.

```ts
import {HeavyComponent} from './heavy.component';
```

Этого достаточно, чтобы сборщик вынес компонент в собственный чанк и загрузил его лениво, когда сработает триггер.

## Практические советы по откладыванию представлений {: #best-practices-for-deferring-views}

### Не допускайте каскадной загрузки у вложенных блоков `@defer` {: #avoid-cascading-loads-with-nested-defer-blocks}

У вложенных блоков `@defer` должны быть разные триггеры, чтобы они не загружались одновременно: одновременная загрузка даёт каскад запросов и может ухудшить скорость загрузки страницы.

### Не допускайте сдвигов вёрстки {: #avoid-layout-shifts}

Не откладывайте компоненты, которые видны в области просмотра пользователя при первой загрузке. Иначе Core Web Vitals могут ухудшиться из-за роста cumulative layout shift (CLS).

Если отложить такой компонент всё же нужно, не используйте триггеры `immediate`, `timer`, `viewport` и собственный `when`, из-за которых содержимое загружается во время первой отрисовки страницы.

### Помните о доступности {: #keep-accessibility-in-mind}

При использовании блоков `@defer` учитывайте пользователей вспомогательных технологий, например программ чтения с экрана.
Программа чтения, которая фокусируется на отложенном участке, сначала прочитает заполнитель или содержимое загрузки, но может не объявить изменения, когда загрузится отложенное содержимое.

Чтобы изменения отложенного содержимого объявлялись программам чтения с экрана, оберните блок `@defer` в элемент с живой областью:

```html
<div aria-live="polite" aria-atomic="true">
  @defer (on timer(2000)) {
    <user-profile [user]="currentUser" />
  } @placeholder {
    Loading user profile...
  } @loading {
    Please wait...
  } @error {
    Failed to load profile
  }
</div>
```

Так изменения объявляются пользователю при переходах (заполнитель &rarr; загрузка &rarr; содержимое/ошибка).


---

Источник: [https://angular.dev/guide/templates/defer](https://angular.dev/guide/templates/defer)
