# Реактивные формы

Реактивные формы обеспечивают модельно-ориентированный подход к обработке входов формы, значения которых меняются с течением времени. В этом руководстве показано, как создать и обновить базовый элемент управления формы, перейти к использованию нескольких элементов управления в группе, проверять значения формы и создавать динамические формы, в которых можно добавлять или удалять элементы управления во время выполнения.

<div class="alert is-helpful">

Попробуйте этот <live-example name="reactive-forms" title="Reactive Forms in Stackblitz">Reactive Forms live-example</live-example>.

</div>

## Предварительные условия

Прежде чем углубляться в реактивные формы, вы должны иметь базовое представление о следующем:

-   [TypeScript](https://www.typescriptlang.org/ 'Язык TypeScript') программирование

-   основы дизайна приложений Angular, описанные в [Angular Concepts](руководство/архитектура 'Введение в концепции Angular')

-   концепции дизайна форм, представленные в [Introduction to Forms](guide/forms-overview 'Обзор форм Angular')

<a id="intro"></a>

## Обзор реактивных форм

Реактивные формы используют явный и неизменяемый подход к управлению состоянием формы в определенный момент времени. Каждое изменение состояния формы возвращает новое состояние, что сохраняет целостность модели между изменениями.

Реактивные формы построены на потоках [observable](guide/glossary#observable 'Observable definition'), где входы и значения формы предоставляются в виде потоков входных значений, к которым можно получить синхронный доступ.

Реактивные формы также обеспечивают прямой путь к тестированию, поскольку вы уверены, что ваши данные последовательны и предсказуемы при запросе. Любые потребители потоков имеют доступ для безопасного манипулирования этими данными.

Реактивные формы отличаются от [template-driven forms](guide/forms 'Template-driven forms guide') различными способами. Реактивные формы обеспечивают синхронный доступ к модели данных, неизменяемость с помощью наблюдаемых операторов и отслеживание изменений с помощью наблюдаемых потоков.

Формы, управляемые шаблонами, позволяют напрямую изменять данные в вашем шаблоне, но они менее явные, чем реактивные формы, поскольку полагаются на директивы, встроенные в шаблон, а также на изменяемые данные для асинхронного отслеживания изменений. Подробное сравнение двух парадигм см. в [Forms Overview](guide/forms-overview 'Overview of Angular forms').

## Добавление базового элемента управления формой

Использование элементов управления формами состоит из трех этапов.

1.  Зарегистрируйте модуль reactive forms в вашем приложении.

    Этот модуль объявляет директивы reactive-form, которые необходимы для использования реактивных форм.

1.  Создайте новый компонент и инстанцируйте новый `FormControl`.

1.  Зарегистрируйте `FormControl` в шаблоне.

Затем вы можете отобразить форму, добавив компонент в шаблон.

В следующих примерах показано, как добавить один элемент управления формой. В примере пользователь вводит свое имя в поле ввода, фиксируется значение ввода и отображается текущее значение элемента управления формой.

| Action | Details | | :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Register the reactive forms module | To use reactive form controls, import `ReactiveFormsModule` from the `@angular/forms` package and add it to your NgModule's `imports` array. <code-example header="src/app/app.module.ts (excerpt)" path="reactive-forms/src/app/app.module.ts" region="imports"></code-example> |
| Generate a new `FormControl` | Use the [CLI command](cli/generate#component-command 'Using the Angular command-line interface') `ng generate` to generate a component in your project to host the control. <code-example header="src/app/name-editor/name-editor.component.ts" path="reactive-forms/src/app/name-editor/name-editor.component.ts" region="create-control"></code-example> Use the constructor of `FormControl` to set its initial value, which in this case is an empty string. By creating these controls in your component class, you get immediate access to listen for, update, and validate the state of the form input. |
| Register the control in the template | After you create the control in the component class, you must associate it with a form control element in the template. Update the template with the form control using the `formControl` binding provided by `FormControlDirective`, which is also included in the `ReactiveFormsModule`. <code-example header="src/app/name-editor/name-editor.component.html" path="reactive-forms/src/app/name-editor/name-editor.component.html" region="control-binding"></code-example> <div class="alert is-helpful"> <ul> <li> For a summary of the classes and directives provided by `ReactiveFormsModule`, see the following [Reactive forms API](#reactive-forms-api 'API summary') section </li> <li> For complete syntax details of these classes and directives, see the API reference documentation for the [Forms package](api/forms 'API reference') </li> </ul> </div> Using the template binding syntax, the form control is now registered to the `name` input element in the template. The form control and DOM element communicate with each other: the view reflects changes in the model, and the model reflects changes in the view. |
| Display the component | The `FormControl` assigned to the `name` property is displayed when the property's host component is added to a template. <code-example header="src/app/app.component.html (name editor)" path="reactive-forms/src/app/app.component.1.html" region="app-name-editor"></code-example> <div class="lightbox"> <img alt="Name Editor, which has a name label and an input so the user can enter a name" src="generated/images/guide/reactive-forms/name-editor-1.png"> </div> |

<a id="display-value"></a>

### Отображение значения элемента управления формы

Вы можете отобразить значение следующими способами.

-   Через наблюдаемую `valueChanges`, где вы можете прослушивать изменения значения формы в шаблоне с помощью `AsyncPipe` или в классе компонента с помощью метода `subscribe()`.

-   с помощью свойства `value`, которое дает вам снимок текущего значения.

В следующем примере показано, как отобразить текущее значение с помощью интерполяции в шаблоне.

<code-example header="src/app/name-editor/name-editor.component.html (значение элемента управления)" path="reactive-forms/src/app/name-editor/name-editor.component.html" region="display-value"></code-example>.

Отображаемое значение изменяется при обновлении элемента управления формы.

Реактивные формы предоставляют доступ к информации о данном элементе управления через свойства и методы, предоставляемые каждому экземпляру. Эти свойства и методы базового класса [AbstractControl](api/forms/AbstractControl 'Ссылка на API') используются для управления состоянием формы и определения времени отображения сообщений при обработке [валидации ввода](#basic-form-validation 'Подробнее о валидации ввода формы').

О других свойствах и методах `FormControl` читайте в [API Reference](api/forms/FormControl 'Подробный синтаксический справочник').

### Замена значения элемента управления формы

Реактивные формы имеют методы для изменения значения элемента управления программно, что дает вам гибкость для обновления значения без участия пользователя. Экземпляр элемента управления формы предоставляет метод `setValue()`, который обновляет значение элемента управления формы и проверяет структуру предоставленного значения на соответствие структуре элемента управления.

Например, при получении данных формы из внутреннего API или сервиса, используйте метод `setValue()` для обновления элемента управления до нового значения, полностью заменяя старое значение.

Следующий пример добавляет метод в класс компонента для обновления значения элемента управления до _Nancy_ с помощью метода `setValue()`.

<code-example header="src/app/name-editor/name-editor.component.ts (update value)" path="reactive-forms/src/app/name-editor/name-editor.component.ts" region="update-value"></code-example>.

Обновление шаблона с помощью кнопки для имитации обновления имени. Когда вы нажимаете кнопку **Update Name**, значение, введенное в элемент управления формы, отражается как его текущее значение.

<code-example header="src/app/name-editor/name-editor.component.html (update value)" path="reactive-forms/src/app/name-editor/name-editor.component.html" region="update-value"></code-example>.

Модель формы является источником истины для элемента управления, поэтому, когда вы нажимаете на кнопку, значение ввода изменяется в классе компонента, переопределяя его текущее значение.

<div class="lightbox">

<img alt="Name Editor Update with a name label, the name Nancy in the input, text specifying that the value of the input is Nancy and an Update Name button" src="generated/images/guide/reactive-forms/name-editor-2.gif">

</div>

<div class="alert is-helpful">

**NOTE**: <br /> In this example, you're using a single control.
When using the `setValue()` method with a [form group](#grouping-form-controls 'Learn more about form groups') or [form array](#creating-dynamic-forms 'Learn more about dynamic forms') instance, the value needs to match the structure of the group or array.

</div>

## Группировка элементов управления формы

Формы обычно содержат несколько связанных элементов управления. Реактивные формы предоставляют два способа группировки нескольких связанных элементов управления в одну форму ввода.

| Группы форм | Подробности | | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | |

| Группа форм | Определяет форму с фиксированным набором элементов управления, которыми можно управлять совместно. В этом разделе рассматриваются основы работы с группами форм. Вы также можете [вложить группы форм](#nested-groups 'Подробнее о вложении групп') для создания более сложных форм. |

| Массив форм | Определяет динамическую форму, в которую можно добавлять и удалять элементы управления во время выполнения. Вы также можете вложить массивы форм для создания более сложных форм. Подробнее об этой опции см. в [Создание динамических форм](#dynamic-forms 'Подробнее о массивах форм'). |

Подобно тому, как экземпляр элемента управления формы дает вам контроль над одним полем ввода, экземпляр группы форм отслеживает состояние формы группы экземпляров элементов управления формы\(например, формы\). Каждый элемент управления в экземпляре группы форм отслеживается по имени при создании группы форм.

В следующем примере показано, как управлять несколькими экземплярами элементов управления формы в одной группе.

Создайте компонент `ProfileEditor` и импортируйте классы `FormGroup` и `FormControl` из пакета `@angular/forms`.

<code-example format="shell" language="shell">

ng generate component ProfileEditor

</code-example>

<code-example header="src/app/profile-editor/profile-editor.component.ts (imports)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="imports"></code-example>.

Чтобы добавить группу форм в этот компонент, выполните следующие действия.

1.  Создайте экземпляр `FormGroup`.

1.  Ассоциируйте модель `FormGroup` и представление.

1.  Сохраните данные формы.

| Action | Details | | :--------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create a `FormGroup` instance | Create a property in the component class named `profileForm` and set the property to a new form group instance. To initialize the form group, provide the constructor with an object of named keys mapped to their control. <br /> For the profile form, add two form control instances with the names `firstName` and `lastName`. <code-example header="src/app/profile-editor/profile-editor.component.ts (form group)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="formgroup"></code-example> The individual form controls are now collected within a group. A `FormGroup` instance provides its model value as an object reduced from the values of each control in the group. A form group instance has the same properties \(such as `value` and `untouched`\) and methods \(such as `setValue()`\) as a form control instance. |
| Associate the `FormGroup` model and view | A form group tracks the status and changes for each of its controls, so if one of the controls changes, the parent control also emits a new status or value change. The model for the group is maintained from its members. After you define the model, you must update the template to reflect the model in the view. <code-example header="src/app/profile-editor/profile-editor.component.html (template form group)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.html" region="formgroup"></code-example> <div class="alert is-helpful"> **NOTE**: <br /> Just as a form group contains a group of controls, the _profileForm_ `FormGroup` is bound to the `form` element with the `FormGroup` directive, creating a communication layer between the model and the form containing the inputs. </div> The `formControlName` input provided by the `FormControlName` directive binds each individual input to the form control defined in `FormGroup`. The form controls communicate with their respective elements. They also communicate changes to the form group instance, which provides the source of truth for the model value. |
| Save form data | The `ProfileEditor` component accepts input from the user, but in a real scenario you want to capture the form value and make available for further processing outside the component. The `FormGroup` directive listens for the `submit` event emitted by the `form` element and emits an `ngSubmit` event that you can bind to a callback function. Add an `ngSubmit` event listener to the `form` tag with the `onSubmit()` callback method. <code-example header="src/app/profile-editor/profile-editor.component.html (submit event)" path="reactive-forms/src/app/profile-editor/profile-editor.component.html" region="ng-submit"></code-example> The `onSubmit()` method in the `ProfileEditor` component captures the current value of `profileForm`. Use `EventEmitter` to keep the form encapsulated and to provide the form value outside the component. The following example uses `console.warn` to log a message to the browser console. <code-example header="src/app/profile-editor/profile-editor.component.ts (submit method)" path="reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="on-submit"></code-example> The `submit` event is emitted by the `form` tag using the built-in DOM event. You trigger the event by clicking a button with `submit` type. This lets the user press the **Enter** key to submit the completed form. <br /> Use a `button` element to add a button to the bottom of the form to trigger the form submission. <code-example header="src/app/profile-editor/profile-editor.component.html (submit button)" path="reactive-forms/src/app/profile-editor/profile-editor.component.html" region="submit-button"></code-example> <div class="alert is-helpful"> **NOTE**: <br /> The button in the preceding snippet also has a `disabled` binding attached to it to disable the button when `profileForm` is invalid. You aren't performing any validation yet, so the button is always enabled. Basic form validation is covered in the [Validating form input](#basic-form-validation 'Basic form validation.') section. </div> |
| Display the component | To display the `ProfileEditor` component that contains the form, add it to a component template. <code-example header="src/app/app.component.html (profile editor)" path="reactive-forms/src/app/app.component.1.html" region="app-profile-editor"></code-example> `ProfileEditor` lets you manage the form control instances for the `firstName` and `lastName` controls within the form group instance. <div class="lightbox"> <img alt="Profile Editor with labels and inputs for first and last name as well as a submit button" src="generated/images/guide/reactive-forms/profile-editor-1.gif"> </div> |

<a id="nested-groups"></a>

### Создание вложенных групп форм

Группы форм могут принимать в качестве дочерних как отдельные экземпляры элементов управления формы, так и другие экземпляры групп форм. Это облегчает создание сложных моделей форм и логически объединяет их в группы.

При создании сложных форм управлять различными областями информации проще в небольших разделах. Использование вложенных экземпляров групп форм позволяет разбивать большие группы форм на более мелкие, более управляемые.

Чтобы создать более сложные формы, выполните следующие действия.

1.  Создайте вложенную группу.

1.  Сгруппируйте вложенную форму в шаблоне.

Некоторые типы информации естественным образом попадают в одну группу. Имя и адрес являются типичными примерами таких вложенных групп и используются в следующих примерах.

| Action | Details | | :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create a nested group | To create a nested group in `profileForm`, add a nested `address` element to the form group instance. <code-example header="src/app/profile-editor/profile-editor.component.ts (nested form group)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="nested-formgroup"></code-example> In this example, `address group` combines the current `firstName` and `lastName` controls with the new `street`, `city`, `state`, and `zip` controls. Even though the `address` element in the form group is a child of the overall `profileForm` element in the form group, the same rules apply with value and status changes. Changes in status and value from the nested form group propagate to the parent form group, maintaining consistency with the overall model. |
| Group the nested form in the template | After you update the model in the component class, update the template to connect the form group instance and its input elements. Add the `address` form group containing the `street`, `city`, `state`, and `zip` fields to the `ProfileEditor` template. <code-example header="src/app/profile-editor/profile-editor.component.html (template nested form group)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.html" region="formgroupname"></code-example> The `ProfileEditor` form is displayed as one group, but the model is broken down further to represent the logical grouping areas. <div class="lightbox"> <img alt="Profile editor update adding address inputs, instructive text for filling out the form to enable the submit button, and a disabled submit button" src="generated/images/guide/reactive-forms/profile-editor-2.png"> </div> <div class="alert is-helpful"> **TIP**: <br /> Display the value for the form group instance in the component template using the `value` property and `JsonPipe`. </div> |

### Обновление частей модели данных

При обновлении значения для экземпляра группы форм, содержащей несколько элементов управления, вы можете захотеть обновить только часть модели. В этом разделе рассматривается, как обновлять определенные части модели данных элемента управления формы.

Существует два способа обновления значения модели:

| Методы | Подробности | | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | |.

| `setValue()` | Установка нового значения для отдельного элемента управления. Метод `setValue()` строго придерживается структуры группы форм и заменяет все значение для элемента управления. |

| `patchValue()` | Заменяет все свойства, определенные в объекте, которые изменились в модели формы. |

Строгие проверки метода `setValue()` помогают выявить ошибки вложенности в сложных формах, в то время как `patchValue()` при таких ошибках молча терпит неудачу.

В `ProfileEditorComponent` используйте метод `updateProfile` со следующим примером для обновления имени и адреса улицы пользователя.

<code-example header="src/app/profile-editor/profile-editor.component.ts (patch value)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="patch-value"></code-example>.

Имитируйте обновление, добавив в шаблон кнопку для обновления профиля пользователя по требованию.

<code-example header="src/app/profile-editor/profile-editor.component.html (update value)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.html" region="patch-value"></code-example>.

Когда пользователь нажимает на кнопку, модель `profileForm` обновляется новыми значениями для `firstName` и `street`. Обратите внимание, что `street` предоставляется в виде объекта внутри свойства `address`.

Это необходимо, потому что метод `patchValue()` применяет обновление к структуре модели.

Метод `PatchValue()` обновляет только те свойства, которые определены моделью формы.

## Использование службы FormBuilder для генерации элементов управления

Создание экземпляров элементов управления формы вручную может стать утомительным при работе с несколькими формами. Служба `FormBuilder` предоставляет удобные методы для генерации элементов управления.

Используйте следующие шаги, чтобы воспользоваться преимуществами этой службы.

1.  Импортируйте класс `FormBuilder`.

1.  Инжектируйте службу `FormBuilder`.

1.  Сгенерируйте содержимое формы.

В следующих примерах показано, как рефакторить компонент `ProfileEditor`, чтобы использовать службу конструктора форм для создания экземпляров элементов управления формами и групп форм.

| Action | Details | | :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Import the FormBuilder class | Import the `FormBuilder` class from the `@angular/forms` package. <code-example header="src/app/profile-editor/profile-editor.component.ts (import)" path="reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="form-builder-imports"></code-example> |
| Inject the FormBuilder service | The `FormBuilder` service is an injectable provider that is provided with the reactive forms module. Inject this dependency by adding it to the component constructor. <code-example header="src/app/profile-editor/profile-editor.component.ts (constructor)" path="reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="inject-form-builder"></code-example> |
| Generate form controls | The `FormBuilder` service has three methods: `control()`, `group()`, and `array()`. These are factory methods for generating instances in your component classes including form controls, form groups, and form arrays. Use the `group` method to create the `profileForm` controls. <code-example header="src/app/profile-editor/profile-editor.component.ts (form builder)" path="reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="form-builder"></code-example> In the preceding example, you use the `group()` method with the same object to define the properties in the model. The value for each control name is an array containing the initial value as the first item in the array. <div class="alert is-helpful"> **TIP**: <br /> You can define the control with just the initial value, but if your controls need sync or async validation, add sync and async validators as the second and third items in the array. </div> Compare using the form builder to creating the instances manually. <code-tabs> <code-pane header="src/app/profile-editor/profile-editor.component.ts (instances)" path="reactive-forms/src/app/profile-editor/profile-editor.component.1.ts" region="formgroup-compare"></code-pane> <code-pane header="src/app/profile-editor/profile-editor.component.ts (form builder)" path="reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="formgroup-compare"></code-pane> </code-tabs> |

<a id="basic-form-validation"></a>

## Валидация ввода формы

Валидация формы используется для обеспечения полноты и правильности вводимых пользователем данных. В этом разделе рассматривается добавление одного валидатора к элементу управления формы и отображение общего состояния формы.

Более подробно валидация формы рассматривается в руководстве [Form Validation](guide/form-validation 'Все о валидации формы').

Для добавления валидации формы выполните следующие действия.

1.  Импортируйте функцию валидатора в компонент формы.

1.  Добавьте валидатор к полю в форме.

1.  Добавьте логику для обработки статуса валидации.

Наиболее распространенная валидация - сделать поле обязательным для заполнения. В следующем примере показано, как добавить обязательную проверку к элементу управления `firstName` и отобразить результат проверки.

| Action | Details | | :-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Import a validator function | Reactive forms include a set of validator functions for common use cases. These functions receive a control to validate against and return an error object or a null value based on the validation check. <br /> Import the `Validators` class from the `@angular/forms` package. <code-example header="src/app/profile-editor/profile-editor.component.ts (import)" path="reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="validator-imports"></code-example> |
| Make a field required | In the `ProfileEditor` component, add the `Validators.required` static method as the second item in the array for the `firstName` control. <code-example header="src/app/profile-editor/profile-editor.component.ts (required validator)" path="reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="required-validator"></code-example> |
| Display form status | When you add a required field to the form control, its initial status is invalid. This invalid status propagates to the parent form group element, making its status invalid. Access the current status of the form group instance through its `status` property. <br /> Display the current status of `profileForm` using interpolation. <code-example header="src/app/profile-editor/profile-editor.component.html (display status)" path="reactive-forms/src/app/profile-editor/profile-editor.component.html" region="display-status"></code-example> <div class="lightbox"> <img alt="Profile Editor with validation status of invalid" src="generated/images/guide/reactive-forms/profile-editor-3.png"> </div> The **Submit** button is disabled because `profileForm` is invalid due to the required `firstName` form control. After you fill out the `firstName` input, the form becomes valid and the **Submit** button is enabled. <br /> For more on form validation, visit the [Form Validation](guide/form-validation 'All about form validation') guide. |

<a id="dynamic-forms"></a>

## Создание динамических форм

`FormArray` - это альтернатива `FormGroup` для управления любым количеством неименованных элементов управления. Как и в случае с экземплярами групп форм, вы можете динамически вставлять и удалять элементы управления из экземпляров массива форм, а значение экземпляра массива форм и статус проверки вычисляются из его дочерних элементов управления.

Однако вам не нужно определять ключ для каждого элемента управления по имени, поэтому это отличный вариант, если вы заранее не знаете количество дочерних значений.

Чтобы определить динамическую форму, выполните следующие действия.

1.  Импортируйте класс `FormArray`.

1.  Определите элемент управления `FormArray`.

1.  Получите доступ к элементу управления `FormArray` с помощью метода getter.

1.  Отображение массива форм в шаблоне.

В следующем примере показано, как управлять массивом _aliases_ в `ProfileEditor`.

| Action | Details | | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Import the `FormArray` class | Import the `FormArray` class from `@angular/forms` to use for type information. The `FormBuilder` service is ready to create a `FormArray` instance. <code-example header="src/app/profile-editor/profile-editor.component.ts (import)" path="reactive-forms/src/app/profile-editor/profile-editor.component.2.ts" region="form-array-imports"></code-example> |
| Define a `FormArray` control | You can initialize a form array with any number of controls, from zero to many, by defining them in an array. Add an `aliases` property to the form group instance for `profileForm` to define the form array. <br /> Use the `FormBuilder.array()` method to define the array, and the `FormBuilder.control()` method to populate the array with an initial control. <code-example header="src/app/profile-editor/profile-editor.component.ts (aliases form array)" path="reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="aliases"></code-example> The aliases control in the form group instance is now populated with a single control until more controls are added dynamically. |
| Access the `FormArray` control | A getter provides access to the aliases in the form array instance compared to repeating the `profileForm.get()` method to get each instance. The form array instance represents an undefined number of controls in an array. It's convenient to access a control through a getter, and this approach is straightforward to repeat for additional controls. <br /> Use the getter syntax to create an `aliases` class property to retrieve the alias's form array control from the parent form group. <code-example header="src/app/profile-editor/profile-editor.component.ts (aliases getter)" path="reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="aliases-getter"></code-example> <div class="alert is-helpful"> **NOTE**: <br /> Because the returned control is of the type `AbstractControl`, you need to provide an explicit type to access the method syntax for the form array instance. </div> Define a method to dynamically insert an alias control into the alias's form array. The `FormArray.push()` method inserts the control as a new item in the array. <code-example header="src/app/profile-editor/profile-editor.component.ts (add alias)" path="reactive-forms/src/app/profile-editor/profile-editor.component.ts" region="add-alias"></code-example> In the template, each control is displayed as a separate input field. |
| Display the form array in the template | To attach the aliases from your form model, you must add it to the template. Similar to the `formGroupName` input provided by `FormGroupNameDirective`, `formArrayName` binds communication from the form array instance to the template with `FormArrayNameDirective`. <br /> Add the following template HTML after the `<div>` closing the `formGroupName` element. <code-example header="src/app/profile-editor/profile-editor.component.html (aliases form array template)" path="reactive-forms/src/app/profile-editor/profile-editor.component.html" region="formarrayname"></code-example> The `*ngFor` directive iterates over each form control instance provided by the aliases form array instance. Because form array elements are unnamed, you assign the index to the `i` variable and pass it to each control to bind it to the `formControlName` input. <div class="lightbox"> <img alt="Profile Editor with aliases section, which includes an alias label, input, and button for adding another alias text input" src="generated/images/guide/reactive-forms/profile-editor-4.png"> </div> Each time a new alias instance is added, the new form array instance is provided its control based on the index. This lets you track each individual control when calculating the status and value of the root control. |
| Add an alias | Initially, the form contains one `Alias` field. To add another field, click the **Add Alias** button. You can also validate the array of aliases reported by the form model displayed by `Form Value` at the bottom of the template. <div class="alert is-helpful"> **NOTE**: <br /> Instead of a form control instance for each alias, you can compose another form group instance with additional fields. The process of defining a control for each item is the same. </div> |

<a id="reactive-forms-api"></a>

## Reactive forms API summary

The following table lists the base classes and services used to create and manage reactive form controls. For complete syntax details, see the API reference documentation for the [Forms package](api/forms 'API reference').

#### Classes

| Class | Details | | :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

| `AbstractControl` | The abstract base class for the concrete form control classes `FormControl`, `FormGroup`, and `FormArray`. It provides their common behaviors and properties. |

| `FormControl` | Manages the value and validity status of an individual form control. It corresponds to an HTML form control such as `<input>` or `<select>`. |

| `FormGroup` | Manages the value and validity state of a group of `AbstractControl` instances. The group's properties include its child controls. The top-level form in your component is `FormGroup`. |

| `FormArray` | Manages the value and validity state of a numerically indexed array of `AbstractControl` instances. |

| | `FormBuilder` | Инжектируемый сервис, предоставляющий фабричные методы для создания экземпляров элементов управления. |

| | `FormRecord` | Отслеживает значение и состояние валидности коллекции экземпляров `FormControl`, каждый из которых имеет один и тот же тип значения. |

</table>

#### Директивы

| Директивы | Подробности | | :--------------------- | :----------------------------------------------------------------------------------------- | |

| `FormControlDirective` | Синхронизирует отдельный экземпляр `FormControl` с элементом управления формой. |

| `FormControlName` | Синхронизирует `FormControl` в существующем экземпляре `FormGroup` с элементом управления формы по имени. |

| | `FormGroupDirective` | Синхронизирует существующий экземпляр `FormGroup` с элементом DOM. |

| | `FormGroupName` | Синхронизирует вложенный экземпляр `FormGroup` с элементом DOM. |

| | `FormArrayName` | Синхронизирует вложенный экземпляр `FormArray` с элементом DOM. |

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
