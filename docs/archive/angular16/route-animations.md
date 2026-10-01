# Анимация перехода между маршрутами

:date: 11.10.2022

**Маршрутизация** позволяет пользователям перемещаться между различными маршрутами в приложении.

## Предварительные условия

Базовое понимание следующих концепций:

-   [Введение в анимации Angular](animations.md)
-   [Переход и триггеры](transition-and-triggers.md)
-   [Многоразовые анимации](reusable-animations.md)

## Включить анимацию перехода маршрутизации

Когда пользователь переходит от одного маршрута к другому, маршрутизатор Angular сопоставляет путь URL с соответствующим компонентом и отображает его вид. Анимация этого перехода маршрута может значительно улучшить пользовательский опыт.

Angular router поставляется с высокоуровневыми функциями анимации, которые позволяют анимировать переходы между представлениями при изменении маршрута. Чтобы создать анимационную последовательность при переключении между маршрутами, необходимо определить вложенные анимационные последовательности.

Начните с компонента верхнего уровня, в котором расположено представление, и вложите анимацию в компоненты, в которых расположены встроенные представления.

Чтобы включить анимацию перехода между маршрутами, сделайте следующее:

1.  Импортируйте модуль маршрутизации в приложение и создайте конфигурацию маршрутизации, определяющую возможные маршруты.

2.  Добавьте выход маршрутизатора, чтобы указать маршрутизатору Angular, где разместить активированные компоненты в DOM.

3.  Определите анимацию.

Проиллюстрируйте анимацию перехода маршрутизатора, перемещаясь между двумя маршрутами, _Home_ и _About_, связанными с представлениями `HomeComponent` и `AboutComponent` соответственно. Оба эти представления компонентов являются дочерними для самого верхнего представления, расположенного в `AppComponent`.

Реализуйте анимацию перехода маршрутизатора, которая при навигации между двумя маршрутами сдвигает новый вид вправо и сдвигает старый вид.

![Animations in action](route-animation.gif)

## Конфигурация маршрутов

Для начала настройте набор маршрутов, используя методы, доступные в классе `RouterModule`. Эта конфигурация маршрутов указывает маршрутизатору, как перемещаться.

Используйте метод `RouterModule.forRoot` для определения набора маршрутов. Также добавьте `RouterModule` в массив `imports` главного модуля, `AppModule`.

!!!note ""

    Используйте метод `RouterModule.forRoot` в корневом модуле, `AppModule`, для регистрации маршрутов и провайдеров приложений верхнего уровня.
    Для функциональных модулей вместо этого вызывайте метод `RouterModule.forChild`.

Следующая конфигурация определяет возможные маршруты для приложения.

```ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { OpenCloseComponent } from './open-close.component';
import { OpenClosePageComponent } from './open-close-page.component';
import { OpenCloseChildComponent } from './open-close.component.4';
import { ToggleAnimationsPageComponent } from './toggle-animations-page.component';
import { StatusSliderComponent } from './status-slider.component';
import { StatusSliderPageComponent } from './status-slider-page.component';
import { HeroListPageComponent } from './hero-list-page.component';
import { HeroListGroupPageComponent } from './hero-list-group-page.component';
import { HeroListGroupsComponent } from './hero-list-groups.component';
import { HeroListEnterLeavePageComponent } from './hero-list-enter-leave-page.component';
import { HeroListEnterLeaveComponent } from './hero-list-enter-leave.component';
import { HeroListAutoCalcPageComponent } from './hero-list-auto-page.component';
import { HeroListAutoComponent } from './hero-list-auto.component';
import { HomeComponent } from './home.component';
import { AboutComponent } from './about.component';
import { InsertRemoveComponent } from './insert-remove.component';
import { QueryingComponent } from './querying.component';

@NgModule({
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        RouterModule.forRoot([
            {
                path: '',
                pathMatch: 'full',
                redirectTo: '/enter-leave',
            },
            {
                path: 'open-close',
                component: OpenClosePageComponent,
                data: { animation: 'openClosePage' },
            },
            {
                path: 'status',
                component: StatusSliderPageComponent,
                data: { animation: 'statusPage' },
            },
            {
                path: 'toggle',
                component: ToggleAnimationsPageComponent,
                data: { animation: 'togglePage' },
            },
            {
                path: 'heroes',
                component: HeroListPageComponent,
                data: { animation: 'filterPage' },
            },
            {
                path: 'hero-groups',
                component: HeroListGroupPageComponent,
                data: { animation: 'heroGroupPage' },
            },
            {
                path: 'enter-leave',
                component: HeroListEnterLeavePageComponent,
                data: { animation: 'enterLeavePage' },
            },
            {
                path: 'auto',
                component: HeroListAutoCalcPageComponent,
                data: { animation: 'autoPage' },
            },
            {
                path: 'insert-remove',
                component: InsertRemoveComponent,
                data: { animation: 'insertRemovePage' },
            },
            {
                path: 'querying',
                component: QueryingComponent,
                data: { animation: 'queryingPage' },
            },
            {
                path: 'home',
                component: HomeComponent,
                data: { animation: 'HomePage' },
            },
            {
                path: 'about',
                component: AboutComponent,
                data: { animation: 'AboutPage' },
            },
        ]),
    ],
});
```

