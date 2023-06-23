# Построение динамических форм

Многие формы, например, анкеты, могут быть очень похожи друг на друга по формату и замыслу. Чтобы быстрее и проще генерировать различные версии таких форм, можно создать _динамический шаблон формы_ на основе метаданных, описывающих модель бизнес-объектов.

Затем использовать шаблон для автоматической генерации новых форм в соответствии с изменениями в модели данных.

Эта техника особенно полезна, когда у вас есть тип формы, содержание которой должно часто меняться, чтобы соответствовать быстро меняющимся требованиям бизнеса и нормативных актов. Типичным примером является анкета.

Вам может понадобиться получить данные от пользователей в различных контекстах.

Формат и стиль форм, которые видит пользователь, должны оставаться постоянными, в то время как фактические вопросы, которые необходимо задать, зависят от контекста.

В этом уроке вы создадите динамическую форму, представляющую собой базовую анкету. Вы создаете онлайн-приложение для героев, ищущих работу.

Агентство постоянно вносит изменения в процесс заполнения анкеты, но с помощью динамической формы

вы можете создавать новые формы "на лету", не изменяя код приложения.

Учебное пособие проведет вас через следующие шаги.

1.  Включите реактивные формы для проекта.

1.  Создайте модель данных для представления элементов управления формы.

1.  Наполните модель данными образца.

1.  Разработайте компонент для динамического создания элементов управления формы.

Созданная вами форма использует валидацию ввода и стилизацию для улучшения пользовательского опыта. В ней есть кнопка "Отправить", которая активируется только в том случае, если все введенные пользователем данные достоверны, а недопустимые данные отмечаются цветовой маркировкой и сообщениями об ошибках.

Базовая версия может развиваться, чтобы поддерживать более богатое разнообразие вопросов, более изящный рендеринг и улучшать пользовательский опыт.

<div class="alert is-helpful">

См. <live-example name="dynamic-form"></live-example>.

</div>

## Предварительные условия

Перед выполнением этого руководства вы должны иметь базовое представление о следующем.

