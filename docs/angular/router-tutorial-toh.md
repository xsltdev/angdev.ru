<a id="router-tutorial"></a>

# Учебник по маршрутизатору: экскурсия по героям

В этом учебнике представлен обширный обзор маршрутизатора Angular. В этом уроке вы, основываясь на базовой конфигурации маршрутизатора, изучите такие возможности, как дочерние маршруты, параметры маршрута, ленивая загрузка NgModules, защитные маршруты и предварительная загрузка данных для улучшения пользовательского опыта.

Рабочий пример окончательной версии приложения смотрите в <live-example name="router"></live-example>.

<a id="router-tutorial-objectives"></a>

## Цели

Это руководство описывает разработку многостраничного маршрутизируемого примера приложения. Попутно в нем освещаются ключевые особенности маршрутизатора, такие как:

-   Организация функций приложения в модули

-   Переход к компоненту \(_Герои_ ссылка на "Список героев"\)

-   Включение параметра маршрута \(передача `id` героя при маршрутизации к "Детали героя"\)

-   Дочерние маршруты \(у _Кризисного центра_ есть свои собственные маршруты\)

-   Страж `canActivate` \(проверка доступа к маршруту\)

-   Страж `canActivateChild` \(проверка доступа к дочерним маршрутам\)

-   Страж `canDeactivate` \(запрашивать разрешение на удаление несохраненных изменений\)

-   Страж `resolve` \(предварительная выборка данных маршрута\\)

-   Ленивая загрузка `NgModule`

-   Страж `canMatch` \(проверка перед загрузкой активов функционального модуля\)

Это руководство построено в виде последовательности этапов, как если бы вы создавали приложение шаг за шагом, но предполагает, что вы знакомы с основными [концепциями Angular](руководство/архитектура). Для общего введения в angular смотрите [Getting Started](начало).

Для более подробного обзора смотрите учебник [Tour of Heroes](tutorial/tour-of-heroes).

## Предварительные условия

Чтобы завершить этот учебник, вы должны иметь базовое понимание следующих концепций:

-   JavaScript

-   HTML

-   CSS

-   [Angular CLI](cli).

Вам может быть полезен учебник [Tour of Heroes](tutorial/tour-of-heroes), но он не обязателен.

## Пример приложения в действии

Пример приложения для этого учебника помогает Агентству по трудоустройству героев находить кризисы для героев.

Приложение имеет три основные функции:

1.  Кризисный центр" для ведения списка кризисов для поручения героям.

1.  Область _Герои_ для ведения списка героев, нанятых агентством.

1.  Область _Админ_ для управления списком кризисов и героев.

Попробуйте это сделать, щелкнув по этой ссылке <live-example name="router" title="Hero Employment Agency Live Example">live example link</live-example>.

Приложение отображается с рядом навигационных кнопок и представлением _Heroes_ со списком героев.

<div class="lightbox">

<img alt="Example application with a row of navigation buttons and a list of heroes" src="generated/images/guide/router/hero-list.gif">

</div>

Выберите одного героя, и приложение переведет вас на экран редактирования героя.

<div class="lightbox">

<img alt="Detail view of hero with additional information, input, and back button" src="generated/images/guide/router/hero-detail.png">

</div>

Измените имя. Нажмите кнопку "Назад", и приложение вернется к списку героев, в котором будет отображаться измененное имя героя.
Обратите внимание, что изменение имени вступило в силу немедленно.

Если бы вы нажали кнопку "Назад" браузера, а не кнопку "Назад" приложения, приложение также вернуло бы вас к списку героев. Навигация в приложениях Angular обновляет историю браузера так же, как и обычная веб-навигация.

Теперь нажмите на ссылку _Кризисный центр_ для получения списка текущих кризисов.

<div class="lightbox">

<img alt="Crisis Center list of crises" src="generated/images/guide/router/crisis-center-list.gif">

</div>

Выберите кризис, и приложение переведет вас на экран редактирования кризиса. На той же странице, под списком, в дочернем компоненте появляется _Деталь кризиса_.

Измените название кризиса. Обратите внимание, что соответствующее название в списке кризисов _не_ изменяется.

<div class="lightbox">

<img alt="Crisis Center detail of a crisis with data, an input, and save and cancel buttons." src="generated/images/guide/router/crisis-center-detail.gif">

</div>

В отличие от _Hero Detail_, который обновляется по мере ввода текста, изменения в _Crisis Detail_ являются временными, пока вы не сохраните или не отмените их нажатием кнопок "Сохранить" или "Отмена". Обе кнопки позволяют вернуться к _Кризисному центру_ и его списку кризисов.

Нажмите кнопку "Назад" браузера или ссылку "Герои", чтобы активировать диалог.

<div class="lightbox">

<img alt="Alert that asks user to confirm discarding changes" src="generated/images/guide/router/confirm-dialog.png">

</div>

Вы можете сказать "OK" и потерять свои изменения или нажать "Cancel" и продолжить редактирование.

За этим поведением стоит защита маршрутизатора `canDeactivate`. Эта защита дает вам шанс очистить или спросить разрешения пользователя, прежде чем переходить от текущего представления.

Кнопки `Admin` и `Login` иллюстрируют другие возможности маршрутизатора, которые будут рассмотрены далее в руководстве.

<a id="getting-started"></a>

## Этап 1: Начало работы

Начните с базовой версии приложения, которое перемещается между двумя пустыми представлениями.

<div class="lightbox">

<img alt="Animated image of application with a Crisis Center button and a Heroes button. The pointer clicks each button to show a view for each." src="generated/images/guide/router/router-1-anim.gif">

</div>

<a id="import"></a>

### Создайте пример приложения

1. Создайте новый проект Angular, _angular-router-tour-of-heroes_.

    <code-example format="shell" language="shell">

    ng new angular-router-tour-of-heroes

    </code-example>

    Когда появится запрос `Вы хотите добавить маршрутизацию Angular?`, выберите `N`.

    На вопрос `Какой формат таблицы стилей вы хотите использовать?` выберите `CSS`.

    Через несколько мгновений новый проект `angular-router-tour-of-heroes` будет готов.

1. В терминале перейдите в каталог `angular-router-tour-of-heroes`.

1. Убедитесь, что ваше новое приложение работает как ожидалось, выполнив команду `ng serve`.

    <code-example language="sh">

    ng serve

    </code-example

1. Откройте браузер на `http://localhost:4200`.

    Вы должны увидеть запущенное приложение в браузере.

### Определение маршрутов

Маршрутизатор должен быть сконфигурирован со списком определений маршрутов.

Каждое определение преобразуется в объект [Route](api/router/Route), который содержит две вещи: `path` - сегмент пути URL для этого маршрута; и `component` - компонент, связанный с этим маршрутом.

Маршрутизатор обращается к своему реестру определений при изменении URL браузера или когда код приложения указывает маршрутизатору перемещаться по пути маршрута.

Первый маршрут делает следующее:

-   Когда URL-адрес местоположения браузера меняется на соответствующий сегмент пути `/crisis-center`, маршрутизатор активирует экземпляр `CrisisListComponent` и отображает его представление.

-   Когда приложение запрашивает навигацию к пути `/crisis-center`, маршрутизатор активирует экземпляр `CrisisListComponent`, отображает его представление и обновляет адрес местоположения и историю браузера с URL для этого пути.

Первая конфигурация определяет массив из двух маршрутов с минимальными путями, ведущими к `CrisisListComponent` и `HeroListComponent`.

Создайте компоненты `CrisisList` и `HeroList`, чтобы маршрутизатору было что отображать.

<code-example format="shell" language="shell">

ng генерировать компонент crisis-list

</code-example>

<code-example format="shell" language="shell">

ng generate component hero-list

</code-example>

Замените содержимое каждого компонента следующим образцом HTML.

<code-tabs> <code-pane header="src/app/crisis-list/crisis-list.component.html" path="router/src/app/crisis-list/crisis-list.component.1.html"></code-pane>
<code-pane header="src/app/hero-list/hero-list.component.html" path="router/src/app/hero-list/hero-list.component.1.html" region="template"></code-pane>
</code-tabs>

### Зарегистрируйте `Router` и `Routes`.

Чтобы использовать `Router`, вы должны сначала зарегистрировать `RouterModule` из пакета `@angular/router`. Определите массив маршрутов, `appRoutes`, и передайте их в метод `RouterModule.forRoot()`.

Метод `RouterModule.forRoot()` возвращает модуль, содержащий настроенный поставщик услуг `Router`, а также другие поставщики, необходимые библиотеке маршрутизации.

После загрузки приложения `Router` выполняет начальную навигацию на основе текущего URL браузера.

<div class="alert is-important">