Пути `home` и `about` связаны с представлениями `HomeComponent` и `AboutComponent`. Конфигурация маршрута указывает маршрутизатору Angular инстанцировать представления `HomeComponent` и `AboutComponent`, когда навигация соответствует соответствующему пути.

Свойство `data` каждого маршрута определяет ключевую конфигурацию, специфичную для анимации, связанную с маршрутом. Значение свойства `data` передается в `AppComponent` при изменении маршрута.

!!!note ""

    Имена свойств `data`, которые вы используете, могут быть произвольными.
    Например, имя _animation_, использованное в предыдущем примере, является произвольным выбором.

## Router outlet

После настройки маршрутов добавьте `<router-outlet>` внутри корневого шаблона `AppComponent`. Директива `<router-outlet>` указывает маршрутизатору Angular, где отображать представления при сопоставлении с маршрутом.

В `ChildrenOutletContexts` хранится информация об аутлетах и активированных маршрутах. Свойство `data` каждого `маршрута` может быть использовано для анимации переходов маршрутизации.

```html
<div [@routeAnimations]="getRouteAnimationData()">
    <router-outlet></router-outlet>
</div>
```

`AppComponent` определяет метод, который может обнаружить, когда представление изменяется. Метод присваивает значение состояния анимации триггеру анимации (`@routeAnimation`) на основе значения свойства `data` конфигурации маршрута.

Вот пример метода `AppComponent`, который обнаруживает изменение маршрута.

```ts
constructor(private contexts: ChildrenOutletContexts) {}

getRouteAnimationData() {
  return this.contexts.getContext('primary')?.route?.snapshot?.data?.['animation'];
}
```

Метод `getRouteAnimationData()` принимает значение розетки. Он возвращает строку, которая представляет состояние анимации, основанное на пользовательских данных текущего активного маршрута. Используйте эти данные для управления тем, какой переход запускать для каждого маршрута.

## Определение анимации

Анимации могут быть определены непосредственно внутри ваших компонентов. В данном примере вы определяете анимации в отдельном файле, что позволяет повторно использовать анимации.

Следующий фрагмент кода определяет многократно используемую анимацию с именем `slideInAnimation`.

```ts
export const slideInAnimation = trigger('routeAnimations', [
    transition('HomePage <=> AboutPage', [
        style({ position: 'relative' }),
        query(':enter, :leave', [
            style({
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
            }),
        ]),
        query(':enter', [style({ left: '-100%' })]),
        query(':leave', animateChild()),
        group([
            query(':leave', [
                animate(
                    '300ms ease-out',
                    style({ left: '100%' })
                ),
            ]),
            query(':enter', [
                animate(
                    '300ms ease-out',
                    style({ left: '0%' })
                ),
            ]),
        ]),
    ]),
    transition('* <=> *', [
        style({ position: 'relative' }),
        query(':enter, :leave', [
            style({
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
            }),
        ]),
        query(':enter', [style({ left: '-100%' })]),
        query(':leave', animateChild()),
        group([
            query(':leave', [
                animate(
                    '200ms ease-out',
                    style({ left: '100%', opacity: 0 })
                ),
            ]),
            query(':enter', [
                animate(
                    '300ms ease-out',
                    style({ left: '0%' })
                ),
            ]),
            query('@*', animateChild()),
        ]),
    ]),
]);
```

