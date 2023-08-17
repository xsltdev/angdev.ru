# Инкапсуляция представления

В Angular стили компонента могут быть инкапсулированы в основной элемент компонента, чтобы они не влияли на остальную часть приложения.

Декоратор `Component` предоставляет опцию [`encapsulation`](https://angular.io/api/core/Component#encapsulation), которую можно использовать для управления тем, как инкапсуляция применяется _для каждого компонента_.

Выберите один из следующих режимов:

<!-- vale off -->

| Режимы                        | Подробности                                                                                                                                                                                                                                                                                              |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ViewEncapsulation.ShadowDom` | Angular использует встроенный в браузер [Shadow DOM API](https://developer.mozilla.org/docs/Web/Web_Components/Shadow_DOM), чтобы заключить представление компонента внутри ShadowRoot, используемого в качестве основного элемента компонента, и применить предоставленные стили изолированным образом. |
| `ViewEncapsulation.Emulated`  | Angular изменяет CSS-селекторы компонента так, что они применяются только к представлению компонента и не влияют на другие элементы в приложении, _эмулируя_ поведение Shadow DOM. Подробнее см. в [Проверка сгенерированного CSS](view-encapsulation.md#inspect-generated-css).                         |
| `ViewEncapsulation.None`      | Angular не применяет никакого вида инкапсуляции представлений, что означает, что любые стили, заданные для компонента, применяются глобально и могут повлиять на любой HTML-элемент, присутствующий в приложении. Этот режим по сути то же самое, что и включение стилей в сам HTML.                     |

## Инспектирование сгенерированного CSS

При использовании инкапсуляции эмулированного представления Angular предварительно обрабатывает все стили компонента, чтобы они применялись только к его представлению.

В DOM запущенного приложения Angular элементы, принадлежащие компонентам, использующим эмулированную инкапсуляцию представления, имеют некоторые дополнительные атрибуты, прикрепленные к ним:

```html
<hero-details _nghost-pmm-5>
    <h2 _ngcontent-pmm-5>Mister Fantastic</h2>
    <hero-team _ngcontent-pmm-5 _nghost-pmm-6>
        <h3 _ngcontent-pmm-6>Team</h3>
    </hero-team>
</hero-details>
```

Существует два вида этих атрибутов:

| Атрибуты     | Подробности                                                                                                                                                                                                            |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_nghost`    | Добавляются к элементам, которые окружают представление компонента и которые были бы ShadowRoots в родной инкапсуляции Shadow DOM. Обычно это относится к элементам хоста компонентов.                                 |
| `_ngcontent` | Добавляются к дочерним элементам внутри представления компонента, они используются для сопоставления элементов с их соответствующими эмулированными ShadowRoots (хост-элементы с соответствующим атрибутом `_nghost`). |

Точные значения этих атрибутов являются частной деталью реализации Angular. Они создаются автоматически, и вы никогда не должны ссылаться на них в коде приложения.

На них нацелены созданные стили компонента, которые внедряются в секцию `<head>` DOM:

```css
[_nghost-pmm-5] {
    display: block;
    border: 1px solid black;
}
h3[_ngcontent-pmm-6] {
    background-color: white;
    border: 1px solid #777;
}
```

Эти стили подвергаются постобработке, в результате чего каждый CSS-селектор дополняется соответствующим атрибутом `_nghost` или `_ngcontent`. Эти модифицированные селекторы обеспечивают изолированное и целенаправленное применение стилей к представлениям компонентов.

## Смешивание режимов инкапсуляции

Как упоминалось ранее, вы указываете режим инкапсуляции в декораторе компонента на основе _каждого компонента_. Это означает, что в вашем приложении вы можете иметь различные компоненты, использующие различные стратегии инкапсуляции.

Хотя это возможно, делать это не рекомендуется. Если это действительно необходимо, вы должны знать, как стили компонентов, использующих различные режимы инкапсуляции, взаимодействуют друг с другом:

| Режимы                        | Подробности                                                                                                                                                                       |
| :---------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ViewEncapsulation.Emulated`  | Стили компонентов добавляются в `<head>` документа, делая их доступными во всем приложении, но их селекторы влияют только на элементы в шаблонах соответствующих компонентов.     |
| `ViewEncapsulation.None`      | Стили компонентов добавляются в `<head>` документа, делая их доступными во всем приложении, поэтому они полностью глобальны и влияют на все соответствующие элементы в документе. |
| `ViewEncapsulation.ShadowDom` | Стили компонентов добавляются только в теневой узел DOM, гарантируя, что они влияют только на элементы в представлениях соответствующих компонентов.                              |

!!!info ""

    Стили компонентов `ViewEncapsulation.Emulated` и `ViewEncapsulation.None` также добавляются в теневой DOM-хост каждого компонента `ViewEncapsulation.ShadowDom`.

    Это означает, что стили для компонентов с `ViewEncapsulation.None` влияют на соответствующие элементы в теневом DOM.

    Поначалу такой подход может показаться неинтуитивным. Но без него компонент с `ViewEncapsulation.None` будет отображаться по-разному в компоненте, использующем `ViewEncapsulation.ShadowDom`, так как его стили не будут доступны.

### Примеры

В этом разделе показаны примеры взаимодействия стилей компонентов с различными `ViewEncapsulation`.

Смотрите [пример](https://angular.io/generated/live-examples/view-encapsulation/stackblitz.html), чтобы попробовать эти компоненты самостоятельно.

#### Без инкапсуляции

Первый пример показывает компонент, который имеет `ViewEncapsulation.None`. Этот компонент окрашивает элементы своего шаблона в красный цвет.

```ts title="src/app/no-encapsulation.component.ts"
@Component({
    selector: 'app-no-encapsulation',
    template: `
        <h2>None</h2>
        <div class="none-message">No encapsulation</div>
    `,
    styles: ['h2, .none-message { color: red; }'],
    encapsulation: ViewEncapsulation.None,
})
export class NoEncapsulationComponent {}
```

Angular добавляет стили для этого компонента в качестве глобальных стилей в `<head>` документа.

Как уже упоминалось, Angular также добавляет стили во все теневые узлы DOM, делая стили доступными для всего приложения.

![component with no encapsulation](no-encapsulation.png)

#### Эмулированная инкапсуляция

Во втором примере показан компонент, который имеет `ViewEncapsulation.Emulated`. Этот компонент окрашивает элементы своего шаблона в зеленый цвет.

```ts title="src/app/emulated-encapsulation.component.ts"
@Component({
    selector: 'app-emulated-encapsulation',
    template: `
        <h2>Emulated</h2>
        <div class="emulated-message">
            Emulated encapsulation
        </div>
        <app-no-encapsulation></app-no-encapsulation>
    `,
    styles: ['h2, .emulated-message { color: green; }'],
    encapsulation: ViewEncapsulation.Emulated,
})
export class EmulatedEncapsulationComponent {}
```

По аналогии с `ViewEncapsulation.None`, Angular добавляет стили для этого компонента в `<head>` документа, но с "scoped" стилями.

Только элементы, находящиеся непосредственно в шаблоне этого компонента, будут соответствовать его стилям. Поскольку стили "scoped" для `EmulatedEncapsulationComponent` являются специфическими, они отменяют глобальные стили для `NoEncapsulationComponent`.

В этом примере `EmulatedEncapsulationComponent` содержит `NoEncapsulationComponent`, но `NoEncapsulationComponent` все еще стилизуется как ожидалось, поскольку "scoped" стили `EmulatedEncapsulationComponent` не соответствуют элементам в его шаблоне.

![component with no encapsulation](emulated-encapsulation.png)

#### Инкапсуляция Shadow DOM

Третий пример показывает компонент, который имеет `ViewEncapsulation.ShadowDom`. Этот компонент окрашивает свои элементы шаблона в синий цвет.

```ts title="src/app/shadow-dom-encapsulation.component.ts"
@Component({
    selector: 'app-shadow-dom-encapsulation',
    template: `
        <h2>ShadowDom</h2>
        <div class="shadow-message">
            Shadow DOM encapsulation
        </div>
        <app-emulated-encapsulation></app-emulated-encapsulation>
        <app-no-encapsulation></app-no-encapsulation>
    `,
    styles: ['h2, .shadow-message { color: blue; }'],
    encapsulation: ViewEncapsulation.ShadowDom,
})
export class ShadowDomEncapsulationComponent {}
```

Angular добавляет стили для этого компонента только в теневой DOM-хост, поэтому они не видны за пределами теневого DOM.

!!!note ""

    Angular также добавляет глобальные стили из `NoEncapsulationComponent` и `EmulatedEncapsulationComponent` в теневой DOM-хост. Эти стили по-прежнему доступны для элементов в шаблоне этого компонента.

В этом примере `ShadowDomEncapsulationComponent` содержит `NoEncapsulationComponent` и `EmulatedEncapsulationComponent`.

Стили, добавленные компонентом `ShadowDomEncapsulationComponent`, доступны во всем теневом DOM этого компонента, а также и для `NoEncapsulationComponent` и `EmulatedEncapsulationComponent`.

Компонент `EmulatedEncapsulationComponent` имеет специфические "scoped" стили, поэтому стилизация шаблона этого компонента не затрагивается.

Поскольку стили из `ShadowDomEncapsulationComponent` добавляются в теневой узел после глобальных стилей, стиль `h2` переопределяет стиль из `NoEncapsulationComponent`. В результате элемент `<h2>` в `NoEncapsulationComponent` окрашивается в синий, а не в красный цвет, что может быть не тем, что задумал автор компонента.

![component with no encapsulation](shadow-dom-encapsulation.png)

:date: 21.04.2023
