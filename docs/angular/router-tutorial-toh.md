# Учебник по маршрутизатору: экскурсия по героям

:date: 28.02.2022

В этом учебнике представлен обширный обзор маршрутизатора Angular. В этом уроке вы, основываясь на базовой конфигурации маршрутизатора, изучите такие возможности, как дочерние маршруты, параметры маршрута, ленивая загрузка NgModules, защитные маршруты и предварительная загрузка данных для улучшения пользовательского опыта.

Рабочий пример окончательной версии приложения смотрите в [коде](https://angular.io/generated/live-examples/router/stackblitz.html).

## Цели {: #router-tutorial-objectives }

Это руководство описывает разработку многостраничного маршрутизируемого примера приложения. Попутно в нем освещаются ключевые особенности маршрутизатора, такие как:

-   Организация функций приложения в модули
-   Переход к компоненту (_Герои_ ссылка на "Список героев")
-   Включение параметра маршрута (передача `id` героя при маршрутизации к "Детали героя")
-   Дочерние маршруты (у _Кризисного центра_ есть свои собственные маршруты)
-   Страж `canActivate` (проверка доступа к маршруту)
-   Страж `canActivateChild` (проверка доступа к дочерним маршрутам)
-   Страж `canDeactivate` (запрашивать разрешение на удаление несохраненных изменений)
-   Страж `resolve` (предварительная выборка данных маршрута)
-   Ленивая загрузка `NgModule`
-   Страж `canMatch` (проверка перед загрузкой активов функционального модуля)

Это руководство построено в виде последовательности этапов, как если бы вы создавали приложение шаг за шагом, но предполагает, что вы знакомы с основными [концепциями Angular](architecture.md). Для общего введения в angular смотрите [Getting Started](start.md).

Для более подробного обзора смотрите учебник [Tour of Heroes](tour-of-heroes.md).

## Предварительные условия

Чтобы завершить этот учебник, вы должны иметь базовое понимание следующих концепций:

-   JavaScript
-   HTML
-   CSS
-   [Angular CLI](https://angular.io/cli.md).

Вам может быть полезен учебник [Tour of Heroes](tour-of-heroes.md), но он не обязателен.

## Пример приложения в действии

Пример приложения для этого учебника помогает Агентству по трудоустройству героев находить кризисы для героев.

Приложение имеет три основные функции:

1.  Кризисный центр" для ведения списка кризисов для поручения героям.

2.  Область _Герои_ для ведения списка героев, нанятых агентством.

3.  Область _Админ_ для управления списком кризисов и героев.

Попробуйте это сделать, щелкнув [по этой ссылке](https://angular.io/generated/live-examples/router/stackblitz.html).

Приложение отображается с рядом навигационных кнопок и представлением _Heroes_ со списком героев.

![Пример приложения с рядом навигационных кнопок и списком героев](hero-list.gif)

Выберите одного героя, и приложение переведет вас на экран редактирования героя.

![Детальное представление героя с дополнительной информацией, вводом данных и кнопкой "Назад"](hero-detail.png)

Измените имя. Нажмите кнопку "Назад", и приложение вернется к списку героев, в котором будет отображаться измененное имя героя.
Обратите внимание, что изменение имени вступило в силу немедленно.

Если бы вы нажали кнопку "Назад" браузера, а не кнопку "Назад" приложения, приложение также вернуло бы вас к списку героев. Навигация в приложениях Angular обновляет историю браузера так же, как и обычная веб-навигация.

Теперь нажмите на ссылку _Кризисный центр_ для получения списка текущих кризисов.

![Crisis Center list of crises](crisis-center-list.gif)

Выберите кризис, и приложение переведет вас на экран редактирования кризиса. На той же странице, под списком, в дочернем компоненте появляется _Деталь кризиса_.

Измените название кризиса. Обратите внимание, что соответствующее название в списке кризисов _не_ изменяется.

![Детализация кризисной ситуации в кризисном центре с данными, вводом, кнопками сохранения и отмены.](crisis-center-detail.gif)

В отличие от _Hero Detail_, который обновляется по мере ввода текста, изменения в _Crisis Detail_ являются временными, пока вы не сохраните или не отмените их нажатием кнопок "Сохранить" или "Отмена". Обе кнопки позволяют вернуться к _Кризисному центру_ и его списку кризисов.

Нажмите кнопку "Назад" браузера или ссылку "Герои", чтобы активировать диалог.

![Предупреждение, которое просит пользователя подтвердить отмену изменений](confirm-dialog.png)

Вы можете сказать "OK" и потерять свои изменения или нажать "Cancel" и продолжить редактирование.

За этим поведением стоит защита маршрутизатора `canDeactivate`. Эта защита дает вам шанс очистить или спросить разрешения пользователя, прежде чем переходить от текущего представления.

Кнопки `Admin` и `Login` иллюстрируют другие возможности маршрутизатора, которые будут рассмотрены далее в руководстве.

## Этап 1: Начало работы {: #getting-started }

Начните с базовой версии приложения, которое перемещается между двумя пустыми представлениями.

![Анимированное изображение приложения с кнопкой Кризисного центра и кнопкой Героев. Указатель нажимает на каждую кнопку, чтобы показать вид для каждой из них.](router-1-anim.gif)

### Создайте пример приложения {: #import }

1.  Создайте новый проект Angular, _angular-router-tour-of-heroes_.

    ```shell
    ng new angular-router-tour-of-heroes
    ```

    Когда появится запрос `Вы хотите добавить маршрутизацию Angular?`, выберите `N`.

    На вопрос `Какой формат таблицы стилей вы хотите использовать?` выберите `CSS`.

    Через несколько мгновений новый проект `angular-router-tour-of-heroes` будет готов.

2.  В терминале перейдите в каталог `angular-router-tour-of-heroes`.

3.  Убедитесь, что ваше новое приложение работает как ожидалось, выполнив команду `ng serve`.

    ```shell
    ng serve
    ```

4.  Откройте браузер на `http://localhost:4200`.

    Вы должны увидеть запущенное приложение в браузере.

### Определение маршрутов

Маршрутизатор должен быть сконфигурирован со списком определений маршрутов.

Каждое определение преобразуется в объект [Route](https://angular.io/api/router/Route), который содержит две вещи: `path` - сегмент пути URL для этого маршрута; и `component` - компонент, связанный с этим маршрутом.

Маршрутизатор обращается к своему реестру определений при изменении URL браузера или когда код приложения указывает маршрутизатору перемещаться по пути маршрута.

Первый маршрут делает следующее:

-   Когда URL-адрес местоположения браузера меняется на соответствующий сегмент пути `/crisis-center`, маршрутизатор активирует экземпляр `CrisisListComponent` и отображает его представление.
-   Когда приложение запрашивает навигацию к пути `/crisis-center`, маршрутизатор активирует экземпляр `CrisisListComponent`, отображает его представление и обновляет адрес местоположения и историю браузера с URL для этого пути.

Первая конфигурация определяет массив из двух маршрутов с минимальными путями, ведущими к `CrisisListComponent` и `HeroListComponent`.

Создайте компоненты `CrisisList` и `HeroList`, чтобы маршрутизатору было что отображать.

```shell
ng generate component crisis-list
```

```shell
ng generate component hero-list
```

Замените содержимое каждого компонента следующим образцом HTML.

=== "src/app/crisis-list/crisis-list.component.html"

    ```html
    <h2>CRISIS CENTER</h2>
    <p>Get your crisis here</p>
    ```

=== "src/app/hero-list/hero-list.component.html"

    ```html
    <h2>HEROES</h2>
    <p>Get your heroes here</p>
    ```

### Зарегистрируйте `Router` и `Routes`

Чтобы использовать `Router`, вы должны сначала зарегистрировать `RouterModule` из пакета `@angular/router`. Определите массив маршрутов, `appRoutes`, и передайте их в метод `RouterModule.forRoot()`.

Метод `RouterModule.forRoot()` возвращает модуль, содержащий настроенный поставщик услуг `Router`, а также другие поставщики, необходимые библиотеке маршрутизации.

После загрузки приложения `Router` выполняет начальную навигацию на основе текущего URL браузера.

!!!warning ""

    Метод `RouterModule.forRoot()` - это шаблон, используемый для регистрации провайдеров всего приложения. Подробнее о провайдерах для всего приложения читайте в руководстве [Singleton services](singleton-services.md#forRoot-router).

```ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { CrisisListComponent } from './crisis-list/crisis-list.component';
import { HeroListComponent } from './hero-list/hero-list.component';

const appRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisListComponent,
    },
    { path: 'heroes', component: HeroListComponent },
];

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        RouterModule.forRoot(
            appRoutes,
            { enableTracing: true } // <-- debugging purposes only
        ),
    ],
    declarations: [
        AppComponent,
        HeroListComponent,
        CrisisListComponent,
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

!!!note ""

    Добавление настроенного `RouterModule` к `AppModule` достаточно для минимальных конфигураций маршрутов. Однако, по мере роста приложения, [рефакторинг конфигурации маршрутизации](#refactor-the-routing-configuration-into-a-routing-module) в отдельный файл и создание [модуля маршрутизации](#routing-module).

    Модуль маршрутизации - это специальный тип `Service Module`, предназначенный для маршрутизации.

Регистрация `RouterModule.forRoot()` в массиве `AppModule` `imports` делает сервис `Router` доступным везде в приложении.

### Добавьте выход маршрутизатора {: #shell}

Корневой `AppComponent` - это оболочка приложения. Она имеет заголовок, панель навигации с двумя ссылками и выход маршрутизатора, в котором маршрутизатор рендерит компоненты.

![Навигатор, состоящий из двух кнопок навигации, с активной первой кнопкой и отображением связанного с ней представления](shell-and-outlet.gif)

Розетка маршрутизатора служит в качестве места, куда выводятся маршрутизируемые компоненты.

Соответствующий шаблон компонента выглядит следующим образом:

```html
<h1>Angular Router</h1>
<nav>
    <a
        routerLink="/crisis-center"
        routerLinkActive="active"
        ariaCurrentWhenActive="page"
        >Crisis Center</a
    >
    <a
        routerLink="/heroes"
        routerLinkActive="active"
        ariaCurrentWhenActive="page"
        >Heroes</a
    >
</nav>
<router-outlet></router-outlet>
```

### Определение маршрута с подстановочным знаком {: #wildcard}

До сих пор вы создали два маршрута в приложении: один к `/crisis-center` и другой к `/heroes`. Любой другой URL вызывает ошибку маршрутизатора и крах приложения.

Добавьте маршрут с подстановочными знаками, чтобы перехватывать недействительные URL и обрабатывать их изящно. Маршрут с подстановочным знаком имеет путь, состоящий из двух звездочек.

Он соответствует любому URL.

Таким образом, маршрутизатор выбирает этот маршрут с подстановочным знаком, если не может найти маршрут в предыдущей конфигурации.

Маршрут с подстановочным знаком может переходить к пользовательскому компоненту "404 Not Found" или [redirect](#redirect) к существующему маршруту.

!!!note

    Маршрутизатор выбирает маршрут с помощью стратегии [_первое совпадение выигрывает_](router-reference.md#example-config). Поскольку маршрут с подстановочным знаком является наименее специфичным маршрутом, поместите его последним в конфигурации маршрута.

Чтобы проверить эту возможность, добавьте кнопку с `RouterLink` в шаблон `HeroListComponent` и установите ссылку на несуществующий маршрут под названием `"/sidekicks"`.

```html
<h2>HEROES</h2>
<p>Get your heroes here</p>

<button type="button" routerLink="/sidekicks">
    Go to sidekicks
</button>
```

Приложение потерпит неудачу, если пользователь нажмет на эту кнопку, потому что вы еще не определили маршрут `"/sidekicks"`.

Вместо добавления маршрута `sidekicks` определите маршрут `wildcard` и попросите его перейти к `PageNotFoundComponent`.

```ts
{ path: '**', component: PageNotFoundComponent }
```

Создайте компонент `PageNotFoundComponent` для отображения, когда пользователи посещают недопустимые URL.

```shell
ng generate component page-not-found
```

```html
<h2>Page not found</h2>
```

Теперь, когда пользователь посещает `/sidekicks`, или любой другой недействительный URL, браузер выдает "Страница не найдена". Адресная строка браузера продолжает указывать на недопустимый URL.

### Настройка перенаправлений {: #redirect}

Когда приложение запускается, по умолчанию в строке браузера находится начальный URL:

```
localhost:4200
```

Это не соответствует ни одному из жестко закодированных маршрутов, что означает, что маршрутизатор переходит на маршрут с подстановочным знаком и отображает `PageNotFoundComponent`.

Приложению нужен маршрут по умолчанию к действительной странице. Страница по умолчанию для этого приложения - это список героев.

Приложение должно переходить на нее, как если бы пользователь щелкнул по ссылке "Heroes" или вставил `localhost:4200/heroes` в адресную строку.

Добавьте маршрут `redirect`, который переводит исходный относительный URL (`''`) в путь по умолчанию (`/heroes`), который вы хотите.

Добавьте маршрут по умолчанию где-то _выше_ маршрута дикого символа. Он находится чуть выше маршрута wildcard в следующей выдержке, показывающей полный `appRoutes` для этой вехи.

```ts
const appRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisListComponent,
    },
    { path: 'heroes', component: HeroListComponent },
    { path: '', redirectTo: '/heroes', pathMatch: 'full' },
    { path: '**', component: PageNotFoundComponent },
];
```

В адресной строке браузера отображается `.../heroes`, как если бы вы перешли туда напрямую.

Маршрут перенаправления требует свойства `pathMatch`, чтобы указать маршрутизатору, как сопоставить URL с путем маршрута. В этом приложении маршрутизатор должен выбрать маршрут к `HeroListComponent` только тогда, когда _полный URL_ соответствует `''`, поэтому установите значение `pathMatch` в `'full'`.

!!!note "Внимание на pathMatch"

    Технически, `pathMatch = 'full'` приводит к попаданию в маршрут, когда _оставшиеся_, несопоставленные сегменты URL совпадают с `''`. В данном примере перенаправление происходит в маршруте верхнего уровня, поэтому _оставшийся_ URL и _полный_ URL - это одно и то же.

    Другим возможным значением `pathMatch` является `'prefix'`, которое указывает маршрутизатору соответствовать маршруту перенаправления, если оставшийся URL начинается с пути префикса маршрута перенаправления. Это не относится к данному примеру приложения, потому что если бы значение `pathMatch` было `'prefix'`, каждый URL совпадал бы с `'prefix'`.

    Попробуйте установить значение `'prefix'` и нажмите кнопку `Go to sidekicks`. Поскольку это плохой URL, вы должны увидеть страницу "Страница не найдена".

    Вместо этого вы все еще находитесь на странице "Герои".

    Введите плохой URL-адрес в адресную строку браузера.

    Вы будете мгновенно перенаправлены на страницу `/heroes`.

    Каждый URL, хороший или плохой, который попадает в это определение маршрута, является подходящим.

    Маршрут по умолчанию должен перенаправлять на `HeroListComponent` только в том случае, если весь URL имеет вид `''`''. Не забудьте восстановить перенаправление на `pathMatch = 'full'`.

    Узнайте больше в [посте Виктора Савкина о редиректах](https://vsavkin.tumblr.com/post/146722301646/angular-router-empty-paths-componentless-routes).

### Завершение этапа 1

Ваш пример приложения может переключаться между двумя представлениями, когда пользователь нажимает на ссылку.

Этап 1 охватывает следующие действия:

-   Загрузить библиотеку маршрутизатора
-   Добавить навигационную панель в шаблон оболочки с тегами якоря, директивами `routerLink` и `routerLinkActive`.
-   Добавить `router-outlet` в шаблон оболочки, где отображаются представления.
-   Настройте модуль маршрутизатора с помощью `RouterModule.forRoot()`.
-   Настройте маршрутизатор на составление HTML5 URL браузера.
-   Обрабатывать недействительные маршруты с помощью `wildcard`.
-   Переход к маршруту по умолчанию, когда приложение запускается с пустым путем.

Структура стартового приложения выглядит следующим образом:

```
angular-router-tour-of-heroes
+- src
|  +- app
|  |  +- crisis-list
|  |  |  +- crisis-list.component.css
|  |  |  +- crisis-list.component.html
|  |  |	 +- crisis-list.component.ts
|  |  +- hero-list
|  |  |  +- hero-list.component.css
|  |  |	 +- hero-list.component.html
|  |  |	 +- hero-list.component.ts
|  |   +- page-not-found
|  |  |  +- page-not-found.component.css
|  |  |	 +- page-not-found.component.html
|  |  |	 +- page-not-found.component.ts
|  |  +- app.component.css
|  |  +- app.component.html
|  |  +- app.component.ts
|  |  +- app.module.ts
|  +- main.ts
|  +- index.html
|  +- styles.css
|  +- tsconfig.json
+- node_modules &hellip;
+- package.json
```

Вот файлы этой вехи.

=== "app.component.html"

    ```html
    <h1>Angular Router</h1>
    <nav>
    	<a
    		routerLink="/crisis-center"
    		routerLinkActive="active"
    		ariaCurrentWhenActive="page"
    		>Crisis Center</a
    	>
    	<a
    		routerLink="/heroes"
    		routerLinkActive="active"
    		ariaCurrentWhenActive="page"
    		>Heroes</a
    	>
    </nav>
    <router-outlet></router-outlet>
    ```

=== "app.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { FormsModule } from '@angular/forms';
    import { RouterModule, Routes } from '@angular/router';

    import { AppComponent } from './app.component';
    import { CrisisListComponent } from './crisis-list/crisis-list.component';
    import { HeroListComponent } from './hero-list/hero-list.component';
    import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

    const appRoutes: Routes = [
    	{
    		path: 'crisis-center',
    		component: CrisisListComponent,
    	},
    	{ path: 'heroes', component: HeroListComponent },

    	{ path: '', redirectTo: '/heroes', pathMatch: 'full' },
    	{ path: '**', component: PageNotFoundComponent },
    ];

    @NgModule({
    	imports: [
    		BrowserModule,
    		FormsModule,
    		RouterModule.forRoot(
    			appRoutes,
    			{ enableTracing: true } // <-- debugging purposes only
    		),
    	],
    	declarations: [
    		AppComponent,
    		HeroListComponent,
    		CrisisListComponent,
    		PageNotFoundComponent,
    	],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "hero-list/hero-list.component.html"

    ```html
    <h2>HEROES</h2>
    <p>Get your heroes here</p>

    <button type="button" routerLink="/sidekicks">
    	Go to sidekicks
    </button>
    ```

=== "crisis-list/crisis-list.component.html"

    ```html
    <h2>CRISIS CENTER</h2>
    <p>Get your crisis here</p>
    ```

=== "page-not-found/page-not-found.component.html"

    ```html
    <h2>Page not found</h2>
    ```

=== "index.html"

    ```html
    <html lang="en">
    	<head>
    		<!-- Set the base href -->
    		<base href="/" />
    		<title>Angular Router</title>
    		<meta charset="UTF-8" />
    		<meta
    			name="viewport"
    			content="width=device-width, initial-scale=1"
    		/>
    	</head>

    	<body>
    		<app-root></app-root>
    	</body>
    </html>
    ```

## Этап 2: Модуль маршрутизации {: #routing-module}

Этот этап показывает, как настроить специализированный модуль _Модуль маршрутизации_, который хранит конфигурацию маршрутизации вашего приложения.

Модуль маршрутизации имеет несколько характеристик:

-   Отделяет проблемы маршрутизации от других проблем приложения.
-   Предоставляет модуль для замены или удаления при тестировании приложения
-   Обеспечивает известное местоположение для поставщиков услуг маршрутизации, таких как охранники и резолверы.
-   Не объявляет компоненты

### Интегрируйте маршрутизацию в ваше приложение {: #integrate-routing}

Пример приложения с маршрутизацией не включает маршрутизацию по умолчанию. Когда вы используете [Angular CLI](https://angular.io/cli) для создания проекта, который использует маршрутизацию, установите опцию `--routing` для проекта или приложения, а также для каждого NgModule.

Когда вы создаете или инициализируете новый проект (используя команду CLI [`ng new`](https://angular.io/cli/new)) или новое приложение (используя команду [`ng generate app`](https://angular.io/cli/generate)), укажите опцию `--routing`.

Это даст команду CLI включить пакет `@angular/router` npm и создать файл с именем `app-routing.module.ts`.

Затем вы сможете использовать маршрутизацию в любом Ng-модуле, который вы добавите в проект или приложение.

Например, следующая команда создает NgModule, который может использовать маршрутизацию.

```shell
ng generate module my-module --routing
```

Это создает отдельный файл `my-module-routing.module.ts` для хранения маршрутов NgModule. Файл включает пустой объект `Routes`, который вы можете заполнить маршрутами к различным компонентам и NgModules.

### Рефакторинг конфигурации маршрутизации в модуль маршрутизации {: #routing-refactor}

Создайте модуль `AppRouting` в папке `/app`, который будет содержать конфигурацию маршрутизации.

```shell
ng generate module app-routing --module app --flat
```

Импортируйте символы `CrisisListComponent`, `HeroListComponent` и `PageNotFoundComponent`, как вы это сделали в `app.module.ts`. Затем перенесите импорт `Router` и конфигурацию маршрутизации, включая `RouterModule.forRoot()`, в этот модуль маршрутизации.

Реэкспортируйте модуль Angular `RouterModule`, добавив его в массив `exports` модуля. Благодаря реэкспорту `RouterModule` здесь, компоненты, объявленные в `AppModule`, получают доступ к директивам маршрутизации, таким как `RouterLink` и `RouterOutlet`.

После этих шагов файл должен выглядеть следующим образом.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CrisisListComponent } from './crisis-list/crisis-list.component';
import { HeroListComponent } from './hero-list/hero-list.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const appRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisListComponent,
    },
    { path: 'heroes', component: HeroListComponent },
    { path: '', redirectTo: '/heroes', pathMatch: 'full' },
    { path: '**', component: PageNotFoundComponent },
];

@NgModule({
    imports: [
        RouterModule.forRoot(
            appRoutes,
            { enableTracing: true } // <-- debugging purposes only
        ),
    ],
    exports: [RouterModule],
})
export class AppRoutingModule {}
```

Далее обновите файл `app.module.ts`, удалив `RouterModule.forRoot` в массиве `imports`.

```ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

import { CrisisListComponent } from './crisis-list/crisis-list.component';
import { HeroListComponent } from './hero-list/hero-list.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

@NgModule({
    imports: [BrowserModule, FormsModule, AppRoutingModule],
    declarations: [
        AppComponent,
        HeroListComponent,
        CrisisListComponent,
        PageNotFoundComponent,
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

!!!note ""

    Позже в этом руководстве будет показано, как создать [несколько модулей маршрутизации](#heroes-functionality) и импортировать эти модули маршрутизации [в правильном порядке](#routing-module-order).

Приложение продолжает работать точно так же, и вы можете использовать `AppRoutingModule` в качестве центрального места для сохранения будущей конфигурации маршрутизации.

### Преимущества модуля маршрутизации {: #why-routing-module}

Модуль маршрутизации, часто называемый `AppRoutingModule`, заменяет конфигурацию маршрутизации в корневом или функциональном модуле.

Модуль маршрутизации полезен по мере роста вашего приложения и когда конфигурация включает специализированные функции `guard` и `resolver`.

Некоторые разработчики пропускают модуль маршрутизации, когда конфигурация минимальна, и объединяют конфигурацию маршрутизации непосредственно в сопутствующий модуль (например, `AppModule`).

Большинство приложений должны реализовать модуль маршрутизации для согласованности. Он сохраняет код чистым, когда конфигурация становится сложной.

Он облегчает тестирование функционального модуля.

Его существование привлекает внимание к тому, что модуль маршрутизирован.

Именно здесь разработчики ожидают найти и расширить конфигурацию маршрутизации.

## Веха 3: Функция героев {: #heroes-feature}

Этот этап включает в себя следующее:

-   Организация приложения и маршрутов в области функций с помощью модулей.
-   Императивная навигация от одного компонента к другому.
-   Передача необходимой и необязательной информации в параметрах маршрута.

Этот пример приложения воссоздает функцию героев в разделе "Услуги" учебника [Tour of Heroes](toh-pt4.md) и использует большую часть кода из [Код примера Tour of Heroes: Услуги](https://angular.io/generated/live-examples/toh-pt4/stackblitz.html).

Типичное приложение имеет несколько функциональных областей, каждая из которых посвящена определенной бизнес-цели и имеет свою собственную папку.

В этом разделе показано, как рефакторить приложение на различные функциональные модули, импортировать их в главный модуль и перемещаться между ними.

### Добавить функциональность героев {: #heroes-functionality}

Выполните следующие шаги:

-   Для управления героями создайте `HeroesModule` с маршрутизацией в папке heroes и зарегистрируйте его в корневом `AppModule`.

    ```shell
    ng generate module heroes/heroes --module app --flat --routing
    ```

-   Переместите папку placeholder `hero-list`, находящуюся в папке `app`, в папку `heroes`.

-   Скопируйте содержимое `heroes/heroes.component.html` из [учебника "Services"](https://angular.io/generated/live-examples/toh-pt4/stackblitz.html) в шаблон `hero-list.component.html`.

    -   Переименуйте `<h2>` в `<h2>HEROES</h2>`.

    -   Удалите компонент `<app-hero-detail>` в нижней части шаблона.

-   Скопируйте содержимое файла `heroes/heroes.component.css` из живого примера в файл `hero-list.component.css`.

-   Скопируйте содержимое `heroes/heroes.component.ts` из живого примера в файл `hero-list.component.ts`.

    -   Измените имя класса компонента на `HeroListComponent`.

    -   Измените `selector` на `app-hero-list`.

        !!!note ""

            Селекторы не требуются для маршрутизируемых компонентов, поскольку компоненты динамически вставляются при отображении страницы.

            Однако они полезны для их идентификации и назначения в дереве элементов HTML.

-   Скопируйте папку `hero-detail`, файлы `hero.ts`, `hero.service.ts` и `mock-heroes.ts` в подпапку `heroes`.

-   Скопируйте файл `message.service.ts` в папку `src/app`.

-   Обновите импорт относительного пути к `message.service` в файле `hero.service.ts`.

Далее обновите метаданные `HeroesModule`.

-   Импортируйте и добавьте `HeroDetailComponent` и `HeroListComponent` в массив `declarations` в `HeroesModule`.

```ts
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { HeroListComponent } from './hero-list/hero-list.component';
import { HeroDetailComponent } from './hero-detail/hero-detail.component';

import { HeroesRoutingModule } from './heroes-routing.module';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        HeroesRoutingModule,
    ],
    declarations: [HeroListComponent, HeroDetailComponent],
})
export class HeroesModule {}
```

Структура файлов управления героями выглядит следующим образом:

```
src/app/heroes
+- hero-detail
|  +- hero-detail.component.css
|  +- hero-detail.component.html
|  +- hero-detail.component.ts
+- hero-list
|  +- hero-list.component.css
|  +- hero-list.component.html
|  +- hero-list.component.ts
+- hero.service.ts
+- hero.ts
+- heroes-routing.module.ts
+- heroes.module.ts
+- mock-heroes.ts
```

#### Требования к маршрутизации функции героев {: #hero-routing-requirements}

Функция героев состоит из двух взаимодействующих компонентов - списка героев и подробной информации о героях. Когда вы переходите к представлению списка, оно получает список героев и отображает их.

Когда вы нажимаете на героя, вид детализации должен отобразить именно этого героя.

Вы указываете детальному представлению, какого героя отображать, включив идентификатор выбранного героя в URL маршрута.

Импортируйте компоненты героев из их новых мест в папке `src/app/heroes/` и определите два маршрута героев.

Теперь, когда у вас есть маршруты для модуля `Heroes`, зарегистрируйте их в `Router` с помощью `RouterModule`, как вы это делали в `AppRoutingModule`, с важным отличием.

В модуле `AppRoutingModule` вы использовали статический метод `RouterModule.forRoot()` для регистрации маршрутов и поставщиков услуг уровня приложения. В функциональном модуле вы используете статический метод `forChild()`.

!!!note ""

    Вызывайте `RouterModule.forRoot()` только в корневом `AppRoutingModule` (или `AppModule`, если в нем вы регистрируете маршруты приложений верхнего уровня).
    В любом другом модуле вы должны вызвать метод `RouterModule.forChild()` для регистрации дополнительных маршрутов.

Обновленный `HeroesRoutingModule` выглядит следующим образом:

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HeroListComponent } from './hero-list/hero-list.component';
import { HeroDetailComponent } from './hero-detail/hero-detail.component';

const heroesRoutes: Routes = [
    { path: 'heroes', component: HeroListComponent },
    { path: 'hero/:id', component: HeroDetailComponent },
];

@NgModule({
    imports: [RouterModule.forChild(heroesRoutes)],
    exports: [RouterModule],
})
export class HeroesRoutingModule {}
```

