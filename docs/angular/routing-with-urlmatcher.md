# Учебник: Создание пользовательских соответствий маршрута

Angular Router поддерживает мощную стратегию соответствия, которую вы можете использовать, чтобы помочь пользователям ориентироваться в вашем приложении. Эта стратегия соответствия поддерживает статические маршруты, переменные маршруты с параметрами, маршруты с подстановочными знаками и так далее.

Кроме того, вы можете создавать свои собственные шаблоны для ситуаций, когда URL-адреса более сложные.

В этом руководстве вы создадите пользовательский сопоставитель маршрутов, используя `UrlMatcher` от Angular. Этот матчер ищет ручку Twitter в URL.

Рабочий пример финальной версии этого руководства смотрите в <live-example></live-example>.

## Задачи

Реализовать `UrlMatcher` от Angular для создания пользовательского матчика маршрутов.

## Предварительные условия

Чтобы завершить этот учебник, вы должны иметь базовое понимание следующих концепций:

-   JavaScript

-   HTML

-   CSS

-   [Angular CLI](cli)

Если вы не знакомы с тем, как работает маршрутизатор Angular, просмотрите [Использование маршрутов Angular в одностраничном приложении](guide/router-tutorial).

## Создайте пример приложения

С помощью Angular CLI создайте новое приложение _angular-custom-route-match_. В дополнение к стандартному каркасу приложения Angular вы также создадите компонент _profile_.

1.  Создайте новый проект Angular, _angular-custom-route-match_.

    <code-example format="shell" language="shell">

    ng new angular-custom-route-match

    </code-example>

    Когда появится запрос `Вы хотите добавить маршрутизацию Angular?`, выберите `Y`.

    На вопрос `Какой формат таблицы стилей вы хотите использовать?` выберите `CSS`.

    Через несколько мгновений новый проект `angular-custom-route-match` будет готов.

1.  В терминале перейдите в каталог `angular-custom-route-match`.

1.  Создайте компонент _profile_.

   <code-example format="shell" language="shell">

ng генерировать профиль компонента

   </code-example>

1.  В редакторе кода найдите файл `profile.component.html` и замените содержимое заполнителя на следующий HTML.

    <code-example header="src/app/profile/profile.component.html" path="routing-with-urlmatcher/src/app/profile/profile.component.html"></code-example>.

1.  В редакторе кода найдите файл `app.component.html` и замените содержимое заполнителя на следующий HTML.

    <code-example header="src/app/app.component.html" path="routing-with-urlmatcher/src/app/app.component.html"></code-example>

## Настройте маршруты для вашего приложения

После установки фреймворка приложения вам нужно добавить возможности маршрутизации в файл `app.module.ts`. В рамках этого процесса вы создадите пользовательский URL-маршрутизатор, который будет искать Twitter handle в URL.

Этот хэндл идентифицируется предшествующим символом `@`.

1.  В редакторе кода откройте файл `app.module.ts`.

1.  Добавьте оператор `импорта` для `RouterModule` и `UrlMatcher` от Angular.

    <code-example header="src/app/app.module.ts" path="routing-with-urlmatcher/src/app/app/app.module.ts" region="import"></code-example>.

1.  В массив imports добавьте оператор `RouterModule.forRoot([])`.

    <code-example header="src/app/app.module.ts" path="routing-with-urlmatcher/src/app/app/app.module.ts" region="imports-array"></code-example>.

1.  Определите пользовательский маршрутный матчинг, добавив следующий код в оператор `RouterModule.forRoot()`.

    <code-example header="src/app/app.module.ts" path="routing-with-urlmatcher/src/app/app/app.module.ts" region="matcher"></code-example>.

Этот пользовательский матчер представляет собой функцию, которая выполняет следующие задачи:

-   Сопоставитель проверяет, что массив содержит только один сегмент
-   Сопоставитель использует регулярное выражение, чтобы убедиться, что формат имени пользователя совпадает.

-   Если совпадение есть, функция возвращает весь URL, определяя параметр маршрута `username` как подстроку пути.

-   Если совпадения нет, функция возвращает null, и маршрутизатор продолжает поиск других маршрутов, соответствующих URL.

<div class="is-helpful">

Пользовательский URL matcher ведет себя так же, как и любое другое определение маршрута. Определяйте дочерние маршруты или маршруты с ленивой загрузкой, как и любой другой маршрут.

</div>

## Subscribe to the route parameters

With the custom matcher in place, you now need to subscribe to the route parameters in the `profile` component.

1.  In your code editor, open your `profile.component.ts` file.
1.  Add an `import` statement for Angular's `ActivatedRoute` and `ParamMap`.

    <code-example header="src/app/profile/profile.component.ts" path="routing-with-urlmatcher/src/app/profile/profile.component.ts" region="activated-route-and-parammap"></code-example>

1.  Add an `import` statement for RxJS `map`.

    <code-example header="src/app/profile/profile.component.ts" path="routing-with-urlmatcher/src/app/profile/profile.component.ts" region="rxjs-map"></code-example>

1.  Subscribe to the `username` route parameter.

    <code-example header="src/app/profile/profile.component.ts" path="routing-with-urlmatcher/src/app/profile/profile.component.ts" region="subscribe"></code-example>

1.  Inject the `ActivatedRoute` into the component's constructor.

    <code-example header="src/app/profile/profile.component.ts" path="routing-with-urlmatcher/src/app/profile/profile.component.ts" region="activatedroute"></code-example>

## Test your custom URL matcher

With your code in place, you can now test your custom URL matcher.

1.  From a terminal window, run the `ng serve` command.

    <code-example format="shell" language="shell">

    ng serve

    </code-example>

1.  Open a browser to `http://localhost:4200`.

    You should see a single web page, consisting of a sentence that reads `Navigate to my profile`.

1.  Click the **my profile** hyperlink.

    A new sentence, reading `Hello, Angular!` appears on the page.

## Next steps

Pattern matching with the Angular Router provides you with a lot of flexibility when you have dynamic URLs in your application. To learn more about the Angular Router, see the following topics:

-   [In-app Routing and Navigation](guide/router)
-   [Router API](api/router)

<div class="alert is-helpful">

This content is based on [Custom Route Matching with the Angular Router](https://medium.com/@brandontroberts/custom-route-matching-with-the-angular-router-fbdd48665483), by [Brandon Roberts](https://twitter.com/brandontroberts).

</div>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
