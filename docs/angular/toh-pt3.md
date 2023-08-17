---
description: На данный момент компонент HeroesComponent отображает как список героев, так и подробную информацию о выбранном герое
---

# Создайте компонент характеристик

На данный момент компонент `HeroesComponent` отображает как список героев, так и подробную информацию о выбранном герое.

Держать все функции в одном компоненте по мере роста приложения будет невозможно. В этом руководстве крупные компоненты разбиваются на более мелкие подкомпоненты, каждый из которых ориентирован на выполнение определенной задачи или рабочего процесса.

Первым шагом будет перемещение деталей героя в отдельный, многократно используемый `HeroDetailComponent`, и в итоге мы получим:

-   `HeroesComponent`, который представляет список героев.
-   Компонент `HeroDetailComponent`, который представляет детали выбранного героя.

!!!note ""

    Пример приложения, которое описывается на этой странице, см.:

    -   [Живой пример](https://angular.io/generated/live-examples/toh-pt3/stackblitz.html)
    -   [Скачать](https://angular.io/generated/zips/toh-pt3/toh-pt3.zip)

## Создайте компонент `HeroDetailComponent`

Используйте эту команду `ng generate` для создания нового компонента с именем `hero-detail`.

```shell
ng generate component hero-detail
```

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

```html
<div *ngIf="hero">
    <h2>{{hero.name | uppercase}} Details</h2>
    <div><span>id: </span>{{hero.id}}</div>
    <div>
        <label for="hero-name">Hero name: </label>
        <input
            id="hero-name"
            [(ngModel)]="hero.name"
            placeholder="name"
        />
    </div>
</div>
```

### Добавьте свойство `@Input()` героя

Шаблон `HeroDetailComponent` привязывается к свойству `hero` компонента, которое имеет тип `Hero`.

Откройте файл класса `HeroDetailComponent` и импортируйте символ `Hero`.

```ts
import { Hero } from '../hero';
```

Свойство `hero` [должно быть свойством `Input`](inputs-outputs.md 'Свойства ввода и вывода'), аннотированным с помощью декоратора `@Input()`, поскольку _внешний_ `HeroesComponent` [привязывается к нему](#heroes-component-template) следующим образом.

```html
<app-hero-detail [hero]="selectedHero"></app-hero-detail>
```

Измените оператор импорта `@angular/core`, чтобы включить символ `Input`.

```ts
import { Component, Input } from '@angular/core';
```

Добавьте свойство `hero`, которому предшествует декоратор `@Input()`.

```ts
@Input() hero?: Hero;
```

Это единственное изменение, которое вы должны внести в класс `HeroDetailComponent`. Больше нет никаких свойств. Нет никакой логики представления.

Этот компонент только получает объект героя через свойство `hero` и отображает его.

## Показать `HeroDetailComponent`

Компонент `HeroesComponent` использовался для самостоятельного отображения деталей героя, до того как вы удалили эту часть шаблона. Этот раздел поможет вам делегировать логику компоненту `HeroDetailComponent`.

Эти два компонента находятся в отношениях родитель/потомок. Родительский компонент, `HeroesComponent`, управляет дочерним компонентом `HeroDetailComponent` путем

посылая ему нового героя для отображения всякий раз, когда пользователь выбирает героя из списка.

Вам не нужно изменять _класс_ `HeroesComponent`, вместо этого измените его _шаблон_.

### Обновите шаблон `HeroesComponent` {#heroes-component-template}

Селектором `HeroDetailComponent` является `'app-hero-detail'`. Добавьте элемент `<app-hero-detail>` в нижней части шаблона `HeroesComponent`, там, где раньше находилось детальное представление героя.

Привяжите `HeroesComponent.selectedHero` к свойству `hero` элемента следующим образом.

```html
<app-hero-detail [hero]="selectedHero"></app-hero-detail>
```

`[hero]="selectedHero"` - это привязка [свойства](property-binding.md) Angular.

Это _односторонняя_ привязка данных от свойства `selectedHero` компонента `HeroesComponent` к свойству `hero` целевого элемента, которое отображается на свойство `hero` компонента `HeroDetailComponent`.

Теперь, когда пользователь нажимает на героя в списке, `selectedHero` изменяется. Когда `selectedHero` изменяется, _привязка свойств_ обновляет `hero` и

компонент `HeroDetailComponent` отображает нового героя.

Переработанный шаблон `HeroesComponent` должен выглядеть следующим образом:

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

<app-hero-detail [hero]="selectedHero"></app-hero-detail>
```

Браузер обновляется, и приложение начинает работать, как и раньше.

## Что изменилось?

Как и [ранее](toh-pt2.md), когда пользователь нажимает на имя героя, подробная информация о герое появляется под списком героев.

Теперь `HeroDetailComponent` представляет эти детали вместо `HeroesComponent`.

Рефакторинг оригинального `HeroesComponent` на два компонента дает преимущества, как сейчас, так и в будущем:

1.  Вы сократили обязанности `HeroesComponent`.
2.  Вы можете развивать `HeroDetailComponent` в богатый редактор героев не трогая родительский `HeroesComponent`.
3.  Вы можете развивать `HeroesComponent`, не трогая детальное представление героя.
4.  Вы можете повторно использовать `HeroDetailComponent` в шаблоне будущего компонента.

## Окончательный обзор кода

Вот файлы кода, рассмотренные на этой странице.

=== "src/app/hero-detail/hero-detail.component.ts"

    ```ts
    import { Component, Input } from '@angular/core';
    import { Hero } from '../hero';

    @Component({
    	selector: 'app-hero-detail',
    	templateUrl: './hero-detail.component.html',
    	styleUrls: ['./hero-detail.component.css'],
    })
    export class HeroDetailComponent {
    	@Input() hero?: Hero;
    }
    ```

=== "src/app/hero-detail/hero-detail.component.html"

    ```html
    <div *ngIf="hero">
    	<h2>{{hero.name | uppercase}} Details</h2>
    	<div><span>id: </span>{{hero.id}}</div>
    	<div>
    		<label for="hero-name">Hero name: </label>
    		<input
    			id="hero-name"
    			[(ngModel)]="hero.name"
    			placeholder="name"
    		/>
    	</div>
    </div>
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

    <app-hero-detail [hero]="selectedHero"></app-hero-detail>
    ```

=== "src/app/app.module.ts"

    ```ts
    import { BrowserModule } from '@angular/platform-browser';
    import { NgModule } from '@angular/core';
    import { FormsModule } from '@angular/forms';

    import { AppComponent } from './app.component';
    import { HeroesComponent } from './heroes/heroes.component';
    import { HeroDetailComponent } from './hero-detail/hero-detail.component';

    @NgModule({
    	declarations: [
    		AppComponent,
    		HeroesComponent,
    		HeroDetailComponent,
    	],
    	imports: [BrowserModule, FormsModule],
    	providers: [],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

## Резюме

-   Вы создали отдельный, многократно используемый `HeroDetailComponent`.
-   Вы использовали [связывание свойств](property-binding.md), чтобы дать родительскому `HeroesComponent` контроль над дочерним `HeroDetailComponent`.
-   Вы использовали декоратор [`@Input`](inputs-outputs.md)

чтобы сделать свойство `hero` доступным для привязки внешним `HeroesComponent`.

## Ссылки

-   [Create a feature component](https://angular.io/tutorial/tour-of-heroes/toh-pt3)
