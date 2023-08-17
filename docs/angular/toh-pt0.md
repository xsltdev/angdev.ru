---
description: Используйте команду ng new, чтобы начать создание приложения Tour of Heroes
---

# Создайте новый проект

:date: 28.02.2022

Используйте команду `ng new`, чтобы начать создание приложения **Tour of Heroes**.

В этом руководстве:

1.  Устанавливает ваше окружение.
2.  Создает новое рабочее пространство и начальный проект приложения.
3.  Обслуживает приложение.
4.  Вносит изменения в новое приложение.

!!!note ""

    Для просмотра кода приложения смотрите:

    -   [Живой пример](https://angular.io/generated/live-examples/toh-pt0/stackblitz.html)
    -   [Скачать](https://angular.io/generated/zips/toh-pt0/toh-pt0.zip)

## Настройка среды

Чтобы настроить среду разработки, следуйте инструкциям в [Local Environment Setup](setup-local.md 'Setting up for Local Development').

## Создайте новое рабочее пространство и начальное приложение

Вы разрабатываете приложения в контексте Angular [workspace](glossary.md#workspace). Рабочее пространство содержит файлы для одного или нескольких [проектов](glossary.md#project).

_Проект_ - это набор файлов, составляющих приложение или библиотеку.

Чтобы создать новое рабочее пространство и начальный проект, выполните следующие действия:

1.  Убедитесь, что вы еще не находитесь в каталоге рабочего пространства Angular.

    Например, если вы находитесь в рабочей области "Начало работы" из предыдущего упражнения, перейдите в ее родительскую директорию.

2.  Выполните команду `ng new`, за которой следует имя приложения, как показано здесь:

    ```shell
    ng new angular-tour-of-heroes
    ```

3.  Функция `ng new` запрашивает информацию о функциях, которые необходимо включить в начальный проект.

    Примите значения по умолчанию, нажав клавишу Enter или Return.

`ng new` устанавливает необходимые пакеты `npm` и другие зависимости, которые требуются Angular. Это может занять несколько минут.

`ng new` также создает следующее рабочее пространство и файлы начального проекта:

-   Новое рабочее пространство с корневым каталогом `angular-tour-of-heroes`.
-   Начальный скелетный проект приложения в подкаталоге `src/app`.
-   Связанные конфигурационные файлы

Начальный проект приложения содержит простое приложение, готовое к запуску.

## Запуск приложения

Перейдите в каталог рабочей области и запустите приложение.

```shell
cd angular-tour-of-heroes
ng serve --open
```

!!!note ""

    Команда `ng serve`:

    -   Создает приложение
    -   Запускает сервер разработки
    -   Следит за исходными файлами
    -   Пересоздает приложение по мере внесения изменений.

    Флаг `--open` открывает браузер на `http://localhost:4200`.

Вы должны увидеть запущенное приложение в браузере.

## компоненты Angular

Страница, которую вы видите, - это _оболочка приложения_. Оболочка управляется компонентом Angular **component** с именем `AppComponent`.

_Компоненты_ - это фундаментальные строительные блоки приложений Angular. Они отображают данные на экране, слушают ввод пользователя и выполняют действия на основе этого ввода.

## Внесение изменений в приложение

Откройте проект в вашем любимом редакторе или IDE. Перейдите в каталог `src/app` для редактирования стартового приложения. В IDE найдите эти файлы, которые составляют `AppComponent`, который вы только что создали:

| Files                | Details                                          |
| :------------------- | :----------------------------------------------- |
| `app.component.ts`   | Код класса компонента, написанный на TypeScript. |
| `app.component.html` | Шаблон компонента, написанный на HTML.           |
| `app.component.css`  | Частные CSS стили компонента.                    |

!!!warning ""

    Когда вы запустили `ng new`, Angular создал тестовые спецификации для вашего нового приложения. К сожалению, внесение этих изменений нарушает только что созданные спецификации.

    Это не будет проблемой, потому что тестирование Angular выходит за рамки данного руководства и не будет использоваться.

    Чтобы узнать больше о тестировании с помощью Angular, смотрите [Тестирование](testing.md).

### Измените заголовок приложения

Откройте файл `app.component.ts` и измените значение свойства `title` на "Tour of Heroes".

```ts
title = 'Tour of Heroes';
```

Откройте `app.component.html` и удалите шаблон по умолчанию, который создал `ng new`. Замените его следующей строкой HTML.

```html
<h1>{{title}}</h1>
```

Двойные фигурные скобки - это синтаксис _интерполяционного связывания_ в Angular. Эта интерполяционная привязка представляет значение свойства компонента `title` внутри тега заголовка HTML.

Браузер обновляется и отображает новый заголовок приложения.

### Добавить стили приложения {#app-wide-styles}

Большинство приложений стремятся к единообразному внешнему виду всего приложения. Для этого `ng new` создал пустой файл `styles.css`.

Поместите туда свои стили для всего приложения.

Откройте `src/styles.css` и добавьте в файл приведенный ниже код.

```css
/* Application-wide Styles */
h1 {
    color: #369;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 250%;
}
h2,
h3 {
    color: #444;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: lighter;
}
body {
    margin: 2em;
}
body,
input[type='text'],
button {
    color: #333;
    font-family: Cambria, Georgia, serif;
}
button {
    background-color: #eee;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    color: black;
    font-size: 1.2rem;
    padding: 1rem;
    margin-right: 1rem;
    margin-bottom: 1rem;
    margin-top: 1rem;
}
button:hover {
    background-color: black;
    color: white;
}
button:disabled {
    background-color: #eee;
    color: #aaa;
    cursor: auto;
}

/* everywhere else */
* {
    font-family: Arial, Helvetica, sans-serif;
}
```

## Окончательный обзор кода

Вот файлы кода, рассмотренные на этой странице.

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
    ```

=== "src/styles.css (excerpt)"

    ```css
    /* Application-wide Styles */
    h1 {
    	color: #369;
    	font-family: Arial, Helvetica, sans-serif;
    	font-size: 250%;
    }
    h2,
    h3 {
    	color: #444;
    	font-family: Arial, Helvetica, sans-serif;
    	font-weight: lighter;
    }
    body {
    	margin: 2em;
    }
    body,
    input[type='text'],
    button {
    	color: #333;
    	font-family: Cambria, Georgia, serif;
    }
    button {
    	background-color: #eee;
    	border: none;
    	border-radius: 4px;
    	cursor: pointer;
    	color: black;
    	font-size: 1.2rem;
    	padding: 1rem;
    	margin-right: 1rem;
    	margin-bottom: 1rem;
    	margin-top: 1rem;
    }
    button:hover {
    	background-color: black;
    	color: white;
    }
    button:disabled {
    	background-color: #eee;
    	color: #aaa;
    	cursor: auto;
    }

    /* everywhere else */
    * {
    	font-family: Arial, Helvetica, sans-serif;
    }
    ```

## Резюме

-   Вы создали начальную структуру приложения с помощью `ng new`.
-   Вы узнали, что компоненты Angular отображают данные
-   Вы использовали двойные фигурные скобки интерполяции для отображения заголовка приложения

## Ссылки

-   [Create a new project](https://angular.io/tutorial/tour-of-heroes/toh-pt0)
