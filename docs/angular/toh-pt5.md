---
description: Добавьте навигацию с маршрутизацией
---

# Добавьте навигацию с маршрутизацией

:date: 28.02.2022

Приложение Tour of Heroes имеет новые требования:

-   Добавить представление _Приборная доска_.
-   Добавить возможность навигации между представлениями _Герои_ и _Панель_.
-   Когда пользователи нажимают на имя героя в любом из представлений, переходят к детальному представлению выбранного героя.
-   Когда пользователи нажимают на _глубокую ссылку_ в электронном письме, открывается детальное представление для конкретного героя.

!!!note ""

    Пример приложения, которое описывается на этой странице, см.:

    -   [Живой пример](https://angular.io/generated/live-examples/toh-pt5/stackblitz.html)
    -   [Скачать](https://angular.io/generated/zips/toh-pt5/toh-pt5.zip)

Когда вы закончите, пользователи смогут перемещаться по приложению следующим образом:

![View navigations](nav-diagram.png)

## Добавьте модуль `AppRoutingModule`

В Angular лучшей практикой является загрузка и настройка маршрутизатора в отдельном модуле верхнего уровня. Маршрутизатор предназначен для маршрутизации и импортируется корневым `AppModule`.

По соглашению, имя класса модуля - `AppRoutingModule`, и он находится в `app-routing.module.ts` в директории `src/app`.

Запустите `ng generate` для создания модуля маршрутизации приложения.

```shell
ng generate module app-routing --flat --module=app
```

| Параметр       | Детали                                                                                 |
| :------------- | :------------------------------------------------------------------------------------- |
| `--flat`       | Помещает файл в `src/app` вместо его собственного каталога.                            |
| `--module=app` | Приказывает `ng generate` зарегистрировать его в массиве `imports` модуля `AppModule`. |

Файл, который создает `ng generate`, выглядит следующим образом:

```ts
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@NgModule({
    imports: [CommonModule],
    declarations: [],
})
export class AppRoutingModule {}
```

Замените его на следующий:

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HeroesComponent } from './heroes/heroes.component';

const routes: Routes = [
    { path: 'heroes', component: HeroesComponent },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule],
})
export class AppRoutingModule {}
```

Во-первых, файл `app-routing.module.ts` импортирует `RouterModule` и `Routes`, чтобы приложение могло иметь возможность маршрутизации. Следующий импорт, `HeroesComponent`, дает маршрутизатору место, куда он может перейти после настройки маршрутов.

Обратите внимание, что ссылки на `CommonModule` и массив `declarations` не нужны, поэтому они больше не являются частью `AppRoutingModule`. Следующие разделы объясняют остальную часть `AppRoutingModule` более подробно.

### Маршруты

В следующей части файла вы настраиваете маршруты. Маршруты указывают маршрутизатору, какой вид отображать, когда пользователь нажимает на ссылку или вставляет URL в адресную строку браузера.

Поскольку `app-routing.module.ts` уже импортирует `HeroesComponent`, вы можете использовать его в массиве `routes`:

```ts
const routes: Routes = [
    { path: 'heroes', component: HeroesComponent },
];
```

Типичный Angular `Route` имеет два свойства:

| Свойства    | Подробнее                                                                      |
| :---------- | :----------------------------------------------------------------------------- |
| `path`      | Строка, которая соответствует URL в адресной строке браузера.                  |
| `component` | Компонент, который маршрутизатор должен создать при переходе к этому маршруту. |

Это указывает маршрутизатору сопоставить URL с `path: 'heroes'` и отобразить `HeroesComponent`, когда URL будет таким, как `localhost:4200/heroes`.

### `RouterModule.forRoot()`

Метаданные `@NgModule` инициализируют маршрутизатор и запускают его прослушивание изменений местоположения браузера.

Следующая строка добавляет `RouterModule` в массив `imports` модуля `AppRoutingModule` и конфигурирует его с `routes` за один шаг, вызывая `RouterModule.forRoot()`:

```ts
imports: [ RouterModule.forRoot(routes) ],
```

!!!note ""

    Метод называется `forRoot()`, потому что вы настраиваете маршрутизатор на корневом уровне приложения. Метод `forRoot()` предоставляет поставщиков услуг и директивы, необходимые для маршрутизации, и выполняет начальную навигацию на основе текущего URL браузера.

Далее, `AppRoutingModule` экспортирует `RouterModule`, чтобы он был доступен во всем приложении.

```ts
exports: [RouterModule];
```

## Добавьте `RouterOutlet`

Откройте шаблон `AppComponent` и замените элемент `<app-heroes>` на элемент `<router-outlet>`.

```html
<h1>{{title}}</h1>
<router-outlet></router-outlet>
<app-messages></app-messages>
```

Шаблон `AppComponent` больше не нуждается в `<app-heroes>`, потому что приложение отображает `HeroesComponent` только тогда, когда пользователь переходит к нему.

Шаблон `<router-outlet>` указывает маршрутизатору, где отображать маршрутизируемые представления.

!!!note ""

    `RouterOutlet` - это одна из директив маршрутизации, которая стала доступна для `AppComponent`, потому что `AppModule` импортирует `AppRoutingModule`, который экспортировал `RouterModule`. Команда `ng generate`, которую вы выполнили в начале этого руководства, добавила этот импорт из-за флага `--module=app`. Если вы не использовали команду `ng generate` для создания `app-routing.module.ts`, импортируйте `AppRoutingModule` в `app.module.ts` и добавьте его в массив `imports` `NgModule`.

### Попробуйте

Если вы еще не обслуживаете свое приложение, запустите `ng serve`, чтобы увидеть свое приложение в браузере.

Браузер должен обновиться и отобразить заголовок приложения, но не список героев.

Посмотрите на адресную строку браузера. URL заканчивается на `/`.

Маршрутный путь к `HeroesComponent` - `/heroes`.

Добавьте `/heroes` к URL в адресной строке браузера. Вы должны увидеть знакомое представление обзора/детализации героев.

Удалите `/heroes` из URL в адресной строке браузера. Браузер должен обновиться и отобразить заголовок приложения, но не список героев.

## Добавление навигационной ссылки с помощью `routerLink` {#routerlink}

В идеале пользователи должны иметь возможность нажать на ссылку для навигации, а не вставлять URL маршрута в адресную строку.

Добавьте элемент `<nav>` и внутри него элемент якоря, который при нажатии вызывает навигацию к `HeroesComponent`. Измененный шаблон `AppComponent` выглядит следующим образом:

```html
<h1>{{title}}</h1>
<nav>
    <a routerLink="/heroes">Heroes</a>