!!!note ""

    Рассмотрите возможность предоставления каждому функциональному модулю собственного файла конфигурации маршрута. Хотя в настоящее время маршруты функций минимальны, маршруты имеют тенденцию к усложнению даже в небольших приложениях.

#### Удаление дубликатов маршрутов героев {: #remove-duplicate-hero-routes}

Маршруты героев в настоящее время определяются в двух местах: в `HeroesRoutingModule`, посредством `HeroesModule`, и в `AppRoutingModule`.

Маршруты, предоставляемые функциональными модулями, объединяются маршрутизатором в маршруты их импортированного модуля. Это позволяет вам продолжать определять маршруты функциональных модулей без изменения конфигурации основных маршрутов.

Удалите импорт `HeroListComponent` и маршрут `/heroes` из файла `app-routing.module.ts`.

Оставьте маршруты по умолчанию и wildcard, так как они все еще используются на верхнем уровне приложения.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CrisisListComponent } from './crisis-list/crisis-list.component';
// import { HeroListComponent } from './hero-list/hero-list.component';  // <-- delete this line
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const appRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisListComponent,
    },
    // { path: 'heroes',     component: HeroListComponent }, // <-- delete this line
    { path: '', redirectTo: '/heroes', pathMatch: 'full' },
    { path: '**', component: PageNotFoundComponent },
];

@NgModule({
    imports: [
        RouterModule.forRoot(
            appRoutes,
            { enableTracing: true } // <-- debugging purposes only
        ),
    ],
    exports: [RouterModule],
})
export class AppRoutingModule {}
```

#### Удалите декларации героев {: #merge-hero-routes}

Поскольку `HeroesModule` теперь предоставляет `HeroListComponent`, удалите его из массива `declarations` модуля `AppModule`. Теперь, когда у вас есть отдельный `HeroesModule`, вы можете развивать функцию героя с помощью большего количества компонентов и различных маршрутов.

После этих шагов `AppModule` должен выглядеть следующим образом:

```ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { HeroesModule } from './heroes/heroes.module';