-   [TypeScript](https://www.typescriptlang.org/ 'Язык TypeScript') и программирование на HTML5

-   Фундаментальные концепции [Angular app design](руководство/архитектура 'Введение в концепции Angular app-design')

-   Базовые знания [реактивных форм](guide/reactive-forms 'Руководство по реактивным формам')

## Включите реактивные формы для вашего проекта

Динамические формы основаны на реактивных формах. Чтобы предоставить приложению доступ к директивам реактивных форм, [корневой модуль](guide/bootstrapping 'Learn about bootstrapping an app from the root module.') импортирует `ReactiveFormsModule` из библиотеки `@angular/forms`.

Следующий код из примера показывает настройку в корневом модуле.

<code-tabs>
     <code-pane header="app.module.ts" path="dynamic-form/src/app/app.module.ts"></code-pane>
    <code-pane header="main.ts" path="dynamic-form/src/main.ts"></code-pane>
</code-tabs>

<a id="object-model"></a>

## Создание объектной модели формы

Динамическая форма требует объектной модели, которая может описать все сценарии, необходимые для функциональности формы. Пример формы hero-application представляет собой набор вопросов &mdash; то есть каждый элемент управления в форме должен задавать вопрос и принимать ответ.

Модель данных для этого типа формы должна представлять вопрос. Пример включает `DynamicFormQuestionComponent`, который определяет вопрос как основной объект в модели.

Следующий `QuestionBase` является базовым классом для набора элементов управления, которые могут представлять вопрос и ответ на него в форме.

<code-example header="src/app/question-base.ts" path="dynamic-form/src/app/question-base.ts"></code-example>.

### Определите классы управления

Из этой базы пример выводит два новых класса, `TextboxQuestion` и `DropdownQuestion`, которые представляют различные типы элементов управления. Когда вы создаете шаблон формы на следующем этапе, вы инстанцируете эти конкретные типы вопросов, чтобы динамически отобразить соответствующие элементы управления.

| Control type | Details | | :------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TextboxQuestion` control type | Presents a question and lets users enter input. <code-example header="src/app/question-textbox.ts" path="dynamic-form/src/app/question-textbox.ts"></code-example> The `TextboxQuestion` control type is represented in a form template using an `<input>` element. The `type` attribute of the element is defined based on the `type` field specified in the `options` argument \(for example `text`, `email`, `url`\). |

| `DropdownQuestion` control type | Presents a list of choices in a select box. <code-example header="src/app/question-dropdown.ts" path="dynamic-form/src/app/question-dropdown.ts"></code-example> |

### Compose form groups

Динамическая форма использует сервис для создания сгруппированных наборов элементов управления вводом на основе модели формы. Следующий `QuestionControlService` собирает набор экземпляров `FormGroup`, которые потребляют метаданные из модели вопроса.
Вы можете указать значения по умолчанию и правила проверки.

<code-example header="src/app/question-control.service.ts" path="dynamic-form/src/app/question-control.service.ts"></code-example>

<a id="form-component"></a>

## Составление содержимого динамической формы

Сама динамическая форма представлена компонентом-контейнером, который вы добавите на следующем этапе. Каждый вопрос представлен в шаблоне компонента формы тегом `<app-question>`, который соответствует экземпляру `DynamicFormQuestionComponent`.

Компонент `DynamicFormQuestionComponent` отвечает за отображение деталей отдельного вопроса на основе значений в связанном с данными объекте вопроса. Форма полагается на директиву [`[formGroup]`] (api/forms/FormGroupDirective 'API reference') для соединения HTML шаблона с базовыми объектами управления.

Компонент `DynamicFormQuestionComponent` создает группы форм и заполняет их элементами управления, определенными в модели вопроса, задавая правила отображения и проверки.

<code-tabs>
     <code-pane header="dynamic-form-question.component.html" path="dynamic-form/src/app/dynamic-form-question.component.html"></code-pane>
    <code-pane header="dynamic-form-question.component.ts" path="dynamic-form/src/app/dynamic-form-question.component.ts"></code-pane>
</code-tabs>

Цель `DynamicFormQuestionComponent` - представить типы вопросов, определенные в вашей модели. На данный момент у вас есть только два типа вопросов, но вы можете придумать гораздо больше.
Оператор `ngSwitch` в шаблоне определяет, какой тип вопроса отображать.

Переключатель использует директивы с селекторами [`formControlName`](api/forms/FormControlName 'FormControlName directive API reference') и [`formGroup`](api/forms/FormGroupDirective 'FormGroupDirective API reference').

Обе директивы определены в `ReactiveFormsModule`.

<a id="questionnaire-data"></a>

### Предоставление данных

Еще один сервис необходим для предоставления определенного набора вопросов, из которых можно построить индивидуальную форму. В этом упражнении вы создадите `QuestionService`, который будет предоставлять массив вопросов из жестко закодированных данных образца.

В реальном приложении сервис может получать данные из внутренней системы.

Ключевым моментом, однако, является то, что вы полностью контролируете вопросы героя анкеты через объекты, возвращаемые из `QuestionService`.

Чтобы поддерживать анкету по мере изменения требований, вам нужно только добавлять, обновлять и удалять объекты из массива `questions`.

Сервис `QuestionService` предоставляет набор вопросов в виде массива, связанного с `@Input()` вопросами.

<code-example header="src/app/question.service.ts" path="dynamic-form/src/app/question.service.ts"></code-example>

<a id="dynamic-template"></a>

## Создание шаблона динамической формы

Компонент `DynamicFormComponent` является точкой входа и основным контейнером для формы, которая представлена с помощью `<app-dynamic-form>` в шаблоне.

Компонент `DynamicFormComponent` представляет список вопросов, связывая каждый из них с элементом `<app-question>`, который соответствует `DynamicFormQuestionComponent`.

<code-tabs>
     <code-pane header="dynamic-form.component.html" path="dynamic-form/src/app/dynamic-form.component.html"></code-pane>
    <code-pane header="dynamic-form.component.ts" path="dynamic-form/src/app/dynamic-form.component.ts"></code-pane>
</code-tabs>

### Отображение формы

Для отображения экземпляра динамической формы шаблон оболочки `AppComponent` передает массив `questions`, возвращаемый `QuestionService`, компоненту-контейнеру формы, `<app-dynamic-form>`.

<code-example header="app.component.ts" path="dynamic-form/src/app/app.component.ts"></code-example>.

Пример предоставляет модель приложения для работы с героями, но в нем нет ссылок на какой-либо конкретный вопрос героя, кроме объектов, возвращаемых `QuestionService`. Такое разделение модели и данных позволяет вам перепрофилировать компоненты для любого типа опросов, если они совместимы с объектной моделью _question_.

### Обеспечение достоверности данных

Шаблон формы использует динамическое связывание метаданных для отображения формы, не делая никаких жестких предположений о конкретных вопросах. Он добавляет метаданные элементов управления и критерии проверки динамически.

Для обеспечения корректного ввода данных кнопка _Сохранить_ отключена до тех пор, пока форма не перейдет в корректное состояние. Когда форма становится валидной, нажмите кнопку _Сохранить_, и приложение отобразит текущие значения формы в виде JSON.

На следующем рисунке показана окончательная форма.

<div class="lightbox">

<img alt="Dynamic-Form" src="generated/images/guide/dynamic-form/dynamic-form.png">

</div>

## Следующие шаги

| Steps                                           | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| :---------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Different types of forms and control collection | This tutorial shows how to build a questionnaire, which is just one kind of dynamic form. The example uses `FormGroup` to collect a set of controls. For an example of a different type of dynamic form, see the section [Creating dynamic forms](guide/reactive-forms#creating-dynamic-forms 'Create dynamic forms with arrays') in the Reactive Forms guide. That example also shows how to use `FormArray` instead of `FormGroup` to collect a set of controls. |
| Validating user input                           | The section [Validating form input](guide/reactive-forms#validating-form-input 'Basic input validation') introduces the basics of how input validation works in reactive forms. <br /> The [Form validation guide](guide/form-validation 'Form validation guide') covers the topic in more depth.                                                                                                                                                                  |

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