</nav>
<router-outlet></router-outlet>
<app-messages></app-messages>
```

Атрибут [`routerLink`](#routerlink) установлен в `"/heroes"`, строку, которую маршрутизатор сопоставляет с маршрутом к `HeroesComponent`. Атрибут `routerLink` является селектором для директивы [`RouterLink`](https://angular.io/api/router/RouterLink), которая превращает клики пользователя в навигацию по маршрутизатору.

Это еще одна из публичных директив в `RouterModule`.

Браузер обновляется и отображает заголовок приложения и ссылку на героев, но не список героев.

Щелкните по ссылке. Адресная строка обновляется до `/heroes`, и появляется список героев.

!!!note ""

    Чтобы эта и будущие навигационные ссылки выглядели лучше, добавьте частные CSS стили в `app.component.css`, как указано в [финальном обзоре кода](#appcomponent) ниже.

## Добавьте представление приборной панели

Маршрутизация имеет больше смысла, когда ваше приложение имеет более одного представления, однако приложение _Тур героев_ имеет только представление героев.

Чтобы добавить `DashboardComponent`, запустите `ng generate`, как показано здесь:

```shell
ng generate component dashboard
```

`ng generate` создает файлы для `DashboardComponent` и объявляет его в `AppModule`.

Замените содержимое по умолчанию в этих файлах, как показано здесь:

=== "src/app/dashboard/dashboard.component.html"

    ```html
    <h2>Top Heroes</h2>
    <div class="heroes-menu">
    	<a *ngFor="let hero of heroes"> {{hero.name}} </a>
    </div>
    ```

=== "src/app/dashboard/dashboard.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';
    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-dashboard',
    	templateUrl: './dashboard.component.html',
    	styleUrls: ['./dashboard.component.css'],
    })
    export class DashboardComponent implements OnInit {
    	heroes: Hero[] = [];

    	constructor(private heroService: HeroService) {}

    	ngOnInit(): void {
    		this.getHeroes();
    	}

    	getHeroes(): void {
    		this.heroService
    			.getHeroes()
    			.subscribe(
    				(heroes) =>
    					(this.heroes = heroes.slice(1, 5))
    			);
    	}
    }
    ```

