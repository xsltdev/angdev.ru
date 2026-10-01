---
description: Этот урок демонстрирует, как добавить форму, собирающую данные пользователя, в приложение Angular. Этот урок начинается с функционального приложения Angular и показывает, как добавить в него форму
---

# Урок 12: Добавление формы в приложение Angular

Этот урок демонстрирует, как добавить форму, собирающую данные пользователя, в приложение Angular. Этот урок начинается с функционального приложения Angular и показывает, как добавить в него форму.

Данные, которые собирает форма, отправляются только в сервис приложения, который записывает их в консоль браузера. Использование REST API для отправки и получения данных формы в этом уроке не рассматривается.

**Затраты времени:** ожидайте, что на прохождение этого урока вы потратите около 20 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в Уроке 11, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите код из Урока 11, где вы можете:

    -   Использовать [живой пример](https://angular.io/generated/live-examples/first-app-lesson-11/stackblitz.html) в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать [download пример](https://angular.io/generated/zips/first-app-lesson-11/first-app-lesson-11.zip) и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](first-app.md), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-12/stackblitz.html) для этого урока.

## После завершения

-   В вашем приложении есть форма, в которую пользователи могут вводить данные, которые отправляются в сервис вашего приложения.

-   Сервис записывает данные из формы в консоль браузера.

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 — Добавление метода для отправки данных формы

Этот шаг добавляет метод в сервис вашего приложения, который получает данные формы для отправки в место назначения данных. В этом примере метод записывает данные из формы в консольный журнал браузера.

В панели **Edit** вашей IDE:

1.  В `src/app/housing.service.ts`, внутри класса `HousingService`, вставьте этот метод в нижней части определения класса.

    ```ts
    submitApplication(firstName: string, lastName: string, email: string) {
        console.log(
    		`Homes application received: firstName: ${firstName}, lastName: ${lastName}, email: ${email}.`
    	);
    }
    ```

2.  Убедитесь, что приложение собирается без ошибок.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

### Шаг 2 — Добавление функций формы на страницу подробностей

Этот шаг добавляет код на страницу подробностей, который обрабатывает взаимодействие с формой.

В панели **Edit** вашей IDE, в `src/app/details/details.component.ts`:

1.  После оператора `import` в верхней части файла добавьте следующий код для импорта классов форм Angular.

    ```ts
    import {
        FormControl,
        FormGroup,
        ReactiveFormsModule,
    } from '@angular/forms';
    ```

2.  В метаданных декоратора `DetailsComponent` обновите свойство `imports` следующим кодом:

    ```ts
    imports: [
    	CommonModule,
    	ReactiveFormsModule
    ],
    ```

3.  В классе `DetailsComponent`, перед методом `constructor()`, добавьте следующий код для создания объекта формы.

    ```ts
    applyForm = new FormGroup({
        firstName: new FormControl(''),
        lastName: new FormControl(''),
        email: new FormControl(''),
    });
    ```

    В Angular `FormGroup` и `FormControl` — это типы, которые позволяют создавать формы. Тип `FormControl` может предоставлять значение по умолчанию и формировать данные формы. В данном примере `firstName` — это `string`, а значение по умолчанию — пустая строка.

4.  В классе `DetailsComponent` после метода `constructor()` добавьте следующий код для обработки клика **Apply now**.

    ```ts
    submitApplication() {
    	this.housingService.submitApplication(
    		this.applyForm.value.firstName ?? '',
    		this.applyForm.value.lastName ?? '',
    		this.applyForm.value.email ?? ''
    	);
    }
    ```

    Эта кнопка еще не существует — вы добавите ее в следующем шаге. В приведенном выше коде `FormControl` может возвращать `null`. Этот код использует оператор nullish coalescing, чтобы по умолчанию вернуть пустую строку, если значение `null`.

5.  Убедитесь, что приложение собирается без ошибок.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

### Шаг 3 — Добавление разметки формы на страницу подробностей

Этот шаг добавляет разметку на страницу подробностей, на которой отображается форма.

В панели **Edit** вашей IDE, в `src/app/details/details.component.ts`:

1.  В метаданных декоратора `DetailsComponent` обновите HTML `template`, чтобы добавить разметку формы в соответствии со следующим кодом.

    ```ts
    template: `
    <article>
    	<img class="listing-photo" [src]="housingLocation?.photo"
    	alt="Exterior photo of {{housingLocation?.name}}"/>
    	<section class="listing-description">
    	<h2 class="listing-heading">{{housingLocation?.name}}</h2>
    	<p class="listing-location">{{housingLocation?.city}}, {{housingLocation?.state}}</p>
    	</section>
    	<section class="listing-features">
    	<h2 class="section-heading">About this housing location</h2>
    	<ul>
    		<li>Units available: {{housingLocation?.availableUnits}}</li>
    		<li>Does this location have wifi: {{housingLocation?.wifi}}</li>
    		<li>Does this location have laundry: {{housingLocation?.laundry}}</li>
    	</ul>
    	</section>
    	<section class="listing-apply">
    	<h2 class="section-heading">Apply now to live here</h2>
    	<form [formGroup]="applyForm" (submit)="submitApplication()">
    		<label for="first-name">First Name</label>
    		<input id="first-name" type="text" formControlName="firstName">

    		<label for="last-name">Last Name</label>
    		<input id="last-name" type="text" formControlName="lastName">

    		<label for="email">Email</label>
    		<input id="email" type="email" formControlName="email">
    		<button type="submit" class="primary">Apply now</button>
    	</form>
    	</section>
    </article>
    `,
    ```

    Теперь шаблон включает обработчик события `(submit)="submitApplication()"`. Angular использует синтаксис круглых скобок вокруг имени события для создания определяемых событий в коде шаблона. Код справа от знака равенства — это код, который должен быть выполнен при срабатывании этого события. Вы можете привязываться к событиям браузера и пользовательским событиям.

2.  Убедитесь, что приложение создается без ошибок.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

    ![страница с формой для подачи заявки на проживание в этом месте](homes-app-lesson-12-step-3.png)

### Шаг 4 — Проверка новой формы вашего приложения

На этом шаге тестируется новая форма, чтобы убедиться, что при отправке данных формы в приложение данные формы появляются в журнале консоли.

1.  В панели **Terminal** вашей IDE запустите `ng serve`, если он еще не запущен.

2.  В браузере откройте ваше приложение по адресу `http://localhost:4200`.

3.  В приложении щелкните правой кнопкой мыши и в контекстном меню выберите **Inspect**.

4.  В окне инструментов разработчика выберите вкладку **Консоль**.

    Убедитесь, что окно инструментов разработчика видно для следующих шагов

5.  В вашем приложении:

    1.  Выберите местоположение жилья и нажмите **Узнать больше**, чтобы увидеть подробную информацию о доме.

    2.  На странице сведений о доме прокрутите страницу в самый низ, чтобы найти новую форму.

    3.  Введите данные в поля формы — подойдут любые данные.

    4.  Выберите **Применить сейчас**, чтобы отправить данные.

6.  В окне инструментов разработчика просмотрите вывод журнала, чтобы найти данные формы.

## Обзор урока

В этом уроке вы обновили свое приложение, чтобы:

-   добавить форму с помощью функции форм Angular

-   подключить данные, полученные в форме, к форме с помощью обработчика событий.

Если у вас возникли трудности с этим уроком, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-12/stackblitz.html) для него.

## Следующие шаги

-   [Урок 13 — Добавление функции поиска в ваше приложение](first-app-lesson-13.md)

## Дополнительная информация

Для получения дополнительной информации по темам, рассмотренным в этом уроке, посетите:

-   [Angular Forms](forms.md)
-   [Обработка событий](event-binding.md)

## Ссылки

-   [Lesson 12: Adding a form to your Angular app](https://angular.io/tutorial/first-app/first-app-lesson-12)
