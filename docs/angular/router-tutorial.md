# Использование маршрутов Angular в одностраничном приложении

Этот учебник описывает, как создать одностраничное приложение, SPA, которое использует несколько маршрутов Angular.

В одностраничном приложении \(SPA\), все функции вашего приложения существуют на одной HTML странице. Когда пользователи обращаются к функциям вашего приложения, браузеру нужно отобразить только те части, которые важны для пользователя, вместо того, чтобы загружать новую страницу.

Этот шаблон может значительно улучшить пользовательское восприятие вашего приложения.

Чтобы определить, как пользователи перемещаются по вашему приложению, вы используете маршруты. Добавьте маршруты, чтобы определить, как пользователи переходят от одной части вашего приложения к другой.

Вы также можете настроить маршруты для защиты от неожиданного или несанкционированного поведения.

Чтобы изучить пример приложения, в котором описано содержание этого руководства, смотрите <live-example></live-example>.

## Задачи

-   Организовать функции примера приложения в модули.

-   Определить, как перейти к компоненту.

-   Передавать информацию компоненту с помощью параметра.

-   Структурировать маршруты путем вложения нескольких маршрутов.

-   Проверять, могут ли пользователи получить доступ к маршруту.

-   Контролировать, может ли приложение отбрасывать несохраненные изменения.

-   Повышение производительности за счет предварительной выборки данных маршрута и "ленивой" загрузки функциональных модулей.

-   Требовать определенные критерии для загрузки компонентов.

## Предварительные условия

Чтобы завершить этот учебник, вы должны иметь базовое представление о следующих концепциях:

-   JavaScript

-   HTML

-   CSS

-   [Angular CLI](cli)

Вам может быть полезен учебник [Tour of Heroes](tutorial/tour-of-heroes), но он не обязателен.

## Создайте пример приложения

Используя Angular CLI, создайте новое приложение, _angular-router-sample_. Это приложение будет состоять из двух компонентов: _crisis-list_ и _heroes-list_.

1.  Создайте новый проект Angular, _angular-router-sample_.

    <code-example format="shell" language="shell">

    ng new angular-router-sample

    </code-example>

    Когда появится запрос `Вы хотите добавить маршрутизацию Angular?`, выберите `N`.

    На вопрос `Какой формат таблицы стилей вы хотите использовать?` выберите `CSS`.

    Через несколько мгновений новый проект `angular-router-sample` будет готов.

1.  В терминале перейдите в каталог `angular-router-sample`.

1.  Создайте компонент _crisis-list_.

    <code-example format="shell" language="shell">

    ng generate component crisis-list

    </code-example>.

1.  В редакторе кода найдите файл `crisis-list.component.html` и замените содержимое placeholder на следующий HTML.

    <code-example header="src/app/crisis-list/crisis-list.component.html" path="router-tutorial/src/app/crisis-list/crisis-list.component.html"></code-example>

1.  Создайте второй компонент, _heroes-list_.

    <code-example format="shell" language="shell">

    ng generate component heroes-list

    </code-example>

1.  В редакторе кода найдите файл `heroes-list.component.html` и замените его содержимое на следующий HTML.

    <code-example header="src/app/heroes-list/heroes-list.component.html" path="router-tutorial/src/app/heroes-list/heroes-list.component.html"></code-example>.

1.  В редакторе кода откройте файл `app.component.html` и замените его содержимое на следующий HTML.

    <code-example header="src/app/app.component.html" path="router-tutorial/src/app/app.component.html" region="setup"></code-example>.

1.  Убедитесь, что ваше новое приложение работает как ожидалось, выполнив команду `ng serve`.

    <code-example format="shell" language="shell">

    ng serve

    </code-example>

1.  Откройте браузер по адресу `http://localhost:4200`.

    Вы должны увидеть одну веб-страницу, состоящую из заголовка и HTML двух ваших компонентов.

## Импортируйте `RouterModule` из `@angular/router`.

Маршрутизация позволяет отображать определенные представления вашего приложения в зависимости от пути URL. Чтобы добавить эту функциональность в ваш пример приложения, вам необходимо обновить файл `app.module.ts` для использования модуля `RouterModule`.
Вы импортируете этот модуль из `@angular/router`.

1.  В редакторе кода откройте файл `app.module.ts`.