**NOTE**: <br /> The `RouterModule.forRoot()` method is a pattern used to register application-wide providers. Read more about application-wide providers in the [Singleton services](guide/singleton-services#forRoot-router) guide.

</div>

<code-example header="src/app/app.module.ts (first-config)" path="router/src/app/app.module.1.ts" region="first-config"></code-example>

<div class="alert is-helpful">

Добавление настроенного `RouterModule` к `AppModule` достаточно для минимальных конфигураций маршрутов. Однако, по мере роста приложения, [рефакторинг конфигурации маршрутизации](#refactor-the-routing-configuration-into-a-routing-module) в отдельный файл и создание [модуля маршрутизации](#routing-module).
Модуль маршрутизации - это специальный тип `Service Module`, предназначенный для маршрутизации.

</div>

Регистрация `RouterModule.forRoot()` в массиве `AppModule` `imports` делает сервис `Router` доступным везде в приложении.

<a id="shell"></a>

### Добавьте выход маршрутизатора

Корневой `AppComponent` - это оболочка приложения. Она имеет заголовок, панель навигации с двумя ссылками и выход маршрутизатора, в котором маршрутизатор рендерит компоненты.

<div class="lightbox">

<img alt="A nav, made of two navigation buttons, with the first button active and its associated view displayed" src="generated/images/guide/router/shell-and-outlet.gif">

</div>

Розетка маршрутизатора служит в качестве места, куда выводятся маршрутизируемые компоненты.

<a id="shell-template"></a>.

Соответствующий шаблон компонента выглядит следующим образом:

<code-example header="src/app/app.component.html" path="router/src/app/app.component.1.html"></code-example>

<a id="wildcard"></a>

### Определение маршрута с подстановочным знаком

До сих пор вы создали два маршрута в приложении: один к `/crisis-center` и другой к `/heroes`. Любой другой URL вызывает ошибку маршрутизатора и крах приложения.

Добавьте маршрут с подстановочными знаками, чтобы перехватывать недействительные URL и обрабатывать их изящно. Маршрут с подстановочным знаком имеет путь, состоящий из двух звездочек.

Он соответствует любому URL.

Таким образом, маршрутизатор выбирает этот маршрут с подстановочным знаком, если не может найти маршрут в предыдущей конфигурации.

Маршрут с подстановочным знаком может переходить к пользовательскому компоненту "404 Not Found" или [redirect](#redirect) к существующему маршруту.

<div class="alert is-helpful">

Маршрутизатор выбирает маршрут с помощью стратегии [_первое совпадение выигрывает_](guide/router-reference#example-config). Поскольку маршрут с подстановочным знаком является наименее специфичным маршрутом, поместите его последним в конфигурации маршрута.

</div>

Чтобы проверить эту возможность, добавьте кнопку с `RouterLink` в шаблон `HeroListComponent` и установите ссылку на несуществующий маршрут под названием `"/sidekicks"`.

<code-example header="src/app/hero-list/hero-list.component.html (excerpt)" path="router/src/app/hero-list/hero-list.component.1.html"></code-example>.

Приложение потерпит неудачу, если пользователь нажмет на эту кнопку, потому что вы еще не определили маршрут `"/sidekicks"`.

Вместо добавления маршрута `sidekicks` определите маршрут `wildcard` и попросите его перейти к `PageNotFoundComponent`.

<code-example header="src/app/app.module.ts (wildcard)" path="router/src/app/app.module.1.ts" region="wildcard"></code-example>

Создайте компонент `PageNotFoundComponent` для отображения, когда пользователи посещают недопустимые URL.

<code-example format="shell" language="shell">

ng generate component page-not-found

</code-example>

<code-example header="src/app/page-not-found.component.html (404 компонент)" path="router/src/app/page-not-found/page-not-found.component.html"></code-example>.

Теперь, когда пользователь посещает `/sidekicks`, или любой другой недействительный URL, браузер выдает "Страница не найдена". Адресная строка браузера продолжает указывать на недопустимый URL.

<a id="redirect"></a>

### Настройка перенаправлений

Когда приложение запускается, по умолчанию в строке браузера находится начальный URL:

<code-example format="http" language="http">

localhost:4200

</code-example>

Это не соответствует ни одному из жестко закодированных маршрутов, что означает, что маршрутизатор переходит на маршрут с подстановочным знаком и отображает `PageNotFoundComponent`.

Приложению нужен маршрут по умолчанию к действительной странице. Страница по умолчанию для этого приложения - это список героев.

Приложение должно переходить на нее, как если бы пользователь щелкнул по ссылке "Heroes" или вставил `localhost:4200/heroes` в адресную строку.

Добавьте маршрут `redirect`, который переводит исходный относительный URL \(`''`\) в путь по умолчанию \(`/heroes`\), который вы хотите.

Добавьте маршрут по умолчанию где-то _выше_ маршрута дикого символа. Он находится чуть выше маршрута wildcard в следующей выдержке, показывающей полный `appRoutes` для этой вехи.

<code-example header="src/app/app-routing.module.ts (appRoutes)" path="router/src/app/app-routing.module.1.ts" region="appRoutes"></code-example>.

В адресной строке браузера отображается `.../heroes`, как если бы вы перешли туда напрямую.

Маршрут перенаправления требует свойства `pathMatch`, чтобы указать маршрутизатору, как сопоставить URL с путем маршрута. В этом приложении маршрутизатор должен выбрать маршрут к `HeroListComponent` только тогда, когда _полный URL_ соответствует `''`, поэтому установите значение `pathMatch` в `'full'`.

<a id="pathmatch"></a>

<div class="callout is-helpful">

<header>Spotlight on pathMatch</header>

Технически, `pathMatch = 'full'` приводит к попаданию в маршрут, когда _оставшиеся_, несопоставленные сегменты URL совпадают с `''`. В данном примере перенаправление происходит в маршруте верхнего уровня, поэтому _оставшийся_ URL и _полный_ URL - это одно и то же.

Другим возможным значением `pathMatch` является `'prefix'`, которое указывает маршрутизатору соответствовать маршруту перенаправления, если оставшийся URL начинается с пути префикса маршрута перенаправления. Это не относится к данному примеру приложения, потому что если бы значение `pathMatch` было `'prefix'`, каждый URL совпадал бы с `'prefix'`.

Попробуйте установить значение `'prefix'` и нажмите кнопку `Go to sidekicks`. Поскольку это плохой URL, вы должны увидеть страницу "Страница не найдена".

Вместо этого вы все еще находитесь на странице "Герои".

Введите плохой URL-адрес в адресную строку браузера.

Вы будете мгновенно перенаправлены на страницу `/heroes`.

Каждый URL, хороший или плохой, который попадает в это определение маршрута, является подходящим.

Маршрут по умолчанию должен перенаправлять на `HeroListComponent` только в том случае, если весь URL имеет вид `''`''. Не забудьте восстановить перенаправление на `pathMatch = 'full'`.

Узнайте больше в [посте Виктора Савкина о редиректах](https://vsavkin.tumblr.com/post/146722301646/angular-router-empty-paths-componentless-routes).

</div>

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

<div class="filetree">   <div class="file">
    angular-router-tour-of-heroes
  </div>
  <div class="children">
    <div class="file">
      src
    </div>
    <div class="children">
      <div class="file">
        app
      </div>
      <div class="children">
        <div class="file">
          crisis-list
        </div>
        <div class="children">
          <div class="file">
            crisis-list.component.css
          </div>
          <div class="file">
            crisis-list.component.html
          </div>
          <div class="file">
            crisis-list.component.ts
          </div>
        </div>
        <div class="file">
          hero-list
        </div>
        <div class="children">
          <div class="file">
            hero-list.component.css
          </div>
          <div class="file">
            hero-list.component.html
          </div>
          <div class="file">
            hero-list.component.ts
          </div>
        </div>
        <div class="file">
          page-not-found
        </div>
        <div class="children">
          <div class="file">
            page-not-found.component.css
          </div>
          <div class="file">
            page-not-found.component.html
          </div>
          <div class="file">
            page-not-found.component.ts
          </div>
        </div>
        <div class="file">
          app.component.css
        </div>
        <div class="file">
          app.component.html
        </div>
        <div class="file">
          app.component.ts
        </div>
        <div class="file">
          app.module.ts
        </div>
      </div>
      <div class="file">
        main.ts
      </div>
      <div class="file">
        index.html
      </div>
      <div class="file">
        styles.css
      </div>
      <div class="file">
        tsconfig.json
      </div>
    </div>
    <div class="file">
      node_modules &hellip;
    </div>
    <div class="file">
      package.json
    </div>
  </div>
</div>

Вот файлы этой вехи.

<code-tabs> <code-pane header="app.component.html" path="router/src/app/app.component.1.html"></code-pane>
<code-pane header="app.module.ts" path="router/src/app/app.module.1.ts"></code-pane>
<code-pane header="hero-list/hero-list.component.html" path="router/src/app/hero-list/hero-list.component.1.html"></code-pane>
<code-pane header="crisis-list/crisis-list.component.html" path="router/src/app/crisis-list/crisis-list.component.1.html"></code-pane>
<code-pane header="page-not-found/page-not-found.component.html" path="router/src/app/page-not-found/page-not-found.component.html"></code-pane>
<code-pane header="index.html" path="router/src/index.html"></code-pane>
</code-tabs>

<a id="routing-module"></a>

## Этап 2: _Модуль маршрутизации_

Этот этап показывает, как настроить специализированный модуль _Модуль маршрутизации_, который хранит конфигурацию маршрутизации вашего приложения.

Модуль маршрутизации имеет несколько характеристик:

-   Отделяет проблемы маршрутизации от других проблем приложения.

-   Предоставляет модуль для замены или удаления при тестировании приложения

-   Обеспечивает известное местоположение для поставщиков услуг маршрутизации, таких как охранники и резолверы.

-   Не объявляет компоненты

<a id="integrate-routing"></a>

### Интегрируйте маршрутизацию в ваше приложение

Пример приложения с маршрутизацией не включает маршрутизацию по умолчанию. Когда вы используете [Angular CLI](cli) для создания проекта, который использует маршрутизацию, установите опцию `--routing` для проекта или приложения, а также для каждого NgModule.

Когда вы создаете или инициализируете новый проект\(используя команду CLI [`ng new`](cli/new)\) или новое приложение\(используя команду [`ng generate app`](cli/generate)\), укажите опцию `--routing`.

Это даст команду CLI включить пакет `@angular/router` npm и создать файл с именем `app-routing.module.ts`.

Затем вы сможете использовать маршрутизацию в любом Ng-модуле, который вы добавите в проект или приложение.

Например, следующая команда создает NgModule, который может использовать маршрутизацию.

<code-example format="shell" language="shell">

ng generate module my-module --routing

</code-example>

Это создает отдельный файл `my-module-routing.module.ts` для хранения маршрутов NgModule. Файл включает пустой объект `Routes`, который вы можете заполнить маршрутами к различным компонентам и NgModules.

<a id="routing-refactor"></a>

### Рефакторинг конфигурации маршрутизации в модуль маршрутизации

Создайте модуль `AppRouting` в папке `/app`, который будет содержать конфигурацию маршрутизации.

<code-example format="shell" language="shell">

ng generate module app-routing --module app --flat

</code-example>

Импортируйте символы `CrisisListComponent`, `HeroListComponent` и `PageNotFoundComponent`, как вы это сделали в `app.module.ts`. Затем перенесите импорт `Router` и конфигурацию маршрутизации, включая `RouterModule.forRoot()`, в этот модуль маршрутизации.

Реэкспортируйте модуль Angular `RouterModule`, добавив его в массив `exports` модуля. Благодаря реэкспорту `RouterModule` здесь, компоненты, объявленные в `AppModule`, получают доступ к директивам маршрутизации, таким как `RouterLink` и `RouterOutlet`.

После этих шагов файл должен выглядеть следующим образом.

<code-example header="src/app/app-routing.module.ts" path="router/src/app/app-routing.module.1.ts"></code-example>.

Далее обновите файл `app.module.ts`, удалив `RouterModule.forRoot` в массиве `imports`.

<code-example header="src/app/app.module.ts" path="router/src/app/app.module.2.ts"></code-example>

<div class="alert is-helpful">

Позже в этом руководстве будет показано, как создать [несколько модулей маршрутизации](#heroes-functionality) и импортировать эти модули маршрутизации [в правильном порядке](#routing-module-order).

</div>

Приложение продолжает работать точно так же, и вы можете использовать `AppRoutingModule` в качестве центрального места для сохранения будущей конфигурации маршрутизации.

<a id="why-routing-module"></a>

### Преимущества модуля маршрутизации

Модуль маршрутизации, часто называемый `AppRoutingModule`, заменяет конфигурацию маршрутизации в корневом или функциональном модуле.

Модуль маршрутизации полезен по мере роста вашего приложения и когда конфигурация включает специализированные функции guard и resolver.

Некоторые разработчики пропускают модуль маршрутизации, когда конфигурация минимальна, и объединяют конфигурацию маршрутизации непосредственно в сопутствующий модуль\(например, `AppModule`\).

Большинство приложений должны реализовать модуль маршрутизации для согласованности. Он сохраняет код чистым, когда конфигурация становится сложной.

Он облегчает тестирование функционального модуля.

Его существование привлекает внимание к тому, что модуль маршрутизирован.

Именно здесь разработчики ожидают найти и расширить конфигурацию маршрутизации.

<a id="heroes-feature"></a>

## Веха 3: Функция героев

Этот этап включает в себя следующее:

-   Организация приложения и маршрутов в области функций с помощью модулей.

-   Императивная навигация от одного компонента к другому.

-   Передача необходимой и необязательной информации в параметрах маршрута.

Этот пример приложения воссоздает функцию героев в разделе "Услуги" учебника [Tour of Heroes](tutorial/tour-of-heroes/toh-pt4 'Tour of Heroes: Услуги') и использует большую часть кода из <live-example name="toh-pt4" title="Код примера Tour of Heroes: Услуги"></live-example>.

Типичное приложение имеет несколько функциональных областей, каждая из которых посвящена определенной бизнес-цели и имеет свою собственную папку.

В этом разделе показано, как рефакторить приложение на различные функциональные модули, импортировать их в главный модуль и перемещаться между ними.

<a id="heroes-functionality"></a>

### Добавить функциональность героев

Выполните следующие шаги:

-   Для управления героями создайте `HeroesModule` с маршрутизацией в папке heroes и зарегистрируйте его в корневом `AppModule`.

      <code-example format="shell" language="shell">

    ng generate module heroes/heroes --module app --flat --routing

      </code-example>

-   Переместите папку placeholder `hero-list`, находящуюся в папке `app`, в папку `heroes`.

-   Скопируйте содержимое `heroes/heroes.component.html` из <live-example name="toh-pt4" title="Tour of Heroes: Services example code">учебника "Services"</live-example> в шаблон `hero-list.component.html`.

    -   Переименуйте `<h2>` в `<h2>HEROES</h2>`.

    -   Удалите компонент `<app-hero-detail>` в нижней части шаблона.

-   Скопируйте содержимое файла `heroes/heroes.component.css` из живого примера в файл `hero-list.component.css`.

-   Скопируйте содержимое `heroes/heroes.component.ts` из живого примера в файл `hero-list.component.ts`.

    -   Измените имя класса компонента на `HeroListComponent`.

    -   Измените `selector` на `app-hero-list`.

          <div class="alert is-helpful">.

        Selectors are not required for routed components because components are dynamically inserted when the page is rendered.

        However, they are useful for identifying and targeting them in your HTML element tree.

          </div>

-   Copy the `hero-detail` folder, the `hero.ts`, `hero.service.ts`, and `mock-heroes.ts` files into the `heroes` sub-folder

-   Copy the `message.service.ts` into the `src/app` folder

-   Update the relative path import to the `message.service` in the `hero.service.ts` file

Next, update the `HeroesModule` metadata.

-   Import and add the `HeroDetailComponent` and `HeroListComponent` to the `declarations` array in the `HeroesModule`.

<code-example header="src/app/heroes/heroes.module.ts" path="router/src/app/heroes/heroes.module.ts"></code-example>

Структура файлов управления героями выглядит следующим образом:

<div class="filetree">   <div class="file">
    src/app/heroes
  </div>
  <div class="children">
    <div class="file">
      hero-detail
    </div>
      <div class="children">
        <div class="file">
          hero-detail.component.css
        </div>
        <div class="file">
          hero-detail.component.html
        </div>
        <div class="file">
          hero-detail.component.ts
        </div>
      </div>
    <div class="file">
      hero-list
    </div>
      <div class="children">
        <div class="file">
          hero-list.component.css
        </div>
        <div class="file">
          hero-list.component.html
        </div>
        <div class="file">
          hero-list.component.ts
        </div>
      </div>
    <div class="file">
      hero.service.ts
    </div>
    <div class="file">
      hero.ts
    </div>
    <div class="file">
      heroes-routing.module.ts
    </div>
    <div class="file">
      heroes.module.ts
    </div>
    <div class="file">
      mock-heroes.ts
    </div>
    </div>
  </div>
</div>

<a id="hero-routing-requirements"></a>

#### Требования к маршрутизации функции героев

Функция героев состоит из двух взаимодействующих компонентов - списка героев и подробной информации о героях. Когда вы переходите к представлению списка, оно получает список героев и отображает их.

Когда вы нажимаете на героя, вид детализации должен отобразить именно этого героя.

Вы указываете детальному представлению, какого героя отображать, включив идентификатор выбранного героя в URL маршрута.

Импортируйте компоненты героев из их новых мест в папке `src/app/heroes/` и определите два маршрута героев.

Теперь, когда у вас есть маршруты для модуля `Heroes`, зарегистрируйте их в `Router` с помощью `RouterModule`, как вы это делали в `AppRoutingModule`, с важным отличием.

В модуле `AppRoutingModule` вы использовали статический метод `RouterModule.forRoot()` для регистрации маршрутов и поставщиков услуг уровня приложения. В функциональном модуле вы используете статический метод `forChild()`.

<div class="alert is-helpful">

Вызывайте `RouterModule.forRoot()` только в корневом `AppRoutingModule` (или `AppModule`, если в нем вы регистрируете маршруты приложений верхнего уровня).
В любом другом модуле вы должны вызвать метод `RouterModule.forChild()` для регистрации дополнительных маршрутов.

</div>

Обновленный `HeroesRoutingModule` выглядит следующим образом:

<code-example header="src/app/heroes/heroes-routing.module.ts" path="router/src/app/heroes/heroes-routing.module.1.ts"></code-example>

<div class="alert is-helpful">

Рассмотрите возможность предоставления каждому функциональному модулю собственного файла конфигурации маршрута. Хотя в настоящее время маршруты функций минимальны, маршруты имеют тенденцию к усложнению даже в небольших приложениях.

</div>

<a id="remove-duplicate-hero-routes"></a>

#### Удаление дубликатов маршрутов героев

Маршруты героев в настоящее время определяются в двух местах: в `HeroesRoutingModule`, посредством `HeroesModule`, и в `AppRoutingModule`.

Маршруты, предоставляемые функциональными модулями, объединяются маршрутизатором в маршруты их импортированного модуля. Это позволяет вам продолжать определять маршруты функциональных модулей без изменения конфигурации основных маршрутов.

Удалите импорт `HeroListComponent` и маршрут `/heroes` из файла `app-routing.module.ts`.

Оставьте маршруты по умолчанию и wildcard, так как они все еще используются на верхнем уровне приложения.

<code-example header="src/app/app-routing.module.ts (v2)" path="router/src/app/app-routing.module.2.ts"></code-example>

<a id="merge-hero-routes"></a>

#### Удалите декларации героев

Поскольку `HeroesModule` теперь предоставляет `HeroListComponent`, удалите его из массива `declarations` модуля `AppModule`. Теперь, когда у вас есть отдельный `HeroesModule`, вы можете развивать функцию героя с помощью большего количества компонентов и различных маршрутов.

После этих шагов `AppModule` должен выглядеть следующим образом:

<code-example header="src/app/app.module.ts" path="router/src/app/app.module.3.ts" region="remove-heroes"></code-example>

<a id="routing-module-order"></a>

### Порядок импорта модулей

Обратите внимание, что в массиве `импортов` модулей, `AppRoutingModule` стоит последним и идет _после_ `HeroesModule`.

<code-example header="src/app/app.module.ts (module-imports)" path="router/src/app/app/app.module.3.ts" region="module-imports"></code-example>.

Порядок конфигурации маршрутов важен, потому что маршрутизатор принимает первый маршрут, который соответствует пути навигационного запроса.

Когда все маршруты были в одном `AppRoutingModule`, вы поместили маршруты по умолчанию и [wildcard](#wildcard) последними, после маршрута `/heroes`, чтобы у маршрутизатора был шанс сопоставить URL с маршрутом `/heroes` _до_ попадания на маршрут wildcard и перехода к "Страница не найдена".

Каждый модуль маршрутизации дополняет конфигурацию маршрута в порядке импорта. Если вы перечислили `AppRoutingModule` первым, маршрут wildcard будет зарегистрирован _перед_ маршрутами героев.

Маршрут дикого знака &mdash; который соответствует _каждому_ URL&mdash; будет перехватывать попытку перехода к маршруту героя.

<div class="alert is-helpful">

Пересмотрите модули маршрутизации, чтобы увидеть, как щелчок по ссылке героев приводит к "Страница не найдена". Узнайте о проверке конфигурации маршрутизатора во время выполнения [ниже](#inspect-config 'Inspect the router config').

</div>

### Параметры маршрута

<a id="route-def-with-parameter"></a>

#### Определение маршрута с параметром

Вернитесь к модулю `HeroesRoutingModule` и снова посмотрите на определения маршрутов. Маршрут к `HeroDetailComponent` имеет токен `:id` в пути.

<code-example header="src/app/heroes/heroes-routing.module.ts (excerpt)" path="router/src/app/heroes/heroes-routing.module.1.ts" region="hero-detail-route"></code-example>.

Токен `:id` создает слот в пути для параметра маршрута. В данном случае эта конфигурация заставляет маршрутизатор вставить `id` героя в этот слот.

Если вы скажете маршрутизатору перейти к компоненту detail и отобразить "Magneta", вы ожидаете, что ID героя появится в URL браузера следующим образом:

<code-example format="nocode">

localhost:4200/hero/15

</code-example>

Если пользователь введет этот URL в адресную строку браузера, маршрутизатор должен распознать шаблон и перейти к тому же детальному представлению "Magneta".

<div class="callout is-helpful">

<header>Route parameter: Required or optional?</header>

Встраивание маркера параметра маршрута, `:id`, в путь определения маршрута является хорошим выбором для данного сценария, поскольку `id` _требуется_ компонентом `HeroDetailComponent` и поскольку значение `15` в пути четко отличает маршрут к "Magneta" от маршрута к какому-либо другому герою.

</div>

<a id="route-parameters"></a>

#### Установка параметров маршрута в представлении списка

После перехода к компоненту `HeroDetailComponent` вы ожидаете увидеть подробную информацию о выбранном герое. Вам нужны две части информации: путь маршрутизации к компоненту и `id` героя.

Соответственно, массив _параметров ссылки_ состоит из двух элементов: _путь маршрутизации_ и _параметр маршрута_, который определяет `id` выбранного героя.

<code-example header="src/app/heroes/hero-list/hero-list.component.html (link-parameters-array)" path="router/src/app/heroes/hero-list/hero-list.component.1.html" region="link-parameters-array"></code-example>.

Маршрутизатор составляет URL назначения из массива следующим образом: `localhost:4200/hero/15`.

Маршрутизатор извлекает параметр маршрута \(`id:15`\) из URL и передает его в `HeroDetailComponent` с помощью сервиса `ActivatedRoute`.

<a id="activated-route-in-action"></a>

### `Активированный маршрут` в действии

Импортируйте токены `Router`, `ActivatedRoute` и `ParamMap` из пакета router.

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (активированный маршрут)" path="router/src/app/heroes/hero-detail/hero-detail.component.1.ts" region="imports"></code-example>.

Импортируйте оператор `switchMap`, поскольку он понадобится вам позже для обработки параметров маршрута `Observable`.

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (импорт оператора switchMap)" path="router/src/app/heroes/hero-detail/hero-detail.component.3.ts" region="rxjs-operator-import"></code-example>.

<a id="hero-detail-ctor"></a>.

Добавьте сервисы как приватные переменные в конструктор, чтобы Angular инжектировал их\ (сделал их видимыми для компонента\).

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (constructor)" path="router/src/app/heroes/hero-detail/hero-detail.component.3.ts" region="ctor"></code-example>.

В методе `ngOnInit()` используйте службу `ActivatedRoute` для получения параметров маршрута, извлечения `id` героя из параметров и получения героя для отображения.

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (ngOnInit)" path="router/src/app/heroes/hero-detail/hero-detail.component.3.ts" region="ngOnInit"></code-example>.

Когда карта изменяется, `paramMap` получает параметр `id` из измененных параметров.

Затем вы говорите `HeroService` получить героя с этим `id` и возвращаете результат запроса `HeroService`.

Оператор `switchMap` делает две вещи. Он сглаживает `Observable<Hero>`, который возвращает `HeroService`, и отменяет предыдущие ожидающие запросы.

Если пользователь повторно переходит на этот маршрут с новым `id`, в то время как `HeroService` все еще получает старый `id`, `switchMap` отбрасывает старый запрос и возвращает героя для нового `id`.

`AsyncPipe` обрабатывает наблюдаемую подписку, и свойство `героя` компонента будет \(re\)установлено с полученным героем.

#### `ParamMap` API

API `ParamMap` вдохновлен интерфейсом [URLSearchParams](https://developer.mozilla.org/docs/Web/API/URLSearchParams). Он предоставляет методы для обработки доступа к параметрам как для параметров маршрута \(`paramMap`\), так и для параметров запроса \(`queryParamMap`\).

| Member | Details | |:--- |:--- |:--- |
| `has(name)` | Возвращает `true`, если имя параметра есть в карте параметров. |

| `get(name)` | Возвращает значение имени параметра \(строку `\), если оно есть, или `null`, если имя параметра отсутствует в карте параметров. Возвращает _первый_ элемент, если значение параметра представляет собой массив значений. |

| `getAll(name)` | Возвращает `строковый массив` значений имени параметра, если он найден, или пустой `массив`, если значение имени параметра отсутствует в карте. Используйте `getAll`, когда один параметр может иметь несколько значений. |

| `keys` | Возвращает массив `строк` всех имен параметров в карте. |

<a id="reuse"></a>

#### Observable `paramMap` и повторное использование компонентов

В этом примере вы получаете карту параметров маршрута из `Observable`. Это означает, что карта параметров маршрута может меняться в течение жизни этого компонента.

По умолчанию маршрутизатор повторно использует экземпляр компонента при повторном переходе к одному и тому же типу компонента без предварительного посещения другого компонента. Параметры маршрута могут меняться каждый раз.

Предположим, на навигационной панели родительского компонента есть кнопки "вперед" и "назад", которые прокручивают список героев. Каждое нажатие кнопки обязательно приводило к переходу к `HeroDetailComponent` со следующим или предыдущим `id`.

Вы не хотите, чтобы маршрутизатор удалял текущий экземпляр `HeroDetailComponent` из DOM только для того, чтобы заново создать его для следующего `id`, так как это приведет к повторному рендерингу представления. Для улучшения UX маршрутизатор повторно использует один и тот же экземпляр компонента и обновляет параметр.

Поскольку `ngOnInit()` вызывается только один раз при инстанцировании компонента, вы можете определить, когда параметры маршрута изменяются _в пределах одного и того же экземпляра_, используя наблюдаемое свойство `paramMap`.

<div class="alert is-helpful">

При подписке на наблюдаемую переменную в компоненте вы почти всегда отписываетесь от нее, когда компонент уничтожается.

Однако наблюдаемые `ActivatedRoute` являются исключением, поскольку `ActivatedRoute` и его наблюдаемые изолированы от самого `Router`. Маршрутизатор" уничтожает маршрутизируемый компонент, когда он больше не нужен.

Это означает, что все члены компонента также будут уничтожены, включая инжектированный `ActivatedRoute` и подписки на его свойства `Observable`.

Маршрутизатор не `завершает` ни одну `обсервируемую` из `ActivatedRoute`, поэтому любые блоки `finalize` или `complete` не будут выполняться. Если вам нужно обработать что-то в `finalize`, вам все равно нужно отписаться в `ngOnDestroy`.

Вы также должны отписаться, если в вашей наблюдаемой трубе есть задержка с кодом, который вы не хотите запускать после уничтожения компонента.

</div>

<a id="snapshot"></a>

#### `snapshot`: ненаблюдаемая альтернатива

Это приложение не будет повторно использовать `HeroDetailComponent`. Пользователь всегда возвращается к списку героев, чтобы выбрать другого героя для просмотра.

Невозможно перейти от одной детали героя к другой детали героя без посещения компонента списка между ними.

Поэтому маршрутизатор каждый раз создает новый экземпляр `HeroDetailComponent`.

Когда вы точно знаете, что экземпляр `HeroDetailComponent` никогда не будет использоваться повторно, вы можете использовать `snapshot`.

`route.snapshot` предоставляет начальное значение карты параметров маршрута. Вы можете получить доступ к параметрам напрямую, без подписки или добавления операторов наблюдения, как показано ниже:

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (ngOnInit snapshot)" path="router/src/app/heroes/hero-detail/hero-detail.component.2.ts" region="snapshot"></code-example>

<div class="alert is-helpful">

При использовании этой техники `snapshot` получает только начальное значение карты параметров. Используйте подход с наблюдаемой `paramMap`, если есть вероятность, что маршрутизатор может повторно использовать компонент.
В этом учебном примере приложения используется наблюдаемая `paramMap`.

</div>

<a id="nav-to-list"></a>

### Навигация назад к компоненту списка

Кнопка "Назад" компонента `HeroDetailComponent` использует метод `gotoHeroes()`, который принудительно перемещает обратно к компоненту `HeroListComponent`.

Метод маршрутизатора `navigate()` принимает тот же массив параметров _ссылки_ из одного элемента, который вы можете связать с директивой `[routerLink]`. Он содержит путь к компоненту `HeroListComponent`:

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (excerpt)" path="router/src/app/heroes/hero-detail/hero-detail.component.1.ts" region="gotoHeroes"></code-example>.

<a id="optional-route-parameters"></a>

#### Параметры маршрута: Обязательные или необязательные?

Используйте [route parameters](#route-parameters) для указания обязательного значения параметра в URL маршрута, как при переходе к `HeroDetailComponent` для просмотра героя с `id` 15:

<code-example format="http" language="http">

localhost:4200/hero/15

</code-example>

Вы также можете добавить необязательную информацию в запрос маршрута. Например, при возврате к списку `hero-detail.component.ts` из представления деталей героя было бы неплохо, если бы просматриваемый герой был предварительно выбран в списке.

<div class="lightbox">   <img alt="Selected hero" src="generated/images/guide/router/selected-hero.png">
</div>

Вы реализуете эту возможность, включив `id` просматриваемого героя в URL в качестве необязательного параметра при возврате из `HeroDetailComponent`.

Необязательная информация может также включать другие формы, такие как:

-   Свободно структурированные критерии поиска; например, `name='wind*'`.

-   Множественные значения; например, `after='12/31/2015' & before='1/1/2017'` &mdash; без особого порядка&mdash; `before='1/1/2017' & after='12/31/2015'` &mdash; в различных форматах&mdash; `during='currentYear'`.

Поскольку такие параметры не вписываются в путь URL, вы можете использовать необязательные параметры для передачи произвольно сложной информации во время навигации. Необязательные параметры не участвуют в сопоставлении шаблонов и обеспечивают гибкость выражения.

Маршрутизатор поддерживает навигацию с необязательными параметрами так же, как и с обязательными параметрами маршрута. Определите необязательные параметры в отдельном объекте _после_ определения обязательных параметров маршрута.

В общем случае, используйте обязательный параметр маршрута, когда значение является обязательным\\ (например, если необходимо отличить один путь маршрута от другого\); и необязательный параметр, когда значение является необязательным, сложным и/или многомерным.

<a id="optionally-selecting"></a>

#### Список героев: опциональный выбор героя

При переходе к компоненту `HeroDetailComponent` вы указали требуемый `id` редактируемого героя в параметре маршрута и сделали его вторым элементом массива [_link parameters array_](#link-parameters-array).

<code-example header="src/app/heroes/hero-list/hero-list.component.html (link-parameters-array)" path="router/src/app/heroes/hero-list/hero-list.component.1.html" region="link-parameters-array"></code-example>.

Маршрутизатор встроил значение `id` в навигационный URL, потому что вы определили его как параметр маршрута с маркером-заполнителем `:id` в маршруте `path`:

<code-example header="src/app/heroes/heroes-routing.module.ts (hero-detail-route)" path="router/src/app/heroes/heroes-routing.module.1.ts" region="hero-detail-route"></code-example>.

Когда пользователь нажимает кнопку "Назад", `HeroDetailComponent` создает другой массив _параметров ссылок_, который он использует для перехода обратно к `HeroListComponent`.

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (gotoHeroes)" path="router/src/app/heroes/hero-detail/hero-detail.component.1.ts" region="gotoHeroes"></code-example>.

В этом массиве отсутствует параметр route, потому что ранее вам не нужно было отправлять информацию в `HeroListComponent`.

Теперь отправьте `id` текущего героя с навигационным запросом, чтобы `HeroListComponent` мог выделить этого героя в своем списке.

Отправьте `id` с объектом, который содержит необязательный параметр `id`. Для демонстрации в объекте есть дополнительный параметр \(`foo`\), который `HeroListComponent` должен игнорировать.

Вот пересмотренный навигационный оператор:

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (перейти к героям)" path="router/src/app/heroes/hero-detail/hero-detail.component.3.ts" region="gotoHeroes"></code-example>.

Приложение по-прежнему работает. Нажатие кнопки "назад" возвращает к представлению списка героев.

Посмотрите на адресную строку браузера.

Она должна выглядеть примерно так, в зависимости от того, где вы ее запустили:

<code-example format="shell" language="shell">

localhost:4200/heroes;id=15;foo=foo

</code-example>

Значение `id` отображается в URL как \(`;id=15;foo=foo`\), а не в пути URL. Путь для маршрута "Герои" не содержит токена `:id`.

Необязательные параметры маршрута не разделены символами "?" и "&", как это было бы в строке запроса URL. Они разделяются точкой с запятой ";".

Это матричная нотация URL.

<div class="alert is-helpful">

Матричная нотация URL - это идея, впервые представленная в [предложении 1996 года] (https://www.w3.org/DesignIssues/MatrixURIs.html) основателем Интернета Тимом Бернерсом-Ли.

Хотя матричная нотация так и не вошла в стандарт HTML, она является легальной и стала популярной среди систем маршрутизации браузеров как способ изолировать параметры, принадлежащие родительским и дочерним маршрутам. Таким образом, Router обеспечивает поддержку матричной нотации во всех браузерах.

</div>

<a id="route-parameters-activated-route"></a>

### Параметры маршрута в сервисе `ActivatedRoute`.

В текущем состоянии разработки список героев не изменяется. Ни одна строка героев не выделена.

Для `HeroListComponent` необходим код, который ожидает параметры.

Ранее, при переходе от `HeroListComponent` к `HeroDetailComponent`, вы подписывались на карту параметров маршрута `Observable` и делали ее доступной для `HeroDetailComponent`

в службе `ActivatedRoute`.

Вы внедрили этот сервис в конструктор `HeroDetailComponent`.

На этот раз вы будете перемещаться в обратном направлении, от `HeroDetailComponent` к `HeroListComponent`.

Сначала расширьте оператор импорта маршрутизатора, включив в него служебный символ `ActivatedRoute`:

<code-example header="src/app/heroes/hero-list/hero-list.component.ts (import)" path="router/src/app/heroes/hero-list/hero-list.component.ts" region="import-router"></code-example>.

Импортируйте оператор `switchMap` для выполнения операции над `Observable` карты параметров маршрута.

<code-example header="src/app/heroes/hero-list/hero-list.component.ts (rxjs imports)" path="router/src/app/heroes/hero-list/hero-list.component.ts" region="rxjs-imports"></code-example>.

Вставьте `ActivatedRoute` в конструктор `HeroListComponent`.

<code-example header="src/app/heroes/hero-list/hero-list.component.ts (constructor and ngOnInit)" path="router/src/app/heroes/hero-list/hero-list.component.ts" region="ctor"></code-example>

The `ActivatedRoute.paramMap` property is an `Observable` map of route parameters. The `paramMap` emits a new map of values that includes `id` when the user navigates to the component.

In `ngOnInit()` you subscribe to those values, set the `selectedId`, and get the heroes.

Update the template with a [class binding](guide/class-binding). The binding adds the `selected` CSS class when the comparison returns `true` and removes it when `false`.

Look for it within the repeated `<li>` tag as shown here:

<code-example header="src/app/heroes/hero-list/hero-list.component.html" path="router/src/app/heroes/hero-list/hero-list.component.html"></code-example>.

Добавьте несколько стилей для применения при выборе героя.

<code-example header="src/app/heroes/hero-list/hero-list.component.css" path="router/src/app/heroes/hero-list/hero-list.component.css" region="selected"></code-example>.

Когда пользователь переходит от списка героев к герою "Magneta" и обратно, "Magneta" отображается выбранной:

<div class="lightbox">

<img alt="Selected hero in list has different background color" src="generated/images/guide/router/selected-hero.png">

</div>

Необязательный параметр маршрута `foo` безвреден, и маршрутизатор продолжает его игнорировать.

<a id="route-animation"></a>

### Добавление маршрутизируемых анимаций

В этом разделе показано, как добавить некоторые [анимации](guide/animations) в `HeroDetailComponent`.

Сначала импортируйте `BrowserAnimationsModule` и добавьте его в массив `imports`:

<code-example header="src/app/app.module.ts (animations-module)" path="router/src/app/app.module.ts" region="animations-module"></code-example>.

Далее, добавьте объект `data` в маршруты для `HeroListComponent` и `HeroDetailComponent`. Переходы основаны на `состояниях`, и вы используете данные `анимации` из маршрута, чтобы предоставить именованную анимацию [`состояние`](api/animations/state) для переходов.

<code-example header="src/app/heroes/heroes-routing.module.ts (данные анимации)" path="router/src/app/heroes/heroes-routing.module.2.ts"></code-example>.

Создайте файл `animations.ts` в корневой папке `src/app/`. Его содержимое выглядит следующим образом:

<code-example header="src/app/animations.ts (excerpt)" path="router/src/app/animations.ts"></code-example>.

Этот файл делает следующее:

-   Импортирует символы анимации, которые создают триггеры анимации, контролируют состояние и управляют переходами между состояниями.

-   Экспортирует константу с именем `slideInAnimation`, установленную на триггер анимации с именем `routeAnimation`.

-   Определяет один переход при переключении между маршрутами `героев` и `героев` для облегчения входа компонента с левой стороны экрана, когда он входит в представление приложения \(`:enter`\), другой для анимации компонента справа, когда он покидает представление приложения \(`:leave`\)

Вернитесь в `AppComponent`, импортируйте токен `RouterOutlet` из пакета `@angular/router` и `slideInAnimation` из `'./animations.ts`.

Добавьте массив `animations` в метаданные `@Component`, содержащие `slideInAnimation`.

<code-example header="src/app/app.component.ts (animations)" path="router/src/app/app.component.2.ts" region="animation-imports"></code-example>.

Чтобы использовать маршрутизируемые анимации, оберните `RouterOutlet` внутри элемента, используйте триггер `@routeAnimation` и привяжите его к элементу.

Чтобы `@routeAnimation` переходила в состояния выключения ключа, предоставьте ей `данные` из `ActivatedRoute`. Переменная `RouterOutlet` раскрывается как переменная шаблона `outlet`, поэтому вы привязываете ссылку на выход маршрутизатора.

В данном примере используется переменная `routerOutlet`.

<code-example header="src/app/app.component.html (router outlet)" path="router/src/app/app.component.2.html"></code-example>

Свойство `@routeAnimation` связано с `getAnimationData()`, которое возвращает свойство анимации из `данных`, предоставленных основным маршрутом. Свойство `animation` соответствует именам `transition`, которые вы использовали в `slideInAnimation`, определенном в `animations.ts`.

<code-example header="src/app/app.component.ts (router outlet)" path="router/src/app/app.component.2.ts" region="function-binding"></code-example>.

При переключении между двумя маршрутами, `HeroDetailComponent` и `HeroListComponent` теперь облегчаются слева при маршрутизации к, и сдвигаются вправо при навигации прочь.

<a id="milestone-3-wrap-up"></a>

### Завершение этапа 3

В этом разделе было рассмотрено следующее:

-   Организация приложения по функциональным областям

-   Императивная навигация от одного компонента к другому

-   Передача информации в параметрах маршрута и подписка на них в компоненте

-   Импорт функциональной области NgModule в `AppModule`.

-   Применение маршрутизируемых анимаций на основе страницы.

После этих изменений структура папок выглядит следующим образом:

<div class="filetree">   <div class="file">
    angular-router-tour-of-heroes
  </div>
  <div class="children">
    <div class="file">
      src
    </div>
    <div class="children">
      <div class="file">
        app
      </div>
      <div class="children">
        <div class="file">
          crisis-list
        </div>
          <div class="children">
            <div class="file">
              crisis-list.component.css
            </div>
            <div class="file">
              crisis-list.component.html
            </div>
            <div class="file">
              crisis-list.component.ts
            </div>
          </div>
        <div class="file">
          heroes
        </div>
        <div class="children">
          <div class="file">
            hero-detail
          </div>
            <div class="children">
              <div class="file">
                hero-detail.component.css
              </div>
              <div class="file">
                hero-detail.component.html
              </div>
              <div class="file">
                hero-detail.component.ts
              </div>
            </div>
          <div class="file">
            hero-list
          </div>
            <div class="children">
              <div class="file">
                hero-list.component.css
              </div>
              <div class="file">
                hero-list.component.html
              </div>
              <div class="file">
                hero-list.component.ts
              </div>
            </div>
          <div class="file">
            hero.service.ts
          </div>
          <div class="file">
            hero.ts
          </div>
          <div class="file">
            heroes-routing.module.ts
          </div>
          <div class="file">
            heroes.module.ts
          </div>
          <div class="file">
            mock-heroes.ts
          </div>
        </div>
        <div class="file">
          page-not-found
        </div>
        <div class="children">
          <div class="file">
            page-not-found.component.css
          </div>
          <div class="file">
            page-not-found.component.html
          </div>
          <div class="file">
            page-not-found.component.ts
          </div>
        </div>
      </div>
      <div class="file">
        animations.ts
      </div>
      <div class="file">
        app.component.css
      </div>
      <div class="file">
        app.component.html
      </div>
      <div class="file">
        app.component.ts
      </div>
      <div class="file">
        app.module.ts
      </div>
      <div class="file">
        app-routing.module.ts
      </div>
      <div class="file">
        main.ts
      </div>
      <div class="file">
        message.service.ts
      </div>
      <div class="file">
        index.html
      </div>
      <div class="file">
        styles.css
      </div>
      <div class="file">
        tsconfig.json
      </div>
    </div>
    <div class="file">
      node_modules &hellip;
    </div>
    <div class="file">
      package.json
    </div>
  </div>
</div>

Вот соответствующие файлы для этой версии примера приложения.

<code-tabs> <code-pane header="animations.ts" path="router/src/app/animations.ts"></code-pane>
<code-pane header="app.component.html" path="router/src/app/app.component.2.html"></code-pane>
<code-pane header="app.component.ts" path="router/src/app/app.component.2.ts"></code-pane>
<code-pane header="app.module.ts" path="router/src/app/app.module.3.ts"></code-pane>
<code-pane header="app-routing.module.ts" path="router/src/app/app-routing.module.2.ts" region="milestone3"></code-pane>
<code-pane header="hero-list.component.css" path="router/src/app/heroes/hero-list/hero-list.component.css"></code-pane>
<code-pane header="hero-list.component.html" path="router/src/app/heroes/hero-list/hero-list.component.html"></code-pane>
<code-pane header="hero-list.component.ts" path="router/src/app/heroes/hero-list/hero-list.component.ts"></code-pane>
<code-pane header="hero-detail.component.html" path="router/src/app/heroes/hero-detail/hero-detail.component.html"></code-pane>
<code-pane header="hero-detail.component.ts" path="router/src/app/heroes/hero-detail/hero-detail.component.3.ts"></code-pane>
<code-pane header="hero.service.ts" path="router/src/app/heroes/hero.service.ts"></code-pane>
<code-pane header="heroes.module.ts" path="router/src/app/heroes/heroes.module.ts"></code-pane>
<code-pane header="heroes-routing.module.ts" path="router/src/app/heroes/heroes-routing.module.2.ts"></code-pane>
<code-pane header="message.service.ts" path="router/src/app/message.service.ts"></code-pane>
</code-tabs>

<a id="milestone-4"></a>

## Веха 4: Функция кризисного центра

В этом разделе показано, как добавлять дочерние маршруты и использовать относительную маршрутизацию в вашем приложении.

Чтобы добавить дополнительные возможности к текущему кризисному центру приложения, проделайте те же шаги, что и для функции героев:

-   Создайте подпапку `crisis-center` в папке `src/app`.

-   Скопируйте файлы и папки из папки `app/heroes` в новую папку `crisis-center`.

-   В новых файлах измените все упоминания "героя" на "кризис", а "героев" на "кризисы".

-   Переименуйте файлы NgModule в `crisis-center.module.ts` и `crisis-center-routing.module.ts`.

Используйте имитацию кризисов вместо имитации героев:

<code-example header="src/app/crisis-center/mock-crises.ts" path="router/src/app/crisis-center/mock-crises.ts"></code-example>.

Получившийся кризисный центр является основой для введения новой концепции &mdash; дочерней маршрутизации. Вы можете оставить Heroes в его текущем состоянии в качестве контраста с Кризисным центром.

<div class="alert is-helpful">

В соответствии с принципом [Separation of Concerns](https://blog.8thlight.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html 'Separation of Concerns'), изменения в Кризисном центре не влияют на `AppModule` или любой другой компонент функции.

</div>

<a id="crisis-child-routes"></a>

### Кризисный центр с дочерними маршрутами

В этом разделе показано, как организовать кризисный центр в соответствии со следующим рекомендуемым шаблоном для приложений Angular:

-   Каждая область функций находится в своей собственной папке.

-   Каждая функция имеет свой модуль функции Angular

-   Каждая область имеет свой корневой компонент области

-   Каждый корневой компонент области имеет свой собственный выход маршрутизатора и дочерние маршруты.

-   Маршруты областей функций редко \(если вообще когда-либо\) пересекаются с маршрутами других функций.

Если в вашем приложении много областей функций, деревья компонентов могут состоять из множества компонентов для этих функций, каждый из которых имеет ответвления от других, связанных с ним компонентов.

<a id="child-routing-component"></a>

### Дочерний компонент маршрутизации

Создайте компонент `CrisisCenter` в папке `crisis-center`:

<code-example format="shell" language="shell">

ng generate component crisis-center/crisis-center

</code-example>

Обновите шаблон компонента с помощью следующей разметки:

<code-example header="src/app/crisis-center/crisis-center/crisis-center.component.html" path="router/src/app/crisis-center/crisis-center/crisis-center.component.html"></code-example>.

Компонент `CrisisCenterComponent` имеет следующее общее с `AppComponent`:

-   Он является корнем области кризисного центра, так же как `AppComponent` является корнем всего приложения.

-   Это оболочка для области функций кризисного управления, так же как `AppComponent` является оболочкой для управления рабочим процессом высокого уровня.

Как и большинство оболочек, класс `CrisisCenterComponent` является минимальным, поскольку в нем нет бизнес-логики, а в его шаблоне нет ссылок, только заголовок и `<router-outlet>` для дочернего компонента кризисного центра.

<a id="child-route-config"></a>

### Конфигурация дочернего маршрута

В качестве главной страницы для функции "Кризисный центр" создайте компонент `CrisisCenterHome` в папке `crisis-center`.

<code-example format="shell" language="shell">

ng generate component crisis-center/crisis-center-home

</code-example>

Обновите шаблон с приветственным сообщением для `Кризисного центра`.

<code-example header="src/app/crisis-center/crisis-center-home/crisis-center-home.component.html" path="router/src/app/crisis-center/crisis-center-home/crisis-center-home.component.html"></code-example>.

Обновите `crisis-center-routing.module.ts`, который вы переименовали после копирования из файла `heroes-routing.module.ts`. На этот раз вы определяете дочерние маршруты внутри родительского маршрута `crisis-center`.

<code-example header="src/app/crisis-center/crisis-center-routing.module.ts (Routes)" path="router/src/app/crisis-center/crisis-center-routing.module.1.ts" region="routes"></code-example>.

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

-   Чтобы перейти к компоненту `CrisisCenterHomeComponent`, полный URL будет `/crisis-center` \(`/crisis-center` + `''` + `''`\)

-   Чтобы перейти к компоненту `CrisisDetailComponent` для кризиса с `id=2`, полный URL будет `/crisisis-center/2` \(`/crisisis-center` + `''` + `'/2'`\)

Абсолютный URL для последнего примера, включая `localhost`, выглядит следующим образом:

<code-example>

localhost:4200/crisis-center/2

</code-example>

Вот полный файл `crisis-center-routing.module.ts` с его импортами.

<code-example header="src/app/crisis-center/crisis-center-routing.module.ts (excerpt)" path="router/src/app/crisis-center/crisis-center-routing.module.1.ts"></code-example>.

<a id="import-crisis-module"></a>

### Импортируйте модуль кризисного центра в маршруты `AppModule`.

Как и в случае с `HeroesModule`, вы должны добавить `CrisisCenterModule` в массив `imports` `AppModule` _перед_ `AppRoutingModule`:

<code-tabs> <code-pane header="src/app/crisis-center/crisis-center.module.ts" path="router/src/app/crisis-center/crisis-center.module.ts"></code-pane>
<code-pane header="src/app/app.module.ts (import CrisisCenterModule)" path="router/src/app/app.module.4.ts" region="crisis-center-module"></code-pane>
</code-tabs>

<div class="alert is-helpful">

Порядок импорта модулей важен, поскольку порядок маршрутов, определенных в модулях, влияет на согласование маршрутов. Если бы `AppModule` был импортирован первым, его маршрут с подстановочным знаком \(`путь: '**'`\) имел бы приоритет над маршрутами, определенными в `CrisisCenterModule`.
Для получения дополнительной информации смотрите раздел [порядок маршрутов](guide/router#route-order).

</div>

Удалите начальный маршрут кризисного центра из файла `app-routing.module.ts`, поскольку теперь модули `HeroesModule` и `CrisisCenter` предоставляют функциональные маршруты.

Файл `app-routing.module.ts` сохраняет маршруты верхнего уровня приложения, такие как маршруты по умолчанию и маршруты подстановочных знаков.

<code-example header="src/app/app-routing.module.ts (v3)" path="router/src/app/app-routing.module.3.ts" region="v3"></code-example>

<a id="relative-navigation"></a>

### Относительная навигация

При создании функции кризисного центра вы перешли к маршруту подробной информации о кризисе, используя абсолютный путь, начинающийся со слэша.

Маршрутизатор сопоставляет такие абсолютные пути с маршрутами, начиная с верхней части конфигурации маршрута.

Вы могли бы продолжать использовать абсолютные пути, подобные этому, для навигации внутри функции Кризисного центра, но это привязывает ссылки к родительской структуре маршрутизации. Если вы измените родительский путь `/crisis-center`, вам придется изменить массив параметров ссылки.

Вы можете освободить ссылки от этой зависимости, определив пути, относительные к текущему сегменту URL. Навигация в области функции остается нетронутой, даже если вы измените путь родительского маршрута к функции.

<div class="alert is-helpful">

The router supports directory-like syntax in a _link parameters list_ to help guide route name lookup:

| Directory-like syntax | Details | |:--- |:--- |

| `./` <br /> `no leading slash` | Relative to the current level. |

| `../` | Up one level in the route path. |

You can combine relative navigation syntax with an ancestor path. If you must navigate to a sibling route, you could use the `../<sibling>` convention to go up

one level, then over and down the sibling route path.

</div>

Чтобы перейти по относительному пути с помощью метода `Router.navigate`, вы должны предоставить `ActivatedRoute`, чтобы маршрутизатор знал, где вы находитесь в текущем дереве маршрутов.

После массива _параметров ссылки_ добавьте объект со свойством `relativeTo`, установленным на `ActivatedRoute`. После этого маршрутизатор вычисляет целевой URL, основываясь на местоположении активного маршрута.

<div class="alert is-helpful">

Всегда указывайте полный абсолютный путь при вызове метода маршрутизатора `navigateByUrl()`.

</div>

<a id="nav-to-crisis"></a>

### Переход к списку кризисов с помощью относительного URL-адреса

Вы уже ввели `ActivatedRoute`, который необходим для составления относительного пути навигации.

При использовании `RouterLink` для навигации вместо сервиса `Router`, вы будете использовать тот же массив параметров ссылки, но не будете предоставлять объекту свойство `relativeTo`. Свойство `ActivatedRoute` является неявным в директиве `RouterLink`.

Обновите метод `gotoCrises()` компонента `CrisisDetailComponent` для перехода обратно к списку кризисных центров, используя навигацию по относительному пути.

<code-example header="src/app/crisis-center/crisis-detail/crisis-detail.component.ts (относительная навигация)" path="router/src/app/crisis-center/crisis-detail/crisis-detail.component.ts" region="gotoCrises-navigate"></code-example>.

Обратите внимание, что путь поднимается на уровень вверх, используя синтаксис `../`. Если текущий кризис `id` равен `3`, то путь обратно к списку кризисов будет `/crisis-center/;id=3;foo=foo`.

<a id="named-outlets"></a>

### Отображение нескольких маршрутов в именованных торговых точках

Вы решили предоставить пользователям возможность связаться с кризисным центром. Когда пользователь нажимает кнопку "Связаться", вы хотите отобразить сообщение во всплывающем окне.

Всплывающее окно должно оставаться открытым, даже при переключении между страницами приложения, пока пользователь не закроет его, отправив сообщение или отменив его. Очевидно, что вы не можете поместить всплывающее окно в ту же розетку, что и другие страницы.

До сих пор вы определяли один аутлет и вставляли дочерние маршруты под этот аутлет, чтобы сгруппировать маршруты вместе. Маршрутизатор поддерживает только один первичный безымянный аутлет для каждого шаблона.

Шаблон также может иметь любое количество именованных аутлетов. Каждый именованный аутлет имеет свой собственный набор маршрутов со своими компонентами.

Несколько розеток могут одновременно отображать различное содержимое, определяемое различными маршрутами.

Добавьте аутлет с именем "popup" в `AppComponent`, непосредственно за неименованным аутлетом.

<code-example header="src/app/app.component.html (outlets)" path="router/src/app/app.component.4.html" region="outlets"></code-example>.

Вот куда попадает всплывающее окно, как только вы узнаете, как направить к нему всплывающий компонент.

<a id="secondary-routes"></a>

#### Вторичные маршруты

Именованные розетки являются целями _вторичных маршрутов_.

Вторичные маршруты похожи на первичные, и вы настраиваете их таким же образом. Они отличаются по нескольким ключевым параметрам.

-   Они независимы друг от друга

-   Они работают в комбинации с другими маршрутами

-   Они отображаются в именованных точках.

Создайте новый компонент для составления сообщения.

<code-example format="shell" language="shell">

ng generate component compose-message

</code-example>

Он отображает короткую форму с заголовком, полем ввода для сообщения и двумя кнопками "Отправить" и "Отмена".

<div class="lightbox">

<img alt="Contact textarea with send and cancel buttons" src="generated/images/guide/router/contact-form.png">

</div>

Вот компонент, его шаблон и стили:

<code-tabs> <code-pane header="src/app/compose-message/compose-message.component.html" path="router/src/app/compose-message/compose-message.component.html"></code-pane>
<code-pane header="src/app/compose-message/compose-message.component.ts" path="router/src/app/compose-message/compose-message.component.ts"></code-pane>
<code-pane header="src/app/compose-message/compose-message.component.css" path="router/src/app/compose-message/compose-message.component.css"></code-pane>
</code-tabs>

Он выглядит так же, как и любой другой компонент в этом руководстве, но есть два ключевых отличия.

<div class="alert is-helpful">

**NOTE**: <br /> The `send()` method simulates latency by waiting a second before "sending" the message and closing the popup.

</div>

Метод `closePopup()` закрывает всплывающее представление, переходя к выходу из всплывающего окна с помощью `null`, о чем говорится в разделе [очистка вторичных маршрутов] (#clear-secondary-routes).

<a id="add-secondary-route"></a>

#### Добавление вторичного маршрута

Откройте модуль `AppRoutingModule` и добавьте новый маршрут `compose` в `appRoutes`.

<code-example header="src/app/app-routing.module.ts (compose route)" path="router/src/app/app-routing.module.3.ts" region="compose"></code-example>.

В дополнение к свойствам `path` и `component`, есть новое свойство `outlet`, которое установлено в `'popup'`. Теперь этот маршрут нацелен на всплывающий аутлет, и компонент `ComposeMessageComponent` будет отображаться там.

Чтобы дать пользователям возможность открыть всплывающее окно, добавьте ссылку "Contact" в шаблон `AppComponent`.

<code-example header="src/app/app.component.html (contact-link)" path="router/src/app/app/app.component.4.html" region="contact-link"></code-example>.

Хотя маршрут `compose` настроен на аутлет "popup", этого недостаточно для подключения маршрута к директиве `RouterLink`. Вы должны указать именованный аутлет в массиве _параметров ссылки_ и связать его с `RouterLink` с помощью привязки свойств.

Массив _параметров ссылки_ содержит объект с одним свойством `outlets`, значением которого является другой объект, ключом которого является одно\(или более\) имя розетки. В данном случае есть только свойство "popup" outlet, и его значением является другой массив _link parameters_, который определяет маршрут `compose`.

Другими словами, когда пользователь нажимает на эту ссылку, маршрутизатор отображает компонент, связанный с маршрутом `compose` в аутлете `popup`.

<div class="alert is-helpful">

Этот объект `outlets` внутри внешнего объекта был ненужным, когда существовал только один маршрут и один безымянный выход.

Маршрутизатор предположил, что ваша спецификация маршрута нацелена на безымянный первичный аутлет, и создал эти объекты для вас.

Маршрутизация к именованной розетке выявила особенность маршрутизатора: вы можете нацелить несколько розеток несколькими маршрутами в одной директиве `RouterLink`.

</div>

<a id="secondary-route-navigation"></a>

#### Вторичная навигация по маршруту: объединение маршрутов во время навигации

Перейдите в _Кризисный центр_ и нажмите "Контакт". В адресной строке браузера вы должны увидеть что-то вроде следующего URL.

<code-example format="http" language="http">

http://&hellip;/crisis-center(popup:compose)

</code-example>

Соответствующая часть URL следует за `...`:

-   `кризисный центр` является основной навигацией.

-   Круглые скобки окружают вторичный маршрут

-   Вторичный маршрут состоит из названия выхода \(`popup`\), разделителя `colon` и пути вторичного маршрута \(`compose`\).

Нажмите на ссылку _Герои_ и снова посмотрите на URL.

<code-example format="http" language="http">

http://&hellip;/heroes(popup:compose)

</code-example>

Первичная навигационная часть изменилась; вторичный маршрут остался прежним.

Маршрутизатор отслеживает две отдельные ветви в навигационном дереве и генерирует представление этого дерева в URL.

Вы можете добавить еще много выходов и маршрутов, на верхнем уровне и во вложенных уровнях, создавая дерево навигации с множеством ветвей, и маршрутизатор будет генерировать URL для этого.

Вы можете указать маршрутизатору на навигацию по всему дереву сразу, заполнив объект `outlets`, а затем передать этот объект внутри массива _параметров ссылок_ методу `router.navigate`.

<a id="clear-secondary-routes"></a>

#### Очистка вторичных маршрутов

Как и обычные аутлеты, вторичные аутлеты сохраняются до тех пор, пока вы не перейдете к новому компоненту.

Каждый вторичный выход имеет свою собственную навигацию, независимую от навигации, управляющей первичным выходом. Изменение текущего маршрута, отображаемого в первичном аутлете, не влияет на всплывающий аутлет.

Вот почему всплывающее окно остается видимым, пока вы перемещаетесь между кризисами и героями.

Снова метод `closePopup()`:

<code-example header="src/app/compose-message/compose-message.component.ts (closePopup)" path="router/src/app/compose-message/compose-message.component.ts" region="closePopup"></code-example>.

Нажатие на кнопки "отправить" или "отменить" очищает всплывающее окно. Функция `closePopup()` осуществляет императивную навигацию с помощью метода `Router.navigate()`, передавая массив [параметров ссылки](#link-parameters-array).

Как и массив, связанный с _Contact_ `RouterLink` в `AppComponent`, этот массив включает объект со свойством `outlets`. Значение свойства `outlets` - это другой объект с именами аутлетов для ключей.

Единственным именованным аутлетом является `'popup'`.

На этот раз значение свойства `'popup'` равно `null`. Это не маршрут, но это легитимное значение.

Установив для popup `RouterOutlet` значение `null`, очистите аутлет и удалите вторичный маршрут popup из текущего URL.

<a id="охранники"></a> <a id="milestone-5-route-guards"></a>

## Веха 5: Охрана маршрутов

В настоящее время любой пользователь может перемещаться в любое место приложения в любое время, но иногда вам необходимо контролировать доступ к различным частям вашего приложения по различным причинам, некоторые из которых могут быть следующими:

-   Возможно, пользователь не имеет права переходить к целевому компоненту.

-   Возможно, пользователь должен сначала войти в систему \(authenticate\)

-   Возможно, вам нужно получить некоторые данные перед отображением целевого компонента.

-   Возможно, вы захотите сохранить изменения перед тем, как покинуть компонент.

-   Вы можете спросить пользователя, можно ли отбросить ожидающие изменения, а не сохранять их.

Для обработки этих сценариев в конфигурацию маршрута добавляются защитные функции.

Возвращаемое значение охранника управляет поведением маршрутизатора:

| Возвращаемое значение охранника | Подробности | | |:--- |:--- |

| `true` | Процесс навигации продолжается |

| `false` | Процесс навигации останавливается, и пользователь остается на месте |

| `UrlTree` | Текущая навигация отменяется и начинается новая навигация к возвращенному `UrlTree`.

<div class="alert is-helpful">

**Примечание:** Guard также может указать маршрутизатору перейти в другое место, фактически отменяя текущую навигацию. Если это делается внутри guard, то guard должен возвращать `UrlTree`.

</div>

Охранник может вернуть свой булев ответ синхронно. Но во многих случаях охранник не может выдать ответ синхронно.
Страж может задать вопрос пользователю, сохранить изменения на сервере или получить свежие данные.

Все это асинхронные операции.

Соответственно, страж маршрутизации может возвращать `Observable<boolean>` или `Promise<boolean>`, а маршрутизатор будет ждать, пока наблюдаемая или обещание разрешатся в `true` или `false`.

<div class="alert is-helpful">

**NOTE**: <br /> The observable provided to the `Router` automatically completes after it retrieves the first value.

</div>

Маршрутизатор поддерживает несколько методов охраны:

| Интерфейсы охраны | Подробности | | |:--- |:--- |:--- |

| [`canActivate`](api/router/CanActivateFn) | Для опосредованной навигации _к_ маршруту |

| [`canActivateChild`](api/router/CanActivateChildFn) | Для опосредования навигации _к_ дочернему маршруту |

| [`canDeactivate`](api/router/CanDeactivateFn) | Для опосредованной навигации _в сторону_ от текущего маршрута | |

| [`resolve`](api/router/ResolveFn) | Для выполнения поиска данных маршрута _до_ активации маршрута | |

| [`canMatch`](api/router/CanMatchFn) | Чтобы контролировать, должен ли вообще использоваться `маршрут`, даже если `путь` соответствует сегменту URL |.

Вы можете иметь несколько защит на каждом уровне иерархии маршрутизации. Сначала маршрутизатор проверяет защиту `canDeactivate`, начиная с самого глубокого дочернего маршрута и заканчивая самым верхним.

Затем он проверяет защиты `canActivate` и `canActivateChild` сверху вниз до самого глубокого дочернего маршрута.

Если функциональный модуль загружается асинхронно, то защита `canMatch` проверяется до загрузки модуля.

За исключением `canMatch`, если _любой_ страж возвращает false, незавершенные стражи отменяются, и вся навигация отменяется. Если защита `canMatch` возвращает значение `false`, `маршрутизатор` продолжает обработку остальных `маршрутов`, чтобы проверить, не соответствует ли URL другой конфигурации `маршрута`. Вы можете думать об этом

как будто `Router` делает вид, что `маршрут` с защитой `canMatch` не существует.

В следующих разделах будет приведено несколько примеров.

<a id="can-activate-guard"></a>

### `canActivate`: требование аутентификации

Приложения часто ограничивают доступ к области функций в зависимости от того, кем является пользователь. Вы можете разрешить доступ только аутентифицированным пользователям или пользователям с определенной ролью.

Можно заблокировать или ограничить доступ до тех пор, пока учетная запись пользователя не будет активирована.

Защита `canActivate` является инструментом для управления этими бизнес-правилами навигации.

#### Добавление модуля функций администратора

Этот раздел поможет вам расширить кризисный центр некоторыми новыми административными функциями. Начните с добавления нового функционального модуля с именем `AdminModule`.

Создайте папку `admin` с файлом функционального модуля и файлом конфигурации маршрутизации.

<code-example format="shell" language="shell">

ng generate module admin --routing

</code-example>

Затем создайте вспомогательные компоненты.

<code-example format="shell" language="shell">

ng generate component admin/admin-dashboard

</code-example>

<code-example format="shell" language="shell">

ng generate component admin/admin

</code-example>

<code-example format="shell" language="shell">

ng generate component admin/manage-crises

</code-example>

<code-example format="shell" language="shell">

ng generate component admin/manage-heroes

</code-example>

Структура файла функции администратора выглядит следующим образом:

<div class="filetree">   <div class="file">
    src/app/admin
  </div>
  <div class="children">
    <div class="file">
      admin
    </div>
      <div class="children">
        <div class="file">
          admin.component.css
        </div>
        <div class="file">
          admin.component.html
        </div>
        <div class="file">
          admin.component.ts
        </div>
      </div>
    <div class="file">
      admin-dashboard
    </div>
      <div class="children">
        <div class="file">
          admin-dashboard.component.css
        </div>
        <div class="file">
          admin-dashboard.component.html
        </div>
        <div class="file">
          admin-dashboard.component.ts
        </div>
      </div>
    <div class="file">
      manage-crises
    </div>
      <div class="children">
        <div class="file">
          manage-crises.component.css
        </div>
        <div class="file">
          manage-crises.component.html
        </div>
        <div class="file">
          manage-crises.component.ts
        </div>
      </div>
    <div class="file">
      manage-heroes
    </div>
      <div class="children">
        <div class="file">
          manage-heroes.component.css
        </div>
        <div class="file">
          manage-heroes.component.html
        </div>
        <div class="file">
          manage-heroes.component.ts
        </div>
      </div>
    <div class="file">
      admin.module.ts
    </div>
    <div class="file">
      admin-routing.module.ts
    </div>
  </div>
</div>

Функциональный модуль администратора содержит `AdminComponent`, используемый для маршрутизации внутри функционального модуля, маршрут приборной панели и два незавершенных компонента для управления кризисами и героями.

<code-tabs> <code-pane header="src/app/admin/admin/admin.component.html"  path="router/src/app/admin/admin/admin.component.html"></code-pane>
<code-pane header="src/app/admin/admin-dashboard/admin-dashboard.component.html" path="router/src/app/admin/admin-dashboard/admin-dashboard.component.1.html"></code-pane>
<code-pane header="src/app/admin/admin.module.ts" path="router/src/app/admin/admin.module.ts"></code-pane>
<code-pane header="src/app/admin/manage-crises/manage-crises.component.html" path="router/src/app/admin/manage-crises/manage-crises.component.html"></code-pane>
<code-pane header="src/app/admin/manage-heroes/manage-heroes.component.html"  path="router/src/app/admin/manage-heroes/manage-heroes.component.html"></code-pane>
</code-tabs>

<div class="alert is-helpful">

Хотя ссылка `RouterLink` на приборную панель администратора содержит только относительную косую черту без дополнительного сегмента URL, она подходит к любому маршруту в области функций администратора. Вы хотите, чтобы ссылка `Dashboard` была активна только тогда, когда пользователь посещает этот маршрут.
Добавление дополнительной привязки к `Dashboard` routerLink, `[routerLinkActiveOptions]="{ exact: true }"`, отмечает ссылку `./` как активную, когда пользователь переходит на URL `/admin`, а не при переходе на любой из дочерних маршрутов.

</div>

<a id="component-less-route"></a>

##### Маршрут без компонента: группировка маршрутов без компонента

Начальная конфигурация маршрутизации администратора:

<code-example header="src/app/admin/admin-routing.module.ts (admin routing)" path="router/src/app/admin/admin-routing.module.1.ts" region="admin-routes"></code-example>.

Дочерний маршрут под `AdminComponent` имеет свойство `path` и `children`, но он не использует `component`. Это определяет маршрут без компонента.

Для группировки маршрутов управления `Кризисного центра` по пути `admin` компонент не нужен. Кроме того, маршрут _без компонента_ облегчает [охрану дочерних маршрутов] (#can-activate-child-guard).

Далее импортируйте `AdminModule` в `app.module.ts` и добавьте его в массив `imports` для регистрации маршрутов администратора.

<code-example header="src/app/app.module.ts (модуль администратора)" path="router/src/app/app.module.4.ts" region="admin-module"></code-example>.

Добавьте ссылку "Admin" в оболочку `AppComponent`, чтобы пользователи могли получить доступ к этой функции.

<code-example header="src/app/app.component.html (template)" path="router/src/app/app.component.5.html"></code-example>.

<a id="guard-admin-feature"></a>

#### Охрана функции администратора

В настоящее время каждый маршрут в Кризисном центре открыт для всех. Новая функция администратора должна быть доступна только для аутентифицированных пользователей.

Напишите защитный метод `canActivate()`, чтобы перенаправлять анонимных пользователей на страницу входа в систему, когда они пытаются войти в область администратора.

Создайте новый файл с именем `auth.guard.ts` в папке `auth`. Файл `auth.guard.ts` будет содержать функцию `authGuard`.

<code-example format="shell" language="shell">

ng generate guard auth/auth

</code-example>

Чтобы продемонстрировать основные принципы, в этом примере только регистрируется в консоли, немедленно возвращается `true` и разрешается продолжить навигацию:

<code-example header="src/app/app/auth/auth.guard.ts (excerpt)" path="router/src/app/auth/auth.guard.1.ts"></code-example>.

Далее откройте `admin-routing.module.ts`, импортируйте функцию `authGuard` и обновите административный маршрут со свойством `canActivate` guard, которое ссылается на нее:

<code-example header="src/app/admin/admin-routing.module.ts (охраняемый маршрут администратора)" path="router/src/app/admin/admin-routing.module.2.ts" region="admin-route"></code-example>.

Функция администрирования теперь защищена стражем, но для полноценной работы стража требуется дополнительная настройка.

<a id="teach-auth"></a>

#### Аутентификация с помощью `authGuard`.

Сделайте `authGuard` имитирующим аутентификацию.

`authGuard` должен вызывать прикладную службу, которая может регистрировать пользователя и сохранять информацию о текущем пользователе. Создайте новый `AuthService` в папке `auth`:

<code-example format="shell" language="shell">

ng generate service auth/auth

</code-example>

Обновите `AuthService` для входа пользователя в систему:

<code-example header="src/app/app/auth/auth.service.ts (excerpt)" path="router/src/app/auth/auth.service.ts"></code-example>

Хотя он не выполняет вход в систему, у него есть флаг `isLoggedIn`, чтобы сообщить вам, аутентифицирован ли пользователь. Его метод `login()` имитирует вызов API к внешней службе, возвращая наблюдаемую, которая успешно разрешается после небольшой паузы.

Свойство `redirectUrl` хранит URL, к которому хотел получить доступ пользователь, чтобы вы могли перейти к нему после аутентификации.

<div class="alert is-helpful">

Чтобы сделать все минимальным, этот пример перенаправляет неаутентифицированных пользователей на `/admin`.

</div>

Пересмотрите `authGuard` для вызова `AuthService`.

<code-example header="src/app/app/auth/auth.guard.ts (v2)" path="router/src/app/auth/auth.guard.2.ts"></code-example>

Эта защита возвращает синхронный булев результат или `UrlTree`. Если пользователь вошел в систему, он возвращает `true` и навигация продолжается.

В противном случае он перенаправляет на страницу входа; страницу, которую вы еще не создали.

Возврат `UrlTree` указывает `Router` отменить текущую навигацию и запланировать новую для перенаправления пользователя.

<a id="add-login-component"></a>

#### Добавьте `LoginComponent`.

Вам нужен `LoginComponent` для входа пользователя в приложение. После входа в систему вы будете перенаправлять на сохраненный URL, если он доступен, или использовать URL по умолчанию.

Нет ничего нового в этом компоненте или способе его использования в конфигурации маршрутизатора.

<code-example format="shell" language="shell">

ng generate component auth/login

</code-example>

Зарегистрируйте маршрут `/login` в файле `auth/auth-routing.module.ts`. В файле `app.module.ts` импортируйте и добавьте `AuthModule` в массив импортов `AppModule`.

<code-tabs> <code-pane header="src/app/app.module.ts" path="router/src/app/app.module.ts" region="auth"></code-pane>
<code-pane header="src/app/auth/login/login.component.html" path="router/src/app/auth/login/login.component.html"></code-pane>
<code-pane header="src/app/auth/login/login.component.ts" path="router/src/app/auth/login/login.component.1.ts"></code-pane>
<code-pane header="src/app/auth/auth.module.ts" path="router/src/app/auth/auth.module.ts"></code-pane>
</code-tabs>

<a id="can-activate-child-guard"></a>

### `canActivateChild`: защита дочерних маршрутов

Вы также можете защитить дочерние маршруты с помощью защиты `canActivateChild`. Защита `canActivateChild` аналогична защите `canActivate`.

Ключевое отличие заключается в том, что он запускается до активации любого дочернего маршрута.

Вы защитили функциональный модуль администратора от несанкционированного доступа. Вам также следует защитить дочерние маршруты _внутри_ функционального модуля.

Добавьте тот же `authGuard` к админскому маршруту `component-less`, чтобы защитить все остальные дочерние маршруты одновременно, вместо того, чтобы добавлять `authGuard` к каждому маршруту по отдельности.

<code-example header="src/app/admin/admin-routing.module.ts (excerpt)" path="router/src/app/admin/admin-routing.module.3.ts" region="can-activate-child"></code-example>.

<a id="can-deactivate-guard"></a>

### `canDeactivate`: обработка несохраненных изменений

Вернемся к рабочему процессу "Герои", приложение принимает каждое изменение героя немедленно без проверки.

В реальном мире вам, возможно, придется накапливать изменения пользователей, проверять их по полям, проверять на сервере или держать изменения в состоянии ожидания, пока пользователь не подтвердит их как группу или не отменит и не вернет все изменения.

Когда пользователь отходит, вы можете позволить ему самому решить, что делать с несохраненными изменениями. Если пользователь отменит изменения, вы останетесь на месте и разрешите новые изменения.

Если пользователь одобрит изменения, приложение можно сохранить.

Вы все еще можете задержать навигацию до тех пор, пока сохранение не будет успешным. Если вы позволите пользователю сразу перейти к следующему экрану, а сохранение окажется неудачным\ (возможно, данные будут признаны недействительными\), вы потеряете контекст ошибки.

Вам нужно остановить навигацию, пока вы асинхронно ждете ответа сервера.

Защита `canDeactivate` поможет вам решить, что делать с несохраненными изменениями и как действовать дальше.

<a id="cancel-save"></a>

#### Отмена и сохранение

Пользователи обновляют информацию о кризисе в компоненте `CrisisDetailComponent`. В отличие от компонента `HeroDetailComponent`, изменения пользователя не обновляют сущность кризиса немедленно.

Вместо этого приложение обновляет сущность, когда пользователь нажимает кнопку Сохранить, и отбрасывает изменения, когда пользователь нажимает кнопку Отмена.

Обе кнопки позволяют вернуться к списку кризисов после сохранения или отмены.

<code-example header="src/app/crisis-center/crisis-detail/crisis-detail.component.ts (методы отмены и сохранения)" path="router/src/app/crisis-center/crisis-detail/crisis-detail.component.ts" region="cancel-save"></code-example>.

В этом сценарии пользователь может нажать на ссылку героев, отменить действие, нажать кнопку возврата браузера или уйти без сохранения.

Этот пример приложения просит пользователя быть явным с диалоговым окном подтверждения, которое асинхронно ожидает ответа пользователя.

<div class="alert is-helpful">

Вы можете ждать ответа пользователя с помощью синхронного, блокирующего кода, однако приложение будет более отзывчивым &mdash; и сможет выполнять другую работу&mdash; если будет ждать ответа пользователя асинхронно.

</div>

Создайте службу `Dialog` для обработки подтверждения пользователя.

<code-example format="shell" language="shell">

ng генерировать диалог обслуживания

</code-example>

Добавьте метод `confirm()` в `DialogService`, чтобы попросить пользователя подтвердить свое намерение. Метод `window.confirm` является блокирующим действием, которое отображает модальный диалог и ожидает взаимодействия с пользователем.

<code-example header="src/app/dialog.service.ts" path="router/src/app/dialog.service.ts"></code-example>.

Он возвращает `Observable`, который разрешается, когда пользователь в конечном итоге решает, что делать: либо отменить изменения и перейти к следующему \(`true`\), либо сохранить ожидающие изменения и остаться в кризисном редакторе \(`false`\).

<a id="canDeactivate"></a>

Создайте защиту, которая проверяет наличие метода `canDeactivate()` в компоненте - любом компоненте.

<code-example format="shell" language="shell">

ng generate guard can-deactivate

</code-example>

Вставьте следующий код в свой страж.

<code-example header="src/app/can-deactivate.guard.ts" path="router/src/app/can-deactivate.guard.ts"></code-example>.

Хотя стражу не обязательно знать, какой компонент имеет метод `deactivate`, он может определить, что компонент `CrisisDetailComponent` имеет метод `canDeactivate()` и вызвать его. Незнание сторожем деталей метода деактивации любого компонента делает его многоразовым.

В качестве альтернативы вы можете сделать специфичный для компонента `canDeactivate` guard для `CrisisDetailComponent`. Метод `canDeactivate()` предоставляет вам текущий экземпляр `компонента`, текущий `ActivatedRoute` и `RouterStateSnapshot` на случай, если вам понадобится доступ к какой-либо внешней информации.

Это было бы полезно, если бы вы хотели использовать эту защиту только для этого компонента и вам нужно было бы получить свойства компонента или подтвердить, должен ли маршрутизатор разрешить навигацию от него.

<code-example header="src/app/can-deactivate.guard.ts (component-specific)" path="router/src/app/can-deactivate.guard.1.ts"></code-example>.

Если вернуться к `CrisisDetailComponent`, то он реализует рабочий процесс подтверждения для несохраненных изменений.

<code-example header="src/app/crisis-center/crisis-detail/crisis-detail.component.ts (excerpt)" path="router/src/app/crisis-center/crisis-detail/crisis-detail.component.ts" region="canDeactivate"></code-example>.

Обратите внимание, что метод `canDeactivate()` может возвращаться синхронно; он возвращает `true` немедленно, если нет кризиса или нет ожидающих изменений. Но он также может возвращать `Promise` или `Observable`, и маршрутизатор будет ждать, пока это разрешится в истинное \(navigate\) или ложное \(stay on the current route\) решение.

Добавьте `Guard` к маршруту деталей кризиса в `crisis-center-routing.module.ts`, используя свойство массива `canDeactivate`.

<code-example header="src/app/crisis-center/crisis-center-routing.module.ts (можно отключить защиту)" path="router/src/app/crisis-center/crisis-center-routing.module.3.ts"></code-example>.

Теперь вы обеспечили пользователю защиту от несохраненных изменений.

<a id="Resolve"></a> <a id="resolve-guard"></a>

### _Resolve_: предварительная выборка данных компонента

В `Hero Detail` и `Crisis Detail` приложение ждало, пока активируется маршрут, чтобы получить данные о соответствующем герое или кризисе.

Если вы используете реальный API, то может возникнуть некоторая задержка, прежде чем данные для отображения будут возвращены с сервера. Вы же не хотите отображать пустой компонент в ожидании данных.

Чтобы улучшить это поведение, вы можете предварительно получить данные с сервера с помощью резольвера, чтобы они были готовы в момент активации маршрута. Это также позволяет обрабатывать ошибки перед маршрутизацией к компоненту.

Нет смысла переходить к детализации кризиса для `id`, для которого нет записи.

Лучше отправить пользователя обратно к `Списку кризисов`, который показывает только действующие кризисные центры.

В общем, вы хотите отложить отображение компонента маршрутизации до тех пор, пока не будут получены все необходимые данные.

<a id="fetch-before-navigating"></a>

#### Выборка данных перед навигацией

В данный момент `CrisisDetailComponent` извлекает данные о выбранном кризисе. Если кризис не найден, маршрутизатор возвращается к представлению списка кризисов.

Возможно, было бы лучше, если бы все это обрабатывалось сначала, до активации маршрута. Резольвер `crisisDetailResolver` мог бы получить `кризис` или перейти в сторону, если `кризис` не существует, _до_ активации маршрута и создания `CrisisDetailComponent`.

Создайте файл `crisis-detail-resolver.ts` в области функции `Crisis Center`. Этот файл будет содержать функцию `crisisDetailResolver`.

<code-example format="shell" language="shell">

ng generate resolver crisis-center/crisis-detail-resolver

</code-example>

<code-example header="src/app/crisis-center/crisis-detail-resolver.ts" path="router/src/app/crisis-center/crisis-detail-resolver.1.ts"></code-example >

Перенесите соответствующие части логики поиска кризисов в `CrisisDetailComponent.ngOnInit()` в `crisisDetailResolver`. Импортируйте модель `Crisis`, `CrisisService` и `Router`, чтобы вы могли перейти в другое место, если не сможете найти кризис.

Будьте явными и используйте тип `ResolveFn` с типом `Crisis`.

Вставьте `CrisisService` и `Router`. Этот метод может возвращать `Promise`, `Observable` или синхронное возвращаемое значение.

Метод `CrisisService.getCrisis()` возвращает наблюдаемое значение, чтобы предотвратить загрузку маршрута до тех пор, пока не будут получены данные.

Если он не возвращает действительный `кризис`, то возвращает пустой `Observable`, отменяет предыдущую текущую навигацию к `CrisisDetailComponent` и возвращает пользователя к `CrisisListComponent`. Обновленная функция resolver выглядит следующим образом:

<code-example header="src/app/crisis-center/crisis-detail-resolver.ts" path="router/src/app/crisis-center/crisis-detail-resolver.ts"></code-example >

Импортируйте этот resolver в `crisis-center-routing.module.ts` и добавьте объект `resolve` в конфигурацию маршрута `CrisisDetailComponent`.

<code-example header="src/app/crisis-center/crisis-center-routing.module.ts (resolver)" path="router/src/app/crisis-center/crisis-center-routing.module.4.ts"></code-example

Компонент `CrisisDetailComponent` больше не должен получать данные о кризисе. Когда вы переконфигурировали маршрут, вы изменили местоположение кризиса.

Обновите `CrisisDetailComponent`, чтобы получить кризис из свойства `ActivatedRoute.data.crisis` вместо этого;

<code-example header="src/app/crisis-center/crisis-detail/crisis-detail.component.ts (ngOnInit v2)" path="router/src/app/crisis-center/crisis-detail/crisis-detail.component.ts" region="ngOnInit"></code-example>

Рассмотрите следующие три важных момента:

1.  Функция маршрутизатора `ResolveFn` является необязательной.

1.  Маршрутизатор вызывает резольвер в любом случае, когда пользователь может переместиться в сторону, поэтому вам не придется писать код для каждого случая использования.

1.  Возвращение пустого `Observable` хотя бы в одном резольвере отменяет навигацию.

Соответствующий код Кризисного центра для этого этапа приведен ниже.

<code-tabs> <code-pane header="app.component.html" path="router/src/app/app.component.html"></code-pane>
<code-pane header="crisis-center-home.component.html" path="router/src/app/crisis-center/crisis-center-home/crisis-center-home.component.html"></code-pane>
<code-pane header="crisis-center.component.html" path="router/src/app/crisis-center/crisis-center/crisis-center.component.html"></code-pane>
<code-pane header="crisis-center-routing.module.ts" path="router/src/app/crisis-center/crisis-center-routing.module.4.ts"></code-pane>
<code-pane header="crisis-list.component.html" path="router/src/app/crisis-center/crisis-list/crisis-list.component.html"></code-pane>
<code-pane header="crisis-list.component.ts" path="router/src/app/crisis-center/crisis-list/crisis-list.component.ts"></code-pane>
<code-pane header="crisis-detail.component.html" path="router/src/app/crisis-center/crisis-detail/crisis-detail.component.html"></code-pane>
<code-pane header="crisis-detail.component.ts" path="router/src/app/crisis-center/crisis-detail/crisis-detail.component.ts"></code-pane>
<code-pane header="crisis-detail-resolver.ts" path="router/src/app/crisis-center/crisis-detail-resolver.ts"></code-pane>
<code-pane header="crisis.service.ts" path="router/src/app/crisis-center/crisis.service.ts"></code-pane>
<code-pane header="dialog.service.ts" path="router/src/app/dialog.service.ts"></code-pane>
</code-tabs>

Охрана

<code-tabs> <code-pane header="auth.guard.ts" path="router/src/app/auth/auth.guard.3.ts"></code-pane>
<code-pane header="can-deactivate.guard.ts" path="router/src/app/can-deactivate.guard.ts"></code-pane>
</code-tabs>

<a id="query-parameters"></a> <a id="fragment"></a>

### Параметры запроса и фрагменты

В разделе [параметры маршрута](#optional-route-parameters) вы имели дело только с параметрами, специфичными для маршрута. Однако вы можете использовать параметры запроса для получения необязательных параметров, доступных для всех маршрутов.

[Фрагменты](https://en.wikipedia.org/wiki/Fragment_identifier) ссылаются на определенные элементы на странице, идентифицируемые атрибутом `id`.

Обновите `authGuard`, чтобы обеспечить запрос `session_id`, который сохраняется после перехода к другому маршруту.

Добавьте элемент `anchor`, чтобы можно было перейти к определенной точке страницы.

Добавьте объект `NavigationExtras` в метод `router.navigate()`, который переводит вас на маршрут `/login`.

<code-example header="src/app/app/auth/auth.guard.ts (v3)" path="router/src/app/auth/auth.guard.4.ts"></code-example>

Вы также можете сохранять параметры запроса и фрагменты при разных навигациях без необходимости предоставлять их снова при переходе. В `LoginComponent` вы добавите _объект_ в качестве второго аргумента в функцию `router.navigate()` и предоставите `queryParamsHandling` и `preserveFragment` для передачи текущих параметров запроса и фрагмента в следующий маршрут.

<code-example header="src/app/auth/login/login.component.ts (preserve)" path="router/src/app/auth/login/login.component.ts" region="preserve"></code-example>

<div class="alert is-helpful">

Функция `queryParamsHandling` также предоставляет опцию `merge`, которая сохраняет и объединяет текущие параметры запроса с любыми предоставленными параметрами запроса при навигации.

</div>

Чтобы перейти к маршруту Admin Dashboard после входа в систему, обновите `admin-dashboard.component.ts` для обработки параметров запроса и фрагмента.

<code-example header="src/app/admin/admin-dashboard/admin-dashboard.component.ts (v2)" path="router/src/app/app/admin/admin-dashboard/admin-dashboard.component.1.ts"></code-example>.

Параметры запроса и фрагменты также доступны через службу `ActivatedRoute`. Как и параметры маршрута, параметры запроса и фрагменты предоставляются в виде `Observable`.

Обновленный компонент Crisis Admin передает `Observable` непосредственно в шаблон с помощью `AsyncPipe`.

Теперь вы можете нажать на кнопку Admin, которая приведет вас на страницу входа с предоставленными `queryParamMap` и `fragment`. После того, как вы нажмете кнопку входа, обратите внимание, что вы были перенаправлены на страницу `Admin Dashboard` с параметрами запроса и фрагментом, все еще сохранившимися в адресной строке.

Вы можете использовать эти постоянные биты информации для вещей, которые необходимо предоставлять на разных страницах, например, токены аутентификации или идентификаторы сессии.

<div class="alert is-helpful">

Параметры `query params` и `fragment` также могут быть сохранены с помощью `RouterLink` с привязками `queryParamsHandling` и `preserveFragment` соответственно.

</div>

<a id="asynchronous-routing"></a>

## Веха 6: Асинхронная маршрутизация

По мере прохождения этапов приложение, естественно, становилось все больше. В какой-то момент вы достигнете точки, когда приложение будет долго загружаться.

Чтобы решить эту проблему, используйте асинхронную маршрутизацию, которая загружает функциональные модули лениво, по запросу. Ленивая загрузка имеет несколько преимуществ.

-   Вы можете загружать функциональные области только по запросу пользователя.

-   Вы можете ускорить время загрузки для пользователей, которые посещают только определенные области приложения

-   Вы можете продолжать расширять области функций с ленивой загрузкой, не увеличивая размер начального пакета загрузки.

Вы уже прошли часть этого пути. Разбив приложение на модули &mdash;`AppModule`, `HeroesModule`, `AdminModule` и `CrisisCenterModule`&mdash; вы получили естественных кандидатов для ленивой загрузки.

Некоторые модули, например `AppModule`, должны быть загружены с самого начала. Но другие можно и нужно загружать в ленивом режиме.

Например, модуль `AdminModule` нужен нескольким авторизованным пользователям, поэтому его следует загружать только по запросу нужных людей.

<a id="lazy-loading-route-config"></a>

### Конфигурация маршрута с ленивой загрузкой

Измените путь `admin` в `admin-routing.module.ts` с `'admin'` на пустую строку, `''`, пустой путь.

Используйте маршруты с пустым путем для группировки маршрутов вместе без добавления дополнительных сегментов пути к URL. Пользователи по-прежнему будут посещать `/admin`, а `AdminComponent` по-прежнему будет служить компонентом маршрутизации, содержащим дочерние маршруты.

Откройте `AppRoutingModule` и добавьте новый маршрут `admin` в его массив `appRoutes`.

Задайте ему свойство `loadChildren` вместо свойства `children`. Свойство `loadChildren` принимает функцию, которая возвращает обещание, используя встроенный в браузер синтаксис для ленивой загрузки кода с использованием динамического импорта `import('...')`.

Путь - это расположение `AdminModule'\ (относительно корня\ приложения).

После запроса и загрузки кода `Promise` разрешает объект, содержащий `NgModule`, в данном случае `AdminModule`.

<code-example header="app-routing.module.ts (load children)" path="router/src/app/app-routing.module.5.ts" region="admin-1"></code-example>

<div class="alert is-important">

**NOTE**: <br /> When using absolute paths, the `NgModule` file location must begin with `src/app` in order to resolve correctly.
For custom [path mapping with absolute paths](https://www.typescriptlang.org/docs/handbook/module-resolution.html#path-mapping), you must configure the `baseUrl` and `paths` properties in the project `tsconfig.json`.

</div>

When the router navigates to this route, it uses the `loadChildren` string to dynamically load the `AdminModule`. Then it adds the `AdminModule` routes to its current route configuration.
Finally, it loads the requested route to the destination admin component.

The lazy loading and re-configuration happen just once, when the route is first requested; the module and routes are available immediately for subsequent requests.

Take the final step and detach the admin feature set from the main application. The root `AppModule` must neither load nor reference the `AdminModule` or its files.

In `app.module.ts`, remove the `AdminModule` import statement from the top of the file and remove the `AdminModule` from the NgModule's `imports` array.

<a id="can-match-guard"></a>

### `canMatch`: guarding unauthorized access of feature modules

You're already protecting the `AdminModule` with a `canActivate` guard that prevents unauthorized users from accessing the admin feature area. It redirects to the login page if the user is not authorized.

But the router is still loading the `AdminModule` even if the user can't visit any of its components. Ideally, you'd only load the `AdminModule` if the user is logged in.

A `canMatch` guard controls whether the `Router` attempts to match a `Route`. This lets you have multiple `Route` configurations that share the same `path` but are matched based on different conditions. This approach
allows the `Router` to match the wildcard `Route` instead.

The existing `authGuard` contains the logic to support the `canMatch` guard.

Finally, add the `authGuard` to the `canMatch` array property for the `admin` route. The completed admin route looks like this:

<code-example header="app-routing.module.ts (lazy admin route)" path="router/src/app/app-routing.module.5.ts" region="admin"></code-example>

<a id="preloading"></a>

### Preloading: background loading of feature areas

In addition to loading modules on-demand, you can load modules asynchronously with preloading.

The `AppModule` is eagerly loaded when the application starts, meaning that it loads right away. Now the `AdminModule` loads only when the user clicks on a link, which is called lazy loading.

Preloading lets you load modules in the background so that the data is ready to render when the user activates a particular route. Consider the Crisis Center.
It isn't the first view that a user sees.
By default, the Heroes are the first view.
For the smallest initial payload and fastest launch time, you should eagerly load the `AppModule` and the `HeroesModule`.

You could lazy load the Crisis Center. But you're almost certain that the user will visit the Crisis Center within minutes of launching the app.
Ideally, the application would launch with just the `AppModule` and the `HeroesModule` loaded and then, almost immediately, load the `CrisisCenterModule` in the background.
By the time the user navigates to the Crisis Center, its module is loaded and ready.

<a id="how-preloading"></a>

#### How preloading works

After each successful navigation, the router looks in its configuration for an unloaded module that it can preload. Whether it preloads a module, and which modules it preloads, depends upon the preload strategy.

The `Router` offers two preloading strategies:

| Strategies | Details | |:--- |:--- |
| No preloading | The default. Lazy loaded feature areas are still loaded on-demand. |
| Preloading | All lazy loaded feature areas are preloaded. |

The router either never preloads, or preloads every lazy loaded module. The `Router` also supports [custom preloading strategies](#custom-preloading) for fine control over which modules to preload and when.

This section guides you through updating the `CrisisCenterModule` to load lazily by default and use the `PreloadAllModules` strategy to load all lazy loaded modules.

<a id="lazy-load-crisis-center"></a>

#### Lazy load the crisis center

Update the route configuration to lazy load the `CrisisCenterModule`. Take the same steps you used to configure `AdminModule` for lazy loading.

1.  Change the `crisis-center` path in the `CrisisCenterRoutingModule` to an empty string.
1.  Add a `crisis-center` route to the `AppRoutingModule`.
1.  Set the `loadChildren` string to load the `CrisisCenterModule`.
1.  Remove all mention of the `CrisisCenterModule` from `app.module.ts`.

Here are the updated modules _before enabling preload_:

<code-tabs> <code-pane header="app.module.ts" path="router/src/app/app.module.ts" region="preload"></code-pane>
<code-pane header="app-routing.module.ts" path="router/src/app/app-routing.module.6.ts" region="preload-v1"></code-pane>
<code-pane header="crisis-center-routing.module.ts" path="router/src/app/crisis-center/crisis-center-routing.module.ts"></code-pane>
</code-tabs>

You could try this now and confirm that the `CrisisCenterModule` loads after you click the "Crisis Center" button.

To enable preloading of all lazy loaded modules, import the `PreloadAllModules` token from the Angular router package.

The second argument in the `RouterModule.forRoot()` method takes an object for additional configuration options. The `preloadingStrategy` is one of those options.
Add the `PreloadAllModules` token to the `forRoot()` call:

<code-example header="src/app/app-routing.module.ts (preload all)" path="router/src/app/app-routing.module.6.ts" region="forRoot"></code-example>

This configures the `Router` preloader to immediately load all lazy loaded routes (routes with a `loadChildren` property).

When you visit `http://localhost:4200`, the `/heroes` route loads immediately upon launch and the router starts loading the `CrisisCenterModule` right after the `HeroesModule` loads.

<a id="custom-preloading"></a>

### Custom Preloading Strategy

Preloading every lazy loaded module works well in many situations. However, in consideration of things such as low bandwidth and user metrics, you can use a custom preloading strategy for specific feature modules.

This section guides you through adding a custom strategy that only preloads routes whose `data.preload` flag is set to `true`. Recall that you can add anything to the `data` property of a route.

Set the `data.preload` flag in the `crisis-center` route in the `AppRoutingModule`.

<code-example header="src/app/app-routing.module.ts (route data preload)" path="router/src/app/app-routing.module.ts" region="preload-v2"></code-example>

Generate a new `SelectivePreloadingStrategy` service.

<code-example format="shell" language="shell">

ng generate service selective-preloading-strategy

</code-example>

Replace the contents of `selective-preloading-strategy.service.ts` with the following:

<code-example header="src/app/selective-preloading-strategy.service.ts" path="router/src/app/selective-preloading-strategy.service.ts"></code-example>

`SelectivePreloadingStrategyService` implements the `PreloadingStrategy`, which has one method, `preload()`.

The router calls the `preload()` method with two arguments:

1.  The route to consider.
1.  A loader function that can load the routed module asynchronously.

An implementation of `preload` must return an `Observable`. If the route does preload, it returns the observable returned by calling the loader function.
If the route does not preload, it returns an `Observable` of `null`.

In this sample, the `preload()` method loads the route if the route's `data.preload` flag is truthy. We also skip loading the `Route` if there is a `canMatch` guard because the user might
not have access to it.

As a side effect, `SelectivePreloadingStrategyService` logs the `path` of a selected route in its public `preloadedModules` array.

Shortly, you'll extend the `AdminDashboardComponent` to inject this service and display its `preloadedModules` array.

But first, make a few changes to the `AppRoutingModule`.

1.  Import `SelectivePreloadingStrategyService` into `AppRoutingModule`.
1.  Replace the `PreloadAllModules` strategy in the call to `forRoot()` with this `SelectivePreloadingStrategyService`.

Now edit the `AdminDashboardComponent` to display the log of preloaded routes.

1.  Import the `SelectivePreloadingStrategyService`.
1.  Inject it into the dashboard's constructor.
1.  Update the template to display the strategy service's `preloadedModules` array.

Now the file is as follows:

<code-example header="src/app/admin/admin-dashboard/admin-dashboard.component.ts (preloaded modules)" path="router/src/app/admin/admin-dashboard/admin-dashboard.component.ts"></code-example>

Once the application loads the initial route, the `CrisisCenterModule` is preloaded. Verify this by logging in to the `Admin` feature area and noting that the `crisis-center` is listed in the `Preloaded Modules`.
It also logs to the browser's console.

<a id="redirect-advanced"></a>

### Migrating URLs with redirects

You've set up the routes for navigating around your application and used navigation imperatively and declaratively. But like any application, requirements change over time.
You've setup links and navigation to `/heroes` and `/hero/:id` from the `HeroListComponent` and `HeroDetailComponent` components.
If there were a requirement that links to `heroes` become `superheroes`, you would still want the previous URLs to navigate correctly.
You also don't want to update every link in your application, so redirects makes refactoring routes trivial.

<a id="url-refactor"></a>

#### Changing `/heroes` to `/superheroes`

This section guides you through migrating the `Hero` routes to new URLs. The `Router` checks for redirects in your configuration before navigating, so each redirect is triggered when needed.
To support this change, add redirects from the old routes to the new routes in the `heroes-routing.module`.

<code-example header="src/app/heroes/heroes-routing.module.ts (heroes redirects)" path="router/src/app/heroes/heroes-routing.module.ts"></code-example>

Notice two different types of redirects. The first change is from `/heroes` to `/superheroes` without any parameters.
The second change is from `/hero/:id` to `/superhero/:id`, which includes the `:id` route parameter.
Router redirects also use powerful pattern-matching, so the `Router` inspects the URL and replaces route parameters in the `path` with their appropriate destination.
Previously, you navigated to a URL such as `/hero/15` with a route parameter `id` of `15`.

<div class="alert is-helpful">

The `Router` also supports [query parameters](#query-parameters) and the [fragment](#fragment) when using redirects.

-   When using absolute redirects, the `Router` uses the query parameters and the fragment from the `redirectTo` in the route config
-   When using relative redirects, the `Router` use the query params and the fragment from the source URL

</div>

Currently, the empty path route redirects to `/heroes`, which redirects to `/superheroes`. This won't work because the `Router` handles redirects once at each level of routing configuration.
This prevents chaining of redirects, which can lead to endless redirect loops.

Instead, update the empty path route in `app-routing.module.ts` to redirect to `/superheroes`.

<code-example header="src/app/app-routing.module.ts (superheroes redirect)" path="router/src/app/app-routing.module.ts"></code-example>

A `routerLink` isn't tied to route configuration, so update the associated router links to remain active when the new route is active. Update the `app.component.ts` template for the `/heroes` `routerLink`.

<code-example header="src/app/app.component.html (superheroes active routerLink)" path="router/src/app/app.component.html"></code-example>

Update the `goToHeroes()` method in the `hero-detail.component.ts` to navigate back to `/superheroes` with the optional route parameters.

<code-example header="src/app/heroes/hero-detail/hero-detail.component.ts (goToHeroes)" path="router/src/app/heroes/hero-detail/hero-detail.component.ts" region="redirect"></code-example>

With the redirects setup, all previous routes now point to their new destinations and both URLs still function as intended.

<a id="inspect-config"></a>

### Inspect the router's configuration

To determine if your routes are actually evaluated [in the proper order](#routing-module-order), you can inspect the router's configuration.

Do this by injecting the router and logging to the console its `config` property. For example, update the `AppModule` as follows and look in the browser console window to see the finished route configuration.

<code-example header="src/app/app.module.ts (inspect the router config)" path="router/src/app/app.module.7.ts" region="inspect-config"></code-example>

<a id="final-app"></a>

## Final application

For the completed router application, see the <live-example name="router"></live-example> for the final source code.

<a id="link-parameters-array"></a>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
