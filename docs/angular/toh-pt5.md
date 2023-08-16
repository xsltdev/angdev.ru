# Добавьте навигацию с маршрутизацией

Приложение Tour of Heroes имеет новые требования:

-   Добавить представление _Приборная доска_.

-   Добавить возможность навигации между представлениями _Герои_ и _Панель_.

-   Когда пользователи нажимают на имя героя в любом из представлений, переходят к детальному представлению выбранного героя.

-   Когда пользователи нажимают на _глубокую ссылку_ в электронном письме, открывается детальное представление для конкретного героя.

<div class="alert is-helpful">

Пример приложения, которое описывается на этой странице, см. в <live-example></live-example>.

</div>

Когда вы закончите, пользователи смогут перемещаться по приложению следующим образом:

<div class="lightbox">

<img alt="View navigations" src="generated/images/guide/toh/nav-diagram.png">

</div>

## Добавьте модуль `AppRoutingModule`.

В Angular лучшей практикой является загрузка и настройка маршрутизатора в отдельном модуле верхнего уровня. Маршрутизатор предназначен для маршрутизации и импортируется корневым `AppModule`.

По соглашению, имя класса модуля - `AppRoutingModule`, и он находится в `app-routing.module.ts` в директории `src/app`.

Запустите `ng generate` для создания модуля маршрутизации приложения.

<code-example format="shell" language="shell">

ng generate module app-routing --flat --module=app

</code-example>

<div class="alert is-helpful">

| Параметр | Детали | | :------------- | :---------------------------------------------------------------------------- | |
| `--flat` | Помещает файл в `src/app` вместо его собственного каталога. |

| `--module=app` | Приказывает `ng generate` зарегистрировать его в массиве `imports` модуля `AppModule`. |

</div>

Файл, который создает `ng generate`, выглядит следующим образом:

<code-example header="src/app/app-routing.module.ts (generated)" path="toh-pt5/src/app/app-routing.module.0.ts"></code-example>.

Замените его на следующий:

<code-example header="src/app/app-routing.module.ts (updated)" path="toh-pt5/src/app/app-routing.module.1.ts"></code-example>.

Во-первых, файл `app-routing.module.ts` импортирует `RouterModule` и `Routes`, чтобы приложение могло иметь возможность маршрутизации. Следующий импорт, `HeroesComponent`, дает маршрутизатору место, куда он может перейти после настройки маршрутов.

Обратите внимание, что ссылки на `CommonModule` и массив `declarations` не нужны, поэтому они больше не являются частью `AppRoutingModule`. Следующие разделы объясняют остальную часть `AppRoutingModule` более подробно.

### Маршруты

В следующей части файла вы настраиваете маршруты. Маршруты\_ указывают маршрутизатору, какой вид отображать, когда пользователь нажимает на ссылку или вставляет URL в адресную строку браузера.

Поскольку `app-routing.module.ts` уже импортирует `HeroesComponent`, вы можете использовать его в массиве `routes`:

<code-example header="src/app/app-routing.module.ts" path="toh-pt5/src/app/app-routing.module.ts" region="heroes-route"></code-example>.

Типичный Angular `Route` имеет два свойства:

| Properties | Details | | :---------- | :------------------------------------------------------------------------- |.

| `path` | Строка, которая соответствует URL в адресной строке браузера. |

| `component` | Компонент, который маршрутизатор должен создать при переходе к этому маршруту. |

Это указывает маршрутизатору сопоставить URL с `path: 'heroes'` и отобразить `HeroesComponent`, когда URL будет таким, как `localhost:4200/heroes`.

### `RouterModule.forRoot()`.

Метаданные `@NgModule` инициализируют маршрутизатор и запускают его прослушивание изменений местоположения браузера.

Следующая строка добавляет `RouterModule` в массив `imports` модуля `AppRoutingModule` и конфигурирует его с `routes` за один шаг, вызывая `RouterModule.forRoot()`:

<code-example header="src/app/app-routing.module.ts" path="toh-pt5/src/app/app-routing.module.ts" region="ngmodule-imports"></code-example>.

<div class="alert is-helpful">

