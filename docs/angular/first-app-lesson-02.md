# Первое приложение Angular урок 2 - Создание компонента Home

Этот урок демонстрирует, как создать новый [компонент](/guide/component-overview) для вашего приложения Angular.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 10 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, который вы создали в Уроке 1, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите <live-example name="first-app-lesson-01"></live-example> из Урока 1, где вы можете:

    -   Использовать _живой пример_ в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать _download пример_ и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](tutorial/first-app), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть готовый код для этого урока в <live-example></live-example> для этого урока.

## После завершения

-   В вашем приложении появился новый компонент: `HomeComponent`.

## Концептуальный обзор компонентов Angular

Приложения Angular строятся на основе компонентов, которые являются строительными блоками Angular. Компоненты содержат код, HTML-макет и информацию о стилях CSS, которые обеспечивают функционирование и внешний вид элемента в приложении.

В Angular компоненты могут содержать другие компоненты. Функции и внешний вид приложения могут быть разделены и разбиты на компоненты.

В [Уроке 1](tutorial/first-app/first-app-lesson-01) вы обновили `AppComponent`, функция которого - содержать все остальные компоненты. В этом уроке вы создадите компонент `HomeComponent` для отображения главной страницы приложения.

В последующих уроках вы создадите больше компонентов для обеспечения дополнительных возможностей приложения.

В Angular компоненты имеют метаданные, которые определяют их свойства. Когда вы создаете свой `HomeComponent`, вы используете эти свойства:

-   `selector`: для описания того, как Angular обращается к компоненту в шаблонах.
-   `standalone`: чтобы описать, требует ли компонент `ngModule`.

-   `imports`: для описания зависимостей компонента.

-   `template`: для описания HTML-разметки и макета компонента.

-   `styleUrls`: перечисление URL файлов CSS, которые использует компонент, в виде массива.

Компоненты имеют и другие [свойства](/api/core/Component), но эти используются `HomeComponent`.

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 - Создание `HomeComponent`.

В этом шаге вы создаете новый компонент для вашего приложения.

В панели **Terminal** вашей IDE:

1.  В каталоге проекта перейдите в каталог `first-app`.

1.  Выполните эту команду для создания нового `HomeComponent`.

    <code-example format="shell" language="shell">

    ng generate component Home --standalone --inline-template --skip-tests

    </code-example>

1.  Выполните эту команду, чтобы собрать и обслужить ваше приложение.

    <code-example format="shell" language="shell">

    ng serve

    </code-example>

1.  Откройте браузер и перейдите по адресу `http://localhost:4200`, чтобы найти приложение.

1.  Убедитесь, что приложение создается без ошибок.

    Примечание: оно должно отображаться так же, как и в предыдущем уроке, потому что, хотя вы и добавили новый компонент, вы еще не включили его ни в один из шаблонов приложения.

1.  Оставьте `ng serve` запущенным, пока вы выполняете следующие шаги.

### Шаг 2 - Добавьте новый компонент в макет вашего приложения.

В этом шаге вы добавите новый компонент `HomeComponent` к корневому компоненту вашего приложения `AppComponent`, чтобы он отображался в макете вашего приложения.

В панели **Редактирование** вашей IDE:

1.  Откройте `app.component.ts` в редакторе.
1.  В `app.component.ts` импортируйте `HomeComponent`, добавив эту строку в импорт на уровне файла.

    <code-example header="Import HomeComponent in src/app/app.component.ts" path="first-app-lesson-02/src/app/app.component.ts" region="import-home"></code-example>.

1.  В `app.component.ts`, в `@Component`, обновите свойство массива `imports` и добавьте `HomeComponent`.

    <code-example header="Replace in src/app/app.component.ts" path="first-app-lesson-02/src/app/app/app.component.ts" region="app-metadata-imports"></code-example>.

1.  В `app.component.ts`, в `@Component`, обновите свойство `template`, чтобы включить следующий HTML код.

    <code-example header="Replace in src/app/app.component.ts" path="first-app-lesson-02/src/app/app/app.component.ts" region="app-metadata-template"></code-example>.

1.  Сохраните изменения в `app.component.ts`.

1.  Если `ng serve` запущен, приложение должно обновиться.

    Если `ng serve` не запущен, запустите его снова.

    _Hello world_ в вашем приложении должно измениться на _home works!_ из `HomeComponent`.

1.  Проверьте запущенное приложение в браузере и убедитесь, что оно было обновлено.

<section class="lightbox">
 <img alt="browser frame of page displaying the text 'home works!'" src="generated/images/guide/faa/homes-app-lesson-02-step-2.png">
</section>

### Шаг 3 - Добавление функций в `Домашний компонент`.

В этом шаге вы добавите функции в `HomeComponent`.

В предыдущем шаге вы добавили стандартный `HomeComponent` в шаблон вашего приложения, чтобы его HTML по умолчанию появился в приложении. В этом шаге вы добавите фильтр поиска и кнопку, которая будет использоваться в одном из последующих уроков.

На данный момент это все, что есть у `HomeComponent`.

Обратите внимание, что этот шаг просто добавляет элементы поиска в макет без какой-либо функции.

В панели **Edit** вашей IDE:

1.  В директории `first-app` откройте в редакторе файл `home.component.ts`.

1.  В `home.component.ts`, в `@Component`, обновите свойство `template` этим кодом.

    <code-example header="Replace in src/app/home/home/home.component.ts" path="first-app-lesson-02/src/app/home/home.component.ts" region="home-template"></code-example>.

1.  Далее откройте `home.component.css` в редакторе и обновите содержимое с помощью этих стилей.

    <code-example header="Replace in src/app/home/home/home.component.css" path="first-app-lesson-02/src/app/happ/home/home.component.css"></code-example>.

1.  Убедитесь, что приложение собирается без ошибок.

    Вы должны найти поле запроса фильтра и кнопку в вашем приложении, и они должны быть оформлены.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

<section class="lightbox">
 <img alt="browser frame of homes-app displaying logo, filter text input box and search button" src="generated/images/guide/faa/homes-app-lesson-02-step-3.png">
</section>

## Обзор урока

В этом уроке вы создали новый компонент для своего приложения и наделили его элементом управления редактирования фильтра и кнопкой.

Если у вас возникли трудности с этим уроком, вы можете просмотреть готовый код для него в <live-example></live-example>.

## Следующие шаги

-   [Первое Angular приложение урок 3 - Создание компонента HousingLocation приложения](tutorial/first-app/first-app-lesson-03)

## Дополнительная информация

Для получения дополнительной информации по темам, рассмотренным в этом уроке, посетите:

-   [`ng generate component`](cli/generate#component-command)

-   [`Ссылка на компонент`](api/core/Component)

-   [Обзор компонентов Angular](guide/component-overview)