Определение анимации выполняет следующие задачи:

-   Определяет два перехода (один `триггер` может определять несколько состояний и переходов)

-   Настраивает стили главного и дочернего представлений для управления их относительным положением во время перехода

-   Использует `query()` для определения того, какое дочернее представление входит, а какое выходит из главного представления.

Изменение маршрута активирует триггер анимации, и применяется переход, соответствующий изменению состояния.

!!!note ""

Состояния перехода должны соответствовать значению свойства `data`, определенному в конфигурации маршрута.

Сделайте определение анимации доступным в вашем приложении, добавив многоразовую анимацию (`slideInAnimation`) в метаданные `animations` компонента `AppComponent`.

```ts
@Component({
    selector: 'app-root',
    templateUrl: 'app.component.html',
    styleUrls: ['app.component.css'],
    animations: [slideInAnimation],
});
```

### Стиль главного и дочернего компонентов

Во время перехода новое представление вставляется непосредственно после старого, и оба элемента появляются на экране одновременно. Чтобы предотвратить такое поведение, обновите основное представление, чтобы оно использовало относительное позиционирование.

Затем обновите удаленные и вставленные дочерние представления, чтобы использовать абсолютное позиционирование.

Добавление этих стилей к представлениям анимирует контейнеры на месте и не позволяет одному представлению влиять на положение другого на странице.

```ts
trigger('routeAnimations', [
    transition('HomePage <=> AboutPage', [
        style({ position: 'relative' }),
        query(':enter, :leave', [
            style({
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
            }),
        ]),
    ]),
]);
```

### Запрос контейнеров представления

Используйте метод `query()` для поиска и анимации элементов внутри текущего компонента хоста. Оператор `query(":enter")` возвращает представление, которое вставляется, а `query(":leave")` возвращает представление, которое удаляется.

Предположим, что вы выполняете маршрутизацию из раздела _Home =&gt; About_.

```ts
query(':enter', [
    style({ left: '-100%' })
  ]),
  query(':leave', animateChild()),
  group([
    query(':leave', [
      animate('300ms ease-out', style({ left: '100%' }))
    ]),
    query(':enter', [
      animate('300ms ease-out', style({ left: '0%' }))
    ]),
  ]),
]),
transition('* <=> *', [
  style({ position: 'relative' }),
  query(':enter, :leave', [
    style({
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%'
    })
  ]),
  query(':enter', [
    style({ left: '-100%' })
  ]),
  query(':leave', animateChild()),
  group([
    query(':leave', [
      animate('200ms ease-out', style({ left: '100%', opacity: 0 }))
    ]),
    query(':enter', [
      animate('300ms ease-out', style({ left: '0%' }))
    ]),
    query('@*', animateChild())
  ]),
])
```

После стилизации представлений код анимации выполняет следующие действия:

1.  `query(':enter', style({ left: '-100%' }))` соответствует добавляемому представлению и скрывает вновь добавленное представление, позиционируя его в крайнем левом углу.

2.  Вызывает `animateChild()` на уходящем представлении, чтобы запустить его дочерние анимации.

3.  Использует функцию `group()`, чтобы внутренние анимации запускались параллельно.

4.  Внутри функции `group()`:

    1.  Запрашивает удаляемый вид и анимирует его сдвиг далеко вправо.

    2.  Вставляет новый вид, анимируя его с помощью функции смягчения и длительности.

        В результате анимации вид `about` сдвигается влево.

5.  Вызывает метод `animateChild()` нового представления, чтобы запустить его дочерние анимации после завершения основной анимации.

Теперь у вас есть базовая маршрутизируемая анимация, которая анимирует переход от одного представления к другому.

## Подробнее об анимации в Angular

Вам также может быть интересно следующее:

-   [Введение в анимации Angular](animations.md)
-   [Переход и триггеры](transition-and-triggers.md)
-   [Сложные анимационные последовательности](complex-animation-sequences.md)
-   [Многоразовые анимации](reusable-animations.md)
