# Динамический загрузчик компонентов

Шаблоны компонентов не всегда фиксированы. Приложению может потребоваться загрузка новых компонентов во время выполнения.

В этой книге рецептов показано, как добавлять компоненты динамически.

Смотрите [пример кода](https://angular.io/generated/live-examples/dynamic-component-loader/stackblitz.html) в этой поваренной книге.

## Динамическая загрузка компонента

В следующем примере показано, как создать динамический рекламный баннер.

Агентство-герой планирует рекламную кампанию с несколькими различными объявлениями, циклически повторяющимися на баннере. Новые рекламные компоненты часто добавляются несколькими различными командами.

Это делает нецелесообразным использование шаблона со статичной структурой компонентов.

Вместо этого необходим способ загрузки нового компонента без фиксированной ссылки на компонент в шаблоне рекламного баннера.

Angular поставляется с собственным API для динамической загрузки компонентов.

## Директива якоря

Перед добавлением компонентов необходимо определить точку привязки, чтобы указать Angular, куда вставлять компоненты.

Рекламный баннер использует вспомогательную директиву `AdDirective` для обозначения допустимых точек вставки в шаблоне.

```ts title=""
import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
    selector: '[adHost]',
})
export class AdDirective {
    constructor(
        public viewContainerRef: ViewContainerRef
    ) {}
}
```

`AdDirective` инжектирует `ViewContainerRef` для получения доступа к контейнеру представления элемента, в котором будет размещен динамически добавляемый компонент.

В декораторе `@Directive` обратите внимание на имя селектора `adHost`; именно его вы используете для применения директивы к элементу. В следующем разделе показано, как это сделать.

## Загрузка компонентов

Большая часть реализации рекламного баннера находится в `ad-banner.component.ts`. Для простоты в этом примере HTML находится в свойстве `@Component` декоратора `template` как строка шаблона.

Элемент `<ng-template>` является местом применения директивы, которую вы только что создали. Чтобы применить `AdDirective`, вспомните селектор из `ad.directive.ts`, `[adHost]`.

Примените его к `<ng-template>` без квадратных скобок.

Теперь Angular знает, куда динамически загружать компоненты.

```ts title="src/app/ad-banner.component.ts (template)"
template: `
  <div class="ad-banner-example">
    <h3>Advertisements</h3>
    <ng-template adHost></ng-template>
  </div>
`;
```

Элемент `<ng-template>` является хорошим выбором для динамических компонентов, поскольку он не выводит никаких дополнительных данных.

## Разрешение компонентов

Рассмотрим подробнее методы в `ad-banner.component.ts`.

`AdBannerComponent` принимает массив объектов `AdItem` в качестве входных данных, которые в конечном итоге поступают из `AdService`. Объекты `AdItem` определяют тип компонента для загрузки и любые данные для привязки к компоненту.`AdService` возвращает фактические объявления, составляющие рекламную кампанию.

Передача массива компонентов в `AdBannerComponent` позволяет получить динамический список объявлений без статических элементов в шаблоне.

С помощью метода `getAds()`, `AdBannerComponent` циклически просматривает массив `AdItems` и загружает новый компонент каждые 3 секунды, вызывая `loadComponent()`.

```ts title="src/app/ad-banner.component.ts (excerpt)"
export class AdBannerComponent
    implements OnInit, OnDestroy {
    @Input() ads: AdItem[] = [];

    currentAdIndex = -1;

    @ViewChild(AdDirective, { static: true })
    adHost!: AdDirective;

    private clearTimer: VoidFunction | undefined;

    ngOnInit(): void {
        this.loadComponent();
        this.getAds();
    }

    ngOnDestroy() {
        this.clearTimer?.();
    }

    loadComponent() {
        this.currentAdIndex =
            (this.currentAdIndex + 1) % this.ads.length;
        const adItem = this.ads[this.currentAdIndex];

        const viewContainerRef = this.adHost
            .viewContainerRef;
        viewContainerRef.clear();

        const componentRef = viewContainerRef.createComponent<
            AdComponent
        >(adItem.component);
        componentRef.instance.data = adItem.data;
    }

    getAds() {
        const interval = setInterval(() => {
            this.loadComponent();
        }, 3000);
        this.clearTimer = () => clearInterval(interval);
    }
}
```

Метод `loadComponent()` выполняет здесь большую часть тяжелой работы. Рассмотрим его шаг за шагом.

Сначала он выбирает объявление.

!!!note "Как `loadComponent()` выбирает объявление"

    Метод `loadComponent()` выбирает объявление с помощью математики.

    Сначала он устанавливает `currentAdIndex`, взяв значение, равное текущему, плюс один, разделив его на длину массива `AdItem`, и используя _оставшуюся часть_ в качестве нового значения `currentAdIndex`. Затем это значение используется для выбора `adItem` из массива.

Далее, вы нацеливаетесь на `viewContainerRef`, который существует на этом конкретном экземпляре компонента. Откуда вы знаете, что это именно этот экземпляр?

Потому что он ссылается на `adHost`, а `adHost` - это директива, которую вы установили ранее, чтобы указать Angular, куда вставлять динамические компоненты.

Как вы помните, `AdDirective` вставляет `ViewContainerRef` в свой конструктор. Так директива получает доступ к элементу, который вы хотите использовать для размещения динамического компонента.

Чтобы добавить компонент в шаблон, вы вызываете `createComponent()` на `ViewContainerRef`.

Метод `createComponent()` возвращает ссылку на загруженный компонент. Используйте эту ссылку для взаимодействия с компонентом, присваивая ему свойства или вызывая его методы.

## Интерфейс `AdComponent`

В рекламном баннере все компоненты реализуют общий интерфейс `AdComponent` для стандартизации API для передачи данных компонентам.

Вот два примера компонентов и интерфейса `AdComponent` для справки:

=== "hero-job-ad.component.ts"

    ```ts
    import { Component, Input } from '@angular/core';

    import { AdComponent } from './ad.component';

    @Component({
    	template: `
    		<div class="job-ad">
    			<h4>{{ data.headline }}</h4>
    			{{ data.body }}
    		</div>
    	`,
    })
    export class HeroJobAdComponent implements AdComponent {
    	@Input() data: any;
    }
    ```

=== "hero-profile.component.ts"

    ```ts
    import { Component, Input } from '@angular/core';

    import { AdComponent } from './ad.component';

    @Component({
    	template: `
    		<div class="hero-profile">
    			<h3>Featured Hero Profile</h3>
    			<h4>{{ data.name }}</h4>

    			<p>{{ data.bio }}</p>

    			<strong>Hire this hero today!</strong>
    		</div>
    	`,
    })
    export class HeroProfileComponent implements AdComponent {
    	@Input() data: any;
    }
    ```

=== "ad.component.ts"

    ```ts
    export interface AdComponent {
    	data: any;
    }
    ```

## Окончательный рекламный баннер

Окончательный рекламный баннер выглядит следующим образом:

![Ads](ads-example.gif)

См. полный [код примера](https://angular.io/generated/live-examples/dynamic-component-loader/stackblitz.html).

:date: 28.02.2022
