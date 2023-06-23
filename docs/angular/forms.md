# Построение формы, управляемой шаблоном

<a id="template-driven"></a>

В этом уроке показано, как создать форму, управляемую шаблоном. Элементы управления в форме связаны со свойствами данных, которые имеют валидацию ввода. Валидация ввода помогает поддерживать целостность данных и стилизацию для улучшения пользовательского опыта.

Формы, основанные на шаблонах, используют [двустороннее связывание данных] (guide/architecture-components#data-binding 'Intro to 2-way data binding') для обновления модели данных в компоненте по мере внесения изменений в шаблон и наоборот.

<div class="alert is-helpful">

Angular поддерживает два подхода к проектированию интерактивных форм. Вы можете создавать формы, используя синтаксис и директивы Angular [template syntax and directives](guide/glossary#template 'Definition of template terms') для написания шаблонов со специфическими для формы директивами.
В этом руководстве описаны директивы и приемы, которые следует использовать при написании шаблонов. Вы также можете использовать реактивный или модельно-ориентированный подход для создания форм.

Формы на основе шаблонов подходят для небольших или простых форм, в то время как реактивные формы более масштабируемы и подходят для сложных форм. Для сравнения этих двух подходов смотрите [Введение в формы](guide/forms-overview 'Обзор форм Angular').

</div>

Вы можете создать практически любую форму с помощью шаблона Angular &mdash; формы входа в систему, контактные формы и практически любые бизнес-формы. Вы можете креативно расположить элементы управления и связать их с данными в вашей объектной модели.
Вы можете задать правила валидации и отображать ошибки валидации, условно разрешать ввод от определенных элементов управления, запускать встроенную визуальную обратную связь и многое другое.

В этом учебном пособии показано, как построить упрощенную форму, подобную форме из учебника [Tour of Heroes](tutorial/tour-of-heroes 'Tour of Heroes'), чтобы проиллюстрировать приемы.

<div class="alert is-helpful">

Запустите или загрузите пример приложения: <live-example></live-example>.

</div>

## Задачи

Этот учебник научит вас делать следующее:

-   Создать форму Angular с помощью компонента и шаблона

-   Использовать `ngModel` для создания двусторонней привязки данных для чтения и записи значений контролов ввода

-   Обеспечить визуальную обратную связь с помощью специальных классов CSS, которые отслеживают состояние элементов управления

-   Отображать ошибки валидации для пользователей и условно разрешать ввод от элементов управления формы в зависимости от состояния формы

-   Обмениваться информацией между элементами HTML с помощью [переменных ссылок шаблона](guide/template-reference-variables)

## Предварительные условия

Прежде чем углубляться в формы, управляемые шаблонами, вы должны иметь базовое представление о следующем.

-   [TypeScript](https://www.typescriptlang.org/ 'The TypeScript language') и программирование на HTML5

-   Основы проектирования приложений Angular, как описано в [Angular Concepts](руководство/архитектура 'Введение в концепции Angular')

-   Основы [синтаксиса шаблонов Angular](guide/template-syntax 'Руководство по синтаксису шаблонов')

-   Концепции дизайна форм, представленные в [Introduction to Forms](guide/forms-overview 'Обзор форм Angular')

<a id="intro"></a>

## Построение формы, управляемой шаблоном

Шаблонно-ориентированные формы полагаются на директивы, определенные в `FormsModule`.

| Directives | Details | | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

| `NgModel` | Согласовывает изменения значений в прикрепленном элементе формы с изменениями в модели данных, позволяя вам реагировать на ввод пользователя с помощью валидации ввода и обработки ошибок. |

| `NgForm` | Создает экземпляр верхнего уровня `FormGroup` и привязывает его к элементу `<form>` для отслеживания агрегированных значений формы и статуса проверки. Как только вы импортируете `FormsModule`, эта директива становится активной по умолчанию для всех тегов `<form>`. Вам не нужно добавлять специальный селектор. |

| `NgModelGroup` | Создает и привязывает экземпляр `FormGroup` к элементу DOM. |

### Пример приложения

Образец формы в этом руководстве используется _Агентством по трудоустройству героев_ для хранения личной информации о героях. Каждому герою нужна работа.

Эта форма помогает агентству найти подходящего героя и подходящий кризис.

<div class="lightbox">

<img alt="Clean Form" src="generated/images/guide/forms/hero-form-1.png">

</div>

Форма отличается некоторыми особенностями дизайна, которые облегчают ее использование. Например, два обязательных поля имеют зеленую полосу слева, чтобы их было легко заметить.
Эти поля имеют начальные значения, поэтому форма действительна и кнопка **Submit** включена.

Работа с этой формой покажет вам:

-   Как включить логику валидации

-   Как настроить представление с помощью стандартного CSS

-   Как обрабатывать условия ошибки для обеспечения корректного ввода

Если пользователь, например, удаляет имя героя, форма становится недействительной. Приложение обнаруживает изменение статуса и отображает ошибку валидации в привлекающем внимание стиле.

Кнопка **Submit** не включается, а полоса "требуется" слева от элемента управления вводом меняется с зеленой на красную.

<div class="lightbox">

<img alt="Invalid, Name Required" src="generated/images/guide/forms/hero-form-2.png">

</div>

### Обзор шагов

В ходе этого урока вы привяжете образец формы к данным и обработаете пользовательский ввод, выполнив следующие шаги.

1.  Создайте базовую форму.

    -   Определите образец модели данных.

    -   Включите необходимую инфраструктуру, такую как `FormsModule`.

1.  Привяжите элементы управления формы к свойствам данных, используя директиву `ngModel` и синтаксис двусторонней привязки данных.

    -   Изучите, как `ngModel` сообщает о состоянии элементов управления с помощью классов CSS

    -   Назовите элементы управления, чтобы сделать их доступными для `ngModel`.

1.  Отслеживание валидности ввода и состояния элемента управления с помощью `ngModel`.

    -   Добавьте пользовательский CSS для визуального отображения состояния.

    -   Показывать и скрывать сообщения об ошибках валидации

1.  Реагируйте на событие нажатия кнопки в HTML, добавляя данные в модель.

1.  Обработка отправки формы с помощью выходного свойства [`ngSubmit`](api/forms/NgForm#properties) формы.

    -   Отключите кнопку **Submit**, пока форма не станет валидной.

    -   После отправки поменяйте готовую форму на другой контент на странице

<a id="step1"></a>

## Постройте форму

Вы можете воссоздать пример приложения из кода, представленного здесь, или изучить или скачать <live-example></live-example>.

1.  The provided sample application creates the `Hero` class which defines the data model reflected in the form.

    <code-example header="src/app/hero.ts" language="typescript" path="forms/src/app/hero.ts"></code-example>

1.  The form layout and details are defined in the `HeroFormComponent` class.

    <code-example header="src/app/hero-form/hero-form.component.ts (v1)" path="forms/src/app/hero-form/hero-form.component.ts" region="v1"></code-example>

    The component's `selector` value of "app-hero-form" means you can drop this form in a parent template using the `<app-hero-form>` tag.

1.  The following code creates a new hero instance, so that the initial form can show an example hero.

    <code-example language="typescript" path="forms/src/app/hero-form/hero-form.component.ts" language="typescript" region="SkyDog"></code-example>

    This demo uses dummy data for `model` and `powers`.
    In a real app, you would inject a data service to get and save real data, or expose these properties as inputs and outputs.

1.  The application enables the Forms feature and registers the created form component.

    <code-example header="src/app/app.module.ts" language="typescript" path="forms/src/app/app.module.ts"></code-example>

1.  The form is displayed in the application layout defined by the root component's template.

    <code-example header="src/app/app.component.html" language="html" path="forms/src/app/app.component.html"></code-example>

    The initial template defines the layout for a form with two form groups and a submit button.
    The form groups correspond to two properties of the Hero data model, name and alterEgo.
    Each group has a label and a box for user input.

    -   The **Name** `<input>` control element has the HTML5 `required` attribute
    -   The **Alter Ego** `<input>` control element does not because `alterEgo` is optional

    The **Submit** button has some classes on it for styling.
    At this point, the form layout is all plain HTML5, with no bindings or directives.

1.  The sample form uses some style classes from [Twitter Bootstrap](https://getbootstrap.com/css): `container`, `form-group`, `form-control`, and `btn`.
    To use these styles, the application's style sheet imports the library.

    <code-example header="src/styles.css" path="forms/src/styles.1.css"></code-example>

1.  The form makes the hero applicant choose one superpower from a fixed list of agency-approved powers.
    The predefined list of `powers` is part of the data model, maintained internally in `HeroFormComponent`.
    The Angular [NgForOf directive](api/common/NgForOf 'API reference') iterates over the data values to populate the `<select>` element.

    <code-example header="src/app/hero-form/hero-form.component.html (powers)" path="forms/src/app/hero-form/hero-form.component.html" region="powers"></code-example>

Если вы запустите приложение прямо сейчас, вы увидите список полномочий в элементе управления выбором. Элементы ввода еще не привязаны к значениям данных или событиям, поэтому они все еще пустые и не имеют никакого поведения.

<div class="lightbox">

<img alt="Early form with no binding" src="generated/images/guide/forms/hero-form-3.png">

</div>

<a id="ngModel"></a>

## Bind input controls to data properties

The next step is to bind the input controls to the corresponding `Hero` properties with two-way data binding, so that they respond to user input by updating the data model, and also respond to programmatic changes in the data by updating the display.

The `ngModel` directive declared in the `FormsModule` lets you bind controls in your template-driven form to properties in your data model. When you include the directive using the syntax for two-way data binding, `[(ngModel)]`, Angular can track the value and user interaction of the control and keep the view synced with the model.

1.  Edit the template file `hero-form.component.html`.

1.  Find the `<input>` tag next to the **Name** label.

1.  Add the `ngModel` directive, using two-way data binding syntax `[(ngModel)]="..."`.

<code-example header="src/app/hero-form/hero-form.component.html (excerpt)" path="forms/src/app/hero-form/hero-form.component.html" region="ngModelName-1"></code-example>.

<div class="alert is-helpful">

В этом примере после каждого входного тега `{{model.name}}' имеется временная диагностическая интерполяция, показывающая текущее значение данных соответствующего свойства. Комментарий напоминает вам о необходимости удалить диагностические строки, когда вы закончите наблюдать за работой двусторонней привязки данных.

</div>

<a id="ngForm"></a>

### Доступ к общему состоянию формы

Когда вы импортировали `FormsModule` в свой компонент, Angular автоматически создал и присоединил директиву [NgForm](api/forms/NgForm 'API reference for NgForm') к тегу `<form>` в шаблоне (поскольку `NgForm` имеет селектор `form`, который соответствует элементам `<form>`).

Чтобы получить доступ к `NgForm` и общему состоянию формы, объявите переменную [template reference variable](guide/template-reference-variables).

1.  Отредактируйте файл шаблона `hero-form.component.html`.

1.  Обновите тег `<form>` с переменной ссылки шаблона, `#heroForm`, и установите ее значение следующим образом.

    <code-example header="src/app/hero-form/hero-form.component.html (excerpt)" path="forms/src/app/hero-form/hero-form.component.html" region="template-variable"></code-example>.

    Переменная шаблона `heroForm` теперь является ссылкой на экземпляр директивы `NgForm`, которая управляет формой в целом.

1.  Запустите приложение.

1.  Начните вводить текст в поле ввода **Имя**.

    По мере добавления и удаления символов вы можете видеть, как они появляются и исчезают из модели данных.

    Например:

    <div class="lightbox">

    <img alt="ngModel in action" src="generated/images/guide/forms/ng-model-in-action.png">

    </div>

The diagnostic line that shows interpolated values demonstrates that values are really flowing from the input box to the model and back again.

### Naming control elements

When you use `[(ngModel)]` on an element, you must define a `name` attribute for that element. Angular uses the assigned name to register the element with the `NgForm` directive attached to the parent `<form>` element.

The example added a `name` attribute to the `<input>` element and set it to "name", which makes sense for the hero's name.

Any unique value will do, but using a descriptive name is helpful.

1.  Add similar `[(ngModel)]` bindings and `name` attributes to **Alter Ego** and **Hero Power**.
1.  You can now remove the diagnostic messages that show interpolated values.

1.  To confirm that two-way data binding works for the entire hero model, add a new text binding with the [`json`](api/common/JsonPipe) pipe at the top to the component's template, which serializes the data to a string.

    After these revisions, the form template should look like the following:

    <code-example header="src/app/hero-form/hero-form.component.html (excerpt)" path="forms/src/app/hero-form/hero-form.component.html" region="ngModel-2"></code-example>

    -   Notice that each `<input>` element has an `id` property.

        This is used by the `<label>` element's `for` attribute to match the label to its input control.

        This is a [standard HTML feature](https://developer.mozilla.org/docs/Web/HTML/Element/label).

    -   Each `<input>` element also has the required `name` property that Angular uses to register the control with the form.

    If you run the application now and change every hero model property, the form might display like this:

    <div class="lightbox">

    <img alt="ngModel in action" src="generated/images/guide/forms/ng-model-in-action-2.png">

    </div>

    Диагностика в верхней части формы подтверждает, что все ваши изменения отражены в модели.

1.  Когда вы наблюдаете эффект, вы можете удалить текстовую привязку `{{ model | json }}''.

## Отслеживание состояний формы

Angular применяет класс `ng-submitted` к элементам `form` после того, как форма была отправлена. Этот класс можно использовать для изменения стиля формы после ее отправки.

## Отслеживание состояний элементов управления

Добавление директивы `NgModel` к элементу управления добавляет к нему имена классов, которые описывают его состояние. Эти классы можно использовать для изменения стиля элемента управления в зависимости от его состояния.

The following table describes the class names that Angular applies based on the control's state.

| States | Class if true | Class if false | | :------------------------------- | :------------ | :------------- |

| The control has been visited. | `ng-touched` | `ng-untouched` |

| The control's value has changed. | `ng-dirty` | `ng-pristine` |

| The control's value is valid. | `ng-valid` | `ng-invalid` |

Angular also applies the `ng-submitted` class to `form` elements upon submission, but not to the controls inside the `form` element.

You use these CSS classes to define the styles for your control based on its status.

### Observe control states

To see how the classes are added and removed by the framework, open the browser's developer tools and inspect the `<input>` element that represents the hero name.

1.  Using your browser's developer tools, find the `<input>` element that corresponds to the **Name** input box.
    You can see that the element has multiple CSS classes in addition to "form-control".

1.  When you first bring it up, the classes indicate that it has a valid value, that the value has not been changed since initialization or reset, and that the control has not been visited since initialization or reset.

    <code-example format="html" language="html">

    &lt;input &hellip; class="form-control ng-untouched ng-pristine ng-valid" &hellip;&gt;

    </code-example>

1.  Take the following actions on the **Name** `<input>` box, and observe which classes appear.

    -   Look but don't touch.

        The classes indicate that it is untouched, pristine, and valid.

    -   Click inside the name box, then click outside it.

        The control has now been visited, and the element has the `ng-touched` class instead of the `ng-untouched` class.

    -   Add slashes to the end of the name.

        It is now touched and dirty.

    -   Erase the name.

        This makes the value invalid, so the `ng-invalid` class replaces the `ng-valid` class.

### Создание визуальной обратной связи для состояний

Пара `ng-valid`/`ng-invalid` особенно интересна, потому что вы хотите посылать сильный визуальный сигнал, когда значения недействительны.

Вы также хотите пометить обязательные поля.

Вы можете отмечать обязательные поля и недействительные данные одновременно с помощью цветной полосы слева от поля ввода:

<div class="lightbox">

<img alt="Invalid Form" src="generated/images/guide/forms/validity-required-indicator.png">

</div>

Чтобы изменить внешний вид таким образом, выполните следующие действия.

1.  Добавьте определения для классов CSS `ng-*`.

1.  Добавьте определения этих классов в новый файл `forms.css`.

1.  Добавьте новый файл в проект как дочерний к `index.html`:

    <code-example header="src/assets/forms.css" language="css" path="forms/src/assets/forms.css"></code-example>.

1.  В файле `index.html` обновите тег `<head>`, чтобы включить новую таблицу стилей.

    <code-example header="src/index.html (styles)" path="forms/src/index.html" region="styles"></code-example>.

### Показывать и скрывать сообщения об ошибках валидации

Поле ввода **Имя** является обязательным, и его очистка делает полосу красной. Это указывает на то, что что-то не так, но пользователь не знает, что именно и что с этим делать.

Вы можете предоставить полезное сообщение, проверяя состояние элемента управления и реагируя на него.

Когда пользователь удаляет имя, форма должна выглядеть следующим образом:

<div class="lightbox">

<img alt="Name required" src="generated/images/guide/forms/name-required-error.png">

</div>

The **Hero Power** select box is also required, but it doesn't need this kind of error handling because the selection box already constrains the selection to valid values.

To define and show an error message when appropriate, take the following steps.

1.  Extend the `<input>` tag with a template reference variable that you can use to access the input box's Angular control from within the template.

    In the example, the variable is `#name="ngModel"`.

    <div class="alert is-helpful">

    The template reference variable \(`#name`\) is set to `"ngModel"` because that is the value of the [`NgModel.exportAs`](api/core/Directive#exportAs) property.

    This property tells Angular how to link a reference variable to a directive.

    </div>

1.  Add a `<div>` that contains a suitable error message.

1.  Show or hide the error message by binding properties of the `name` control to the message `<div>` element's `hidden` property.

    <code-example header="src/app/hero-form/hero-form.component.html (hidden-error-msg)" path="forms/src/app/hero-form/hero-form.component.html" region="hidden-error-msg"></code-example>

1.  Add a conditional error message to the `name` input box, as in the following example.

    <code-example header="src/app/hero-form/hero-form.component.html (excerpt)" path="forms/src/app/hero-form/hero-form.component.html" region="name-with-error-msg"></code-example>.

<div class="callout is-helpful">

<header>Illustrating the "pristine" state</header>

В этом примере вы скрываете сообщение, когда элемент управления либо действителен, либо _чист_. Первозданное состояние означает, что пользователь не изменял значение с тех пор, как оно было отображено в этой форме.
Если игнорировать состояние `pristine`, то сообщение будет скрыто только тогда, когда значение действительно.

Если вы зайдете в этот компонент с новым, пустым героем или недействительным героем, вы увидите сообщение об ошибке сразу же, еще ничего не сделав.

Возможно, вы захотите, чтобы сообщение отображалось только тогда, когда пользователь внесет недопустимое изменение. Скрытие сообщения, пока элемент управления находится в `чистом` состоянии, достигает этой цели.

Вы увидите значение этого выбора, когда добавите нового героя в форму на следующем шаге.

</div>

## Add a new hero

This exercise shows how you can respond to a native HTML button-click event by adding to the model data. To let form users add a new hero, you will add a **New Hero** button that responds to a click event.

1.  In the template, place a "New Hero" `<button>` element at the bottom of the form.

1.  In the component file, add the hero-creation method to the hero data model.

    <code-example header="src/app/hero-form/hero-form.component.ts (New Hero method)" path="forms/src/app/hero-form/hero-form.component.ts" region="new-hero"></code-example>

1.  Bind the button's click event to a hero-creation method, `newHero()`.

    <code-example header="src/app/hero-form/hero-form.component.html (New Hero button)" path="forms/src/app/hero-form/hero-form.component.html" region="new-hero-button-no-reset"></code-example>

1.  Run the application again and click the **New Hero** button.

    The form clears, and the _required_ bars to the left of the input box are red, indicating invalid `name` and `power` properties.

    Notice that the error messages are hidden.

    This is because the form is pristine; you haven't changed anything yet.

1.  Введите имя и снова нажмите **Новый герой**.

    Теперь приложение отображает сообщение об ошибке `Name is required`, поскольку поле ввода больше не является нетронутым.

    Форма помнит, что вы ввели имя перед тем, как нажать **Новый герой**.

1.  Чтобы восстановить первозданное состояние элементов управления формы, императивно очистите все флаги, вызвав метод формы `reset()` после вызова метода `newHero()`.

    <code-example header="src/app/hero-form/hero-form.component.html (Сброс формы)" path="forms/src/app/hero-form/hero-form.component.html" region="new-hero-button-form-reset"></code-example>.

    Теперь нажатие **New Hero** сбрасывает и форму, и ее флаги управления.

<div class="alert is-helpful">

См. руководство [User Input](guide/user-input) для получения дополнительной информации о прослушивании событий DOM с привязкой к событию и обновлении соответствующего свойства компонента.

</div>

## Отправьте форму с помощью `ngSubmit`.

Пользователь должен иметь возможность отправить форму после ее заполнения. Кнопка **Submit** в нижней части формы сама по себе ничего не делает, но она вызывает событие отправки формы из-за своего типа \(`type="submit"`\).

Чтобы отреагировать на это событие, выполните следующие действия.

1.  Привяжите свойство события формы [`ngSubmit`](api/forms/NgForm#properties) к методу `onSubmit()` компонента hero-form.

    <code-example header="src/app/hero-form/hero-form.component.html (ngSubmit)" path="forms/src/app/hero-form/hero-form.component.html" region="ngSubmit"></code-example>.

1.  Используйте переменную ссылки шаблона `#heroForm` для доступа к форме, содержащей кнопку **Submit**, и создайте привязку события.

    Вы свяжете свойство формы, указывающее на ее общую валидность, со свойством `disabled` кнопки **Submit**.

    <code-example header="src/app/hero-form/hero-form.component.html (submit-button)" path="forms/src/app/hero-form/hero-form.component.html" region="submit-button"></code-example>.

1.  Запустите приложение.

    Обратите внимание, что кнопка включена &mdash; хотя она пока не делает ничего полезного.

1.  Удалите значение **Name**.

    Это нарушает правило "required", поэтому выводится сообщение об ошибке &mdash; и обратите внимание, что это также отключает кнопку **Submit**.

    Вам не нужно было явно связывать включенное состояние кнопки с действительностью формы.

    Модуль `FormsModule` сделал это автоматически, когда вы определили переменную ссылки шаблона на расширенный элемент формы, а затем сослались на эту переменную в элементе управления кнопкой.

### Ответ на отправку формы

Чтобы показать ответ на отправку формы, вы можете скрыть область ввода данных и отобразить на ее месте что-то другое.

1.  Wrap the entire form in a `<div>` and bind its `hidden` property to the `HeroFormComponent.submitted` property.

    <code-example header="src/app/hero-form/hero-form.component.html (excerpt)" path="forms/src/app/hero-form/hero-form.component.html" region="edit-div"></code-example>

    -   The main form is visible from the start because the `submitted` property is false until you submit the form, as this fragment from the `HeroFormComponent` shows:

        <code-example header="src/app/hero-form/hero-form.component.ts (submitted)" path="forms/src/app/hero-form/hero-form.component.ts" region="submitted"></code-example>

    -   When you click the **Submit** button, the `submitted` flag becomes true and the form disappears.

1.  To show something else while the form is in the submitted state, add the following HTML below the new `<div>` wrapper.

    <code-example header="src/app/hero-form/hero-form.component.html (excerpt)" path="forms/src/app/hero-form/hero-form.component.html" region="submitted"></code-example>

    This `<div>`, which shows a read-only hero with interpolation bindings, appears only while the component is in the submitted state.

    The alternative display includes an _Edit_ button whose click event is bound to an expression that clears the `submitted` flag.

1.  Нажмите кнопку _Редактировать_, чтобы переключить отображение обратно в редактируемую форму.

## Резюме

Форма Angular, рассмотренная на этой странице, использует следующие возможности фреймворка для обеспечения поддержки модификации данных, валидации и многого другого.

-   Шаблон формы Angular HTML
-   Класс компонента формы с декоратором `@Component`.

-   Обработка отправки формы путем привязки к свойству события `NgForm.ngSubmit`.

-   Переменные, связанные с шаблоном, такие как `#heroForm` и `#name`.

-   Синтаксис `[(ngModel)]` для двустороннего связывания данных

-   Использование атрибутов `name` для валидации и отслеживания изменений элементов формы

-   Свойство переменной ссылки `valid` для элементов управления вводом указывает, является ли элемент управления действительным или должен показывать сообщения об ошибках

-   Управление включенным состоянием кнопки **Submit** путем привязки к валидности `NgForm`.

-   Пользовательские CSS классы, которые обеспечивают визуальную обратную связь для пользователей о недействительных элементах управления.

Вот код для финальной версии приложения:

<code-tabs>
     <code-pane header="hero-form/hero-form.component.ts" path="forms/src/app/hero-form/hero-form.component.ts" region="final"></code-pane>
    <code-pane header="hero-form/hero-form.component.html" path="forms/src/app/hero-form/hero-form.component.html" region="final"></code-pane>
    <code-pane header="hero.ts" path="forms/src/app/hero.ts"></code-pane>
    <code-pane header="app.module.ts" path="forms/src/app/app.module.ts"></code-pane>
    <code-pane header="app.component.html" path="forms/src/app/app.component.html"></code-pane>
    <code-pane header="app.component.ts" path="forms/src/app/app.component.ts"></code-pane>
    <code-pane header="main.ts" path="forms/src/main.ts"></code-pane>
    <code-pane header="forms.css" path="forms/src/assets/forms.css"></code-pane>
</code-tabs>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