import { CrisisListComponent } from './crisis-list/crisis-list.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HeroesModule,
        AppRoutingModule,
    ],
    declarations: [
        AppComponent,
        CrisisListComponent,
        PageNotFoundComponent,
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

### Порядок импорта модулей {: #routing-module-order}

Обратите внимание, что в массиве `импортов` модулей, `AppRoutingModule` стоит последним и идет _после_ `HeroesModule`.

```ts
imports: [
  BrowserModule,
  FormsModule,
  HeroesModule,
  AppRoutingModule
],
```

Порядок конфигурации маршрутов важен, потому что маршрутизатор принимает первый маршрут, который соответствует пути навигационного запроса.

Когда все маршруты были в одном `AppRoutingModule`, вы поместили маршруты по умолчанию и [wildcard](#wildcard) последними, после маршрута `/heroes`, чтобы у маршрутизатора был шанс сопоставить URL с маршрутом `/heroes` _до_ попадания на маршрут wildcard и перехода к "Страница не найдена".

Каждый модуль маршрутизации дополняет конфигурацию маршрута в порядке импорта. Если вы перечислили `AppRoutingModule` первым, маршрут wildcard будет зарегистрирован _перед_ маршрутами героев.

Маршрут дикого знака &mdash; который соответствует _каждому_ URL&mdash; будет перехватывать попытку перехода к маршруту героя.

!!!note ""

    Пересмотрите модули маршрутизации, чтобы увидеть, как щелчок по ссылке героев приводит к "Страница не найдена". Узнайте о проверке конфигурации маршрутизатора во время выполнения [ниже](#inspect-config).

### Параметры маршрута

#### Определение маршрута с параметром {: #route-def-with-parameter}

Вернитесь к модулю `HeroesRoutingModule` и снова посмотрите на определения маршрутов. Маршрут к `HeroDetailComponent` имеет токен `:id` в пути.

```ts
{ path: 'hero/:id', component: HeroDetailComponent }
```

Токен `:id` создает слот в пути для параметра маршрута. В данном случае эта конфигурация заставляет маршрутизатор вставить `id` героя в этот слот.

Если вы скажете маршрутизатору перейти к компоненту detail и отобразить "Magneta", вы ожидаете, что ID героя появится в URL браузера следующим образом:

```
localhost:4200/hero/15
```

Если пользователь введет этот URL в адресную строку браузера, маршрутизатор должен распознать шаблон и перейти к тому же детальному представлению "Magneta".

!!!note "Параметр маршрута: Обязательный или необязательный?"

    Встраивание маркера параметра маршрута, `:id`, в путь определения маршрута является хорошим выбором для данного сценария, поскольку `id` _требуется_ компонентом `HeroDetailComponent` и поскольку значение `15` в пути четко отличает маршрут к "Magneta" от маршрута к какому-либо другому герою.

#### Установка параметров маршрута в представлении списка {: #route-parameters}

После перехода к компоненту `HeroDetailComponent` вы ожидаете увидеть подробную информацию о выбранном герое. Вам нужны две части информации: путь маршрутизации к компоненту и `id` героя.

Соответственно, массив _параметров ссылки_ состоит из двух элементов: _путь маршрутизации_ и _параметр маршрута_, который определяет `id` выбранного героя.

```html
<a [routerLink]="['/hero', hero.id]"></a>
```

Маршрутизатор составляет URL назначения из массива следующим образом: `localhost:4200/hero/15`.

Маршрутизатор извлекает параметр маршрута (`id:15`) из URL и передает его в `HeroDetailComponent` с помощью сервиса `ActivatedRoute`.

### `Активированный маршрут` в действии {: #activated-route-in-action}

Импортируйте токены `Router`, `ActivatedRoute` и `ParamMap` из пакета router.

```ts
import {
    Router,
    ActivatedRoute,
    ParamMap,
} from '@angular/router';
```

Импортируйте оператор `switchMap`, поскольку он понадобится вам позже для обработки параметров маршрута `Observable`.

```ts
import { switchMap } from 'rxjs/operators';
```

Добавьте сервисы как приватные переменные в конструктор, чтобы Angular инжектировал их (сделал их видимыми для компонента).

```ts
constructor(
  private route: ActivatedRoute,
  private router: Router,
  private service: HeroService
) {}
```

В методе `ngOnInit()` используйте службу `ActivatedRoute` для получения параметров маршрута, извлечения `id` героя из параметров и получения героя для отображения.

```ts
ngOnInit() {
  this.hero$ = this.route.paramMap.pipe(
    switchMap((params: ParamMap) =>
      this.service.getHero(params.get('id')!))
  );
}
```

Когда карта изменяется, `paramMap` получает параметр `id` из измененных параметров.

Затем вы говорите `HeroService` получить героя с этим `id` и возвращаете результат запроса `HeroService`.

Оператор `switchMap` делает две вещи. Он сглаживает `Observable<Hero>`, который возвращает `HeroService`, и отменяет предыдущие ожидающие запросы.

Если пользователь повторно переходит на этот маршрут с новым `id`, в то время как `HeroService` все еще получает старый `id`, `switchMap` отбрасывает старый запрос и возвращает героя для нового `id`.

`AsyncPipe` обрабатывает наблюдаемую подписку, и свойство `hero` компонента будет установлено с полученным героем.

#### `ParamMap` API

API `ParamMap` вдохновлен интерфейсом [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams). Он предоставляет методы для обработки доступа к параметрам как для параметров маршрута (`paramMap`), так и для параметров запроса (`queryParamMap`).

| Member         | Details                                                                                                                                                                                                                   |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `has(name)`    | Возвращает `true`, если имя параметра есть в карте параметров.                                                                                                                                                            |
| `get(name)`    | Возвращает значение имени параметра (строку), если оно есть, или `null`, если имя параметра отсутствует в карте параметров. Возвращает _первый_ элемент, если значение параметра представляет собой массив значений.      |
| `getAll(name)` | Возвращает `строковый массив` значений имени параметра, если он найден, или пустой `массив`, если значение имени параметра отсутствует в карте. Используйте `getAll`, когда один параметр может иметь несколько значений. |
| `keys`         | Возвращает массив `строк` всех имен параметров в карте.                                                                                                                                                                   |

#### Observable `paramMap` и повторное использование компонентов {: #reuse}

В этом примере вы получаете карту параметров маршрута из `Observable`. Это означает, что карта параметров маршрута может меняться в течение жизни этого компонента.

По умолчанию маршрутизатор повторно использует экземпляр компонента при повторном переходе к одному и тому же типу компонента без предварительного посещения другого компонента. Параметры маршрута могут меняться каждый раз.

Предположим, на навигационной панели родительского компонента есть кнопки "вперед" и "назад", которые прокручивают список героев. Каждое нажатие кнопки обязательно приводило к переходу к `HeroDetailComponent` со следующим или предыдущим `id`.

Вы не хотите, чтобы маршрутизатор удалял текущий экземпляр `HeroDetailComponent` из DOM только для того, чтобы заново создать его для следующего `id`, так как это приведет к повторному рендерингу представления. Для улучшения UX маршрутизатор повторно использует один и тот же экземпляр компонента и обновляет параметр.

Поскольку `ngOnInit()` вызывается только один раз при инстанцировании компонента, вы можете определить, когда параметры маршрута изменяются _в пределах одного и того же экземпляра_, используя наблюдаемое свойство `paramMap`.

!!!note ""

    При подписке на наблюдаемую переменную в компоненте вы почти всегда отписываетесь от нее, когда компонент уничтожается.

    Однако наблюдаемые `ActivatedRoute` являются исключением, поскольку `ActivatedRoute` и его наблюдаемые изолированы от самого `Router`. Маршрутизатор" уничтожает маршрутизируемый компонент, когда он больше не нужен.

    Это означает, что все члены компонента также будут уничтожены, включая инжектированный `ActivatedRoute` и подписки на его свойства `Observable`.

    Маршрутизатор не `завершает` ни одну `обсервируемую` из `ActivatedRoute`, поэтому любые блоки `finalize` или `complete` не будут выполняться. Если вам нужно обработать что-то в `finalize`, вам все равно нужно отписаться в `ngOnDestroy`.

    Вы также должны отписаться, если в вашем наблюдаемом пайпе есть задержка с кодом, который вы не хотите запускать после уничтожения компонента.

#### `snapshot`: ненаблюдаемая альтернатива {: #snapshot}

Это приложение не будет повторно использовать `HeroDetailComponent`. Пользователь всегда возвращается к списку героев, чтобы выбрать другого героя для просмотра.

Невозможно перейти от одной детали героя к другой детали героя без посещения компонента списка между ними.

Поэтому маршрутизатор каждый раз создает новый экземпляр `HeroDetailComponent`.

Когда вы точно знаете, что экземпляр `HeroDetailComponent` никогда не будет использоваться повторно, вы можете использовать `snapshot`.

`route.snapshot` предоставляет начальное значение карты параметров маршрута. Вы можете получить доступ к параметрам напрямую, без подписки или добавления операторов наблюдения, как показано ниже:

```ts
ngOnInit() {
  const id = this.route.snapshot.paramMap.get('id')!;

  this.hero$ = this.service.getHero(id);
}
```

!!!note ""

    При использовании этой техники `snapshot` получает только начальное значение карты параметров. Используйте подход с наблюдаемой `paramMap`, если есть вероятность, что маршрутизатор может повторно использовать компонент.
    В этом учебном примере приложения используется наблюдаемая `paramMap`.

### Навигация назад к компоненту списка {: #nav-to-list}

Кнопка "Назад" компонента `HeroDetailComponent` использует метод `gotoHeroes()`, который принудительно перемещает обратно к компоненту `HeroListComponent`.

Метод маршрутизатора `navigate()` принимает тот же массив параметров _ссылки_ из одного элемента, который вы можете связать с директивой `[routerLink]`. Он содержит путь к компоненту `HeroListComponent`:

```ts
gotoHeroes() {
  this.router.navigate(['/heroes']);
}
```

#### Параметры маршрута: Обязательные или необязательные? {: #optional-route-parameters}

Используйте [route parameters](#route-parameters) для указания обязательного значения параметра в URL маршрута, как при переходе к `HeroDetailComponent` для просмотра героя с `id` 15:

```
localhost:4200/hero/15
```

Вы также можете добавить необязательную информацию в запрос маршрута. Например, при возврате к списку `hero-detail.component.ts` из представления деталей героя было бы неплохо, если бы просматриваемый герой был предварительно выбран в списке.

![Selected hero](selected-hero.png)

Вы реализуете эту возможность, включив `id` просматриваемого героя в URL в качестве необязательного параметра при возврате из `HeroDetailComponent`.

Необязательная информация может также включать другие формы, такие как:

-   Свободно структурированные критерии поиска; например, `name='wind*'`.
-   Множественные значения; например, `after='12/31/2015' & before='1/1/2017'` &mdash; без особого порядка &mdash; `before='1/1/2017' & after='12/31/2015'` &mdash; в различных форматах &mdash; `during='currentYear'`.

Поскольку такие параметры не вписываются в путь URL, вы можете использовать необязательные параметры для передачи произвольно сложной информации во время навигации. Необязательные параметры не участвуют в сопоставлении шаблонов и обеспечивают гибкость выражения.

Маршрутизатор поддерживает навигацию с необязательными параметрами так же, как и с обязательными параметрами маршрута. Определите необязательные параметры в отдельном объекте _после_ определения обязательных параметров маршрута.

В общем случае, используйте обязательный параметр маршрута, когда значение является обязательным (например, если необходимо отличить один путь маршрута от другого); и необязательный параметр, когда значение является необязательным, сложным и/или многомерным.

#### Список героев: опциональный выбор героя {: #optionally-selecting}

При переходе к компоненту `HeroDetailComponent` вы указали требуемый `id` редактируемого героя в параметре маршрута и сделали его вторым элементом массива [_link parameters array_](#link-parameters-array).

```html
<a [routerLink]="['/hero', hero.id]"></a>
```

Маршрутизатор встроил значение `id` в навигационный URL, потому что вы определили его как параметр маршрута с маркером-заполнителем `:id` в маршруте `path`:

```ts
{ path: 'hero/:id', component: HeroDetailComponent }
```

Когда пользователь нажимает кнопку "Назад", `HeroDetailComponent` создает другой массив _параметров ссылок_, который он использует для перехода обратно к `HeroListComponent`.

```ts
gotoHeroes() {
  this.router.navigate(['/heroes']);
}
```

В этом массиве отсутствует параметр route, потому что ранее вам не нужно было отправлять информацию в `HeroListComponent`.

Теперь отправьте `id` текущего героя с навигационным запросом, чтобы `HeroListComponent` мог выделить этого героя в своем списке.

Отправьте `id` с объектом, который содержит необязательный параметр `id`. Для демонстрации в объекте есть дополнительный параметр (`foo`), который `HeroListComponent` должен игнорировать.

Вот пересмотренный навигационный оператор:

```ts
gotoHeroes(hero: Hero) {
  const heroId = hero ? hero.id : null;
  // Pass along the hero id if available
  // so that the HeroList component can select that hero.
  // Include a junk 'foo' property for fun.
  this.router.navigate(['/heroes', { id: heroId, foo: 'foo' }]);
}
```

Приложение по-прежнему работает. Нажатие кнопки "назад" возвращает к представлению списка героев.

Посмотрите на адресную строку браузера.

Она должна выглядеть примерно так, в зависимости от того, где вы ее запустили:

```
localhost:4200/heroes;id=15;foo=foo
```

Значение `id` отображается в URL как (`;id=15;foo=foo`), а не в пути URL. Путь для маршрута "Герои" не содержит токена `:id`.

Необязательные параметры маршрута не разделены символами "?" и "&", как это было бы в строке запроса URL. Они разделяются точкой с запятой ";".

Это матричная нотация URL.

!!!note ""

    Матричная нотация URL - это идея, впервые представленная в [предложении 1996 года](https://www.w3.org/DesignIssues/MatrixURIs.html) основателем Интернета Тимом Бернерсом-Ли.

    Хотя матричная нотация так и не вошла в стандарт HTML, она является легальной и стала популярной среди систем маршрутизации браузеров как способ изолировать параметры, принадлежащие родительским и дочерним маршрутам. Таким образом, Router обеспечивает поддержку матричной нотации во всех браузерах.

### Параметры маршрута в сервисе `ActivatedRoute` {: #route-parameters-activated-route}

В текущем состоянии разработки список героев не изменяется. Ни одна строка героев не выделена.

Для `HeroListComponent` необходим код, который ожидает параметры.

Ранее, при переходе от `HeroListComponent` к `HeroDetailComponent`, вы подписывались на карту параметров маршрута `Observable` и делали ее доступной для `HeroDetailComponent`

в службе `ActivatedRoute`.

Вы внедрили этот сервис в конструктор `HeroDetailComponent`.

На этот раз вы будете перемещаться в обратном направлении, от `HeroDetailComponent` к `HeroListComponent`.

Сначала расширьте оператор импорта маршрутизатора, включив в него служебный символ `ActivatedRoute`:

```ts
import { ActivatedRoute } from '@angular/router';
```

Импортируйте оператор `switchMap` для выполнения операции над `Observable` карты параметров маршрута.

```ts
import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';
```

Вставьте `ActivatedRoute` в конструктор `HeroListComponent`.

```ts
export class HeroListComponent implements OnInit {
    heroes$!: Observable<Hero[]>;
    selectedId = 0;

    constructor(
        private service: HeroService,
        private route: ActivatedRoute
    ) {}

    ngOnInit() {
        this.heroes$ = this.route.paramMap.pipe(
            switchMap((params) => {
                this.selectedId = parseInt(
                    params.get('id')!,
                    10
                );
                return this.service.getHeroes();
            })
        );
    }
}
```

Свойство `ActivatedRoute.paramMap` представляет собой `Observable` карту параметров маршрута. При переходе пользователя к компоненту `paramMap` выдает новую карту значений, включающую `id`.

В функции `ngOnInit()` вы подписываетесь на эти значения, устанавливаете `selectedId` и получаете героев.

Обновите шаблон с помощью [class binding](class-binding.md). Привязка добавляет CSS-класс `selected`, когда сравнение возвращает `true`, и удаляет его, когда `false`.

Ищите его в повторяющемся теге `<li>`, как показано здесь:

```html
<h2>Heroes</h2>
<ul class="heroes">
    <li
        *ngFor="let hero of heroes$ | async"
        [class.selected]="hero.id === selectedId"
    >
        <a [routerLink]="['/hero', hero.id]">
            <span class="badge">{{ hero.id }}</span>{{
            hero.name }}
        </a>
    </li>
</ul>

<button type="button" routerLink="/sidekicks">
    Go to sidekicks
</button>
```

Добавьте несколько стилей для применения при выборе героя.

```css
.heroes .selected a {
    background-color: #d6e6f7;
}

.heroes .selected a:hover {
    background-color: #bdd7f5;
}
```

Когда пользователь переходит от списка героев к герою "Magneta" и обратно, "Magneta" отображается выбранной:

![Выбранный герой в списке имеет разный цвет фона](selected-hero.png)

Необязательный параметр маршрута `foo` безвреден, и маршрутизатор продолжает его игнорировать.

### Добавление маршрутизируемых анимаций {: #route-animation}

В этом разделе показано, как добавить некоторые [анимации](animations.md) в `HeroDetailComponent`.

Сначала импортируйте `BrowserAnimationsModule` и добавьте его в массив `imports`:

```ts
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  imports: [
    BrowserAnimationsModule,
  ],
})
```

Далее, добавьте объект `data` в маршруты для `HeroListComponent` и `HeroDetailComponent`. Переходы основаны на `states`, и вы используете данные `animation` из маршрута, чтобы предоставить именованную анимацию [`state`](https://angular.io/api/animations/state) для переходов.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HeroListComponent } from './hero-list/hero-list.component';
import { HeroDetailComponent } from './hero-detail/hero-detail.component';

const heroesRoutes: Routes = [
    {
        path: 'heroes',
        component: HeroListComponent,
        data: { animation: 'heroes' },
    },
    {
        path: 'hero/:id',
        component: HeroDetailComponent,
        data: { animation: 'hero' },
    },
];

@NgModule({
    imports: [RouterModule.forChild(heroesRoutes)],
    exports: [RouterModule],
})
export class HeroesRoutingModule {}
```

Создайте файл `animations.ts` в корневой папке `src/app/`. Его содержимое выглядит следующим образом:

```ts
import {
    trigger,
    animateChild,
    group,
    transition,
    animate,
    style,
    query,
} from '@angular/animations';

// Routable animations
export const slideInAnimation = trigger('routeAnimation', [
    transition('heroes <=> hero', [
        style({ position: 'relative' }),
        query(':enter, :leave', [
            style({
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
            }),
        ]),
        query(':enter', [style({ left: '-100%' })]),
        query(':leave', animateChild()),
        group([
            query(':leave', [
                animate(
                    '300ms ease-out',
                    style({ left: '100%' })
                ),
            ]),
            query(':enter', [
                animate(
                    '300ms ease-out',
                    style({ left: '0%' })
                ),
            ]),
        ]),
        query(':enter', animateChild()),
    ]),
]);
```

Этот файл делает следующее:

-   Импортирует символы анимации, которые создают триггеры анимации, контролируют состояние и управляют переходами между состояниями.
-   Экспортирует константу с именем `slideInAnimation`, установленную на триггер анимации с именем `routeAnimation`.
-   Определяет один переход при переключении между маршрутами `героев` и `героев` для облегчения входа компонента с левой стороны экрана, когда он входит в представление приложения (`:enter`), другой для анимации компонента справа, когда он покидает представление приложения (`:leave`)

Вернитесь в `AppComponent`, импортируйте токен `RouterOutlet` из пакета `@angular/router` и `slideInAnimation` из `'./animations.ts`.

Добавьте массив `animations` в метаданные `@Component`, содержащие `slideInAnimation`.

```ts
import { ChildrenOutletContexts } from '@angular/router';
import { slideInAnimation } from './animations';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.css'],
  animations: [ slideInAnimation ]
})
```

Чтобы использовать маршрутизируемые анимации, оберните `RouterOutlet` внутри элемента, используйте триггер `@routeAnimation` и привяжите его к элементу.

Чтобы `@routeAnimation` переходила в состояния выключения ключа, предоставьте ей `данные` из `ActivatedRoute`. Переменная `RouterOutlet` раскрывается как переменная шаблона `outlet`, поэтому вы привязываете ссылку на выход маршрутизатора.

В данном примере используется переменная `routerOutlet`.

```html
<h1>Angular Router</h1>
<nav>
    <a
        routerLink="/crisis-center"
        routerLinkActive="active"
        ariaCurrentWhenActive="page"
        >Crisis Center</a
    >
    <a
        routerLink="/heroes"
        routerLinkActive="active"
        ariaCurrentWhenActive="page"
        >Heroes</a
    >
</nav>
<div [@routeAnimation]="getAnimationData()">
    <router-outlet></router-outlet>
</div>
```

Свойство `@routeAnimation` связано с `getAnimationData()`, которое возвращает свойство анимации из `данных`, предоставленных основным маршрутом. Свойство `animation` соответствует именам `transition`, которые вы использовали в `slideInAnimation`, определенном в `animations.ts`.

```ts
export class AppComponent {
    constructor(private contexts: ChildrenOutletContexts) {}

    getAnimationData() {
        return this.contexts.getContext('primary')?.route
            ?.snapshot?.data?.['animation'];
    }
}
```

При переключении между двумя маршрутами, `HeroDetailComponent` и `HeroListComponent` теперь облегчаются слева при маршрутизации к, и сдвигаются вправо при навигации прочь.

### Завершение этапа 3 {: #milestone-3-wrap-up}

В этом разделе было рассмотрено следующее:

-   Организация приложения по функциональным областям
-   Императивная навигация от одного компонента к другому
-   Передача информации в параметрах маршрута и подписка на них в компоненте
-   Импорт функциональной области NgModule в `AppModule`.
-   Применение маршрутизируемых анимаций на основе страницы.

После этих изменений структура папок выглядит следующим образом:

```
angular-router-tour-of-heroes
+- src
|  +- app
|  |  +- crisis-list
|  |  |  +- crisis-list.component.css
|  |  |  +- crisis-list.component.html
|  |  |  +- crisis-list.component.ts
|  |  +- heroes
|  |  |  +- hero-detail
|  |  |  |  +- hero-detail.component.css
|  |  |  |  +- hero-detail.component.html
|  |  |  |  +- hero-detail.component.ts
|  |  |  +- hero-list
|  |  |  |  +- hero-list.component.css
|  |  |  |  +- hero-list.component.html
|  |  |  |  +- hero-list.component.ts
|  |  |  +- hero.service.ts
|  |  |  +- hero.ts
|  |  |  +- heroes-routing.module.ts
|  |  |  +- heroes.module.ts
|  |  |  +- mock-heroes.ts
|  |  +- page-not-found
|  |  |  +- page-not-found.component.css
|  |  |  +- page-not-found.component.html
|  |  |  +- page-not-found.component.ts
|  +- animations.ts
|  +- app.component.css
|  +- app.component.html
|  +- app.component.ts
|  +- app.module.ts
|  +- app-routing.module.ts
|  +- main.ts
|  +- message.service.ts
|  +- index.html
|  +- styles.css
|  +- tsconfig.json
+- node_modules …
+- package.json
```

Вот соответствующие файлы для этой версии примера приложения.

=== "animations.ts"

    ```ts
    import {
    	trigger,
    	animateChild,
    	group,
    	transition,
    	animate,
    	style,
    	query,
    } from '@angular/animations';

    // Routable animations
    export const slideInAnimation = trigger('routeAnimation', [
    	transition('heroes <=> hero', [
    		style({ position: 'relative' }),
    		query(':enter, :leave', [
    			style({
    				position: 'absolute',
    				top: 0,
    				left: 0,
    				width: '100%',
    			}),
    		]),
    		query(':enter', [style({ left: '-100%' })]),
    		query(':leave', animateChild()),
    		group([
    			query(':leave', [
    				animate(
    					'300ms ease-out',
    					style({ left: '100%' })
    				),
    			]),
    			query(':enter', [
    				animate(
    					'300ms ease-out',
    					style({ left: '0%' })
    				),
    			]),
    		]),
    		query(':enter', animateChild()),
    	]),
    ]);
    ```

=== "app.component.html"

    ```html
    <h1>Angular Router</h1>
    <nav>
    	<a
    		routerLink="/crisis-center"
    		routerLinkActive="active"
    		ariaCurrentWhenActive="page"
    		>Crisis Center</a
    	>
    	<a
    		routerLink="/heroes"
    		routerLinkActive="active"
    		ariaCurrentWhenActive="page"
    		>Heroes</a
    	>
    </nav>
    <div [@routeAnimation]="getAnimationData()">
    	<router-outlet></router-outlet>
    </div>
    ```

=== "app.component.ts"

    ```ts
    import { Component } from '@angular/core';
    import { ChildrenOutletContexts } from '@angular/router';
    import { slideInAnimation } from './animations';

    @Component({
    	selector: 'app-root',
    	templateUrl: 'app.component.html',
    	styleUrls: ['app.component.css'],
    	animations: [slideInAnimation],
    })
    export class AppComponent {
    	constructor(private contexts: ChildrenOutletContexts) {}

    	getAnimationData() {
    		return this.contexts.getContext('primary')?.route
    			?.snapshot?.data?.['animation'];
    	}
    }
    ```

=== "app.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { FormsModule } from '@angular/forms';
    import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

    import { AppComponent } from './app.component';
    import { AppRoutingModule } from './app-routing.module';
    import { HeroesModule } from './heroes/heroes.module';

    import { CrisisListComponent } from './crisis-list/crisis-list.component';
    import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

    @NgModule({
    	imports: [
    		BrowserModule,
    		BrowserAnimationsModule,
    		FormsModule,
    		HeroesModule,
    		AppRoutingModule,
    	],
    	declarations: [
    		AppComponent,
    		CrisisListComponent,
    		PageNotFoundComponent,
    	],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "app-routing.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { RouterModule, Routes } from '@angular/router';

    import { CrisisListComponent } from './crisis-list/crisis-list.component';
    /* . . . */
    import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

    const appRoutes: Routes = [
    	{
    		path: 'crisis-center',
    		component: CrisisListComponent,
    	},
    	/* . . . */
    	{ path: '', redirectTo: '/heroes', pathMatch: 'full' },
    	{ path: '**', component: PageNotFoundComponent },
    ];

    @NgModule({
    	imports: [
    		RouterModule.forRoot(
    			appRoutes,
    			{ enableTracing: true } // <-- debugging purposes only
    		),
    	],
    	exports: [RouterModule],
    })
    export class AppRoutingModule {}
    ```

=== "hero-list.component.css"

    ```css
    /* HeroListComponent's private CSS styles */
    .heroes {
    	margin: 0 0 2em 0;
    	list-style-type: none;
    	padding: 0;
    	width: 100%;
    }
    .heroes li {
    	position: relative;
    	cursor: pointer;
    }

    .heroes li:hover {
    	left: 0.1em;
    }

    .heroes a {
    	color: black;
    	text-decoration: none;
    	display: block;
    	font-size: 1.2rem;
    	background-color: #eee;
    	margin: 0.5rem 0.5rem 0.5rem 0;
    	padding: 0.5rem 0;
    	border-radius: 4px;
    }

    .heroes a:hover {
    	color: #2c3a41;
    	background-color: #e6e6e6;
    }

    .heroes a:active {
    	background-color: #525252;
    	color: #fafafa;
    }

    .heroes .selected a {
    	background-color: #d6e6f7;
    }

    .heroes .selected a:hover {
    	background-color: #bdd7f5;
    }

    .heroes .badge {
    	padding: 0.5em 0.6em;
    	color: white;
    	background-color: #435b60;
    	min-width: 16px;
    	margin-right: 0.8em;
    	border-radius: 4px 0 0 4px;
    }
    ```

=== "hero-list.component.html"

    ```html
    <h2>Heroes</h2>
    <ul class="heroes">
    	<li
    		*ngFor="let hero of heroes$ | async"
    		[class.selected]="hero.id === selectedId"
    	>
    		<a [routerLink]="['/hero', hero.id]">
    			<span class="badge">{{ hero.id }}</span>{{
    			hero.name }}
    		</a>
    	</li>
    </ul>

    <button type="button" routerLink="/sidekicks">
    	Go to sidekicks
    </button>
    ```

=== "hero-list.component.ts"

    ```ts
    // TODO: Feature Componetized like CrisisCenter
    import { Observable } from 'rxjs';
    import { switchMap } from 'rxjs/operators';
    import { Component, OnInit } from '@angular/core';
    import { ActivatedRoute } from '@angular/router';

    import { HeroService } from '../hero.service';
    import { Hero } from '../hero';

    @Component({
    	selector: 'app-hero-list',
    	templateUrl: './hero-list.component.html',
    	styleUrls: ['./hero-list.component.css'],
    })
    export class HeroListComponent implements OnInit {
    	heroes$!: Observable<Hero[]>;
    	selectedId = 0;

    	constructor(
    		private service: HeroService,
    		private route: ActivatedRoute
    	) {}

    	ngOnInit() {
    		this.heroes$ = this.route.paramMap.pipe(
    			switchMap((params) => {
    				this.selectedId = parseInt(
    					params.get('id')!,
    					10
    				);
    				return this.service.getHeroes();
    			})
    		);
    	}
    }
    ```

=== "hero-detail.component.html"

    ```html
    <h2>Heroes</h2>
    <div *ngIf="hero$ | async as hero">
    	<h3>{{ hero.name }}</h3>
    	<p>Id: {{ hero.id }}</p>
    	<label for="hero-name">Hero name: </label>
    	<input
    		type="text"
    		id="hero-name"
    		[(ngModel)]="hero.name"
    		placeholder="name"
    	/>
    	<button type="button" (click)="gotoHeroes(hero)">
    		Back
    	</button>
    </div>
    ```

=== "hero-detail.component.ts"

    ```ts
    import { switchMap } from 'rxjs/operators';
    import { Component, OnInit } from '@angular/core';
    import {
    	Router,
    	ActivatedRoute,
    	ParamMap,
    } from '@angular/router';
    import { Observable } from 'rxjs';

    import { HeroService } from '../hero.service';
    import { Hero } from '../hero';

    @Component({
    	selector: 'app-hero-detail',
    	templateUrl: './hero-detail.component.html',
    	styleUrls: ['./hero-detail.component.css'],
    })
    export class HeroDetailComponent implements OnInit {
    	hero$!: Observable<Hero>;

    	constructor(
    		private route: ActivatedRoute,
    		private router: Router,
    		private service: HeroService
    	) {}

    	ngOnInit() {
    		this.hero$ = this.route.paramMap.pipe(
    			switchMap((params: ParamMap) =>
    				this.service.getHero(params.get('id')!)
    			)
    		);
    	}

    	gotoHeroes(hero: Hero) {
    		const heroId = hero ? hero.id : null;
    		// Pass along the hero id if available
    		// so that the HeroList component can select that hero.
    		// Include a junk 'foo' property for fun.
    		this.router.navigate([
    			'/heroes',
    			{ id: heroId, foo: 'foo' },
    		]);
    	}
    }
    ```

=== "hero.service.ts"

    ```ts
    import { Injectable } from '@angular/core';

    import { Observable, of } from 'rxjs';
    import { map } from 'rxjs/operators';

    import { Hero } from './hero';
    import { HEROES } from './mock-heroes';
    import { MessageService } from '../message.service';

    @Injectable({
    	providedIn: 'root',
    })
    export class HeroService {
    	constructor(private messageService: MessageService) {}

    	getHeroes(): Observable<Hero[]> {
    		// TODO: send the message _after_ fetching the heroes
    		this.messageService.add(
    			'HeroService: fetched heroes'
    		);
    		return of(HEROES);
    	}

    	getHero(id: number | string) {
    		return this.getHeroes().pipe(
    			// (+) before `id` turns the string into a number
    			map(
    				(heroes: Hero[]) =>
    					heroes.find((hero) => hero.id === +id)!
    			)
    		);
    	}
    }
    ```

=== "heroes.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { CommonModule } from '@angular/common';
    import { FormsModule } from '@angular/forms';

    import { HeroListComponent } from './hero-list/hero-list.component';
    import { HeroDetailComponent } from './hero-detail/hero-detail.component';

    import { HeroesRoutingModule } from './heroes-routing.module';

    @NgModule({
    	imports: [
    		CommonModule,
    		FormsModule,
    		HeroesRoutingModule,
    	],
    	declarations: [HeroListComponent, HeroDetailComponent],
    })
    export class HeroesModule {}
    ```

=== "heroes-routing.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { RouterModule, Routes } from '@angular/router';

    import { HeroListComponent } from './hero-list/hero-list.component';
    import { HeroDetailComponent } from './hero-detail/hero-detail.component';

    const heroesRoutes: Routes = [
    	{
    		path: 'heroes',
    		component: HeroListComponent,
    		data: { animation: 'heroes' },
    	},
    	{
    		path: 'hero/:id',
    		component: HeroDetailComponent,
    		data: { animation: 'hero' },
    	},
    ];

    @NgModule({
    	imports: [RouterModule.forChild(heroesRoutes)],
    	exports: [RouterModule],
    })
    export class HeroesRoutingModule {}
    ```

=== "message.service.ts"

    ```ts
    import { Injectable } from '@angular/core';

    @Injectable({
    	providedIn: 'root',
    })
    export class MessageService {
    	messages: string[] = [];

    	add(message: string) {
    		this.messages.push(message);
    	}

    	clear() {
    		this.messages = [];
    	}
    }
    ```

## Веха 4: Функция кризисного центра {: #milestone-4}

В этом разделе показано, как добавлять дочерние маршруты и использовать относительную маршрутизацию в вашем приложении.

Чтобы добавить дополнительные возможности к текущему кризисному центру приложения, проделайте те же шаги, что и для функции героев:

-   Создайте подпапку `crisis-center` в папке `src/app`.
-   Скопируйте файлы и папки из папки `app/heroes` в новую папку `crisis-center`.
-   В новых файлах измените все упоминания "героя" на "кризис", а "героев" на "кризисы".
-   Переименуйте файлы NgModule в `crisis-center.module.ts` и `crisis-center-routing.module.ts`.

Используйте имитацию кризисов вместо имитации героев:

```ts
import { Crisis } from './crisis';

export const CRISES: Crisis[] = [
    { id: 1, name: 'Dragon Burning Cities' },
    { id: 2, name: 'Sky Rains Great White Sharks' },
    { id: 3, name: 'Giant Asteroid Heading For Earth' },
    {
        id: 4,
        name: 'Procrastinators Meeting Delayed Again',
    },
];
```

Получившийся кризисный центр является основой для введения новой концепции &mdash; дочерней маршрутизации. Вы можете оставить Heroes в его текущем состоянии в качестве контраста с Кризисным центром.

!!!note ""

    В соответствии с принципом [Separation of Concerns](https://blog.8thlight.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html 'Separation of Concerns'), изменения в Кризисном центре не влияют на `AppModule` или любой другой компонент функции.

### Кризисный центр с дочерними маршрутами {: #crisis-child-routes}

В этом разделе показано, как организовать кризисный центр в соответствии со следующим рекомендуемым шаблоном для приложений Angular:

-   Каждая область функций находится в своей собственной папке.
-   Каждая функция имеет свой модуль функции Angular
-   Каждая область имеет свой корневой компонент области
-   Каждый корневой компонент области имеет свой собственный выход маршрутизатора и дочерние маршруты.
-   Маршруты областей функций редко (если вообще когда-либо) пересекаются с маршрутами других функций.

Если в вашем приложении много областей функций, деревья компонентов могут состоять из множества компонентов для этих функций, каждый из которых имеет ответвления от других, связанных с ним компонентов.

### Дочерний компонент маршрутизации {: #child-routing-component}

Создайте компонент `CrisisCenter` в папке `crisis-center`:

```
ng generate component crisis-center/crisis-center
```

Обновите шаблон компонента с помощью следующей разметки:

```html
<h2>Crisis Center</h2>
<router-outlet></router-outlet>
```

Компонент `CrisisCenterComponent` имеет следующее общее с `AppComponent`:

-   Он является корнем области кризисного центра, так же как `AppComponent` является корнем всего приложения.
-   Это оболочка для области функций кризисного управления, так же как `AppComponent` является оболочкой для управления рабочим процессом высокого уровня.

Как и большинство оболочек, класс `CrisisCenterComponent` является минимальным, поскольку в нем нет бизнес-логики, а в его шаблоне нет ссылок, только заголовок и `<router-outlet>` для дочернего компонента кризисного центра.

### Конфигурация дочернего маршрута {: #child-route-config}

В качестве главной страницы для функции "Кризисный центр" создайте компонент `CrisisCenterHome` в папке `crisis-center`.

```
ng generate component crisis-center/crisis-center-home
```

Обновите шаблон с приветственным сообщением для `Кризисного центра`.

```html
<h3>Welcome to the Crisis Center</h3>
```

Обновите `crisis-center-routing.module.ts`, который вы переименовали после копирования из файла `heroes-routing.module.ts`. На этот раз вы определяете дочерние маршруты внутри родительского маршрута `crisis-center`.

```ts
const crisisCenterRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisCenterComponent,
        children: [
            {
                path: '',
                component: CrisisListComponent,
                children: [
                    {
                        path: ':id',
                        component: CrisisDetailComponent,
                    },
                    {
                        path: '',
                        component: CrisisCenterHomeComponent,
                    },
                ],
            },
        ],
    },
];
```

Обратите внимание, что родительский маршрут `crisis-center` имеет свойство `children` с единственным маршрутом, содержащим `CrisisListComponent`. Маршрут `CrisisListComponent` также имеет массив `children` с двумя маршрутами.

Эти два маршрута ведут к дочерним компонентам кризисного центра, `CrisisCenterHomeComponent` и `CrisisDetailComponent`, соответственно.

Существуют важные различия в том, как маршрутизатор обрабатывает дочерние маршруты.

Маршрутизатор отображает компоненты этих маршрутов в `RouterOutlet` оболочки `CrisisCenterComponent`, а не в `RouterOutlet` оболочки `AppComponent`.

Компонент `CrisisListComponent` содержит список кризисов и `RouterOutlet` для отображения компонентов маршрута `Crisis Center Home` и `Crisis Detail`.

Маршрут `Crisis Detail` является дочерним для `Crisis List`. По умолчанию маршрутизатор [повторно использует компоненты](#reuse), поэтому компонент `Crisis Detail` используется повторно при выборе различных кризисов.

В отличие от этого, в маршруте `Деталь героя` [компонент создавался заново](#snapshot-the-no-observable-alternative) каждый раз, когда вы выбирали другого героя из списка героев.

На верхнем уровне пути, начинающиеся с `/`, ссылаются на корень приложения. Но дочерние маршруты расширяют путь родительского маршрута.

При каждом шаге вниз по дереву маршрута добавляется косая черта, за которой следует путь маршрута, если только путь не пуст.

Примените эту логику к навигации внутри кризисного центра, для которого родительский путь - `/crisis-center`.

-   Чтобы перейти к компоненту `CrisisCenterHomeComponent`, полный URL будет `/crisis-center` (`/crisis-center` + `''` + `''`)
-   Чтобы перейти к компоненту `CrisisDetailComponent` для кризиса с `id=2`, полный URL будет `/crisisis-center/2` (`/crisisis-center` + `''` + `'/2'`)

Абсолютный URL для последнего примера, включая `localhost`, выглядит следующим образом:

```
localhost:4200/crisis-center/2
```

Вот полный файл `crisis-center-routing.module.ts` с его импортами.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CrisisCenterHomeComponent } from './crisis-center-home/crisis-center-home.component';
import { CrisisListComponent } from './crisis-list/crisis-list.component';
import { CrisisCenterComponent } from './crisis-center/crisis-center.component';
import { CrisisDetailComponent } from './crisis-detail/crisis-detail.component';

const crisisCenterRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisCenterComponent,
        children: [
            {
                path: '',
                component: CrisisListComponent,
                children: [
                    {
                        path: ':id',
                        component: CrisisDetailComponent,
                    },
                    {
                        path: '',
                        component: CrisisCenterHomeComponent,
                    },
                ],
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(crisisCenterRoutes)],
    exports: [RouterModule],
})
export class CrisisCenterRoutingModule {}
```

### Импортируйте модуль кризисного центра в маршруты `AppModule` {: #import-crisis-module}

Как и в случае с `HeroesModule`, вы должны добавить `CrisisCenterModule` в массив `imports` `AppModule` _перед_ `AppRoutingModule`:

=== "src/app/crisis-center/crisis-center.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { FormsModule } from '@angular/forms';
    import { CommonModule } from '@angular/common';

    import { CrisisCenterHomeComponent } from './crisis-center-home/crisis-center-home.component';
    import { CrisisListComponent } from './crisis-list/crisis-list.component';
    import { CrisisCenterComponent } from './crisis-center/crisis-center.component';
    import { CrisisDetailComponent } from './crisis-detail/crisis-detail.component';

    import { CrisisCenterRoutingModule } from './crisis-center-routing.module';

    @NgModule({
    	imports: [
    		CommonModule,
    		FormsModule,
    		CrisisCenterRoutingModule,
    	],
    	declarations: [
    		CrisisCenterComponent,
    		CrisisListComponent,
    		CrisisCenterHomeComponent,
    		CrisisDetailComponent,
    	],
    })
    export class CrisisCenterModule {}
    ```

=== "src/app/app.module.ts (import CrisisCenterModule)"

    ```ts
    import { NgModule } from '@angular/core';
    import { CommonModule } from '@angular/common';
    import { FormsModule } from '@angular/forms';

    import { AppComponent } from './app.component';
    import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
    import { ComposeMessageComponent } from './compose-message/compose-message.component';

    import { AppRoutingModule } from './app-routing.module';
    import { HeroesModule } from './heroes/heroes.module';
    import { CrisisCenterModule } from './crisis-center/crisis-center.module';

    @NgModule({
    	imports: [
    		CommonModule,
    		FormsModule,
    		HeroesModule,
    		CrisisCenterModule,
    		AppRoutingModule,
    	],
    	declarations: [AppComponent, PageNotFoundComponent],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

!!!note ""

    Порядок импорта модулей важен, поскольку порядок маршрутов, определенных в модулях, влияет на согласование маршрутов. Если бы `AppModule` был импортирован первым, его маршрут с подстановочным знаком (`путь: '**'`) имел бы приоритет над маршрутами, определенными в `CrisisCenterModule`.
    Для получения дополнительной информации смотрите раздел [порядок маршрутов](router.md#route-order).

Удалите начальный маршрут кризисного центра из файла `app-routing.module.ts`, поскольку теперь модули `HeroesModule` и `CrisisCenter` предоставляют функциональные маршруты.

Файл `app-routing.module.ts` сохраняет маршруты верхнего уровня приложения, такие как маршруты по умолчанию и маршруты подстановочных знаков.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const appRoutes: Routes = [
    { path: '', redirectTo: '/heroes', pathMatch: 'full' },
    { path: '**', component: PageNotFoundComponent },
];

@NgModule({
    imports: [
        RouterModule.forRoot(
            appRoutes,
            { enableTracing: true } // <-- debugging purposes only
        ),
    ],
    exports: [RouterModule],
})
export class AppRoutingModule {}
```

### Относительная навигация {: #relative-navigation}

При создании функции кризисного центра вы перешли к маршруту подробной информации о кризисе, используя абсолютный путь, начинающийся со слэша.

Маршрутизатор сопоставляет такие абсолютные пути с маршрутами, начиная с верхней части конфигурации маршрута.

Вы могли бы продолжать использовать абсолютные пути, подобные этому, для навигации внутри функции Кризисного центра, но это привязывает ссылки к родительской структуре маршрутизации. Если вы измените родительский путь `/crisis-center`, вам придется изменить массив параметров ссылки.

Вы можете освободить ссылки от этой зависимости, определив пути, относительные к текущему сегменту URL. Навигация в области функции остается нетронутой, даже если вы измените путь родительского маршрута к функции.

!!!note ""

    Маршрутизатор поддерживает синтаксис, подобный каталогу, в списке параметров _ссылки_, чтобы помочь в поиске имени маршрута:

    | Синтаксис, подобный директории | Подробности                             |
    | :----------------------------- | :-------------------------------------- |
    | `./` без ведущей косой черты   | Относительно текущего уровня.           |
    | `../`                          | На один уровень вверх по пути маршрута. |

    Можно комбинировать синтаксис относительной навигации и путь предка. Если вам нужно перейти к родственному маршруту, вы можете использовать соглашение `../<sibling>` для перехода на один уровень вверх, затем на другой и вниз по маршруту родственника.

Чтобы перейти по относительному пути с помощью метода `Router.navigate`, вы должны предоставить `ActivatedRoute`, чтобы маршрутизатор знал, где вы находитесь в текущем дереве маршрутов.

После массива _параметров ссылки_ добавьте объект со свойством `relativeTo`, установленным на `ActivatedRoute`. После этого маршрутизатор вычисляет целевой URL, основываясь на местоположении активного маршрута.

!!!note ""

    Всегда указывайте полный абсолютный путь при вызове метода маршрутизатора `navigateByUrl()`.

### Переход к списку кризисов с помощью относительного URL-адреса {: #nav-to-crisis}

Вы уже ввели `ActivatedRoute`, который необходим для составления относительного пути навигации.

При использовании `RouterLink` для навигации вместо сервиса `Router`, вы будете использовать тот же массив параметров ссылки, но не будете предоставлять объекту свойство `relativeTo`. Свойство `ActivatedRoute` является неявным в директиве `RouterLink`.

Обновите метод `gotoCrises()` компонента `CrisisDetailComponent` для перехода обратно к списку кризисных центров, используя навигацию по относительному пути.

```ts
// Relative navigation back to the crises
this.router.navigate(
    ['../', { id: crisisId, foo: 'foo' }],
    { relativeTo: this.route }
);
```

Обратите внимание, что путь поднимается на уровень вверх, используя синтаксис `../`. Если текущий кризис `id` равен `3`, то путь обратно к списку кризисов будет `/crisis-center/;id=3;foo=foo`.

### Отображение нескольких маршрутов в именованных торговых точках {: #named-outlets}

Вы решили предоставить пользователям возможность связаться с кризисным центром. Когда пользователь нажимает кнопку "Связаться", вы хотите отобразить сообщение во всплывающем окне.

Всплывающее окно должно оставаться открытым, даже при переключении между страницами приложения, пока пользователь не закроет его, отправив сообщение или отменив его. Очевидно, что вы не можете поместить всплывающее окно в ту же розетку, что и другие страницы.

До сих пор вы определяли один аутлет и вставляли дочерние маршруты под этот аутлет, чтобы сгруппировать маршруты вместе. Маршрутизатор поддерживает только один первичный безымянный аутлет для каждого шаблона.

Шаблон также может иметь любое количество именованных аутлетов. Каждый именованный аутлет имеет свой собственный набор маршрутов со своими компонентами.

Несколько розеток могут одновременно отображать различное содержимое, определяемое различными маршрутами.

Добавьте аутлет с именем "popup" в `AppComponent`, непосредственно за неименованным аутлетом.

```html
<div [@routeAnimation]="getAnimationData()">
    <router-outlet></router-outlet>
</div>
<router-outlet name="popup"></router-outlet>
```

Вот куда попадает всплывающее окно, как только вы узнаете, как направить к нему всплывающий компонент.

#### Вторичные маршруты {: #secondary-routes}

Именованные розетки являются целями _вторичных маршрутов_.

Вторичные маршруты похожи на первичные, и вы настраиваете их таким же образом. Они отличаются по нескольким ключевым параметрам.

-   Они независимы друг от друга
-   Они работают в комбинации с другими маршрутами
-   Они отображаются в именованных точках.

Создайте новый компонент для составления сообщения.

```
ng generate component compose-message
```

Он отображает короткую форму с заголовком, полем ввода для сообщения и двумя кнопками "Отправить" и "Отмена".

![Контактная текстовая область с кнопками отправки и отмены](contact-form.png)

Вот компонент, его шаблон и стили:

=== "src/app/compose-message/compose-message.component.html"

    ```html
    <h3>Contact Crisis Center</h3>
    <div *ngIf="details">{{ details }}</div>
    <div>
    	<div>
    		<label for="message">Enter your message: </label>
    	</div>
    	<div>
    		<textarea
    			id="message"
    			[(ngModel)]="message"
    			rows="10"
    			cols="35"
    			[disabled]="sending"
    		></textarea>
    	</div>
    </div>
    <p *ngIf="!sending">
    	<button type="button" (click)="send()">Send</button>
    	<button type="button" (click)="cancel()">Cancel</button>
    </p>
    ```

=== "src/app/compose-message/compose-message.component.ts"

    ```ts
    import { Component } from '@angular/core';
    import { Router } from '@angular/router';

    @Component({
    	selector: 'app-compose-message',
    	templateUrl: './compose-message.component.html',
    	styleUrls: ['./compose-message.component.css'],
    })
    export class ComposeMessageComponent {
    	details = '';
    	message = '';
    	sending = false;

    	constructor(private router: Router) {}

    	send() {
    		this.sending = true;
    		this.details = 'Sending Message...';

    		setTimeout(() => {
    			this.sending = false;
    			this.closePopup();
    		}, 1000);
    	}

    	cancel() {
    		this.closePopup();
    	}

    	closePopup() {
    		// Providing a `null` value to the named outlet
    		// clears the contents of the named outlet
    		this.router.navigate([
    			{ outlets: { popup: null } },
    		]);
    	}
    }
    ```

== "src/app/compose-message/compose-message.component.css"

    ```css
    textarea {
    	width: 100%;
    	margin-top: 1rem;
    	font-size: 1.2rem;
    	box-sizing: border-box;
    }
    ```

Он выглядит так же, как и любой другой компонент в этом руководстве, но есть два ключевых отличия.

!!!note ""

    Метод `send()` имитирует задержку, ожидая секунду перед "отправкой" сообщения и закрытием всплывающего окна.

Метод `closePopup()` закрывает всплывающее представление, переходя к выходу из всплывающего окна с помощью `null`, о чем говорится в разделе [очистка вторичных маршрутов](#clear-secondary-routes).

#### Добавление вторичного маршрута {: #add-secondary-route}

Откройте модуль `AppRoutingModule` и добавьте новый маршрут `compose` в `appRoutes`.

```ts
{
  path: 'compose',
  component: ComposeMessageComponent,
  outlet: 'popup'
},
```

В дополнение к свойствам `path` и `component`, есть новое свойство `outlet`, которое установлено в `'popup'`. Теперь этот маршрут нацелен на всплывающий аутлет, и компонент `ComposeMessageComponent` будет отображаться там.

Чтобы дать пользователям возможность открыть всплывающее окно, добавьте ссылку "Contact" в шаблон `AppComponent`.

```html
<a [routerLink]="[{ outlets: { popup: ['compose'] } }]"
    >Contact</a
>
```

Хотя маршрут `compose` настроен на аутлет "popup", этого недостаточно для подключения маршрута к директиве `RouterLink`. Вы должны указать именованный аутлет в массиве _параметров ссылки_ и связать его с `RouterLink` с помощью привязки свойств.

Массив _параметров ссылки_ содержит объект с одним свойством `outlets`, значением которого является другой объект, ключом которого является одно (или более) имя розетки. В данном случае есть только свойство "popup" outlet, и его значением является другой массив _link parameters_, который определяет маршрут `compose`.

Другими словами, когда пользователь нажимает на эту ссылку, маршрутизатор отображает компонент, связанный с маршрутом `compose` в аутлете `popup`.

!!!note ""

    Этот объект `outlets` внутри внешнего объекта был ненужным, когда существовал только один маршрут и один безымянный выход.

    Маршрутизатор предположил, что ваша спецификация маршрута нацелена на безымянный первичный аутлет, и создал эти объекты для вас.

    Маршрутизация к именованной розетке выявила особенность маршрутизатора: вы можете нацелить несколько розеток несколькими маршрутами в одной директиве `RouterLink`.

#### Вторичная навигация по маршруту: объединение маршрутов во время навигации {: #secondary-route-navigation}

Перейдите в _Кризисный центр_ и нажмите "Контакт". В адресной строке браузера вы должны увидеть что-то вроде следующего URL.

```
http://&hellip;/crisis-center(popup:compose)
```

Соответствующая часть URL следует за `...`:

-   `кризисный центр` является основной навигацией.
-   Круглые скобки окружают вторичный маршрут
-   Вторичный маршрут состоит из названия выхода (`popup`), разделителя `colon` и пути вторичного маршрута (`compose`).

Нажмите на ссылку _Герои_ и снова посмотрите на URL.

```
http://&hellip;/heroes(popup:compose)
```

Первичная навигационная часть изменилась; вторичный маршрут остался прежним.

Маршрутизатор отслеживает две отдельные ветви в навигационном дереве и генерирует представление этого дерева в URL.

Вы можете добавить еще много выходов и маршрутов, на верхнем уровне и во вложенных уровнях, создавая дерево навигации с множеством ветвей, и маршрутизатор будет генерировать URL для этого.

Вы можете указать маршрутизатору на навигацию по всему дереву сразу, заполнив объект `outlets`, а затем передать этот объект внутри массива _параметров ссылок_ методу `router.navigate`.

#### Очистка вторичных маршрутов {: #clear-secondary-routes}

Как и обычные аутлеты, вторичные аутлеты сохраняются до тех пор, пока вы не перейдете к новому компоненту.

Каждый вторичный выход имеет свою собственную навигацию, независимую от навигации, управляющей первичным выходом. Изменение текущего маршрута, отображаемого в первичном аутлете, не влияет на всплывающий аутлет.

Вот почему всплывающее окно остается видимым, пока вы перемещаетесь между кризисами и героями.

Снова метод `closePopup()`:

```ts
closePopup() {
  // Providing a `null` value to the named outlet
  // clears the contents of the named outlet
  this.router.navigate([{ outlets: { popup: null }}]);
}
```

Нажатие на кнопки "отправить" или "отменить" очищает всплывающее окно. Функция `closePopup()` осуществляет императивную навигацию с помощью метода `Router.navigate()`, передавая массив [параметров ссылки](#link-parameters-array).

Как и массив, связанный с _Contact_ `RouterLink` в `AppComponent`, этот массив включает объект со свойством `outlets`. Значение свойства `outlets` - это другой объект с именами аутлетов для ключей.

Единственным именованным аутлетом является `'popup'`.

На этот раз значение свойства `'popup'` равно `null`. Это не маршрут, но это легитимное значение.

Установив для popup `RouterOutlet` значение `null`, очистите аутлет и удалите вторичный маршрут popup из текущего URL.

## Веха 5: Охрана маршрутов {: #milestone-5-route-guards}

В настоящее время любой пользователь может перемещаться в любое место приложения в любое время, но иногда вам необходимо контролировать доступ к различным частям вашего приложения по различным причинам, некоторые из которых могут быть следующими:

-   Возможно, пользователь не имеет права переходить к целевому компоненту.
-   Возможно, пользователь должен сначала войти в систему (authenticate)
-   Возможно, вам нужно получить некоторые данные перед отображением целевого компонента.
-   Возможно, вы захотите сохранить изменения перед тем, как покинуть компонент.
-   Вы можете спросить пользователя, можно ли отбросить ожидающие изменения, а не сохранять их.

Для обработки этих сценариев в конфигурацию маршрута добавляются защитные функции.

Возвращаемое значение охранника управляет поведением маршрутизатора:

| Возвращаемое значение | Подробности                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------- |
| `true`                | Процесс навигации продолжается                                                       |
| `false`               | Процесс навигации останавливается, и пользователь остается на месте                  |
| `UrlTree`             | Текущая навигация отменяется и начинается новая навигация к возвращенному `UrlTree`. |

!!!note "Примечание"

    Guard также может указать маршрутизатору перейти в другое место, фактически отменяя текущую навигацию. Если это делается внутри `guard`, то guard должен возвращать `UrlTree`.

Охранник может вернуть свой булев ответ синхронно. Но во многих случаях охранник не может выдать ответ синхронно.
Страж может задать вопрос пользователю, сохранить изменения на сервере или получить свежие данные.

Все это асинхронные операции.

Соответственно, страж маршрутизации может возвращать `Observable<boolean>` или `Promise<boolean>`, а маршрутизатор будет ждать, пока наблюдаемая или обещание разрешатся в `true` или `false`.

!!!note ""

    Наблюдаемая, предоставленная `Router`, автоматически завершается после получения первого значения.

Маршрутизатор поддерживает несколько методов охраны:

| Интерфейсы охраны                                                      | Подробности                                                                                                  |
| :--------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| [`canActivate`](https://angular.io/api/router/CanActivateFn)           | Для опосредованной навигации _к_ маршруту                                                                    |
| [`canActivateChild`](https://angular.io/api/router/CanActivateChildFn) | Для опосредования навигации _к_ дочернему маршруту                                                           |
| [`canDeactivate`](https://angular.io/api/router/CanDeactivateFn)       | Для опосредованной навигации _в сторону_ от текущего маршрута                                                |
| [`resolve`](https://angular.io/api/router/ResolveFn)                   | Для выполнения поиска данных маршрута _до_ активации маршрута                                                |
| [`canMatch`](https://angular.io/api/router/CanMatchFn)                 | Чтобы контролировать, должен ли вообще использоваться `маршрут`, даже если `путь` соответствует сегменту URL |

Вы можете иметь несколько защит на каждом уровне иерархии маршрутизации. Сначала маршрутизатор проверяет защиту `canDeactivate`, начиная с самого глубокого дочернего маршрута и заканчивая самым верхним.

Затем он проверяет защиты `canActivate` и `canActivateChild` сверху вниз до самого глубокого дочернего маршрута.

Если функциональный модуль загружается асинхронно, то защита `canMatch` проверяется до загрузки модуля.

За исключением `canMatch`, если _любой_ страж возвращает false, незавершенные стражи отменяются, и вся навигация отменяется. Если защита `canMatch` возвращает значение `false`, `маршрутизатор` продолжает обработку остальных `маршрутов`, чтобы проверить, не соответствует ли URL другой конфигурации `маршрута`. Вы можете думать об этом

как будто `Router` делает вид, что `маршрут` с защитой `canMatch` не существует.

В следующих разделах будет приведено несколько примеров.

### `canActivate`: требование аутентификации {: #can-activate-guard}

Приложения часто ограничивают доступ к области функций в зависимости от того, кем является пользователь. Вы можете разрешить доступ только аутентифицированным пользователям или пользователям с определенной ролью.

Можно заблокировать или ограничить доступ до тех пор, пока учетная запись пользователя не будет активирована.

Защита `canActivate` является инструментом для управления этими бизнес-правилами навигации.

#### Добавление модуля функций администратора

Этот раздел поможет вам расширить кризисный центр некоторыми новыми административными функциями. Начните с добавления нового функционального модуля с именем `AdminModule`.

Создайте папку `admin` с файлом функционального модуля и файлом конфигурации маршрутизации.

```shell
ng generate module admin --routing
```

Затем создайте вспомогательные компоненты.

```shell
ng generate component admin/admin-dashboard
```

```shell
ng generate component admin/admin
```

```shell
ng generate component admin/manage-crises
```

```shell
ng generate component admin/manage-heroes
```

Структура файла функции администратора выглядит следующим образом:

```
src/app/admin
+- admin
|  +- admin.component.css
|  +- admin.component.html
|  +- admin.component.ts
+- admin-dashboard
|  +- admin-dashboard.component.css
|  +- admin-dashboard.component.html
|  +- admin-dashboard.component.ts
+- manage-crises
|  +- manage-crises.component.css
|  +- manage-crises.component.html
|  +- manage-crises.component.ts
+- manage-heroes
|  +- manage-heroes.component.css
|  +- manage-heroes.component.html
|  +- manage-heroes.component.ts
+- admin.module.ts
+- admin-routing.module.ts
```

Функциональный модуль администратора содержит `AdminComponent`, используемый для маршрутизации внутри функционального модуля, маршрут приборной панели и два незавершенных компонента для управления кризисами и героями.

=== "src/app/admin/admin/admin.component.html"

    ```html
    <h2>Admin</h2>
    <nav>
    	<a
    		routerLink="./"
    		routerLinkActive="active"
    		[routerLinkActiveOptions]="{ exact: true }"
    		ariaCurrentWhenActive="page"
    		>Dashboard</a
    	>
    	<a
    		routerLink="./crises"
    		routerLinkActive="active"
    		ariaCurrentWhenActive="page"
    		>Manage Crises</a
    	>
    	<a
    		routerLink="./heroes"
    		routerLinkActive="active"
    		ariaCurrentWhenActive="page"
    		>Manage Heroes</a
    	>
    </nav>
    <router-outlet></router-outlet>
    ```

=== "src/app/admin/admin-dashboard/admin-dashboard.component.html"

    ```html
    <h3>Dashboard</h3>
    ```

=== "src/app/admin/admin.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { CommonModule } from '@angular/common';

    import { AdminComponent } from './admin/admin.component';
    import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
    import { ManageCrisesComponent } from './manage-crises/manage-crises.component';
    import { ManageHeroesComponent } from './manage-heroes/manage-heroes.component';

    import { AdminRoutingModule } from './admin-routing.module';

    @NgModule({
    	imports: [CommonModule, AdminRoutingModule],
    	declarations: [
    		AdminComponent,
    		AdminDashboardComponent,
    		ManageCrisesComponent,
    		ManageHeroesComponent,
    	],
    })
    export class AdminModule {}
    ```

=== "src/app/admin/manage-crises/manage-crises.component.html"

    ```html
    <p>Manage your crises here</p>
    ```

=== "src/app/admin/manage-heroes/manage-heroes.component.html"

    ```html
    <p>Manage your heroes here</p>
    ```

!!!note ""

    Хотя ссылка `RouterLink` на приборную панель администратора содержит только относительную косую черту без дополнительного сегмента URL, она подходит к любому маршруту в области функций администратора. Вы хотите, чтобы ссылка `Dashboard` была активна только тогда, когда пользователь посещает этот маршрут.
    Добавление дополнительной привязки к `Dashboard` routerLink, `[routerLinkActiveOptions]="{ exact: true }"`, отмечает ссылку `./` как активную, когда пользователь переходит на URL `/admin`, а не при переходе на любой из дочерних маршрутов.

##### Маршрут без компонента: группировка маршрутов без компонента {: #component-less-route}

Начальная конфигурация маршрутизации администратора:

```ts
const adminRoutes: Routes = [
    {
        path: 'admin',
        component: AdminComponent,
        children: [
            {
                path: '',
                children: [
                    {
                        path: 'crises',
                        component: ManageCrisesComponent,
                    },
                    {
                        path: 'heroes',
                        component: ManageHeroesComponent,
                    },
                    {
                        path: '',
                        component: AdminDashboardComponent,
                    },
                ],
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(adminRoutes)],
    exports: [RouterModule],
})
export class AdminRoutingModule {}
```

Дочерний маршрут под `AdminComponent` имеет свойство `path` и `children`, но он не использует `component`. Это определяет маршрут без компонента.

Для группировки маршрутов управления `Кризисного центра` по пути `admin` компонент не нужен. Кроме того, маршрут _без компонента_ облегчает [охрану дочерних маршрутов](#can-activate-child-guard).

Далее импортируйте `AdminModule` в `app.module.ts` и добавьте его в массив `imports` для регистрации маршрутов администратора.

```ts
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { ComposeMessageComponent } from './compose-message/compose-message.component';

import { AppRoutingModule } from './app-routing.module';
import { HeroesModule } from './heroes/heroes.module';
import { CrisisCenterModule } from './crisis-center/crisis-center.module';

import { AdminModule } from './admin/admin.module';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        HeroesModule,
        CrisisCenterModule,
        AdminModule,
        AppRoutingModule,
    ],
    declarations: [
        AppComponent,
        ComposeMessageComponent,
        PageNotFoundComponent,
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

Добавьте ссылку "Admin" в оболочку `AppComponent`, чтобы пользователи могли получить доступ к этой функции.

```html
<h1 class="title">Angular Router</h1>
<nav>
    <a
        routerLink="/crisis-center"
        routerLinkActive="active"
        ariaCurrentWhenActive="page"
        >Crisis Center</a
    >
    <a
        routerLink="/heroes"
        routerLinkActive="active"
        ariaCurrentWhenActive="page"
        >Heroes</a
    >
    <a
        routerLink="/admin"
        routerLinkActive="active"
        ariaCurrentWhenActive="page"
        >Admin</a
    >
    <a [routerLink]="[{ outlets: { popup: ['compose'] } }]"
        >Contact</a
    >
</nav>
<div [@routeAnimation]="getAnimationData()">
    <router-outlet></router-outlet>
</div>
<router-outlet name="popup"></router-outlet>
```

#### Охрана функции администратора {: #guard-admin-feature}

В настоящее время каждый маршрут в Кризисном центре открыт для всех. Новая функция администратора должна быть доступна только для аутентифицированных пользователей.

Напишите защитный метод `canActivate()`, чтобы перенаправлять анонимных пользователей на страницу входа в систему, когда они пытаются войти в область администратора.

Создайте новый файл с именем `auth.guard.ts` в папке `auth`. Файл `auth.guard.ts` будет содержать функцию `authGuard`.

```shell
ng generate guard auth/auth
```

Чтобы продемонстрировать основные принципы, в этом примере только регистрируется в консоли, немедленно возвращается `true` и разрешается продолжить навигацию:

```ts
export const authGuard = () => {
    console.log('authGuard#canActivate called');
    return true;
};
```

Далее откройте `admin-routing.module.ts`, импортируйте функцию `authGuard` и обновите административный маршрут со свойством `canActivate` guard, которое ссылается на нее:

```ts
import { authGuard } from '../auth/auth.guard';

import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { AdminComponent } from './admin/admin.component';
import { ManageCrisesComponent } from './manage-crises/manage-crises.component';
import { ManageHeroesComponent } from './manage-heroes/manage-heroes.component';

const adminRoutes: Routes = [
    {
        path: 'admin',
        component: AdminComponent,
        canActivate: [authGuard],

        children: [
            {
                path: '',
                children: [
                    {
                        path: 'crises',
                        component: ManageCrisesComponent,
                    },
                    {
                        path: 'heroes',
                        component: ManageHeroesComponent,
                    },
                    {
                        path: '',
                        component: AdminDashboardComponent,
                    },
                ],
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(adminRoutes)],
    exports: [RouterModule],
})
export class AdminRoutingModule {}
```

Функция администрирования теперь защищена стражем, но для полноценной работы стража требуется дополнительная настройка.

#### Аутентификация с помощью `authGuard` {: #teach-auth}

Сделайте `authGuard` имитирующим аутентификацию.

`authGuard` должен вызывать прикладную службу, которая может регистрировать пользователя и сохранять информацию о текущем пользователе. Создайте новый `AuthService` в папке `auth`:

```shell
ng generate service auth/auth
```

Обновите `AuthService` для входа пользователя в систему:

```ts
import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';
import { tap, delay } from 'rxjs/operators';

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    isLoggedIn = false;

    // store the URL so we can redirect after logging in
    redirectUrl: string | null = null;

    login(): Observable<boolean> {
        return of(true).pipe(
            delay(1000),
            tap(() => (this.isLoggedIn = true))
        );
    }

    logout(): void {
        this.isLoggedIn = false;
    }
}
```

Хотя он не выполняет вход в систему, у него есть флаг `isLoggedIn`, чтобы сообщить вам, аутентифицирован ли пользователь. Его метод `login()` имитирует вызов API к внешней службе, возвращая наблюдаемую, которая успешно разрешается после небольшой паузы.

Свойство `redirectUrl` хранит URL, к которому хотел получить доступ пользователь, чтобы вы могли перейти к нему после аутентификации.

!!!note ""

    Чтобы сделать все минимальным, этот пример перенаправляет неаутентифицированных пользователей на `/admin`.

Пересмотрите `authGuard` для вызова `AuthService`.

```ts
import { inject } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from './auth.service';

export const authGuard = () => {
    const authService = inject(AuthService);
    const router = inject(Router);

    if (authService.isLoggedIn) {
        return true;
    }

    // Redirect to the login page
    return router.parseUrl('/login');
};
```

Эта защита возвращает синхронный булев результат или `UrlTree`. Если пользователь вошел в систему, он возвращает `true` и навигация продолжается.

В противном случае он перенаправляет на страницу входа; страницу, которую вы еще не создали.

Возврат `UrlTree` указывает `Router` отменить текущую навигацию и запланировать новую для перенаправления пользователя.

#### Добавьте `LoginComponent` {: #add-login-component}

Вам нужен `LoginComponent` для входа пользователя в приложение. После входа в систему вы будете перенаправлять на сохраненный URL, если он доступен, или использовать URL по умолчанию.

Нет ничего нового в этом компоненте или способе его использования в конфигурации маршрутизатора.

```shell
ng generate component auth/login
```

Зарегистрируйте маршрут `/login` в файле `auth/auth-routing.module.ts`. В файле `app.module.ts` импортируйте и добавьте `AuthModule` в массив импортов `AppModule`.

=== "src/app/app.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { FormsModule } from '@angular/forms';
    import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

    import { AppComponent } from './app.component';
    import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
    import { ComposeMessageComponent } from './compose-message/compose-message.component';

    import { AppRoutingModule } from './app-routing.module';
    import { HeroesModule } from './heroes/heroes.module';
    import { AuthModule } from './auth/auth.module';

    @NgModule({
    	imports: [
    		BrowserModule,
    		BrowserAnimationsModule,
    		FormsModule,
    		HeroesModule,
    		AuthModule,
    		AppRoutingModule,
    	],
    	declarations: [
    		AppComponent,
    		ComposeMessageComponent,
    		PageNotFoundComponent,
    	],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "src/app/auth/login/login.component.html"

    ```html
    <h2>Login</h2>
    <p>{{message}}</p>
    <p>
    	<button
    		type="button"
    		(click)="login()"
    		*ngIf="!authService.isLoggedIn"
    	>
    		Login
    	</button>
    	<button
    		type="button"
    		(click)="logout()"
    		*ngIf="authService.isLoggedIn"
    	>
    		Logout
    	</button>
    </p>
    ```

=== "src/app/auth/login/login.component.ts"

    ```ts
    import { Component } from '@angular/core';
    import { Router } from '@angular/router';
    import { AuthService } from '../auth.service';

    @Component({
    	selector: 'app-login',
    	templateUrl: './login.component.html',
    	styleUrls: ['./login.component.css'],
    })
    export class LoginComponent {
    	message: string;

    	constructor(
    		public authService: AuthService,
    		public router: Router
    	) {
    		this.message = this.getMessage();
    	}

    	getMessage() {
    		return (
    			'Logged ' +
    			(this.authService.isLoggedIn ? 'in' : 'out')
    		);
    	}

    	login() {
    		this.message = 'Trying to log in ...';

    		this.authService.login().subscribe(() => {
    			this.message = this.getMessage();
    			if (this.authService.isLoggedIn) {
    				// Usually you would use the redirect URL from the auth service.
    				// However to keep the example simple, we will always redirect to `/admin`.
    				const redirectUrl = '/admin';

    				// Redirect the user
    				this.router.navigate([redirectUrl]);
    			}
    		});
    	}

    	logout() {
    		this.authService.logout();
    		this.message = this.getMessage();
    	}
    }
    ```

=== "src/app/auth/auth.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { CommonModule } from '@angular/common';
    import { FormsModule } from '@angular/forms';

    import { LoginComponent } from './login/login.component';
    import { AuthRoutingModule } from './auth-routing.module';

    @NgModule({
    	imports: [CommonModule, FormsModule, AuthRoutingModule],
    	declarations: [LoginComponent],
    })
    export class AuthModule {}
    ```

### `canActivateChild`: защита дочерних маршрутов {: #can-activate-child-guard}

Вы также можете защитить дочерние маршруты с помощью защиты `canActivateChild`. Защита `canActivateChild` аналогична защите `canActivate`.

Ключевое отличие заключается в том, что он запускается до активации любого дочернего маршрута.

Вы защитили функциональный модуль администратора от несанкционированного доступа. Вам также следует защитить дочерние маршруты _внутри_ функционального модуля.

Добавьте тот же `authGuard` к админскому маршруту `component-less`, чтобы защитить все остальные дочерние маршруты одновременно, вместо того, чтобы добавлять `authGuard` к каждому маршруту по отдельности.

```ts
const adminRoutes: Routes = [
    {
        path: 'admin',
        component: AdminComponent,
        canActivate: [authGuard],
        children: [
            {
                path: '',
                canActivateChild: [authGuard],
                children: [
                    {
                        path: 'crises',
                        component: ManageCrisesComponent,
                    },
                    {
                        path: 'heroes',
                        component: ManageHeroesComponent,
                    },
                    {
                        path: '',
                        component: AdminDashboardComponent,
                    },
                ],
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(adminRoutes)],
    exports: [RouterModule],
})
export class AdminRoutingModule {}
```

### `canDeactivate`: обработка несохраненных изменений {: #can-deactivate-guard}

Вернемся к рабочему процессу "Герои", приложение принимает каждое изменение героя немедленно без проверки.

В реальном мире вам, возможно, придется накапливать изменения пользователей, проверять их по полям, проверять на сервере или держать изменения в состоянии ожидания, пока пользователь не подтвердит их как группу или не отменит и не вернет все изменения.

Когда пользователь отходит, вы можете позволить ему самому решить, что делать с несохраненными изменениями. Если пользователь отменит изменения, вы останетесь на месте и разрешите новые изменения.

Если пользователь одобрит изменения, приложение можно сохранить.

Вы все еще можете задержать навигацию до тех пор, пока сохранение не будет успешным. Если вы позволите пользователю сразу перейти к следующему экрану, а сохранение окажется неудачным (возможно, данные будут признаны недействительными), вы потеряете контекст ошибки.

Вам нужно остановить навигацию, пока вы асинхронно ждете ответа сервера.

Защита `canDeactivate` поможет вам решить, что делать с несохраненными изменениями и как действовать дальше.

#### Отмена и сохранение {: #cancel-save}

Пользователи обновляют информацию о кризисе в компоненте `CrisisDetailComponent`. В отличие от компонента `HeroDetailComponent`, изменения пользователя не обновляют сущность кризиса немедленно.

Вместо этого приложение обновляет сущность, когда пользователь нажимает кнопку Сохранить, и отбрасывает изменения, когда пользователь нажимает кнопку Отмена.

Обе кнопки позволяют вернуться к списку кризисов после сохранения или отмены.

```ts
cancel() {
  this.gotoCrises();
}

save() {
  this.crisis.name = this.editName;
  this.gotoCrises();
}
```

В этом сценарии пользователь может нажать на ссылку героев, отменить действие, нажать кнопку возврата браузера или уйти без сохранения.

Этот пример приложения просит пользователя быть явным с диалоговым окном подтверждения, которое асинхронно ожидает ответа пользователя.

!!!note ""

    Вы можете ждать ответа пользователя с помощью синхронного, блокирующего кода, однако приложение будет более отзывчивым &mdash; и сможет выполнять другую работу &mdash; если будет ждать ответа пользователя асинхронно.

Создайте службу `Dialog` для обработки подтверждения пользователя.

```shell
ng generate service dialog
```

Добавьте метод `confirm()` в `DialogService`, чтобы попросить пользователя подтвердить свое намерение. Метод `window.confirm` является блокирующим действием, которое отображает модальный диалог и ожидает взаимодействия с пользователем.

```ts
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

/**
 * Async modal dialog service
 * DialogService makes this app easier to test by faking this service.
 * TODO: better modal implementation that doesn't use window.confirm
 */
@Injectable({
    providedIn: 'root',
})
export class DialogService {
    /**
     * Ask user to confirm an action. `message` explains the action and choices.
     * Returns observable resolving to `true`=confirm or `false`=cancel
     */
    confirm(message?: string): Observable<boolean> {
        const confirmation = window.confirm(
            message || 'Is it OK?'
        );

        return of(confirmation);
    }
}
```

Он возвращает `Observable`, который разрешается, когда пользователь в конечном итоге решает, что делать: либо отменить изменения и перейти к следующему (`true`), либо сохранить ожидающие изменения и остаться в кризисном редакторе (`false`).

Создайте защиту, которая проверяет наличие метода `canDeactivate()` в компоненте - любом компоненте.

```shell
ng generate guard can-deactivate
```

Вставьте следующий код в свой страж.

```ts
import { CanDeactivateFn } from '@angular/router';
import { Observable } from 'rxjs';

export interface CanComponentDeactivate {
    canDeactivate?: () =>
        | Observable<boolean>
        | Promise<boolean>
        | boolean;
}

export const canDeactivateGuard: CanDeactivateFn<CanComponentDeactivate> = (
    component: CanComponentDeactivate
) =>
    component.canDeactivate
        ? component.canDeactivate()
        : true;
```

Хотя стражу не обязательно знать, какой компонент имеет метод `deactivate`, он может определить, что компонент `CrisisDetailComponent` имеет метод `canDeactivate()` и вызвать его. Незнание сторожем деталей метода деактивации любого компонента делает его многоразовым.

В качестве альтернативы вы можете сделать специфичный для компонента `canDeactivate` guard для `CrisisDetailComponent`. Метод `canDeactivate()` предоставляет вам текущий экземпляр `компонента`, текущий `ActivatedRoute` и `RouterStateSnapshot` на случай, если вам понадобится доступ к какой-либо внешней информации.

Это было бы полезно, если бы вы хотели использовать эту защиту только для этого компонента и вам нужно было бы получить свойства компонента или подтвердить, должен ли маршрутизатор разрешить навигацию от него.

```ts
import { Observable } from 'rxjs';
import {
    CanDeactivateFn,
    ActivatedRouteSnapshot,
    RouterStateSnapshot,
} from '@angular/router';

import { CrisisDetailComponent } from './crisis-center/crisis-detail/crisis-detail.component';

export const canDeactivateGuard: CanDeactivateFn<CrisisDetailComponent> = (
    component: CrisisDetailComponent,
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
): Observable<boolean> | boolean => {
    // Get the Crisis Center ID
    console.log(route.paramMap.get('id'));

    // Get the current URL
    console.log(state.url);

    // Allow synchronous navigation (`true`) if no crisis or the crisis is unchanged
    if (
        !component.crisis ||
        component.crisis.name === component.editName
    ) {
        return true;
    }
    // Otherwise ask the user with the dialog service and return its
    // observable which resolves to true or false when the user decides
    return component.dialogService.confirm(
        'Discard changes?'
    );
};
```

Если вернуться к `CrisisDetailComponent`, то он реализует рабочий процесс подтверждения для несохраненных изменений.

```ts
canDeactivate(): Observable<boolean> | boolean {
  // Allow synchronous navigation (`true`) if no crisis or the crisis is unchanged
  if (!this.crisis || this.crisis.name === this.editName) {
    return true;
  }
  // Otherwise ask the user with the dialog service and return its
  // observable which resolves to true or false when the user decides
  return this.dialogService.confirm('Discard changes?');
}
```

Обратите внимание, что метод `canDeactivate()` может возвращаться синхронно; он возвращает `true` немедленно, если нет кризиса или нет ожидающих изменений. Но он также может возвращать `Promise` или `Observable`, и маршрутизатор будет ждать, пока это разрешится в истинное (navigate) или ложное (stay on the current route) решение.

Добавьте `Guard` к маршруту деталей кризиса в `crisis-center-routing.module.ts`, используя свойство массива `canDeactivate`.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CrisisCenterHomeComponent } from './crisis-center-home/crisis-center-home.component';
import { CrisisListComponent } from './crisis-list/crisis-list.component';
import { CrisisCenterComponent } from './crisis-center/crisis-center.component';
import { CrisisDetailComponent } from './crisis-detail/crisis-detail.component';

import { canDeactivateGuard } from '../can-deactivate.guard';

const crisisCenterRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisCenterComponent,
        children: [
            {
                path: '',
                component: CrisisListComponent,
                children: [
                    {
                        path: ':id',
                        component: CrisisDetailComponent,
                        canDeactivate: [canDeactivateGuard],
                    },
                    {
                        path: '',
                        component: CrisisCenterHomeComponent,
                    },
                ],
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(crisisCenterRoutes)],
    exports: [RouterModule],
})
export class CrisisCenterRoutingModule {}
```

Теперь вы обеспечили пользователю защиту от несохраненных изменений.

### _Resolve_: предварительная выборка данных компонента {: #resolve-guard}

В `Hero Detail` и `Crisis Detail` приложение ждало, пока активируется маршрут, чтобы получить данные о соответствующем герое или кризисе.

Если вы используете реальный API, то может возникнуть некоторая задержка, прежде чем данные для отображения будут возвращены с сервера. Вы же не хотите отображать пустой компонент в ожидании данных.

Чтобы улучшить это поведение, вы можете предварительно получить данные с сервера с помощью резольвера, чтобы они были готовы в момент активации маршрута. Это также позволяет обрабатывать ошибки перед маршрутизацией к компоненту.

Нет смысла переходить к детализации кризиса для `id`, для которого нет записи.

Лучше отправить пользователя обратно к `Списку кризисов`, который показывает только действующие кризисные центры.

В общем, вы хотите отложить отображение компонента маршрутизации до тех пор, пока не будут получены все необходимые данные.

#### Выборка данных перед навигацией {: #fetch-before-navigating}

В данный момент `CrisisDetailComponent` извлекает данные о выбранном кризисе. Если кризис не найден, маршрутизатор возвращается к представлению списка кризисов.

Возможно, было бы лучше, если бы все это обрабатывалось сначала, до активации маршрута. Резольвер `crisisDetailResolver` мог бы получить `кризис` или перейти в сторону, если `кризис` не существует, _до_ активации маршрута и создания `CrisisDetailComponent`.

Создайте файл `crisis-detail-resolver.ts` в области функции `Crisis Center`. Этот файл будет содержать функцию `crisisDetailResolver`.

```shell
ng generate resolver crisis-center/crisis-detail-resolver
```

```ts
export function crisisDetailResolver() {}
```

Перенесите соответствующие части логики поиска кризисов в `CrisisDetailComponent.ngOnInit()` в `crisisDetailResolver`. Импортируйте модель `Crisis`, `CrisisService` и `Router`, чтобы вы могли перейти в другое место, если не сможете найти кризис.

Будьте явными и используйте тип `ResolveFn` с типом `Crisis`.

Вставьте `CrisisService` и `Router`. Этот метод может возвращать `Promise`, `Observable` или синхронное возвращаемое значение.

Метод `CrisisService.getCrisis()` возвращает наблюдаемое значение, чтобы предотвратить загрузку маршрута до тех пор, пока не будут получены данные.

Если он не возвращает действительный `кризис`, то возвращает пустой `Observable`, отменяет предыдущую текущую навигацию к `CrisisDetailComponent` и возвращает пользователя к `CrisisListComponent`. Обновленная функция resolver выглядит следующим образом:

```ts
import { inject } from '@angular/core';
import {
    ActivatedRouteSnapshot,
    ResolveFn,
    Router,
} from '@angular/router';
import { EMPTY, of } from 'rxjs';
import { mergeMap } from 'rxjs/operators';

import { Crisis } from './crisis';
import { CrisisService } from './crisis.service';

export const crisisDetailResolver: ResolveFn<Crisis> = (
    route: ActivatedRouteSnapshot
) => {
    const router = inject(Router);
    const cs = inject(CrisisService);
    const id = route.paramMap.get('id')!;

    return cs.getCrisis(id).pipe(
        mergeMap((crisis) => {
            if (crisis) {
                return of(crisis);
            } else {
                // id not found
                router.navigate(['/crisis-center']);
                return EMPTY;
            }
        })
    );
};
```

Импортируйте этот resolver в `crisis-center-routing.module.ts` и добавьте объект `resolve` в конфигурацию маршрута `CrisisDetailComponent`.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CrisisCenterHomeComponent } from './crisis-center-home/crisis-center-home.component';
import { CrisisListComponent } from './crisis-list/crisis-list.component';
import { CrisisCenterComponent } from './crisis-center/crisis-center.component';
import { CrisisDetailComponent } from './crisis-detail/crisis-detail.component';

import { canDeactivateGuard } from '../can-deactivate.guard';
import { crisisDetailResolver } from './crisis-detail-resolver';

const crisisCenterRoutes: Routes = [
    {
        path: 'crisis-center',
        component: CrisisCenterComponent,
        children: [
            {
                path: '',
                component: CrisisListComponent,
                children: [
                    {
                        path: ':id',
                        component: CrisisDetailComponent,
                        canDeactivate: [canDeactivateGuard],
                        resolve: {
                            crisis: crisisDetailResolver,
                        },
                    },
                    {
                        path: '',
                        component: CrisisCenterHomeComponent,
                    },
                ],
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(crisisCenterRoutes)],
    exports: [RouterModule],
})
export class CrisisCenterRoutingModule {}
```

Компонент `CrisisDetailComponent` больше не должен получать данные о кризисе. Когда вы переконфигурировали маршрут, вы изменили местоположение кризиса.

Обновите `CrisisDetailComponent`, чтобы получить кризис из свойства `ActivatedRoute.data.crisis` вместо этого;

```ts
ngOnInit() {
  this.route.data
    .subscribe(data => {
      const crisis: Crisis = data['crisis'];
      this.editName = crisis.name;
      this.crisis = crisis;
    });
}
```

Рассмотрите следующие три важных момента:

1.  Функция маршрутизатора `ResolveFn` является необязательной.

2.  Маршрутизатор вызывает резольвер в любом случае, когда пользователь может переместиться в сторону, поэтому вам не придется писать код для каждого случая использования.

3.  Возвращение пустого `Observable` хотя бы в одном резольвере отменяет навигацию.

Соответствующий код Кризисного центра для этого этапа приведен ниже.

=== "app.component.html"

    ```html
    <div class="wrapper">
    	<h1 class="title">Angular Router</h1>
    	<nav>
    		<a
    			routerLink="/crisis-center"
    			routerLinkActive="active"
    			ariaCurrentWhenActive="page"
    			>Crisis Center</a
    		>
    		<a
    			routerLink="/superheroes"
    			routerLinkActive="active"
    			ariaCurrentWhenActive="page"
    			>Heroes</a
    		>
    		<a
    			routerLink="/admin"
    			routerLinkActive="active"
    			ariaCurrentWhenActive="page"
    			>Admin</a
    		>
    		<a
    			routerLink="/login"
    			routerLinkActive="active"
    			ariaCurrentWhenActive="page"
    			>Login</a
    		>
    		<a
    			[routerLink]="[{ outlets: { popup: ['compose'] } }]"
    			>Contact</a
    		>
    	</nav>
    	<div [@routeAnimation]="getRouteAnimationData()">
    		<router-outlet></router-outlet>
    	</div>
    	<router-outlet name="popup"></router-outlet>
    </div>
    ```

=== "crisis-center-home.component.html"

    ```html
    <h3>Welcome to the Crisis Center</h3>
    ```

=== "crisis-center.component.html"

    ```html
    <h2>Crisis Center</h2>
    <router-outlet></router-outlet>
    ```

=== "crisis-center-routing.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { RouterModule, Routes } from '@angular/router';

    import { CrisisCenterHomeComponent } from './crisis-center-home/crisis-center-home.component';
    import { CrisisListComponent } from './crisis-list/crisis-list.component';
    import { CrisisCenterComponent } from './crisis-center/crisis-center.component';
    import { CrisisDetailComponent } from './crisis-detail/crisis-detail.component';

    import { canDeactivateGuard } from '../can-deactivate.guard';
    import { crisisDetailResolver } from './crisis-detail-resolver';

    const crisisCenterRoutes: Routes = [
    	{
    		path: 'crisis-center',
    		component: CrisisCenterComponent,
    		children: [
    			{
    				path: '',
    				component: CrisisListComponent,
    				children: [
    					{
    						path: ':id',
    						component: CrisisDetailComponent,
    						canDeactivate: [canDeactivateGuard],
    						resolve: {
    							crisis: crisisDetailResolver,
    						},
    					},
    					{
    						path: '',
    						component: CrisisCenterHomeComponent,
    					},
    				],
    			},
    		],
    	},
    ];

    @NgModule({
    	imports: [RouterModule.forChild(crisisCenterRoutes)],
    	exports: [RouterModule],
    })
    export class CrisisCenterRoutingModule {}
    ```

=== "crisis-list.component.html"

    ```html
    <ul class="crises">
    	<li
    		*ngFor="let crisis of crises$ | async"
    		[class.selected]="crisis.id === selectedId"
    	>
    		<a [routerLink]="[crisis.id]">
    			<span class="badge">{{ crisis.id }}</span>{{
    			crisis.name }}
    		</a>
    	</li>
    </ul>

    <router-outlet></router-outlet>
    ```

=== "crisis-list.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';
    import { ActivatedRoute } from '@angular/router';

    import { CrisisService } from '../crisis.service';
    import { Crisis } from '../crisis';
    import { Observable } from 'rxjs';
    import { switchMap } from 'rxjs/operators';

    @Component({
    	selector: 'app-crisis-list',
    	templateUrl: './crisis-list.component.html',
    	styleUrls: ['./crisis-list.component.css'],
    })
    export class CrisisListComponent implements OnInit {
    	crises$?: Observable<Crisis[]>;
    	selectedId = 0;

    	constructor(
    		private service: CrisisService,
    		private route: ActivatedRoute
    	) {}

    	ngOnInit() {
    		this.crises$ = this.route.firstChild?.paramMap.pipe(
    			switchMap((params) => {
    				this.selectedId = parseInt(
    					params.get('id')!,
    					10
    				);
    				return this.service.getCrises();
    			})
    		);
    	}
    }
    ```

=== "crisis-detail.component.html"

    ```html
    <div *ngIf="crisis">
    	<h3>{{ editName }}</h3>
    	<p>Id: {{ crisis.id }}</p>
    	<label for="crisis-name">Crisis name: </label>
    	<input
    		type="text"
    		id="crisis-name"
    		[(ngModel)]="editName"
    		placeholder="name"
    	/>
    	<div>
    		<button type="button" (click)="save()">Save</button>
    		<button type="button" (click)="cancel()">
    			Cancel
    		</button>
    	</div>
    </div>
    ```

=== "crisis-detail.component.ts"

    ```ts
    import { Component, OnInit } from '@angular/core';
    import { ActivatedRoute, Router } from '@angular/router';
    import { Observable } from 'rxjs';

    import { Crisis } from '../crisis';
    import { DialogService } from '../../dialog.service';

    @Component({
    	selector: 'app-crisis-detail',
    	templateUrl: './crisis-detail.component.html',
    	styleUrls: ['./crisis-detail.component.css'],
    })
    export class CrisisDetailComponent implements OnInit {
    	crisis!: Crisis;
    	editName = '';

    	constructor(
    		private route: ActivatedRoute,
    		private router: Router,
    		public dialogService: DialogService
    	) {}

    	ngOnInit() {
    		this.route.data.subscribe((data) => {
    			const crisis: Crisis = data['crisis'];
    			this.editName = crisis.name;
    			this.crisis = crisis;
    		});
    	}

    	cancel() {
    		this.gotoCrises();
    	}

    	save() {
    		this.crisis.name = this.editName;
    		this.gotoCrises();
    	}

    	canDeactivate(): Observable<boolean> | boolean {
    		// Allow synchronous navigation (`true`) if no crisis or the crisis is unchanged
    		if (
    			!this.crisis ||
    			this.crisis.name === this.editName
    		) {
    			return true;
    		}
    		// Otherwise ask the user with the dialog service and return its
    		// observable which resolves to true or false when the user decides
    		return this.dialogService.confirm(
    			'Discard changes?'
    		);
    	}

    	gotoCrises() {
    		const crisisId = this.crisis
    			? this.crisis.id
    			: null;
    		// Pass along the crisis id if available
    		// so that the CrisisListComponent can select that crisis.
    		// Add a totally useless `foo` parameter for kicks.
    		// Relative navigation back to the crises
    		this.router.navigate(
    			['../', { id: crisisId, foo: 'foo' }],
    			{ relativeTo: this.route }
    		);
    	}
    }
    ```

=== "crisis-detail-resolver.ts"

    ```ts
    import { inject } from '@angular/core';
    import {
    	ActivatedRouteSnapshot,
    	ResolveFn,
    	Router,
    } from '@angular/router';
    import { EMPTY, of } from 'rxjs';
    import { mergeMap } from 'rxjs/operators';

    import { Crisis } from './crisis';
    import { CrisisService } from './crisis.service';

    export const crisisDetailResolver: ResolveFn<Crisis> = (
    	route: ActivatedRouteSnapshot
    ) => {
    	const router = inject(Router);
    	const cs = inject(CrisisService);
    	const id = route.paramMap.get('id')!;

    	return cs.getCrisis(id).pipe(
    		mergeMap((crisis) => {
    			if (crisis) {
    				return of(crisis);
    			} else {
    				// id not found
    				router.navigate(['/crisis-center']);
    				return EMPTY;
    			}
    		})
    	);
    };
    ```

=== "crisis.service.ts"

    ```ts
    import { BehaviorSubject } from 'rxjs';
    import { map } from 'rxjs/operators';

    import { Injectable } from '@angular/core';
    import { MessageService } from '../message.service';
    import { Crisis } from './crisis';
    import { CRISES } from './mock-crises';

    @Injectable({
    	providedIn: 'root',
    })
    export class CrisisService {
    	static nextCrisisId = 100;
    	private crises$: BehaviorSubject<
    		Crisis[]
    	> = new BehaviorSubject<Crisis[]>(CRISES);

    	constructor(private messageService: MessageService) {}

    	getCrises() {
    		return this.crises$;
    	}

    	getCrisis(id: number | string) {
    		return this.getCrises().pipe(
    			map(
    				(crises) =>
    					crises.find(
    						(crisis) => crisis.id === +id
    					)!
    			)
    		);
    	}
    }
    ```

=== "dialog.service.ts"

    ```ts
    import { Injectable } from '@angular/core';
    import { Observable, of } from 'rxjs';

    /**
     * Async modal dialog service
     * DialogService makes this app easier to test by faking this service.
     * TODO: better modal implementation that doesn't use window.confirm
     */
    @Injectable({
    	providedIn: 'root',
    })
    export class DialogService {
    	/**
    	 * Ask user to confirm an action. `message` explains the action and choices.
    	 * Returns observable resolving to `true`=confirm or `false`=cancel
    	 */
    	confirm(message?: string): Observable<boolean> {
    		const confirmation = window.confirm(
    			message || 'Is it OK?'
    		);

    		return of(confirmation);
    	}
    }
    ```

Гварды

=== "auth.guard.ts"

    ```ts
    import { inject } from '@angular/core';
    import { Router } from '@angular/router';
    import { AuthService } from './auth.service';

    export const authGuard = () => {
    	const authService = inject(AuthService);
    	const router = inject(Router);

    	if (authService.isLoggedIn) {
    		return true;
    	}

    	// Redirect to the login page
    	return router.parseUrl('/login');
    };
    ```

=== "can-deactivate.guard.ts"

    ```ts
    import { CanDeactivateFn } from '@angular/router';
    import { Observable } from 'rxjs';

    export interface CanComponentDeactivate {
    	canDeactivate?: () =>
    		| Observable<boolean>
    		| Promise<boolean>
    		| boolean;
    }

    export const canDeactivateGuard: CanDeactivateFn<CanComponentDeactivate> = (
    	component: CanComponentDeactivate
    ) =>
    	component.canDeactivate
    		? component.canDeactivate()
    		: true;
    ```

### Параметры запроса и фрагменты {: #query-parameters}

В разделе [параметры маршрута](#optional-route-parameters) вы имели дело только с параметрами, специфичными для маршрута. Однако вы можете использовать параметры запроса для получения необязательных параметров, доступных для всех маршрутов.

[Фрагменты](https://en.wikipedia.org/wiki/Fragment_identifier) ссылаются на определенные элементы на странице, идентифицируемые атрибутом `id`.

Обновите `authGuard`, чтобы обеспечить запрос `session_id`, который сохраняется после перехода к другому маршруту.

Добавьте элемент `anchor`, чтобы можно было перейти к определенной точке страницы.

Добавьте объект `NavigationExtras` в метод `router.navigate()`, который переводит вас на маршрут `/login`.

```ts
import { inject } from '@angular/core';
import { Router, NavigationExtras } from '@angular/router';
import { AuthService } from './auth.service';

export const authGuard = () => {
    const authService = inject(AuthService);
    const router = inject(Router);

    if (authService.isLoggedIn) {
        return true;
    }

    // Create a dummy session id
    const sessionId = 123456789;

    // Set our navigation extras object
    // that contains our global query params and fragment
    const navigationExtras: NavigationExtras = {
        queryParams: { session_id: sessionId },
        fragment: 'anchor',
    };

    // Redirect to the login page with extras
    return router.createUrlTree(
        ['/login'],
        navigationExtras
    );
};
```

Вы также можете сохранять параметры запроса и фрагменты при разных навигациях без необходимости предоставлять их снова при переходе. В `LoginComponent` вы добавите _объект_ в качестве второго аргумента в функцию `router.navigate()` и предоставите `queryParamsHandling` и `preserveFragment` для передачи текущих параметров запроса и фрагмента в следующий маршрут.

```ts
// Set our navigation extras object
// that passes on our global query params and fragment
const navigationExtras: NavigationExtras = {
    queryParamsHandling: 'preserve',
    preserveFragment: true,
};

// Redirect the user
this.router.navigate([redirectUrl], navigationExtras);
```

!!!note ""

    Функция `queryParamsHandling` также предоставляет опцию `merge`, которая сохраняет и объединяет текущие параметры запроса с любыми предоставленными параметрами запроса при навигации.

Чтобы перейти к маршруту Admin Dashboard после входа в систему, обновите `admin-dashboard.component.ts` для обработки параметров запроса и фрагмента.

```ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Component({
    selector: 'app-admin-dashboard',
    templateUrl: './admin-dashboard.component.html',
    styleUrls: ['./admin-dashboard.component.css'],
})
export class AdminDashboardComponent implements OnInit {
    sessionId!: Observable<string>;
    token!: Observable<string>;

    constructor(private route: ActivatedRoute) {}

    ngOnInit() {
        // Capture the session ID if available
        this.sessionId = this.route.queryParamMap.pipe(
            map(
                (params) =>
                    params.get('session_id') || 'None'
            )
        );

        // Capture the fragment if available
        this.token = this.route.fragment.pipe(
            map((fragment) => fragment || 'None')
        );
    }
}
```

Параметры запроса и фрагменты также доступны через службу `ActivatedRoute`. Как и параметры маршрута, параметры запроса и фрагменты предоставляются в виде `Observable`.

Обновленный компонент Crisis Admin передает `Observable` непосредственно в шаблон с помощью `AsyncPipe`.

Теперь вы можете нажать на кнопку Admin, которая приведет вас на страницу входа с предоставленными `queryParamMap` и `fragment`. После того, как вы нажмете кнопку входа, обратите внимание, что вы были перенаправлены на страницу `Admin Dashboard` с параметрами запроса и фрагментом, все еще сохранившимися в адресной строке.

Вы можете использовать эти постоянные биты информации для вещей, которые необходимо предоставлять на разных страницах, например, токены аутентификации или идентификаторы сессии.

!!!note ""

    Параметры `query params` и `fragment` также могут быть сохранены с помощью `RouterLink` с привязками `queryParamsHandling` и `preserveFragment` соответственно.

## Веха 6: Асинхронная маршрутизация {: #asynchronous-routing}

По мере прохождения этапов приложение, естественно, становилось все больше. В какой-то момент вы достигнете точки, когда приложение будет долго загружаться.

Чтобы решить эту проблему, используйте асинхронную маршрутизацию, которая загружает функциональные модули лениво, по запросу. Ленивая загрузка имеет несколько преимуществ.

-   Вы можете загружать функциональные области только по запросу пользователя.
-   Вы можете ускорить время загрузки для пользователей, которые посещают только определенные области приложения
-   Вы можете продолжать расширять области функций с ленивой загрузкой, не увеличивая размер начального пакета загрузки.

Вы уже прошли часть этого пути. Разбив приложение на модули &mdash;`AppModule`, `HeroesModule`, `AdminModule` и `CrisisCenterModule`&mdash; вы получили естественных кандидатов для ленивой загрузки.

Некоторые модули, например `AppModule`, должны быть загружены с самого начала. Но другие можно и нужно загружать в ленивом режиме.

Например, модуль `AdminModule` нужен нескольким авторизованным пользователям, поэтому его следует загружать только по запросу нужных людей.

### Конфигурация маршрута с ленивой загрузкой {: #lazy-loading-route-config}

Измените путь `admin` в `admin-routing.module.ts` с `'admin'` на пустую строку, `''`, пустой путь.

Используйте маршруты с пустым путем для группировки маршрутов вместе без добавления дополнительных сегментов пути к URL. Пользователи по-прежнему будут посещать `/admin`, а `AdminComponent` по-прежнему будет служить компонентом маршрутизации, содержащим дочерние маршруты.

Откройте `AppRoutingModule` и добавьте новый маршрут `admin` в его массив `appRoutes`.

Задайте ему свойство `loadChildren` вместо свойства `children`. Свойство `loadChildren` принимает функцию, которая возвращает обещание, используя встроенный в браузер синтаксис для ленивой загрузки кода с использованием динамического импорта `import('...')`.

Путь - это расположение `AdminModule' (относительно корня приложения).

После запроса и загрузки кода `Promise` разрешает объект, содержащий `NgModule`, в данном случае `AdminModule`.

```ts
{
  path: 'admin',
  loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule),
},
```

!!!warning ""

    При использовании абсолютных путей расположение файла `NgModule` должно начинаться с `src/app` для корректного разрешения.
    Для пользовательского [отображения путей с абсолютными путями](https://www.typescriptlang.org/docs/handbook/module-resolution.html#path-mapping) необходимо настроить свойства `baseUrl` и `paths` в проекте `tsconfig.json`.

Когда маршрутизатор переходит к этому маршруту, он использует строку `loadChildren` для динамической загрузки `AdminModule`. Затем он добавляет маршруты `AdminModule` в свою текущую конфигурацию маршрутов.
Наконец, он загружает запрошенный маршрут в целевой компонент администратора.

Ленивая загрузка и переконфигурация происходят только один раз, когда маршрут запрашивается впервые; модуль и маршруты сразу же становятся доступными для последующих запросов.

Сделайте последний шаг и отделите набор функций администратора от основного приложения. Корневой `AppModule` не должен загружать или ссылаться на `AdminModule` или его файлы.

В файле `app.module.ts` удалите оператор импорта `AdminModule` из верхней части файла и удалите `AdminModule` из массива `imports` модуля NgModule.

### `canMatch`: защита несанкционированного доступа к функциональным модулям {: #can-match-guard}

Вы уже защищаете модуль `AdminModule` защитой `canActivate`, которая предотвращает доступ неавторизованных пользователей к области функций администратора. Он перенаправляет на страницу входа в систему, если пользователь не авторизован.

Но маршрутизатор все равно загружает `AdminModule`, даже если пользователь не может посетить ни один из его компонентов. В идеале, вы должны загружать `AdminModule`, только если пользователь вошел в систему.

Защита `canMatch` контролирует, пытается ли `Router` соответствовать `Route`. Это позволяет вам иметь несколько конфигураций `маршрутов`, которые имеют один и тот же `путь`, но сопоставляются на основе различных условий. Такой подход
позволяет `маршрутизатору` вместо подстановочного знака `маршрут`.

Существующий `authGuard` содержит логику для поддержки защиты `canMatch`.

Наконец, добавьте `authGuard` к свойству массива `canMatch` для маршрута `admin`. Готовый маршрут администратора выглядит следующим образом:

```ts
{
  path: 'admin',
  loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule),
  canMatch: [authGuard]
},
```

### Предварительная загрузка: фоновая загрузка областей функций {: #preloading}

Помимо загрузки модулей по требованию, вы можете загружать модули асинхронно с помощью предварительной загрузки.

Модуль `AppModule` загружается с нетерпением при запуске приложения, что означает, что он загружается сразу. Теперь `AdminModule` загружается только тогда, когда пользователь нажимает на ссылку, что называется ленивой загрузкой.

Предварительная загрузка позволяет загружать модули в фоновом режиме, чтобы данные были готовы к отображению, когда пользователь активирует определенный маршрут. Рассмотрим кризисный центр.
Это не первый вид, который видит пользователь.
По умолчанию Герои являются первым видом.
Для наименьшей начальной полезной нагрузки и быстрого времени запуска вам следует нетерпеливо загружать `AppModule` и `HeroesModule`.

Вы можете лениво загрузить Кризисный центр. Но вы почти уверены, что пользователь посетит Кризисный центр в течение нескольких минут после запуска приложения.
В идеале приложение должно запускаться только с загруженными `AppModule` и `HeroesModule`, а затем, почти сразу, загружать `CrisisCenterModule` в фоновом режиме.
К тому времени, когда пользователь переходит в Кризисный центр, его модуль уже загружен и готов к работе.

#### Как работает предварительная загрузка {: #how-preloading}

После каждой успешной навигации маршрутизатор ищет в своей конфигурации незагруженный модуль, который он может предварительно загрузить. Будет ли он предварительно загружать модуль, и какие модули он предварительно загружает, зависит от стратегии предварительной загрузки.

Маршрутизатор `Router` предлагает две стратегии предварительной загрузки:

| Стратегии                    | Подробности                                                                             |
| :--------------------------- | :-------------------------------------------------------------------------------------- |
| Без предварительной загрузки | По умолчанию. Лениво загруженные области функций по-прежнему загружаются по требованию. |
| Предварительная загрузка     | Все лениво загруженные области функций предварительно загружаются.                      |

Маршрутизатор либо никогда не выполняет предварительную загрузку, либо выполняет предварительную загрузку каждого лениво загруженного модуля. Маршрутизатор также поддерживает [пользовательские стратегии предварительной загрузки](#custom-preloading) для точного контроля над тем, какие модули и когда предварительно загружать.

Этот раздел поможет вам обновить модуль `CrisisCenterModule`, чтобы он загружался лениво по умолчанию и использовал стратегию `PreloadAllModules` для загрузки всех лениво загруженных модулей.

#### Ленивая загрузка кризисного центра {: #lazy-load-crisis-center}

Обновите конфигурацию маршрута для ленивой загрузки модуля `CrisisCenterModule`. Выполните те же шаги, что и при настройке `AdminModule` для ленивой загрузки.

1.  Измените путь `crisis-center` в `CrisisCenterRoutingModule` на пустую строку.
2.  Добавьте маршрут `кризисного центра` в `AppRoutingModule`.
3.  Установите строку `loadChildren` для загрузки модуля `CrisisCenterModule`.
4.  Удалите все упоминания о `CrisisCenterModule` из `app.module.ts`.

Вот обновленные модули _до включения предварительной загрузки_:

=== "app.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { FormsModule } from '@angular/forms';
    import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

    import { Router } from '@angular/router';

    import { AppComponent } from './app.component';
    import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
    import { ComposeMessageComponent } from './compose-message/compose-message.component';

    import { AppRoutingModule } from './app-routing.module';
    import { HeroesModule } from './heroes/heroes.module';
    import { AuthModule } from './auth/auth.module';

    @NgModule({
    	imports: [
    		BrowserModule,
    		BrowserAnimationsModule,
    		FormsModule,
    		HeroesModule,
    		AuthModule,
    		AppRoutingModule,
    	],
    	declarations: [
    		AppComponent,
    		ComposeMessageComponent,
    		PageNotFoundComponent,
    	],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

=== "app-routing.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { RouterModule, Routes } from '@angular/router';

    import { ComposeMessageComponent } from './compose-message/compose-message.component';
    import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

    import { authGuard } from './auth/auth.guard';

    const appRoutes: Routes = [
    	{
    		path: 'compose',
    		component: ComposeMessageComponent,
    		outlet: 'popup',
    	},
    	{
    		path: 'admin',
    		loadChildren: () =>
    			import('./admin/admin.module').then(
    				(m) => m.AdminModule
    			),
    		canMatch: [authGuard],
    	},
    	{
    		path: 'crisis-center',
    		loadChildren: () =>
    			import(
    				'./crisis-center/crisis-center.module'
    			).then((m) => m.CrisisCenterModule),
    	},
    	{ path: '', redirectTo: '/heroes', pathMatch: 'full' },
    	{ path: '**', component: PageNotFoundComponent },
    ];

    @NgModule({
    	imports: [RouterModule.forRoot(appRoutes)],
    	exports: [RouterModule],
    })
    export class AppRoutingModule {}
    ```

=== "crisis-center-routing.module.ts"

    ```ts
    import { NgModule } from '@angular/core';
    import { RouterModule, Routes } from '@angular/router';

    import { CrisisCenterHomeComponent } from './crisis-center-home/crisis-center-home.component';
    import { CrisisListComponent } from './crisis-list/crisis-list.component';
    import { CrisisCenterComponent } from './crisis-center/crisis-center.component';
    import { CrisisDetailComponent } from './crisis-detail/crisis-detail.component';

    import { canDeactivateGuard } from '../can-deactivate.guard';
    import { crisisDetailResolver } from './crisis-detail-resolver';

    const crisisCenterRoutes: Routes = [
    	{
    		path: '',
    		component: CrisisCenterComponent,
    		children: [
    			{
    				path: '',
    				component: CrisisListComponent,
    				children: [
    					{
    						path: ':id',
    						component: CrisisDetailComponent,
    						canDeactivate: [canDeactivateGuard],
    						resolve: {
    							crisis: crisisDetailResolver,
    						},
    					},
    					{
    						path: '',
    						component: CrisisCenterHomeComponent,
    					},
    				],
    			},
    		],
    	},
    ];

    @NgModule({
    	imports: [RouterModule.forChild(crisisCenterRoutes)],
    	exports: [RouterModule],
    })
    export class CrisisCenterRoutingModule {}
    ```

Вы можете попробовать сделать это сейчас и убедиться, что модуль `CrisisCenterModule` загружается после нажатия кнопки "Crisis Center".

Чтобы включить предварительную загрузку всех лениво загруженных модулей, импортируйте маркер `PreloadAllModules` из пакета Angular router.

Второй аргумент в методе `RouterModule.forRoot()` принимает объект для дополнительных опций конфигурации. Одним из таких параметров является `preloadingStrategy`.
Добавьте маркер `PreloadAllModules` к вызову `forRoot()`:

```ts
RouterModule.forRoot(appRoutes, {
    enableTracing: true, // <-- debugging purposes only
    preloadingStrategy: PreloadAllModules,
});
```

Это настраивает предзагрузчик `Router` на немедленную загрузку всех лениво загруженных маршрутов (маршруты со свойством `loadChildren`).

Когда вы посещаете сайт `http://localhost:4200`, маршрут `/heroes` загружается сразу после запуска, а маршрутизатор начинает загружать `CrisisCenterModule` сразу после загрузки `HeroesModule`.

### Пользовательская стратегия предзагрузки {: #custom-preloading}

Предварительная загрузка каждого лениво загруженного модуля хорошо работает во многих ситуациях. Однако, учитывая такие вещи, как низкая пропускная способность и пользовательские показатели, вы можете использовать пользовательскую стратегию предварительной загрузки для определенных функциональных модулей.

Этот раздел поможет вам добавить пользовательскую стратегию, которая будет предзагружать только те маршруты, флаг `data.preload` которых установлен на `true`. Напомним, что в свойство `data` маршрута можно добавить что угодно.

Установите флаг `data.preload` в маршруте `crisis-center` в модуле `AppRoutingModule`.

```ts
{
  path: 'crisis-center',
  loadChildren: () => import('./crisis-center/crisis-center.module').then(m => m.CrisisCenterModule),
  data: { preload: true }
},
```

Создайте новую службу `SelectivePreloadingStrategy`.

```shell
ng generate service selective-preloading-strategy
```

Замените содержимое `selective-preloading-strategy.service.ts` на следующее:

```ts
import { Injectable } from '@angular/core';
import { PreloadingStrategy, Route } from '@angular/router';
import { Observable, of } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class SelectivePreloadingStrategyService
    implements PreloadingStrategy {
    preloadedModules: string[] = [];

    preload(
        route: Route,
        load: () => Observable<any>
    ): Observable<any> {
        if (
            route.canMatch === undefined &&
            route.data?.['preload'] &&
            route.path != null
        ) {
            // add the route path to the preloaded module array
            this.preloadedModules.push(route.path);

            // log the route path to the console
            console.log('Preloaded: ' + route.path);

            return load();
        } else {
            return of(null);
        }
    }
}
```

`SelectivePreloadingStrategyService` реализует `PreloadingStrategy`, которая имеет один метод `preload()`.

Маршрутизатор вызывает метод `preload()` с двумя аргументами:

1.  Маршрут, который необходимо рассмотреть.
1.  Функция загрузчика, которая может асинхронно загружать маршрутизируемый модуль.

Реализация `preload` должна возвращать `Observable`. Если маршрут выполняет предварительную загрузку, он возвращает наблюдаемую, полученную при вызове функции-загрузчика.
Если маршрут не загружается, он возвращает `Observable` в значении `null`.

В этом примере метод `preload()` загружает маршрут, если флаг маршрута `data.preload` является истинным. Мы также пропускаем загрузку `маршрута`, если есть защита `canMatch`, потому что пользователь может не иметь к ней доступа.
не имеет к нему доступа.

В качестве побочного эффекта, `SelectivePreloadingStrategyService` записывает `путь` выбранного маршрута в свой публичный массив `preloadedModules`.

Вскоре вы расширите `AdminDashboardComponent`, чтобы внедрить этот сервис и отобразить его массив `preloadedModules`.

Но сначала внесите несколько изменений в `AppRoutingModule`.

1.  Импортируйте `SelectivePreloadingStrategyService` в `AppRoutingModule`.
1.  Замените стратегию `PreloadAllModules` в вызове `forRoot()` на эту `SelectivePreloadingStrategyService`.

Теперь отредактируйте `AdminDashboardComponent` для отображения журнала предварительно загруженных маршрутов.

1.  Импортируйте `SelectivePreloadingStrategyService`.
1.  Вставьте его в конструктор приборной панели.
1.  Обновите шаблон, чтобы отобразить массив `preloadedModules` службы стратегий.

Теперь файл выглядит следующим образом:

```ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { SelectivePreloadingStrategyService } from '../../selective-preloading-strategy.service';

@Component({
    selector: 'app-admin-dashboard',
    templateUrl: './admin-dashboard.component.html',
    styleUrls: ['./admin-dashboard.component.css'],
})
export class AdminDashboardComponent implements OnInit {
    sessionId!: Observable<string>;
    token!: Observable<string>;
    modules: string[] = [];

    constructor(
        private route: ActivatedRoute,
        preloadStrategy: SelectivePreloadingStrategyService
    ) {
        this.modules = preloadStrategy.preloadedModules;
    }

    ngOnInit() {
        // Capture the session ID if available
        this.sessionId = this.route.queryParamMap.pipe(
            map(
                (params) =>
                    params.get('session_id') || 'None'
            )
        );

        // Capture the fragment if available
        this.token = this.route.fragment.pipe(
            map((fragment) => fragment || 'None')
        );
    }
}
```

Как только приложение загрузит начальный маршрут, модуль `Кризис-центр` будет предварительно загружен. Убедитесь в этом, войдя в область функций `Admin` и отметив, что `кризис-центр` находится в списке `предзагруженных модулей`.

Он также регистрируется в консоли браузера.

### Перенос URL-адресов с помощью перенаправлений {: #redirect-advanced}

Вы настроили маршруты для перемещения по вашему приложению и используете навигацию императивно и декларативно. Но, как и в любом приложении, требования со временем меняются.
Вы настроили ссылки и навигацию на `/heroes` и `/hero/:id` из компонентов `HeroListComponent` и `HeroDetailComponent`.

Если бы существовало требование, чтобы ссылки на `героев` стали `супергероями`, вы бы все равно хотели, чтобы предыдущие URL были корректными для навигации.
Вы также не хотите обновлять каждую ссылку в вашем приложении, поэтому перенаправления делают рефакторинг маршрутов тривиальным.

#### Изменение `/heroes` на `/superheroes` {: #url-refactor}

Этот раздел поможет вам перенести маршруты `Hero` на новые URL. Маршрутизатор `Router` проверяет наличие перенаправлений в вашей конфигурации перед началом навигации, поэтому каждое перенаправление запускается по мере необходимости.

Чтобы поддержать это изменение, добавьте перенаправления со старых маршрутов на новые в `heroes-routing.module`.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HeroListComponent } from './hero-list/hero-list.component';
import { HeroDetailComponent } from './hero-detail/hero-detail.component';

const heroesRoutes: Routes = [
    { path: 'heroes', redirectTo: '/superheroes' },
    { path: 'hero/:id', redirectTo: '/superhero/:id' },
    {
        path: 'superheroes',
        component: HeroListComponent,
        data: { animation: 'heroes' },
    },
    {
        path: 'superhero/:id',
        component: HeroDetailComponent,
        data: { animation: 'hero' },
    },
];

@NgModule({
    imports: [RouterModule.forChild(heroesRoutes)],
    exports: [RouterModule],
})
export class HeroesRoutingModule {}
```

Обратите внимание на два разных типа перенаправления. Первое изменение - с `/heroes` на `/superheroes` без каких-либо параметров.
Второе изменение - с `/hero/:id` на `/superhero/:id`, которое включает параметр маршрута `:id`.
Перенаправления маршрутизатора также используют мощное сопоставление шаблонов, поэтому `Router` проверяет URL и заменяет параметры маршрута в `path` на соответствующие назначения.
Ранее вы переходили на URL, например `/hero/15`, с параметром маршрута `id`, равным `15`.

!!!note ""

    Маршрутизатор `Router` также поддерживает [параметры запроса](#query-parameters) и [фрагмент](#fragment) при использовании перенаправлений.

    - При использовании абсолютных перенаправлений `Router` использует параметры запроса и фрагмент из `redirectTo` в конфигурации маршрута.
    - При использовании относительных перенаправлений `Router` использует параметры запроса и фрагмент из исходного URL

В настоящее время пустой маршрут перенаправляет на `/heroes`, который перенаправляет на `/superheroes`. Это не будет работать, потому что `Router` обрабатывает перенаправления один раз на каждом уровне конфигурации маршрутизации.
Это предотвращает цепочку перенаправлений, которая может привести к бесконечным петлям перенаправления.

Вместо этого обновите пустой маршрут пути в `app-routing.module.ts`, чтобы он перенаправлял на `/superheroes`.

```ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ComposeMessageComponent } from './compose-message/compose-message.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

import { authGuard } from './auth/auth.guard';
import { SelectivePreloadingStrategyService } from './selective-preloading-strategy.service';

const appRoutes: Routes = [
    {
        path: 'compose',
        component: ComposeMessageComponent,
        outlet: 'popup',
    },
    {
        path: 'admin',
        loadChildren: () =>
            import('./admin/admin.module').then(
                (m) => m.AdminModule
            ),
        canMatch: [authGuard],
    },
    {
        path: 'crisis-center',
        loadChildren: () =>
            import(
                './crisis-center/crisis-center.module'
            ).then((m) => m.CrisisCenterModule),
        data: { preload: true },
    },
    {
        path: '',
        redirectTo: '/superheroes',
        pathMatch: 'full',
    },
    { path: '**', component: PageNotFoundComponent },
];

@NgModule({
    imports: [
        RouterModule.forRoot(appRoutes, {
            enableTracing: false, // <-- debugging purposes only
            preloadingStrategy: SelectivePreloadingStrategyService,
        }),
    ],
    exports: [RouterModule],
})
export class AppRoutingModule {}
```

Ссылка `routerLink` не привязана к конфигурации маршрута, поэтому обновите связанные с ней ссылки маршрутизатора, чтобы они оставались активными при активном новом маршруте. Обновите шаблон `app.component.ts` для `/heroes` `routerLink`.

```html
<div class="wrapper">
    <h1 class="title">Angular Router</h1>
    <nav>
        <a
            routerLink="/crisis-center"
            routerLinkActive="active"
            ariaCurrentWhenActive="page"
            >Crisis Center</a
        >
        <a
            routerLink="/superheroes"
            routerLinkActive="active"
            ariaCurrentWhenActive="page"
            >Heroes</a
        >
        <a
            routerLink="/admin"
            routerLinkActive="active"
            ariaCurrentWhenActive="page"
            >Admin</a
        >
        <a
            routerLink="/login"
            routerLinkActive="active"
            ariaCurrentWhenActive="page"
            >Login</a
        >
        <a
            [routerLink]="[{ outlets: { popup: ['compose'] } }]"
            >Contact</a
        >
    </nav>
    <div [@routeAnimation]="getRouteAnimationData()">
        <router-outlet></router-outlet>
    </div>
    <router-outlet name="popup"></router-outlet>
</div>
```

Обновите метод `goToHeroes()` в `hero-detail.component.ts` для перехода к `/superheroes` с необязательными параметрами маршрута.

```ts
gotoHeroes(hero: Hero) {
  const heroId = hero ? hero.id : null;
  // Pass along the hero id if available
  // so that the HeroList component can select that hero.
  // Include a junk 'foo' property for fun.
  this.router.navigate(['/superheroes', {id: heroId, foo: 'foo'}]);
}
```

После установки перенаправлений все предыдущие маршруты теперь указывают на новые места назначения, и оба URL по-прежнему функционируют как положено.

### Проверка конфигурации маршрутизатора {: #inspect-config}

Чтобы определить, действительно ли ваши маршруты оцениваются [в правильном порядке](#routing-module-order), вы можете проверить конфигурацию маршрутизатора.

Для этого нужно внедрить маршрутизатор и записать в консоль его свойство `config`. Например, обновите `AppModule` следующим образом и посмотрите в окне консоли браузера готовую конфигурацию маршрута.

```ts
export class AppModule {
    // Diagnostic only: inspect router configuration
    constructor(router: Router) {
        // Use a custom replacer to display function names in the route configs
        const replacer = (key, value) =>
            typeof value === 'function'
                ? value.name
                : value;

        console.log(
            'Routes: ',
            JSON.stringify(router.config, replacer, 2)
        );
    }
}
```

## Готовое приложение {: #final-app}

Готовое приложение маршрутизатора смотрите в [примере](https://angular.io/generated/live-examples/router/stackblitz.html) для окончательного исходного кода.