Метод называется `forRoot()`, потому что вы настраиваете маршрутизатор на корневом уровне приложения. Метод `forRoot()` предоставляет поставщиков услуг и директивы, необходимые для маршрутизации, и выполняет начальную навигацию на основе текущего URL браузера.

</div>

Далее, `AppRoutingModule` экспортирует `RouterModule`, чтобы он был доступен во всем приложении.

<code-example header="src/app/app-routing.module.ts (exports array)" path="toh-pt5/src/app/app-routing.module.ts" region="export-routermodule"></code-example>.

## Добавьте `RouterOutlet`.

<!-- markdownlint-disable MD001 -->

Откройте шаблон `AppComponent` и замените элемент `<app-heroes>` на элемент `<router-outlet>`.

<code-example header="src/app/app.component.html (router-outlet)" path="toh-pt5/src/app/app.component.html" region="outlet"></code-example>.

Шаблон `AppComponent` больше не нуждается в `<app-heroes>`, потому что приложение отображает `HeroesComponent` только тогда, когда пользователь переходит к нему.

Шаблон `<router-outlet>` указывает маршрутизатору, где отображать маршрутизируемые представления.

<div class="alert is-helpful">

`RouterOutlet` - это одна из директив маршрутизации, которая стала доступна для `AppComponent`, потому что `AppModule` импортирует `AppRoutingModule`, который экспортировал `RouterModule`. Команда `ng generate`, которую вы выполнили в начале этого руководства, добавила этот импорт из-за флага `--module=app`.
Если вы не использовали команду `ng generate` для создания `app-routing.module.ts`, импортируйте `AppRoutingModule` в `app.module.ts` и добавьте его в массив `imports` `NgModule`.

</div>

<!-- markdownlint-disable MD024 -->

#### Попробуйте.

Если вы еще не обслуживаете свое приложение, запустите `ng serve`, чтобы увидеть свое приложение в браузере.

Браузер должен обновиться и отобразить заголовок приложения, но не список героев.

Посмотрите на адресную строку браузера. URL заканчивается на `/`.

Маршрутный путь к `HeroesComponent` - `/heroes`.

Добавьте `/heroes` к URL в адресной строке браузера. Вы должны увидеть знакомое представление обзора/детализации героев.

Удалите `/heroes` из URL в адресной строке браузера. Браузер должен обновиться и отобразить заголовок приложения, но не список героев.

<!-- markdownlint-enable MD001 -->

<!-- markdownlint-enable MD024 -->

<a id="routerlink"></a>

## Добавление навигационной ссылки с помощью `routerLink`.

В идеале пользователи должны иметь возможность нажать на ссылку для навигации, а не вставлять URL маршрута в адресную строку.

Добавьте элемент `<nav>` и внутри него элемент якоря, который при нажатии вызывает навигацию к `HeroesComponent`. Измененный шаблон `AppComponent` выглядит следующим образом:

<code-example header="src/app/app.component.html (heroes RouterLink)" path="toh-pt5/src/app/app.component.html" region="heroes"></code-example>

