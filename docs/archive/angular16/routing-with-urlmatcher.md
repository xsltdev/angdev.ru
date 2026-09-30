# Учебник: Создание пользовательских соответствий маршрута

:date: 28.02.2022

Angular Router поддерживает мощную стратегию соответствия, которую вы можете использовать, чтобы помочь пользователям ориентироваться в вашем приложении. Эта стратегия соответствия поддерживает статические маршруты, переменные маршруты с параметрами, маршруты с подстановочными знаками и так далее.

Кроме того, вы можете создавать свои собственные шаблоны для ситуаций, когда URL-адреса более сложные.

В этом руководстве вы создадите пользовательский сопоставитель маршрутов, используя `UrlMatcher` от Angular. Этот матчер ищет ручку Twitter в URL.

Рабочий пример финальной версии этого руководства смотрите в [коде](https://angular.io/generated/live-examples/routing-with-urlmatcher/stackblitz.html).

## Задачи

Реализовать `UrlMatcher` от Angular для создания пользовательского матчика маршрутов.

## Предварительные условия

Чтобы завершить этот учебник, вы должны иметь базовое понимание следующих концепций:

-   JavaScript
-   HTML
-   CSS
-   [Angular CLI](https://angular.io/cli.md)

Если вы не знакомы с тем, как работает маршрутизатор Angular, просмотрите [Использование маршрутов Angular в одностраничном приложении](router-tutorial.md).

## Создайте пример приложения

С помощью Angular CLI создайте новое приложение _angular-custom-route-match_. В дополнение к стандартному каркасу приложения Angular вы также создадите компонент _profile_.

1.  Создайте новый проект Angular, _angular-custom-route-match_.

    ```shell
    ng new angular-custom-route-match
    ```

    Когда появится запрос `Вы хотите добавить маршрутизацию Angular?`, выберите `Y`.

    На вопрос `Какой формат таблицы стилей вы хотите использовать?` выберите `CSS`.

    Через несколько мгновений новый проект `angular-custom-route-match` будет готов.

2.  В терминале перейдите в каталог `angular-custom-route-match`.

3.  Создайте компонент _profile_.

    ```
    ng generate component profile
    ```

4.  В редакторе кода найдите файл `profile.component.html` и замените содержимое заполнителя на следующий HTML.

    ```html
    <p>Hello {{ username$ | async }}!</p>
    ```

5.  В редакторе кода найдите файл `app.component.html` и замените содержимое заполнителя на следующий HTML.

    ```html
    <h2>Routing with Custom Matching</h2>

    Navigate to <a routerLink="/@Angular">my profile</a>

    <router-outlet></router-outlet>
    ```

## Настройте маршруты для вашего приложения

После установки фреймворка приложения вам нужно добавить возможности маршрутизации в файл `app.module.ts`. В рамках этого процесса вы создадите пользовательский URL-маршрутизатор, который будет искать Twitter handle в URL.

Этот хэндл идентифицируется предшествующим символом `@`.

1.  В редакторе кода откройте файл `app.module.ts`.

2.  Добавьте оператор `импорта` для `RouterModule` и `UrlMatcher` от Angular.

    ```ts
    import {
        RouterModule,
        UrlSegment,
    } from '@angular/router';
    ```

3.  В массив imports добавьте оператор `RouterModule.forRoot([])`.

    ```ts
    @NgModule({
    imports: [
    	BrowserModule,
    	FormsModule,
    	RouterModule.forRoot([
    		/* . . . */
    	])
    ],
    declarations: [ AppComponent, ProfileComponent ],
    bootstrap:    [ AppComponent ]
    })
    ```

4.  Определите пользовательский маршрутный матчинг, добавив следующий код в оператор `RouterModule.forRoot()`.

    ```ts
    {
    	matcher: (url) => {
    		if (url.length === 1 && url[0].path.match(/^@[\w]+$/gm)) {
    		return {
    			consumed: url,
    			posParams: {
    			username: new UrlSegment(url[0].path.slice(1), {})
    			}
    		};
    		}

    		return null;
    	},
    	component: ProfileComponent
    }
    ```

Этот пользовательский матчер представляет собой функцию, которая выполняет следующие задачи:

-   Сопоставитель проверяет, что массив содержит только один сегмент
-   Сопоставитель использует регулярное выражение, чтобы убедиться, что формат имени пользователя совпадает.
-   Если совпадение есть, функция возвращает весь URL, определяя параметр маршрута `username` как подстроку пути.
-   Если совпадения нет, функция возвращает null, и маршрутизатор продолжает поиск других маршрутов, соответствующих URL.

!!!note ""

    Пользовательский URL `matcher` ведет себя так же, как и любое другое определение маршрута. Определяйте дочерние маршруты или маршруты с ленивой загрузкой, как и любой другой маршрут.

## Подписка на параметры маршрута

Теперь, когда пользовательский матчер установлен, вам нужно подписаться на параметры маршрута в компоненте `profile`.

1.  В редакторе кода откройте файл `profile.component.ts`.

2.  Добавьте оператор `импорта` для `ActivatedRoute` и `ParamMap` от Angular.

    ```ts
    import {
        ActivatedRoute,
        ParamMap,
    } from '@angular/router';
    ```

3.  Добавьте оператор `импорта` для RxJS `map`.

    ```ts
    import { map } from 'rxjs/operators';
    ```

4.  Подписка на параметр маршрута `username`.

    ```ts
    username$ = this.route.paramMap.pipe(
        map((params: ParamMap) => params.get('username'))
    );
    ```

5.  Вставьте `ActivatedRoute` в конструктор компонента.

    ```ts
    constructor(private route: ActivatedRoute) { }
    ```

## Тестирование пользовательского URL-матчика

Теперь, когда ваш код установлен, вы можете протестировать ваш пользовательский URL matcher.

1.  В окне терминала выполните команду `ng serve`.

    ```shell
    ng serve
    ```

2.  Откройте браузер по адресу `http://localhost:4200`.

    Вы должны увидеть единственную веб-страницу, состоящую из предложения `Перейдите к моему профилю`.

3.  Щелкните на гиперссылке **мой профиль**.

    На странице появится новое предложение с текстом `Здравствуй, Angular!`.

## Следующие шаги

Сопоставление шаблонов с помощью Angular Router обеспечивает большую гибкость при использовании динамических URL-адресов в вашем приложении. Чтобы узнать больше об Angular Router, см. следующие темы:

-   [Маршрутизация и навигация в приложении](router.md)
-   [Router API](https://angular.io/api/router)

!!!note ""

    Этот материал основан на [Custom Route Matching with the Angular Router](https://medium.com/@brandontroberts/custom-route-matching-with-the-angular-router-fbdd48665483), автор [Brandon Roberts](https://twitter.com/brandontroberts).