=== "src/app/dashboard/dashboard.component.css"

    ```css
    /* DashboardComponent's private CSS styles */

    h2 {
    	text-align: center;
    }

    .heroes-menu {
    	padding: 0;
    	margin: auto;
    	max-width: 1000px;

    	/* flexbox */
    	display: flex;
    	flex-direction: row;
    	flex-wrap: wrap;
    	justify-content: space-around;
    	align-content: flex-start;
    	align-items: flex-start;
    }

    a {
    	background-color: #3f525c;
    	border-radius: 2px;
    	padding: 1rem;
    	font-size: 1.2rem;
    	text-decoration: none;
    	display: inline-block;
    	color: #fff;
    	text-align: center;
    	width: 100%;
    	min-width: 70px;
    	margin: 0.5rem auto;
    	box-sizing: border-box;

    	/* flexbox */
    	order: 0;
    	flex: 0 1 auto;
    	align-self: auto;
    }

    @media (min-width: 600px) {
    	a {
    		width: 18%;
    		box-sizing: content-box;
    	}
    }

    a:hover {
    	background-color: #000;
    }
    ```

Шаблон _template_ представляет сетку ссылок на имена героев.

-   Повторитель `*ngFor` создает столько ссылок, сколько находится в массиве `heroes` компонента.
-   Ссылки оформляются как цветные блоки в `dashboard.component.css`.
-   Ссылки пока никуда не ведут.

Класс _class_ похож на класс `HeroesComponent`.

-   Он определяет свойство массива `heroes`.
-   Конструктор ожидает, что Angular внедрит `HeroService` в приватное свойство `heroService`.
-   Хук жизненного цикла `ngOnInit()` вызывает `getHeroes()`.

Эта `getHeroes()` возвращает нарезанный список героев на позициях 1 и 5, возвращая только героев два, три, четыре и пять.

```ts
getHeroes(): void {
  this.heroService.getHeroes()
    .subscribe(heroes => this.heroes = heroes.slice(1, 5));
}
```

### Добавьте маршрут к приборной панели

Чтобы перейти к приборной панели, маршрутизатору нужен соответствующий маршрут.

Импортируйте `DashboardComponent` в файл `app-routing.module.ts`.

```ts
import { DashboardComponent } from './dashboard/dashboard.component';
```

Добавьте маршрут в массив `routes`, который соответствует пути к `DashboardComponent`.

```ts
{ path: 'dashboard', component: DashboardComponent },
```

### Добавьте маршрут по умолчанию

Когда приложение запускается, адресная строка браузера указывает на корень сайта. Это не совпадает ни с одним существующим маршрутом, поэтому маршрутизатор никуда не переходит.

Пространство под `<router-outlet>` пустует.

Чтобы приложение автоматически переходило на приборную панель, добавьте следующий маршрут в массив `routes`.

```ts
{ path: '', redirectTo: '/dashboard', pathMatch: 'full' },
```

Этот маршрут перенаправляет URL, полностью соответствующий пустому пути, на маршрут, путь которого `'/dashboard'`.

После обновления браузера маршрутизатор загружает `DashboardComponent` и в адресной строке браузера отображается URL `/dashboard`.

### Добавление ссылки на приборную панель в оболочку

Пользователь должен иметь возможность перемещаться между `DashboardComponent` и `HeroesComponent`, нажимая на ссылки в области навигации в верхней части страницы.