1.  Добавьте следующий оператор `import`.

    <code-example header="src/app/app.module.ts" path="router-tutorial/src/app/app/app.module.ts" region="router-import"></code-example>

## Определите ваши маршруты

В этом разделе вы определите два маршрута:

-   Маршрут `/crisis-center` открывает компонент `crisis-center`.

-   Маршрут `/heroes-list` открывает компонент `heroes-list`.

Определение маршрута - это объект JavaScript. Каждый маршрут обычно имеет два свойства.

Первое свойство, `path`, представляет собой строку, указывающую путь URL для маршрута.

Второе свойство, `component`, - это строка, указывающая, какой компонент должно отображать ваше приложение для этого пути.

1.  В редакторе кода откройте файл `app.module.ts`.

1.  Найдите раздел `@NgModule()`.

1.  Замените массив `imports` в этой секции на следующий.

    <code-example header="src/app/app.module.ts" path="router-tutorial/src/app/app.module.ts" region="import-basic"></code-example>.

Этот код добавляет `RouterModule` в массив `imports`. Далее код использует метод `forRoot()` модуля `RouterModule` для определения двух маршрутов.

Этот метод принимает массив объектов JavaScript, каждый из которых определяет свойства маршрута.

Метод `forRoot()` гарантирует, что ваше приложение создаст только один `RouterModule`.

