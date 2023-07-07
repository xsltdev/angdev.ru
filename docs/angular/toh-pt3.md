# Создайте компонент характеристик

На данный момент компонент `HeroesComponent` отображает как список героев, так и подробную информацию о выбранном герое.

Держать все функции в одном компоненте по мере роста приложения будет невозможно. В этом руководстве крупные компоненты разбиваются на более мелкие подкомпоненты, каждый из которых ориентирован на выполнение определенной задачи или рабочего процесса.

Первым шагом будет перемещение деталей героя в отдельный, многократно используемый `HeroDetailComponent`, и в итоге мы получим:

-   `HeroesComponent`, который представляет список героев.

-   Компонент `HeroDetailComponent`, который представляет детали выбранного героя.

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, см. в <live-example></live-example>.

</div>

## Создайте компонент `HeroDetailComponent`.

Используйте эту команду `ng generate` для создания нового компонента с именем `hero-detail`.

<code-example format="shell" language="shell">

ng generate component hero-detail

</code-example>

Команда выполняет следующее:

-   Создает каталог `src/app/hero-detail`.

Внутри этого каталога создаются четыре файла:

-   CSS-файл для стилей компонента.

-   HTML-файл для шаблона компонента.

-   TypeScript-файл с классом компонента с именем `HeroDetailComponent`.

-   Тестовый файл для класса `HeroDetailComponent`.

Команда также добавляет `HeroDetailComponent` в качестве объявления в декораторе `@NgModule` файла `src/app/app.module.ts`.

### Написать шаблон

Вырежьте HTML для детализации героя из нижней части шаблона `HeroesComponent` и вставьте его поверх содержимого шаблона в шаблоне `HeroDetailComponent`.

Вставленный HTML ссылается на `selectedHero`. Новый `HeroDetailComponent` может представлять _любого_ героя, а не только выбранного.

Замените `selectedHero` на `hero` везде в шаблоне.

Когда вы закончите, шаблон `HeroDetailComponent` должен выглядеть следующим образом:

<code-example header="src/app/hero-detail/hero-detail.component.html" path="toh-pt3/src/app/hero-detail/hero-detail.component.html"></code-example>.

### Добавьте свойство `@Input()` героя

Шаблон `HeroDetailComponent` привязывается к свойству `hero` компонента, которое имеет тип `Hero`.

Откройте файл класса `HeroDetailComponent` и импортируйте символ `Hero`.

<code-example path="toh-pt3/src/app/hero-detail/hero-detail.component.ts" region="import-hero" header="src/app/hero-detail/hero-detail.component.ts (import Hero)"></code-example>.

Свойство `hero` [должно быть свойством `Input`] (guide/inputs-outputs "Свойства ввода и вывода"),

аннотированным с помощью декоратора `@Input()`,

поскольку _внешний_ `HeroesComponent` [привязывается к нему](#heroes-component-template) следующим образом.

<code-example path="toh-pt3/src/app/heroes/heroes.component.html" region="hero-detail-binding"></code-example>.

Измените оператор импорта `@angular/core`, чтобы включить символ `Input`.

<code-example header="src/app/hero-detail/hero-detail.component.ts (import Input)" path="toh-pt3/src/app/hero-detail/hero-detail.component.ts" region="import-input"></code-example>.

Добавьте свойство `hero`, которому предшествует декоратор `@Input()`.

<code-example header="src/app/hero-detail/hero-detail.component.ts" path="toh-pt3/src/app/hero-detail/hero-detail.component.ts" region="input-hero"></code-example>.

Это единственное изменение, которое вы должны внести в класс `HeroDetailComponent`. Больше нет никаких свойств. Нет никакой логики представления.

Этот компонент только получает объект героя через свойство `hero` и отображает его.

## Показать `HeroDetailComponent`.

Компонент `HeroesComponent` использовался для самостоятельного отображения деталей героя, до того как вы удалили эту часть шаблона. Этот раздел поможет вам делегировать логику компоненту `HeroDetailComponent`.

Эти два компонента находятся в отношениях родитель/потомок. Родительский компонент, `HeroesComponent`, управляет дочерним компонентом `HeroDetailComponent` путем

посылая ему нового героя для отображения всякий раз, когда пользователь выбирает героя из списка.

Вам не нужно изменять _класс_ `HeroesComponent`, вместо этого измените его _шаблон_.

<a id="heroes-component-template"></a>

### Обновите шаблон `HeroesComponent`.

Селектором `HeroDetailComponent` является `'app-hero-detail'`. Добавьте элемент `<app-hero-detail>` в нижней части шаблона `HeroesComponent`, там, где раньше находилось детальное представление героя.

Привяжите `HeroesComponent.selectedHero` к свойству `hero` элемента следующим образом.

<code-example header="heroes.component.html (привязка HeroDetail)" path="toh-pt3/src/app/heroes/heroes.component.html" region="hero-detail-binding"></code-example>.

`[hero]="selectedHero"` - это привязка [свойства] (guide/property-binding) Angular.

Это _односторонняя_ привязка данных от свойства `selectedHero` компонента `HeroesComponent` к свойству `hero` целевого элемента, которое отображается на свойство `hero` компонента `HeroDetailComponent`.

Теперь, когда пользователь нажимает на героя в списке, `selectedHero` изменяется. Когда `selectedHero` изменяется, _привязка свойств_ обновляет `hero` и

компонент `HeroDetailComponent` отображает нового героя.

Переработанный шаблон `HeroesComponent` должен выглядеть следующим образом:

<code-example path="toh-pt3/src/app/heroes/heroes.component.html" header="heroes.component.html"></code-example>.

Браузер обновляется, и приложение начинает работать, как и раньше.

## Что изменилось?

Как и [ранее] (tutorial/tour-of-heroes/toh-pt2), когда пользователь нажимает на имя героя, подробная информация о герое появляется под списком героев.

Теперь `HeroDetailComponent` представляет эти детали вместо `HeroesComponent`.

Рефакторинг оригинального `HeroesComponent` на два компонента дает преимущества, как сейчас, так и в будущем:

1. Вы сократили обязанности `HeroesComponent`.

1. Вы можете развивать `HeroDetailComponent` в богатый редактор героев

не трогая родительский `HeroesComponent`.

1. Вы можете развивать `HeroesComponent`, не трогая детальное представление героя.

1. Вы можете повторно использовать `HeroDetailComponent` в шаблоне будущего компонента.

## Окончательный обзор кода

Вот файлы кода, рассмотренные на этой странице.

<code-tabs>

<code-pane header="src/app/hero-detail/hero-detail.component.ts" path="toh-pt3/src/app/hero-detail/hero-detail.component.ts"></code-pane>

<code-pane header="src/app/hero-detail/hero-detail.component.html" path="toh-pt3/src/app/hero-detail/hero-detail.component.html"></code-pane>

<code-pane header="src/app/heroes/heroes.component.html" path="toh-pt3/src/app/heroes/heroes.component.html"></code-pane>

<code-pane header="src/app/app.module.ts" path="toh-pt3/src/app/app/app.module.ts"></code-pane>

</code-tabs>

## Резюме

-   Вы создали отдельный, многократно используемый `HeroDetailComponent`.

-   Вы использовали [связывание свойств](guide/property-binding), чтобы дать родительскому `HeroesComponent` контроль над дочерним `HeroDetailComponent`.

-   Вы использовали декоратор [`@Input`](guide/inputs-outputs)

чтобы сделать свойство `hero` доступным для привязки внешним `HeroesComponent`.