Атрибут [`routerLink`](#routerlink) установлен в `"/heroes"`, строку, которую маршрутизатор сопоставляет с маршрутом к `HeroesComponent`. Атрибут `routerLink` является селектором для директивы [`RouterLink`](api/router/RouterLink), которая превращает клики пользователя в навигацию по маршрутизатору.

Это еще одна из публичных директив в `RouterModule`.

Браузер обновляется и отображает заголовок приложения и ссылку на героев, но не список героев.

Щелкните по ссылке. Адресная строка обновляется до `/heroes`, и появляется список героев.

<div class="alert is-helpful">

Чтобы эта и будущие навигационные ссылки выглядели лучше, добавьте частные CSS стили в `app.component.css`, как указано в [финальном обзоре кода](#appcomponent) ниже.

</div>

## Добавьте представление приборной панели

Маршрутизация имеет больше смысла, когда ваше приложение имеет более одного представления, однако приложение _Тур героев_ имеет только представление героев.

Чтобы добавить `DashboardComponent`, запустите `ng generate`, как показано здесь:

<code-example format="shell" language="shell">

ng generate component dashboard

</code-example>

`ng generate` создает файлы для `DashboardComponent` и объявляет его в `AppModule`.

Замените содержимое по умолчанию в этих файлах, как показано здесь:

<code-tabs> <code-pane header="src/app/dashboard/dashboard.component.html" path="toh-pt5/src/app/dashboard/dashboard.component.1.html"></code-pane>
<code-pane header="src/app/dashboard/dashboard.component.ts" path="toh-pt5/src/app/dashboard/dashboard.component.ts"></code-pane>
<code-pane header="src/app/dashboard/dashboard.component.css" path="toh-pt5/src/app/dashboard/dashboard.component.css"></code-pane>
</code-tabs>

Шаблон _template_ представляет сетку ссылок на имена героев.

-   Повторитель `*ngFor` создает столько ссылок, сколько находится в массиве `heroes` компонента.

-   Ссылки оформляются как цветные блоки в `dashboard.component.css`.

-   Ссылки пока никуда не ведут.

Класс _class_ похож на класс `HeroesComponent`.

-   Он определяет свойство массива `heroes`.

-   Конструктор ожидает, что Angular внедрит `HeroService` в приватное свойство `heroService`.

-   Хук жизненного цикла `ngOnInit()` вызывает `getHeroes()`.

Эта `getHeroes()` возвращает нарезанный список героев на позициях 1 и 5, возвращая только героев два, три, четыре и пять.

<code-example header="src/app/dashboard/dashboard.component.ts" path="toh-pt5/src/app/dashboard/dashboard.component.ts" region="getHeroes"></code-example>.

### Добавьте маршрут к приборной панели

Чтобы перейти к приборной панели, маршрутизатору нужен соответствующий маршрут.

Импортируйте `DashboardComponent` в файл `app-routing.module.ts`.

<code-example header="src/app/app-routing.module.ts (import DashboardComponent)" path="toh-pt5/src/app/app-routing.module.ts" region="import-dashboard"></code-example>.

Добавьте маршрут в массив `routes`, который соответствует пути к `DashboardComponent`.

<code-example header="src/app/app-routing.module.ts" path="toh-pt5/src/app/app-routing.module.ts" region="dashboard-route"></code-example>.

### Добавьте маршрут по умолчанию

Когда приложение запускается, адресная строка браузера указывает на корень сайта. Это не совпадает ни с одним существующим маршрутом, поэтому маршрутизатор никуда не переходит.

Пространство под `<router-outlet>` пустует.

Чтобы приложение автоматически переходило на приборную панель, добавьте следующий маршрут в массив `routes`.

<code-example header="src/app/app-routing.module.ts" path="toh-pt5/src/app/app-routing.module.ts" region="redirect-route"></code-example>.

Этот маршрут перенаправляет URL, полностью соответствующий пустому пути, на маршрут, путь которого `'/dashboard'`.

После обновления браузера маршрутизатор загружает `DashboardComponent` и в адресной строке браузера отображается URL `/dashboard`.

### Добавление ссылки на приборную панель в оболочку

Пользователь должен иметь возможность перемещаться между `DashboardComponent` и `HeroesComponent`, нажимая на ссылки в области навигации в верхней части страницы.

Добавьте навигационную ссылку на приборную панель в шаблон оболочки `AppComponent`, чуть выше ссылки _Heroes_.

<code-example header="src/app/app.component.html" path="toh-pt5/src/app/app/app.component.html"></code-example>.

После обновления браузера вы можете свободно перемещаться между двумя представлениями, щелкая по ссылкам.

<a id="hero-details"></a>

## Переход к деталям героя

Компонент `HeroDetailComponent` отображает подробную информацию о выбранном герое. В настоящее время компонент `HeroDetailComponent` виден только в нижней части компонента `HeroesComponent`.

Пользователь должен иметь возможность получить доступ к этим деталям тремя способами.

1.  Нажав на героя в приборной панели.

1.  Щелкнув героя в списке героев.

1.  Вставляя URL "глубокой ссылки" в адресную строку браузера, который идентифицирует героя для отображения.

Этот раздел позволяет перейти к компоненту `HeroDetailComponent` и освободить его от компонента `HeroesComponent`.

### Удалить _детали героя_ из `HeroesComponent`.

Когда пользователь нажимает на героя в `HeroesComponent`, приложение должно перейти к `HeroDetailComponent`, заменив представление списка героев на представление подробностей о герое. Представление списка героев больше не должно показывать детали героя, как это происходит сейчас.

Откройте файл `heroes/heroes.component.html` и удалите элемент `<app-hero-detail>` снизу.

Щелчок по элементу героя теперь ничего не делает. Вы можете исправить это после того, как включите маршрутизацию к `HeroDetailComponent`.

### Добавьте маршрут _геройской детализации_.

URL типа `~/detail/11` будет хорошим URL для перехода к представлению _Hero Detail_ героя, чей `id` равен `11`.

Откройте `app-routing.module.ts` и импортируйте `HeroDetailComponent`.

<code-example header="src/app/app-routing.module.ts (import HeroDetailComponent)" path="toh-pt5/src/app/app-routing.module.ts" region="import-herodetail"></code-example>.

Затем добавьте _параметризованный_ маршрут в массив `routes`, который соответствует шаблону пути к представлению _геройская деталь_.

<code-example header="src/app/app-routing.module.ts" path="toh-pt5/src/app/app-routing.module.ts" region="detail-route"></code-example>.

Символ двоеточия `:` в `пути` указывает на то, что `:id` является заполнителем для конкретного героя `id`.

На данном этапе все маршруты приложения уже созданы.

<code-example header="src/app/app-routing.module.ts (все маршруты)" path="toh-pt5/src/app/app-routing.module.ts" region="routes"></code-example>.

### `DashboardComponent` ссылки на героев

Ссылки героев `DashboardComponent` на данный момент ничего не делают.

Теперь, когда маршрутизатор имеет маршрут к `HeroDetailComponent`, исправьте ссылки героев приборной панели для навигации с помощью _параметризированного_ маршрута приборной панели.

<code-example header="src/app/dashboard/dashboard.component.html (ссылки на героев)" path="toh-pt5/src/app/dashboard/dashboard.component.html" region="click"></code-example>.

Вы используете Angular [interpolation binding](interpolation.md) внутри повторителя `*ngFor` для вставки `hero.id` текущей итерации в каждый [`routerLink`](#routerlink).

<a id="heroes-component-links"></a>

### `HeroesComponent` hero links

The hero items in the `HeroesComponent` are `<li>` elements whose click events are bound to the component's `onSelect()` method.

<code-example header="src/app/heroes/heroes.component.html (list with onSelect)" path="toh-pt4/src/app/heroes/heroes.component.html" region="list"></code-example>

Remove the inner HTML of `<li>`. Wrap the badge and name in an anchor `<a>` element.

Add a `routerLink` attribute to the anchor that's the same as in the dashboard template.

<code-example header="src/app/heroes/heroes.component.html (список со ссылками)" path="toh-pt5/src/app/heroes/heroes.component.html" region="list"></code-example>.

Обязательно исправьте частную таблицу стилей в `heroes.component.css`, чтобы список выглядел как раньше. Исправленные стили находятся в [финальном обзоре кода](#heroescomponent) внизу этого руководства.

#### Удаление мертвого кода - необязательно

Хотя класс `HeroesComponent` все еще работает, метод `onSelect()` и свойство `selectedHero` больше не используются.

Неплохо привести все в порядок для вашего будущего. Вот класс после обрезки мертвого кода.

<code-example header="src/app/heroes/heroes.component.ts (очищено)" path="toh-pt5/src/app/heroes/heroes.component.ts" region="class"></code-example>.

## Маршрутизируемый `HeroDetailComponent`.

Родительский `HeroesComponent` использовался для установки свойства `HeroDetailComponent.hero` и `HeroDetailComponent` отображал героя.

Теперь `HeroesComponent` этого не делает. Теперь маршрутизатор создает `HeroDetailComponent` в ответ на URL, такой как `~/detail/12`.

Компоненту `HeroDetailComponent` нужен новый способ заставить героя отображаться. В этом разделе объясняется следующее:

-   Получить маршрут, который его создал

-   Извлечь `id` из маршрута

-   Получите героя с этим `id` с сервера, используя `HeroService`.

Добавьте следующие импорты:

<code-example header="src/app/hero-detail/hero-detail.component.ts" path="toh-pt5/src/app/hero-detail/hero-detail.component.ts" region="added-imports"></code-example>

<a id="hero-detail-ctor"></a>

Вставьте в конструктор сервисы `ActivatedRoute`, `HeroService` и `Location`, сохранив их значения в приватных полях:

<code-example header="src/app/hero-detail/hero-detail.component.ts" path="toh-pt5/src/app/hero-detail/hero-detail.component.ts" region="ctor"></code-example>.

В [`ActivatedRoute`](api/router/ActivatedRoute) хранится информация о маршруте к данному экземпляру `HeroDetailComponent`. Этот компонент интересуют параметры маршрута, извлеченные из URL.

Параметр "id" - это `id` героя для отображения.

Сервис [`HeroService`](tutorial/tour-of-heroes/toh-pt4) получает данные о героях с удаленного сервера, и этот компонент использует их для получения героя для отображения.

[`location`](api/common/Location) - это сервис Angular для взаимодействия с браузером. Этот сервис позволяет вам вернуться к предыдущему представлению.

### Извлечение параметра маршрута `id`

В `ngOnInit()` [lifecycle hook](lifecycle-hooks.md#oninit) вызовите `getHero()` и определите его следующим образом.

<code-example header="src/app/hero-detail/hero-detail.component.ts" path="toh-pt5/src/app/hero-detail/hero-detail.component.ts" region="ngOnInit"></code-example>.

Снимок `route.snapshot` - это статическое изображение информации о маршруте сразу после создания компонента.

`paramMap` - это словарь значений параметров маршрута, извлеченных из URL. Ключ `"id"` возвращает `id` героя для выборки.

Параметры маршрута всегда являются строками. Функция JavaScript `Number` преобразует строку в число,

которым и должен быть `id` героя.

Браузер обновляется, и приложение падает с ошибкой компилятора. У `HeroService` нет метода `getHero()`.

Добавьте его сейчас.

### Добавьте `HeroService.getHero()`.

Откройте `HeroService` и добавьте следующий метод `getHero()` с `id` после метода `getHeroes()`:

<code-example header="src/app/hero.service.ts (getHero)" path="toh-pt5/src/app/hero.service.ts" region="getHero"></code-example>.

<div class="alert is-important">

**IMPORTANT**: <br /> The backtick \( <code>&grave;</code> \) characters define a JavaScript [template literal](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Template_literals) for embedding the `id`.

</div>

Как и [`getHeroes()`](tutorial/tour-of-heroes/toh-pt4#observable-heroservice), `getHero()` имеет асинхронную сигнатуру. Она возвращает _макет героя_ как `Observable`, используя функцию RxJS `of()`.

Вы можете переписать `getHero()` как настоящий `Http` запрос без необходимости изменять `HeroDetailComponent`, который его вызывает.

<!-- markdownlint-disable MD024 -->

#### Попробуйте.

Браузер обновляется, и приложение снова работает. Вы можете щелкнуть героя на приборной панели или в списке героев и перейти к детальному представлению этого героя.

Если вы введете `localhost:4200/detail/12` в адресную строку браузера, маршрутизатор перейдет к детальному представлению для героя с `id: 12`, **Dr Nice**.

<!-- markdownlint-enable MD024 -->

<a id="goback"></a>

### Найти дорогу назад

Нажав кнопку "Назад" в браузере, вы можете вернуться на предыдущую страницу. Это может быть список героев или представление приборной панели, в зависимости от того, что отправило вас к детальному представлению.

Было бы неплохо иметь кнопку на представлении `HeroDetail`, которая могла бы это сделать.

Добавьте кнопку _go back_ в нижнюю часть шаблона компонента и привяжите ее к методу компонента `goBack()`.

<code-example header="src/app/hero-detail/hero-detail.component.html (кнопка назад)" path="toh-pt5/src/app/hero-detail/hero-detail.component.html" region="back-button"></code-example>.

Добавьте \_метод `goBack()` в класс компонента, который перемещается на один шаг назад в стеке истории браузера, используя службу `Location`, которую вы [использовали для инъекции](#hero-detail-ctor).

<code-example header="src/app/hero-detail/hero-detail.component.ts (goBack)" path="toh-pt5/src/app/hero-detail/hero-detail.component.ts" region="goBack"></code-example>.

Обновите браузер и начните кликать. Теперь пользователи могут перемещаться по приложению с помощью новых кнопок.

Детали выглядят лучше, если добавить частные CSS стили в `hero-detail.component.css`, как указано в одной из вкладок ["final code review"](#final-code-review) ниже.

## Окончательный обзор кода

<!-- markdownlint-disable MD001 -->

Здесь представлены файлы кода, обсуждаемые на этой странице.

<a id="approutingmodule"></a> <a id="appmodule"></a>

#### `AppRoutingModule`, `AppModule` и `HeroService`.

<code-tabs> <code-pane header="src/app/app.module.ts" path="toh-pt5/src/app/app.module.ts"></code-pane>
<code-pane header="src/app/app-routing.module.ts" path="toh-pt5/src/app/app-routing.module.ts"></code-pane>
<code-pane header="src/app/hero.service.ts" path="toh-pt5/src/app/hero.service.ts"></code-pane>
</code-tabs>

<a id="appcomponent"></a>

#### `AppComponent`

<code-tabs> <code-pane header="src/app/app.component.html" path="toh-pt5/src/app/app.component.html"></code-pane>
<code-pane header="src/app/app.component.ts" path="toh-pt5/src/app/app.component.ts"></code-pane>
<code-pane header="src/app/app.component.css" path="toh-pt5/src/app/app.component.css"></code-pane>
</code-tabs>

<a id="dashboardcomponent"></a>

#### `DashboardComponent`.

<code-tabs> <code-pane header="src/app/dashboard/dashboard.component.html" path="toh-pt5/src/app/dashboard/dashboard.component.html"></code-pane>
<code-pane header="src/app/dashboard/dashboard.component.ts" path="toh-pt5/src/app/dashboard/dashboard.component.ts"></code-pane>
<code-pane header="src/app/dashboard/dashboard.component.css" path="toh-pt5/src/app/dashboard/dashboard.component.css"></code-pane>
</code-tabs>

<a id="heroescomponent"></a>

#### `HeroesComponent`.

<code-tabs> <code-pane header="src/app/heroes/heroes.component.html" path="toh-pt5/src/app/heroes/heroes.component.html"></code-pane>
<code-pane header="src/app/heroes/heroes.component.ts" path="toh-pt5/src/app/heroes/heroes.component.ts"></code-pane>
<code-pane header="src/app/heroes/heroes.component.css" path="toh-pt5/src/app/heroes/heroes.component.css"></code-pane>
</code-tabs>

<a id="herodetailcomponent"></a>

#### `HeroDetailComponent`.

<code-tabs> <code-pane header="src/app/hero-detail/hero-detail.component.html" path="toh-pt5/src/app/hero-detail/hero-detail.component.html"></code-pane>
<code-pane header="src/app/hero-detail/hero-detail.component.ts" path="toh-pt5/src/app/hero-detail/hero-detail.component.ts"></code-pane>
<code-pane header="src/app/hero-detail/hero-detail.component.css" path="toh-pt5/src/app/hero-detail/hero-detail.component.css"></code-pane>
</code-tabs>

<!-- markdownlint-enable MD001 -->

## Summary

-   You added the Angular router to navigate among different components

-   You turned the `AppComponent` into a navigation shell with `<a>` links and a `<router-outlet>`

-   You configured the router in an `AppRoutingModule`

-   You defined routes, a redirect route, and a parameterized route

-   You used the `routerLink` directive in anchor elements

-   You refactored a tightly coupled main/detail view into a routed detail view

-   You used router link parameters to navigate to the detail view of a user-selected hero

-   You shared the `HeroService` with other components

:date: 28.02.2022