Для получения дополнительной информации смотрите [Singleton Services](guide/singleton-services#forroot-and-the-router).

## Обновите ваш компонент с помощью `router-outlet`.

На данном этапе вы определили два маршрута для своего приложения. Однако ваше приложение по-прежнему имеет компоненты `crisis-list` и `heroes-list`, жестко закодированные в шаблоне `app.component.html`.
Чтобы ваши маршруты работали, вам нужно обновить шаблон, чтобы динамически загружать компонент на основе пути URL.

Чтобы реализовать эту функциональность, вы добавляете директиву `router-outlet` в файл шаблона.

1.  В редакторе кода откройте файл `app.component.html`.

1.  Удалите следующие строки.

    <code-example header="src/app/app.component.html" path="router-tutorial/src/app/app/app.component.html" region="components"></code-example

1.  Добавьте директиву `router-outlet`.

    <code-example header="src/app/app.component.html" path="router-tutorial/src/app/app.component.html" region="router-outlet"></code-example>.

Просмотрите обновленное приложение в браузере. Вы должны увидеть только заголовок приложения.

Чтобы просмотреть компонент `crisis-list`, добавьте `crisis-list` в конец пути в адресной строке браузера.

Например:

<code-example format="https" language="https">

http://localhost:4200/crisis-list

</code-example>

Обратите внимание, что компонент `crisis-list` отображается. Angular использует определенный вами маршрут для динамической загрузки компонента.
Вы можете загрузить компонент `heroes-list` таким же образом:

<code-example format="https" language="https">

http://localhost:4200/heroes-list

</code-example>

## Управление навигацией с помощью элементов пользовательского интерфейса

В настоящее время ваше приложение поддерживает два маршрута. Однако единственный способ использовать эти маршруты - это вручную ввести путь в адресную строку браузера.

В этом разделе вы добавите две ссылки, по которым пользователи смогут переходить между компонентами `heroes-list` и `crisis-list`.

Вы также добавите несколько стилей CSS.

Хотя эти стили не являются обязательными, они облегчают определение ссылки для отображаемого в данный момент компонента.

Вы добавите эту функциональность в следующем разделе.

1.  Откройте файл `app.component.html` и добавьте следующий HTML под заголовком.

    <code-example header="src/app/app.component.html" path="router-tutorial/src/app/app/app.component.html" region="nav"></code-example>.

    Этот HTML использует директиву Angular, `routerLink`.

    Эта директива соединяет определенные вами маршруты с файлами вашего шаблона.

1.  Откройте файл `app.component.css` и добавьте следующие стили.

    <code-example header="src/app/app.component.css" path="router-tutorial/src/app/app.component.css"></code-example>.

Если вы просмотрите ваше приложение в браузере, вы должны увидеть эти две ссылки. Когда вы щелкаете по ссылке, появляется соответствующий компонент.

## Определение активного маршрута

Хотя пользователи могут перемещаться по вашему приложению с помощью ссылок, добавленных в предыдущем разделе, у них нет простого способа определить активный маршрут. Добавьте эту возможность с помощью директивы Angular `routerLinkActive`.

1.  В редакторе кода откройте файл `app.component.html`.

1.  Обновите теги якорей, чтобы включить директиву `routerLinkActive`.

    <code-example header="src/app/app.component.html" path="router-tutorial/src/app/app.component.html" region="routeractivelink"></code-example>

Снова просмотрите свое приложение. Когда вы нажимаете на одну из кнопок, стиль этой кнопки автоматически обновляется, идентифицируя активный компонент для пользователя.
Добавляя директиву `routerLinkActive`, вы сообщаете своему приложению о необходимости применения определенного CSS-класса к активному маршруту.

В данном руководстве этот CSS-класс - `activebutton`, но вы можете использовать любой класс, который вам нужен.

Обратите внимание, что мы также указываем значение для `routerLinkActive` в `ariaCurrentWhenActive`. Это гарантирует, что пользователи с ослабленным зрением (которые могут не воспринимать различные применяемые стилизации) также смогут определить активную кнопку. Для получения дополнительной информации см. раздел Accessibility Best Practices [Active links identification section](/guide/accessibility#active-links-identification).

## Добавление перенаправления

На этом этапе руководства вы добавляете маршрут, который перенаправляет пользователя на отображение компонента `/heroes-list`.

1.  В редакторе кода откройте файл `app.module.ts`.
1.  В массиве `imports` обновите секцию `RouterModule` следующим образом.

    <code-example header="src/app/app.module.ts" path="router-tutorial/src/app/app/app.module.ts" region="import-redirect"></code-example>.

    Обратите внимание, что этот новый маршрут использует пустую строку в качестве пути.

    Кроме того, он заменяет свойство `component` на два новых:

    | Properties | Details |

    | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

    | `redirectTo` | Это свойство указывает Angular перенаправлять с пустого пути на путь `heroes-list`. |

    | `pathMatch` | Это свойство указывает Angular на то, какую часть URL следует проверять. В данном руководстве вы должны установить это свойство в `full`. Эта стратегия рекомендуется, когда у вас есть пустая строка для пути. Более подробную информацию об этом свойстве можно найти в документации [Route API](api/router/Route). |

Теперь, когда вы открываете свое приложение, оно по умолчанию отображает компонент `heroes-list`.

## Добавление страницы 404

Пользователь может попытаться получить доступ к маршруту, который вы не определили. Чтобы учесть такое поведение, лучшей практикой является отображение страницы 404.
В этом разделе вы создадите страницу 404 и обновите конфигурацию маршрутов, чтобы отображать эту страницу для всех неопределенных маршрутов.

1.  В терминале создайте новый компонент `PageNotFound`.

    <code-example format="shell" language="shell">

    ng generate component page-not-found

    </code-example>.

1.  В редакторе кода откройте файл `page-not-found.component.html` и замените его содержимое на следующий HTML.

    <code-example header="src/app/page-not-found/page-not-found.component.html" path="router-tutorial/src/app/page-not-found/page-not-found.component.html"></code-example>.

1.  Откройте файл `app.module.ts`.

    В массиве `imports` обновите секцию `RouterModule` следующим образом.

    <code-example header="src/app/app.module.ts" path="router-tutorial/src/app/app/app.module.ts" region="import-wildcard"></code-example>.

    Новый маршрут использует путь, `**`.

    Этот путь - то, как Angular идентифицирует маршрут с подстановочным знаком.

    Любой маршрут, который не совпадает с существующим в вашей конфигурации, будет использовать этот путь.

    <div class="alert is-important">

    Notice that the wildcard route is placed at the end of the array.

    The order of your routes is important, as Angular applies routes in order and uses the first match it finds.

    </div>

Try navigating to a non-existing route on your application, such as `http://localhost:4200/powers`. This route doesn't match anything defined in your `app.module.ts` file.

However, because you defined a wildcard route, the application automatically displays your `PageNotFound` component.

## Next steps

At this point, you have a basic application that uses Angular's routing feature to change what components the user can see based on the URL address. You have extended these features to include a redirect, as well as a wildcard route to display a custom 404 page.

Для получения дополнительной информации о маршрутизации см. следующие темы:

-   [In-app Routing and Navigation](guide/router)

-   [API маршрутизатора](api/router)

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
