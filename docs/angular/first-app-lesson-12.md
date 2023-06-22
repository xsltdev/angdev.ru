# Первое приложение Angular урок 12 - Добавление формы в приложение Angular

Этот урок демонстрирует, как добавить форму, собирающую данные пользователя, в приложение Angular. Этот урок начинается с функционального приложения Angular и показывает, как добавить в него форму.

Данные, которые собирает форма, отправляются только в сервис приложения, который записывает их в консоль браузера. Использование REST API для отправки и получения данных формы в этом уроке не рассматривается.

**Затраты времени:** ожидайте, что на прохождение этого урока вы потратите около 20 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в Уроке 11, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите <live-example name="first-app-lesson-11"></live-example> из Урока 11, где вы можете:

    -   Использовать _живой пример_ в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать _download пример_ и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](tutorial/first-app), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть готовый код для этого урока в <live-example></live-example> для этого урока.

## После завершения

-   В вашем приложении есть форма, в которую пользователи могут вводить данные, которые отправляются в сервис вашего приложения.

-   Сервис записывает данные из формы в консоль браузера.

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 - Добавление метода для отправки данных формы

Этот шаг добавляет метод в сервис вашего приложения, который получает данные формы для отправки в место назначения данных. В этом примере метод записывает данные из формы в консольный журнал браузера.

В панели **Edit** вашей IDE:

1.  В `src/app/housing.service.ts`, внутри класса `HousingService`, вставьте этот метод в нижней части определения класса.

    <code-example header="Submit method in src/app/housing.service.ts" path="first-app-lesson-12/src/app/housing.service.ts" region="submit-method"></code-example>.

1.  Убедитесь, что приложение собирается без ошибок.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

### Шаг 2 - Добавление функций формы на страницу подробностей

Этот шаг добавляет код на страницу подробностей, который обрабатывает взаимодействие с формой.

В панели **Edit** вашей IDE, в `src/app/details/details.component.ts`:

1.  После оператора `import` в верхней части файла добавьте следующий код для импорта классов форм Angular.

    <code-example header="Forms imports in src/app/details/details.component.ts" path="first-app-lesson-12/src/app/details/details.component.ts" region="form-imports"></code-example>.

1.  В метаданных декоратора `DetailsComponent` обновите свойство `imports` следующим кодом:

    <code-example header="imports directive in src/app/details/details.component.ts" path="first-app-lesson-12/src/app/details/details.component.ts" region="component-imports"></code-example>.

1.  В классе `DetailsComponent`, перед методом `constructor()`, добавьте следующий код для создания объекта формы.

    <code-example header="template directive in src/app/details/details.component.ts" path="first-app-lesson-12/src/app/details/details.component.ts" region="form-code"></code-example>.

    В Angular `FormGroup` и `FormControl` - это типы, которые позволяют создавать формы. Тип `FormControl` может предоставлять значение по умолчанию и формировать данные формы. В данном примере `firstName` - это `string`, а значение по умолчанию - пустая строка.

1.  В классе `DetailsComponent` после метода `constructor()` добавьте следующий код для обработки клика **Apply now**.

    <code-example header="template directive in src/app/details/details.component.ts" path="first-app-lesson-12/src/app/details/details.component.ts" region="form-submit"></code-example>.

    Эта кнопка еще не существует - вы добавите ее в следующем шаге. В приведенном выше коде `FormControl` может возвращать `null`. Этот код использует оператор nullish coalescing, чтобы по умолчанию вернуть пустую строку, если значение `null`.

1.  Убедитесь, что приложение собирается без ошибок.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

### Шаг 3 - Добавление разметки формы на страницу подробностей

Этот шаг добавляет разметку на страницу подробностей, на которой отображается форма.

В панели **Edit** вашей IDE, в `src/app/details/details.component.ts`:

1. В метаданных декоратора `DetailsComponent` обновите HTML `template`, чтобы добавить разметку формы в соответствии со следующим кодом.

    <code-example header="template directive in src/app/details/details.component.ts" path="first-app-lesson-12/src/app/details/details.component.ts" region="component-template"></code-example>.

    Теперь шаблон включает обработчик события `(submit)="submitApplication()"`. Angular использует синтаксис круглых скобок вокруг имени события для создания определяемых событий в коде шаблона. Код справа от знака равенства - это код, который должен быть выполнен при срабатывании этого события. Вы можете привязываться к событиям браузера и пользовательским событиям.

1. Убедитесь, что приложение создается без ошибок.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

     <section class="lightbox">

     <img alt="страница с формой для подачи заявки на проживание в этом месте" src="generated/images/guide/faa/homes-app-lesson-12-step-3.png">

     </section>

### Шаг 4 - Проверка новой формы вашего приложения

На этом шаге тестируется новая форма, чтобы убедиться, что при отправке данных формы в приложение данные формы появляются в журнале консоли.

1.  В панели **Terminal** вашей IDE запустите `ng serve`, если он еще не запущен.

1.  В браузере откройте ваше приложение по адресу `http://localhost:4200`.

1.  В приложении щелкните правой кнопкой мыши и в контекстном меню выберите **Inspect**.

1.  В окне инструментов разработчика выберите вкладку **Консоль**.

    Убедитесь, что окно инструментов разработчика видно для следующих шагов

1.  В вашем приложении:

    1.  Выберите местоположение жилья и нажмите **Узнать больше**, чтобы увидеть подробную информацию о доме.

    1.  На странице сведений о доме прокрутите страницу в самый низ, чтобы найти новую форму.

    1.  Введите данные в поля формы - подойдут любые данные.

    1.  Выберите **Применить сейчас**, чтобы отправить данные.

1.  В окне инструментов разработчика просмотрите вывод журнала, чтобы найти данные формы.

## Обзор урока

В этом уроке вы обновили свое приложение, чтобы:

-   добавить форму с помощью функции форм Angular

-   подключить данные, полученные в форме, к форме с помощью обработчика событий.

Если у вас возникли трудности с этим уроком, вы можете просмотреть готовый код для него в <live-example></live-example>.

## Следующие шаги

-   [Урок 13 - Добавление функции поиска в ваше приложение](tutorial/first-app/first-app-lesson-13)

## Дополнительная информация

Для получения дополнительной информации по темам, рассмотренным в этом уроке, посетите:

-   [Angular Forms](/guide/forms)

-   [Обработка событий](/guide/event-binding)