Добавьте навигационную ссылку на приборную панель в шаблон оболочки `AppComponent`, чуть выше ссылки _Heroes_.

```html
<h1>{{title}}</h1>
<nav>
    <a routerLink="/dashboard">Dashboard</a>
    <a routerLink="/heroes">Heroes</a>
</nav>
<router-outlet></router-outlet>
<app-messages></app-messages>
```

После обновления браузера вы можете свободно перемещаться между двумя представлениями, щелкая по ссылкам.

## Переход к деталям героя {#hero-details}

Компонент `HeroDetailComponent` отображает подробную информацию о выбранном герое. В настоящее время компонент `HeroDetailComponent` виден только в нижней части компонента `HeroesComponent`.

Пользователь должен иметь возможность получить доступ к этим деталям тремя способами.

1.  Нажав на героя в приборной панели.
2.  Щелкнув героя в списке героев.
3.  Вставляя URL "глубокой ссылки" в адресную строку браузера, который идентифицирует героя для отображения.

Этот раздел позволяет перейти к компоненту `HeroDetailComponent` и освободить его от компонента `HeroesComponent`.

### Удалить _детали героя_ из `HeroesComponent`

Когда пользователь нажимает на героя в `HeroesComponent`, приложение должно перейти к `HeroDetailComponent`, заменив представление списка героев на представление подробностей о герое. Представление списка героев больше не должно показывать детали героя, как это происходит сейчас.

Откройте файл `heroes/heroes.component.html` и удалите элемент `<app-hero-detail>` снизу.

Щелчок по элементу героя теперь ничего не делает. Вы можете исправить это после того, как включите маршрутизацию к `HeroDetailComponent`.

### Добавьте маршрут _геройской детализации_

URL типа `~/detail/11` будет хорошим URL для перехода к представлению _Hero Detail_ героя, чей `id` равен `11`.

Откройте `app-routing.module.ts` и импортируйте `HeroDetailComponent`.

```ts
import { HeroDetailComponent } from './hero-detail/hero-detail.component';
```

Затем добавьте _параметризованный_ маршрут в массив `routes`, который соответствует шаблону пути к представлению _геройская деталь_.

```ts
{ path: 'detail/:id', component: HeroDetailComponent },
```

Символ двоеточия `:` в `пути` указывает на то, что `:id` является заполнителем для конкретного героя `id`.

На данном этапе все маршруты приложения уже созданы.

```ts
const routes: Routes = [
    {
        path: '',
        redirectTo: '/dashboard',
        pathMatch: 'full',
    },
    { path: 'dashboard', component: DashboardComponent },
    { path: 'detail/:id', component: HeroDetailComponent },
    { path: 'heroes', component: HeroesComponent },
];
```

### `DashboardComponent` ссылки на героев

Ссылки героев `DashboardComponent` на данный момент ничего не делают.

Теперь, когда маршрутизатор имеет маршрут к `HeroDetailComponent`, исправьте ссылки героев приборной панели для навигации с помощью _параметризированного_ маршрута приборной панели.

```html
<a
    *ngFor="let hero of heroes"
    routerLink="/detail/{{hero.id}}"
>
    {{hero.name}}
</a>
```

