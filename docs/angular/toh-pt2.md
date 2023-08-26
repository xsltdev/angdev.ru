---
description: В этом руководстве показано, как развернуть приложение Tour of Heroes для отображения списка героев
---

# Отображение списка выбора

:date: 23.05.2022

В этом руководстве показано, как:

-   Развернуть приложение Tour of Heroes для отображения списка героев.
-   Позволить пользователям выбрать героя и отобразить его подробную информацию.

!!!note ""

    Пример приложения, которое описывается на этой странице, см.:

    -   [Живой пример](https://angular.io/generated/live-examples/toh-pt2/stackblitz.html)
    -   [Скачать](https://angular.io/generated/zips/toh-pt2/toh-pt2.zip)

## Создайте героев

Первым шагом будет создание героев для отображения.

Создайте файл `mock-heroes.ts` в каталоге `src/app/`. Определите константу `HEROES` как массив из десяти героев и экспортируйте его.

Файл должен выглядеть следующим образом.

```ts
import { Hero } from './hero';

export const HEROES: Hero[] = [
    { id: 12, name: 'Dr. Nice' },
    { id: 13, name: 'Bombasto' },
    { id: 14, name: 'Celeritas' },
    { id: 15, name: 'Magneta' },
    { id: 16, name: 'RubberMan' },
    { id: 17, name: 'Dynama' },
    { id: 18, name: 'Dr. IQ' },
    { id: 19, name: 'Magma' },
    { id: 20, name: 'Tornado' },
];
```

## Отображение героев

Откройте файл класса `HeroesComponent` и импортируйте макет `HEROES`.

```ts
import { HEROES } from '../mock-heroes';
```

В классе `HeroesComponent` определите свойство компонента под названием `heroes`, чтобы открыть массив `HEROES` для привязки.

```ts
export class HeroesComponent {
    heroes = HEROES;
}
```

### Список героев с помощью `*ngFor`

Откройте файл шаблона `HeroesComponent` и внесите в него следующие изменения:

1.  Добавьте `<h2>` в верхней части.
2.  Ниже `<h2>` добавьте элемент `<ul>`.
3.  В элемент `<ul>` вставьте элемент `<li>`.
4.  Поместите `<button>` внутрь `<li>` который отображает свойства `hero` внутри элементов `<span>`.
5.  Добавьте CSS-классы для стилизации компонента.

чтобы он выглядел следующим образом:

```html
<h2>My Heroes</h2>
<ul class="heroes">
    <li>
        <button type="button">
            <span class="badge">{{hero.id}}</span>
            <span class="name">{{hero.name}}</span>
        </button>
    </li>
</ul>
```

В результате будет выдана ошибка, поскольку свойство `hero` не существует. Чтобы получить доступ к каждому отдельному герою и перечислить их всех, добавьте `*ngFor` к `<li>` для итерации по списку героев:

```html
<li *ngFor="let hero of heroes"></li>
```

Директива [`*ngFor`](built-in-directives.md#ngFor) — это директива Angular _repeater_. Она повторяет ведущий элемент для каждого элемента списка.

Синтаксис в данном примере выглядит следующим образом:

| Синтаксис | Детали                                                                 |
| :-------- | :--------------------------------------------------------------------- |
| `<li>`    | Принимающий элемент.                                                   |
| `heroes`  | Хранит список героев из класса `HeroesComponent`, список героев-макет. |
| `hero`    | Удерживает объект текущего героя для каждой итерации по списку.        |

!!!warning ""

    Не забудьте поставить звездочку `*` перед `ngFor`. Это важная часть синтаксиса.

После обновления браузера появится список героев.

!!!note "Интерактивные элементы"

    Внутри элемента `<li>` добавьте элемент `<button>` для обертывания информации о герое, а затем сделайте его кликабельным. Для повышения доступности используйте элементы HTML, которые по своей сути являются интерактивными, вместо того чтобы добавлять слушатель событий к неинтерактивному элементу. В данном случае вместо добавления события к элементу `<li>` используется интерактивный элемент `<button>`.

    Подробнее о доступности см. в [Accessibility in Angular](accessibility.md).

### Стиль героев {#styles}

Список героев должен быть привлекательным и визуально реагировать, когда пользователи наводят курсор и выбирают героя из списка.

В [первом уроке](toh-pt0.md#app-wide-styles) вы задали основные стили для всего приложения в `styles.css`. Эта таблица стилей не включала стили для этого списка героев.

Вы можете добавить больше стилей в `styles.css` и продолжать расширять эту таблицу стилей по мере добавления компонентов.

Вместо этого вы можете определить частные стили для конкретного компонента. В этом случае все, что нужно компоненту, например, код, HTML и CSS, будет собрано в одном месте.

Такой подход облегчает повторное использование компонента в других местах и обеспечивает нужный внешний вид компонента, даже если глобальные стили отличаются.

Вы определяете частные стили либо в строке в массиве `@Component.styles`, либо в виде файлов таблиц стилей, определенных в массиве `@Component.styleUrls`.

Когда `ng generate` создал `HeroesComponent`, он создал пустую таблицу стилей `heroes.component.css` для `HeroesComponent` и указал на нее в `@Component.styleUrls` следующим образом.

```ts
@Component({
  selector: 'app-heroes',
  templateUrl: './heroes.component.html',
  styleUrls: ['./heroes.component.css']
})
```

Откройте файл `heroes.component.css` и вставьте частные CSS стили для `HeroesComponent` из [финального обзора кода](#final-code-review).

!!!warning ""

    Стили и таблицы стилей, определенные в метаданных `@Component`, привязаны к конкретному компоненту. Стили `heroes.component.css` применяются только к `HeroesComponent` и не влияют на внешний HTML или HTML в любом другом компоненте.

## Просмотр подробностей

Когда пользователь щелкает на герое в списке, компонент должен отображать информацию о выбранном герое в нижней части страницы.

Код, приведенный в этом разделе, прослушивает событие щелчка по элементу героя и отображает/обновляет информацию о нем.

### Добавьте привязку к событию щелчка мыши

Добавьте привязку события щелчка к `<button>` в `<li>` следующим образом:

```html
<li *ngFor="let hero of heroes">
    <button type="button" (click)="onSelect(hero)">
        <!-- ... -->
    </button>
</li>
```

Это пример синтаксиса Angular [event binding](event-binding.md).

Круглые скобки вокруг `click` указывают Angular на необходимость прослушивания события `click` элемента `<button>`. Когда пользователь щелкает на элементе `<button>`, Angular выполняет выражение `onSelect(hero)`.

В следующем разделе определим метод `onSelect()` в `HeroesComponent` для отображения героя, который был определен в выражении `*ngFor`.

### Добавьте обработчик события щелчка мыши

Переименуйте свойство `hero` компонента в `selectedHero`, но не присваивайте ему никакого значения, поскольку при запуске приложения не существует _выбранного героя_.

Добавьте следующий метод `onSelect()`, который присваивает щелкнутому герою из шаблона значение `selectedHero` компонента.

```ts
selectedHero?: Hero;
onSelect(hero: Hero): void {
  this.selectedHero = hero;
}
```

### Добавьте раздел подробностей

В настоящее время у вас есть список в шаблоне компонента. Чтобы показать подробную информацию о герое, когда вы нажимаете на его имя в списке, добавьте секцию

в шаблон, который отображает подробную информацию о герое.

Добавьте следующее в `heroes.component.html` под секцией списка:

```html
<div *ngIf="selectedHero">
    <h2>{{selectedHero.name | uppercase}} Details</h2>
    <div>id: {{selectedHero.id}}</div>
    <div>
        <label for="hero-name">Hero name: </label>
        <input
            id="hero-name"
            [(ngModel)]="selectedHero.name"
            placeholder="name"
        />
    </div>
</div>
```

Информация о герое должна отображаться только в том случае, если герой выбран. Когда компонент создается изначально, выбранного героя нет. Добавьте директиву `*ngIf` в `<div>`, который оборачивает детали героя. Эта директива указывает Angular на то, что секция должна отображаться только в том случае, если определено `selectedHero` после того, как герой был выбран щелчком на нем.

!!!note ""

    Не забывайте о символе звездочки `*` перед `ngIf`. Это критически важная часть синтаксиса.

### Стиль выбранного героя

Для идентификации выбранного героя можно использовать CSS-класс `.selected` в стилях, добавленных ранее. Чтобы применить класс `.selected` к элементу `<li>`, когда пользователь щелкнет на нем, используйте привязку класса.

![Selected hero with dark background and light text that differentiates it from unselected list items](heroes-list-selected.png)

С помощью [class binding](class-binding.md) в Angular можно условно добавлять и удалять CSS-класс. Добавьте `[class.some-css-class]="some-condition"` к элементу, который вы хотите стилизовать.

Добавьте следующую привязку `[class.selected]` к элементу `<button>` в шаблоне `HeroesComponent`:

```html
[class.selected]="hero === selectedHero"
```

Если герой текущей строки совпадает с `selectedHero`, Angular добавляет CSS-класс `selected`. Когда оба героя разные, Angular удаляет класс.

Готовый `<li>` выглядит следующим образом:

```html
<li *ngFor="let hero of heroes">
    <button
        [class.selected]="hero === selectedHero"
        type="button"
        (click)="onSelect(hero)"
    >
        <span class="badge">{{hero.id}}</span>
        <span class="name">{{hero.name}}</span>
    </button>
</li>
```

## Окончательный обзор кода {#final-code-review}

Здесь находятся файлы кода, обсуждаемые на этой странице, включая стили `HeroesComponent`.

=== "src/app/mock-heroes.ts"

    ```ts
    import { Hero } from './hero';

    export const HEROES: Hero[] = [
    	{ id: 12, name: 'Dr. Nice' },
    	{ id: 13, name: 'Bombasto' },
    	{ id: 14, name: 'Celeritas' },
    	{ id: 15, name: 'Magneta' },
    	{ id: 16, name: 'RubberMan' },
    	{ id: 17, name: 'Dynama' },
    	{ id: 18, name: 'Dr. IQ' },
    	{ id: 19, name: 'Magma' },
    	{ id: 20, name: 'Tornado' },
    ];
    ```

=== "src/app/heroes/heroes.component.ts"

    ```ts
    import { Component } from '@angular/core';
    import { Hero } from '../hero';
    import { HEROES } from '../mock-heroes';

    @Component({
    	selector: 'app-heroes',
    	templateUrl: './heroes.component.html',
    	styleUrls: ['./heroes.component.css'],
    })
    export class HeroesComponent {
    	heroes = HEROES;
    	selectedHero?: Hero;

    	onSelect(hero: Hero): void {
    		this.selectedHero = hero;
    	}
    }
    ```

=== "src/app/heroes/heroes.component.html"

    ```html
    <h2>My Heroes</h2>
    <ul class="heroes">
    	<li *ngFor="let hero of heroes">
    		<button
    			[class.selected]="hero === selectedHero"
    			type="button"
    			(click)="onSelect(hero)"
    		>
    			<span class="badge">{{hero.id}}</span>
    			<span class="name">{{hero.name}}</span>
    		</button>
    	</li>
    </ul>

    <div *ngIf="selectedHero">
    	<h2>{{selectedHero.name | uppercase}} Details</h2>
    	<div>id: {{selectedHero.id}}</div>
    	<div>
    		<label for="hero-name">Hero name: </label>
    		<input
    			id="hero-name"
    			[(ngModel)]="selectedHero.name"
    			placeholder="name"
    		/>
    	</div>
    </div>
    ```

=== "src/app/heroes/heroes.component.css"

    ```css
    /* HeroesComponent's private CSS styles */
    .heroes {
    	margin: 0 0 2em 0;
    	list-style-type: none;
    	padding: 0;
    	width: 15em;
    }

    .heroes li {
    	display: flex;
    }

    .heroes button {
    	flex: 1;
    	cursor: pointer;
    	position: relative;
    	left: 0;
    	background-color: #eee;
    	margin: 0.5em;
    	padding: 0;
    	border-radius: 4px;
    	display: flex;
    	align-items: stretch;
    	height: 1.8em;
    }

    .heroes button:hover {
    	color: #2c3a41;
    	background-color: #e6e6e6;
    	left: 0.1em;
    }

    .heroes button:active {
    	background-color: #525252;
    	color: #fafafa;
    }

    .heroes button.selected {
    	background-color: black;
    	color: white;
    }

    .heroes button.selected:hover {
    	background-color: #505050;
    	color: white;
    }

    .heroes button.selected:active {
    	background-color: black;
    	color: white;
    }

    .heroes .badge {
    	display: inline-block;
    	font-size: small;
    	color: white;
    	padding: 0.8em 0.7em 0 0.7em;
    	background-color: #405061;
    	line-height: 1em;
    	margin-right: 0.8em;
    	border-radius: 4px 0 0 4px;
    }

    .heroes .name {
    	align-self: center;
    }
    ```

## Резюме

-   Приложение Tour of Heroes отображает список героев с подробным представлением.
-   Пользователь может выбрать героя и просмотреть его подробную информацию.
-   Вы использовали `*ngFor` для отображения списка.
-   Вы использовали `*ngIf` для условного включения или исключения блока HTML.
-   Вы можете переключить класс стиля CSS с помощью привязки `class`.

## Ссылки

-   [Display a selection list](https://angular.io/tutorial/tour-of-heroes/toh-pt2)
