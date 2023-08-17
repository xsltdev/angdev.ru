---
description: Теперь у приложения есть базовый заголовок. Далее создайте новый компонент для отображения информации о герое и поместите этот компонент в оболочку приложения
---

# Редактор героев

:date: 28.02.2022

Теперь у приложения есть базовый заголовок. Далее создайте новый компонент для отображения информации о герое и поместите этот компонент в оболочку приложения.

!!!note ""

    Пример приложения, которое описывается на этой странице, см.:

    - [Живой пример](https://angular.io/generated/live-examples/toh-pt1/stackblitz.html)
    - [Скачать](https://angular.io/generated/zips/toh-pt1/toh-pt1.zip)

## Создание компонента heroes

Используйте `ng generate` для создания нового компонента с именем `heroes`.

```shell
ng generate component heroes
```

`ng generate` создает новый каталог `src/app/heroes/` и генерирует три файла `HeroesComponent` вместе с тестовым файлом.

Файл класса `HeroesComponent` выглядит следующим образом:

```ts
import { Component } from '@angular/core';

@Component({
    selector: 'app-heroes',
    templateUrl: './heroes.component.html',
    styleUrls: ['./heroes.component.css'],
})
export class HeroesComponent {}
```

Вы всегда импортируете символ `Component` из библиотеки ядра Angular и аннотируете класс компонента с помощью `@Component`.

`@Component` - это функция-декоратор, которая определяет метаданные Angular для компонента.

Функция `ng generate` создала три свойства метаданных:

| Properties    | Details                                     |
| :------------ | :------------------------------------------ |
| `selector`    | Селектор CSS элементов компонента.          |
| `templateUrl` | Расположение файла шаблона компонента.      |
| `styleUrls`   | Расположение частных стилей CSS компонента. |

Селектор [CSS элемента](https://developer.mozilla.org/docs/Web/CSS/Type_selectors), `'app-heroes'`, соответствует имени HTML элемента, который идентифицирует этот компонент в шаблоне родительского компонента.

Всегда `export` класс компонента, чтобы вы могли `import` его в другое место &hellip; например, в `AppModule`.

### Добавить свойство `hero`

Добавьте свойство `hero` в `HeroesComponent` для героя по имени `Windstorm`.

```ts
hero = 'Windstorm';
```

### Показать героя

Откройте файл шаблона `heroes.component.html`. Удалите текст по умолчанию, созданный `ng generate`, и замените его привязкой данных к новому свойству `hero`.

```html
<h2>{{hero}}</h2>
```

## Показать представление `HeroesComponent`

Чтобы отобразить `HeroesComponent`, вы должны добавить его в шаблон оболочки `AppComponent`.

Помните, что `app-heroes` является селектором элемента для `HeroesComponent`. Добавьте элемент `<app-heroes>` в файл шаблона `AppComponent`, чуть ниже заголовка.

```html
<h1>{{title}}</h1>
<app-heroes></app-heroes>
```

Если `ng serve` все еще запущен, браузер должен обновиться и отобразить заголовок приложения и имя героя.

## Создание интерфейса `Hero`

Настоящий герой - это больше, чем имя.

Создайте интерфейс `Hero` в собственном файле в каталоге `src/app`. Дайте ему свойства `id` и `name`.

```ts
export interface Hero {
    id: number;
    name: string;
}
```

Вернитесь к классу `HeroesComponent` и импортируйте интерфейс `Hero`.

Переделайте свойство `hero` компонента так, чтобы оно имело тип `Hero`. Инициализируйте его с `id` равным `1` и именем `Windstorm`.

Измененный файл класса `HeroesComponent` должен выглядеть следующим образом:

```ts
import { Component } from '@angular/core';
import { Hero } from '../hero';

@Component({
    selector: 'app-heroes',
    templateUrl: './heroes.component.html',
    styleUrls: ['./heroes.component.css'],
})
export class HeroesComponent {
    hero: Hero = {
        id: 1,
        name: 'Windstorm',
    };
}
```

Страница больше не отображается должным образом, потому что вы изменили героя со строки на объект.

## Показать объект героя

Обновите привязку в шаблоне, чтобы объявить имя героя и показать и `id`, и `name` в подробном отображении, как показано ниже:

```html
<h2>{{hero.name}} Details</h2>
<div><span>id: </span>{{hero.id}}</div>
<div><span>name: </span>{{hero.name}}</div>
```

Браузер обновляется и отображает информацию о герое.

## Форматирование с помощью `UppercasePipe`

Отредактируйте привязку `hero.name` следующим образом:

```html
<h2>{{hero.name | uppercase}} Details</h2>
```

Браузер обновляется, и теперь имя героя отображается заглавными буквами.

Слово `uppercase` в интерполяционной привязке после символа пайпа <code>&verbar;</code> активизирует встроенную функцию `UppercasePipe`.

[Пайпы](pipes.md) - это хороший способ форматирования строк, валютных сумм, дат и других отображаемых данных. В Angular поставляется несколько встроенных пайпов, и вы можете создать свой собственный.

## Редактирование героя

Пользователи должны иметь возможность редактировать имя героя в текстовом поле `<input>`.

Текстовое поле должно как _отображать_ свойство `name` героя, так и _обновлять_ его по мере ввода пользователем. Это означает, что данные поступают из класса компонента _на экран_ и с экрана _обратно в класс_.

Чтобы автоматизировать этот поток данных, установите двустороннюю привязку между элементом формы `<input>` и свойством `hero.name`.

### Двусторонняя связь

Переделайте область подробностей в шаблоне `HeroesComponent` так, чтобы она выглядела следующим образом:

```html
<div>
    <label for="name">Hero name: </label>
    <input
        id="name"
        [(ngModel)]="hero.name"
        placeholder="name"
    />
</div>
```

`[(ngModel)]` - это синтаксис двустороннего связывания данных Angular.

Здесь он связывает свойство `hero.name` с текстовым полем HTML, чтобы данные могли поступать _в обоих направлениях_. Данные могут поступать из свойства `hero.name` в текстовое поле и из текстового поля обратно в `hero.name`.

### Отсутствующий `FormsModule`

Обратите внимание, что приложение перестало работать, когда вы добавили `[(ngModel)]`.

Чтобы увидеть ошибку, откройте средства разработки браузера и найдите в консоли сообщение вида

```shell
Template parse errors:
Can't bind to 'ngModel' since it isn't a known property of 'input'.
```

Хотя `ngModel` является действительной директивой Angular, она не доступна по умолчанию.

Она относится к дополнительному модулю `FormsModule`, и вы должны _оптировать_ ее использование.

## `AppModule`

Angular необходимо знать, как части вашего приложения сочетаются друг с другом и какие другие файлы и библиотеки требуются приложению. Эта информация называется _метаданные_.

Часть метаданных находится в декораторах `@Component`, которые вы добавили в классы компонентов. Другие важные метаданные находятся в декораторах [`@NgModule`](ngmodules.md).

Самый важный декоратор `@NgModule` аннотирует класс верхнего уровня **AppModule**.

При создании проекта `ng new` создал класс `AppModule` в `src/app/app.module.ts`. Именно здесь вы _входите_ в `FormsModule`.

### Импортируйте `FormsModule`

Откройте `app.module.ts` и импортируйте символ `FormsModule` из библиотеки `@angular/forms`.

```ts
import { FormsModule } from '@angular/forms'; // <-- NgModel lives here
```

Добавьте `FormsModule` в массив `imports` в `@NgModule`. Массив `imports` содержит список внешних модулей, которые необходимы приложению.

```ts
imports: [
  BrowserModule,
  FormsModule
],
```

Когда браузер обновится, приложение должно снова работать. Вы можете отредактировать имя героя и увидеть изменения, отраженные сразу же в `<h2>` над текстовым полем.

### Объявление `HeroesComponent`

Каждый компонент должен быть объявлен в _только одном_ [NgModule](ngmodules.md).

Вы не объявили `HeroesComponent`. Почему приложение сработало?

Оно заработало, потому что `ng generate` объявил `HeroesComponent` в `AppModule`, когда создавал этот компонент.

Откройте `src/app/app.module.ts` и найдите импортированный `HeroesComponent` в самом верху.

```ts
import { HeroesComponent } from './heroes/heroes.component';
```

Компонент `HeroesComponent` объявлен в массиве `@NgModule.declarations`.

```ts
declarations: [
  AppComponent,
  HeroesComponent
],
```

!!!note ""

    `AppModule` объявляет оба компонента приложения, `AppComponent` и `HeroesComponent`.

## Окончательный обзор кода

Вот файлы кода, обсуждаемые на этой странице.

=== "src/app/heroes/heroes.component.ts"

```ts
import { Component } from '@angular/core';
import { Hero } from '../hero';

@Component({
    selector: 'app-heroes',
    templateUrl: './heroes.component.html',
    styleUrls: ['./heroes.component.css'],
})
export class HeroesComponent {
    hero: Hero = {
        id: 1,
        name: 'Windstorm',
    };
}
```

=== "src/app/heroes/heroes.component.html"

```html
<h2>{{hero.name | uppercase}} Details</h2>
<div><span>id: </span>{{hero.id}}</div>
<div>
    <label for="name">Hero name: </label>
    <input
        id="name"
        [(ngModel)]="hero.name"
        placeholder="name"
    />
</div>
```

=== "src/app/app.module.ts"

```ts
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'; // <-- NgModel lives here

import { AppComponent } from './app.component';
import { HeroesComponent } from './heroes/heroes.component';

@NgModule({
    declarations: [AppComponent, HeroesComponent],
    imports: [BrowserModule, FormsModule],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
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

=== "src/app/app.component.html"

```html
<h1>{{title}}</h1>
<app-heroes></app-heroes>
```

=== "src/app/hero.ts"

```ts
export interface Hero {
    id: number;
    name: string;
}
```

## Резюме

-   Вы использовали `ng generate` для создания второго `HeroesComponent`.
-   Вы отобразили `HeroesComponent`, добавив его в оболочку `AppComponent`.
-   Вы применили `UppercasePipe` для форматирования имени.
-   Вы использовали двустороннее связывание данных с помощью директивы `ngModel`.
-   Вы узнали о модуле `AppModule`.
-   Вы импортировали `FormsModule` в `AppModule`, чтобы Angular распознал и применил директиву `ngModel`.
-   Вы узнали о важности объявления компонентов в `AppModule`.

## Ссылки

-   [The hero editor](https://angular.io/tutorial/tour-of-heroes/toh-pt1)