Вы используете Angular [interpolation binding](interpolation.md) внутри повторителя `*ngFor` для вставки `hero.id` текущей итерации в каждый [`routerLink`](#routerlink).

### `HeroesComponent` ссылки на героев {#heroes-component-links}

Элементы-герои в `HeroesComponent` представляют собой `<li>` элементы, события нажатия на которые привязаны к методу `onSelect()` компонента.

```html
<ul class="heroes">
    <li *ngFor="let hero of heroes">
        <button
            type="button"
            (click)="onSelect(hero)"
            [class.selected]="hero === selectedHero"
        >
            <span class="badge">{{hero.id}}</span>
            <span class="name">{{hero.name}}</span>
        </button>
    </li>
</ul>
```

Удалите внутренний HTML из `<li>`. Оберните значок и имя в якорный элемент `<a>`.

Добавьте к якорю атрибут `routerLink`, такой же, как в шаблоне приборной панели.

```html
<ul class="heroes">
    <li *ngFor="let hero of heroes">
        <a routerLink="/detail/{{hero.id}}">
            <span class="badge">{{hero.id}}</span>
            {{hero.name}}
        </a>
    </li>
</ul>
```

Обязательно исправьте частную таблицу стилей в `heroes.component.css`, чтобы список выглядел как раньше. Исправленные стили находятся в [финальном обзоре кода](#heroescomponent) внизу этого руководства.

#### Удаление мертвого кода - необязательно

Хотя класс `HeroesComponent` все еще работает, метод `onSelect()` и свойство `selectedHero` больше не используются.

Неплохо привести все в порядок для вашего будущего. Вот класс после обрезки мертвого кода.

```ts
export class HeroesComponent implements OnInit {
    heroes: Hero[] = [];

    constructor(private heroService: HeroService) {}

    ngOnInit(): void {
        this.getHeroes();
    }

    getHeroes(): void {
        this.heroService
            .getHeroes()
            .subscribe((heroes) => (this.heroes = heroes));
    }
}
```

## Маршрутизируемый `HeroDetailComponent`

Родительский `HeroesComponent` использовался для установки свойства `HeroDetailComponent.hero` и `HeroDetailComponent` отображал героя.

Теперь `HeroesComponent` этого не делает. Теперь маршрутизатор создает `HeroDetailComponent` в ответ на URL, такой как `~/detail/12`.

Компоненту `HeroDetailComponent` нужен новый способ заставить героя отображаться. В этом разделе объясняется следующее:

-   Получить маршрут, который его создал
-   Извлечь `id` из маршрута
-   Получите героя с этим `id` с сервера, используя `HeroService`.

Добавьте следующие импорты:

```ts
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { HeroService } from '../hero.service';
```

Вставьте в конструктор сервисы `ActivatedRoute`, `HeroService` и `Location`, сохранив их значения в приватных полях:

```ts
constructor(
  private route: ActivatedRoute,
  private heroService: HeroService,
  private location: Location
) {}
```

В [`ActivatedRoute`](https://angular.io/api/router/ActivatedRoute) хранится информация о маршруте к данному экземпляру `HeroDetailComponent`. Этот компонент интересуют параметры маршрута, извлеченные из URL.

Параметр "id" - это `id` героя для отображения.

Сервис [`HeroService`](toh-pt4.md) получает данные о героях с удаленного сервера, и этот компонент использует их для получения героя для отображения.

[`location`](https://angular.io/api/common/Location) - это сервис Angular для взаимодействия с браузером. Этот сервис позволяет вам вернуться к предыдущему представлению.

### Извлечение параметра маршрута `id`

В `ngOnInit()` [lifecycle hook](lifecycle-hooks.md#oninit) вызовите `getHero()` и определите его следующим образом.

```ts
ngOnInit(): void {
  this.getHero();
}

getHero(): void {
  const id = Number(this.route.snapshot.paramMap.get('id'));
  this.heroService.getHero(id)
    .subscribe(hero => this.hero = hero);
}
```

Снимок `route.snapshot` - это статическое изображение информации о маршруте сразу после создания компонента.

`paramMap` - это словарь значений параметров маршрута, извлеченных из URL. Ключ `"id"` возвращает `id` героя для выборки.

Параметры маршрута всегда являются строками. Функция JavaScript `Number` преобразует строку в число, которым и должен быть `id` героя.

Браузер обновляется, и приложение падает с ошибкой компилятора. У `HeroService` нет метода `getHero()`.

Добавьте его сейчас.

### Добавьте `HeroService.getHero()`

Откройте `HeroService` и добавьте следующий метод `getHero()` с `id` после метода `getHeroes()`:

```ts
getHero(id: number): Observable<Hero> {
  // For now, assume that a hero with the specified `id` always exists.
  // Error handling will be added in the next step of the tutorial.
  const hero = HEROES.find(h => h.id === id)!;
  this.messageService.add(`HeroService: fetched hero id=${id}`);
  return of(hero);
}
```

!!!warning ""

    Символы backtick ( <code>&grave;</code> ) определяют JavaScript [template literal](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals) для встраивания `id`.

Как и [`getHeroes()`](toh-pt4.md#observable-heroservice), `getHero()` имеет асинхронную сигнатуру. Она возвращает _макет героя_ как `Observable`, используя функцию RxJS `of()`.

Вы можете переписать `getHero()` как настоящий `Http` запрос без необходимости изменять `HeroDetailComponent`, который его вызывает.

### Попробуйте

Браузер обновляется, и приложение снова работает. Вы можете щелкнуть героя на приборной панели или в списке героев и перейти к детальному представлению этого героя.

Если вы введете `localhost:4200/detail/12` в адресную строку браузера, маршрутизатор перейдет к детальному представлению для героя с `id: 12`, **Dr Nice**.

### Найти дорогу назад {#goback}

Нажав кнопку "Назад" в браузере, вы можете вернуться на предыдущую страницу. Это может быть список героев или представление приборной панели, в зависимости от того, что отправило вас к детальному представлению.

Было бы неплохо иметь кнопку на представлении `HeroDetail`, которая могла бы это сделать.

Добавьте кнопку _go back_ в нижнюю часть шаблона компонента и привяжите ее к методу компонента `goBack()`.

```html
<button type="button" (click)="goBack()">go back</button>
```

Добавьте метод `goBack()` в класс компонента, который перемещается на один шаг назад в стеке истории браузера, используя службу `Location`, которую вы [использовали для инъекции](#hero-detail-ctor).

```ts
goBack(): void {
  this.location.back();
}
```

Обновите браузер и начните кликать. Теперь пользователи могут перемещаться по приложению с помощью новых кнопок.

Детали выглядят лучше, если добавить частные CSS стили в `hero-detail.component.css`, как указано в одной из вкладок ["final code review"](#final-code-review) ниже.

## Окончательный обзор кода

Здесь представлены файлы кода, обсуждаемые на этой странице.

### `AppRoutingModule`, `AppModule` и `HeroService`

=== "src/app/app.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { FormsModule } from '@angular/forms';

    import { AppComponent } from './app.component';
    import { DashboardComponent } from './dashboard/dashboard.component';
    import { HeroDetailComponent } from './hero-detail/hero-detail.component';
    import { HeroesComponent } from './heroes/heroes.component';
    import { MessagesComponent } from './messages/messages.component';

    import { AppRoutingModule } from './app-routing.module';

    @NgModule({
    	imports: [BrowserModule, FormsModule, AppRoutingModule],
    	declarations: [
    		AppComponent,
    		DashboardComponent,
    		HeroesComponent,
    		HeroDetailComponent,
    		MessagesComponent,
    	],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "src/app/app-routing.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { RouterModule, Routes } from '@angular/router';

    import { DashboardComponent } from './dashboard/dashboard.component';
    import { HeroesComponent } from './heroes/heroes.component';
    import { HeroDetailComponent } from './hero-detail/hero-detail.component';

    const routes: Routes = [
    	{
    		path: '',
    		redirectTo: '/dashboard',
    		pathMatch: 'full',
    	},
    	{ path: 'dashboard', component: DashboardComponent },
    	{ path: 'detail/:id', component: HeroDetailComponent },
    	{ path: 'heroes', component: HeroesComponent },
    ];

    @NgModule({
    	imports: [RouterModule.forRoot(routes)],
    	exports: [RouterModule],
    })
    export class AppRoutingModule {}
    ```

=== "src/app/hero.service.ts"

    ```ts
    import { Injectable } from '@angular/core';

    import { Observable, of } from 'rxjs';

    import { Hero } from './hero';
    import { HEROES } from './mock-heroes';
    import { MessageService } from './message.service';

    @Injectable({ providedIn: 'root' })
    export class HeroService {
    	constructor(private messageService: MessageService) {}

    	getHeroes(): Observable<Hero[]> {
    		const heroes = of(HEROES);
    		this.messageService.add(
    			'HeroService: fetched heroes'
    		);
    		return heroes;
    	}

    	getHero(id: number): Observable<Hero> {
    		// For now, assume that a hero with the specified `id` always exists.
    		// Error handling will be added in the next step of the tutorial.
    		const hero = HEROES.find((h) => h.id === id)!;
    		this.messageService.add(
    			`HeroService: fetched hero id=${id}`
    		);
    		return of(hero);
    	}
    }
    ```

#### `AppComponent` {#appcomponent}

=== "src/app/app.component.html"

    ```html
    <h1>{{title}}</h1>
    <nav>
    	<a routerLink="/dashboard">Dashboard</a>
    	<a routerLink="/heroes">Heroes</a>
    </nav>
    <router-outlet></router-outlet>
    <app-messages></app-messages>
    ```

=== "src/app/app.component.ts"

    ```ts
    import { Component } from '@angular/core';

    @Component({
    	selector: 'app-root',
    	templateUrl: './app.component.html',
    	styleUrls: ['./app.component.css'],
    })
    export class AppComponent {
    	title = 'Tour of Heroes';
    }
    ```

=== "src/app/app.component.css"

    ```css
    /* AppComponent's private CSS styles */
    h1 {
    	margin-bottom: 0;
    }
    nav a {
    	padding: 1rem;
    	text-decoration: none;
    	margin-top: 10px;
    	display: inline-block;
    	background-color: #e8e8e8;
    	color: #3d3d3d;
    	border-radius: 4px;
    }

    nav a:hover {
    	color: white;
    	background-color: #42545c;
    }
    nav a:active {
    	background-color: black;
    }
    ```

#### `DashboardComponent` {#dashboardcomponent}

=== "src/app/dashboard/dashboard.component.html"

    ```html
    <h2>Top Heroes</h2>
    <div class="heroes-menu">
    	<a
    		*ngFor="let hero of heroes"
    		routerLink="/detail/{{hero.id}}"
    	>
    		{{hero.name}}
    	</a>
    </div>
    ```

=== "src/app/dashboard/dashboard.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';
    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-dashboard',
    	templateUrl: './dashboard.component.html',
    	styleUrls: ['./dashboard.component.css'],
    })
    export class DashboardComponent implements OnInit {
    	heroes: Hero[] = [];

    	constructor(private heroService: HeroService) {}

    	ngOnInit(): void {
    		this.getHeroes();
    	}

    	getHeroes(): void {
    		this.heroService
    			.getHeroes()
    			.subscribe(
    				(heroes) =>
    					(this.heroes = heroes.slice(1, 5))
    			);
    	}
    }
    ```

=== "src/app/dashboard/dashboard.component.css"

    ```css
    /* DashboardComponent's private CSS styles */

    h2 {
    	text-align: center;
    }

    .heroes-menu {
    	padding: 0;
    	margin: auto;
    	max-width: 1000px;

    	/* flexbox */
    	display: flex;
    	flex-direction: row;
    	flex-wrap: wrap;
    	justify-content: space-around;
    	align-content: flex-start;
    	align-items: flex-start;
    }

    a {
    	background-color: #3f525c;
    	border-radius: 2px;
    	padding: 1rem;
    	font-size: 1.2rem;
    	text-decoration: none;
    	display: inline-block;
    	color: #fff;
    	text-align: center;
    	width: 100%;
    	min-width: 70px;
    	margin: 0.5rem auto;
    	box-sizing: border-box;

    	/* flexbox */
    	order: 0;
    	flex: 0 1 auto;
    	align-self: auto;
    }

    @media (min-width: 600px) {
    	a {
    		width: 18%;
    		box-sizing: content-box;
    	}
    }

    a:hover {
    	background-color: #000;
    }
    ```

#### `HeroesComponent` {#heroescomponent}

=== "src/app/heroes/heroes.component.html"

    ```html
    <h2>My Heroes</h2>
    <ul class="heroes">
    	<li *ngFor="let hero of heroes">
    		<a routerLink="/detail/{{hero.id}}">
    			<span class="badge">{{hero.id}}</span>
    			{{hero.name}}
    		</a>
    	</li>
    </ul>
    ```

=== "src/app/heroes/heroes.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';

    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-heroes',
    	templateUrl: './heroes.component.html',
    	styleUrls: ['./heroes.component.css'],
    })
    export class HeroesComponent implements OnInit {
    	heroes: Hero[] = [];

    	constructor(private heroService: HeroService) {}

    	ngOnInit(): void {
    		this.getHeroes();
    	}

    	getHeroes(): void {
    		this.heroService
    			.getHeroes()
    			.subscribe((heroes) => (this.heroes = heroes));
    	}
    }
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
    	position: relative;
    	cursor: pointer;
    }

    .heroes li:hover {
    	left: 0.1em;
    }

    .heroes a {
    	color: #333;
    	text-decoration: none;
    	background-color: #eee;
    	margin: 0.5em;
    	padding: 0.3em 0;
    	height: 1.6em;
    	border-radius: 4px;
    	display: block;
    	width: 100%;
    }

    .heroes a:hover {
    	color: #2c3a41;
    	background-color: #e6e6e6;
    }

    .heroes a:active {
    	background-color: #525252;
    	color: #fafafa;
    }

    .heroes .badge {
    	display: inline-block;
    	font-size: small;
    	color: white;
    	padding: 0.8em 0.7em 0 0.7em;
    	background-color: #405061;
    	line-height: 1em;
    	position: relative;
    	left: -1px;
    	top: -4px;
    	height: 1.8em;
    	min-width: 16px;
    	text-align: right;
    	margin-right: 0.8em;
    	border-radius: 4px 0 0 4px;
    }
    ```

#### `HeroDetailComponent` {#herodetailcomponent}

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
    			placeholder="Hero name"
    		/>
    	</div>
    	<button type="button" (click)="goBack()">
    		go back
    	</button>
    </div>
    ```

=== "src/app/hero-detail/hero-detail.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';
    import { ActivatedRoute } from '@angular/router';
    import { Location } from '@angular/common';

    import { Hero } from '../hero';
    import { HeroService } from '../hero.service';

    @Component({
    	selector: 'app-hero-detail',
    	templateUrl: './hero-detail.component.html',
    	styleUrls: ['./hero-detail.component.css'],
    })
    export class HeroDetailComponent implements OnInit {
    	hero: Hero | undefined;

    	constructor(
    		private route: ActivatedRoute,
    		private heroService: HeroService,
    		private location: Location
    	) {}

    	ngOnInit(): void {
    		this.getHero();
    	}

    	getHero(): void {
    		const id = Number(
    			this.route.snapshot.paramMap.get('id')
    		);
    		this.heroService
    			.getHero(id)
    			.subscribe((hero) => (this.hero = hero));
    	}

    	goBack(): void {
    		this.location.back();
    	}
    }
    ```

=== "src/app/hero-detail/hero-detail.component.css"

    ```css
    /* HeroDetailComponent's private CSS styles */
    label {
    	color: #435960;
    	font-weight: bold;
    }
    input {
    	font-size: 1em;
    	padding: 0.5rem;
    }
    button {
    	margin-top: 20px;
    	background-color: #eee;
    	padding: 1rem;
    	border-radius: 4px;
    	font-size: 1rem;
    }
    button:hover {
    	background-color: #cfd8dc;
    }
    button:disabled {
    	background-color: #eee;
    	color: #ccc;
    	cursor: auto;
    }
    ```

## Резюме

-   Вы добавили маршрутизатор Angular для навигации между различными компонентами
-   Вы превратили `AppComponent` в навигационную оболочку со ссылками `<a>` и `<router-outlet>`.
-   Вы сконфигурировали маршрутизатор в модуле `AppRoutingModule`.
-   Определены маршруты, маршрут перенаправления и параметризованный маршрут
-   использована директива `routerLink` в элементах якоря
-   Рефакторинг тесно связанного представления main/detail в маршрутизируемое представление detail
-   использование параметров ссылки маршрутизатора для перехода к детальному представлению выбранного пользователем героя
-   Вы разделили `HeroService` с другими компонентами

## Ссылки

-   [Add navigation with routing](https://angular.io/tutorial/tour-of-heroes/toh-pt5)
