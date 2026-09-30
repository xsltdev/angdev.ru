---
description: "Реактивные формы задают модель для полей, значения которых меняются со временем: элемент управления, группа, проверка и динамический состав."
---

# Реактивные формы {: #reactive-forms}

:date: 30.09.2026

Реактивные формы задают подход от модели: так обрабатывают поля, значения которых меняются со временем.
В этом руководстве — как создать и обновить базовый элемент управления, собрать несколько элементов в группу, проверить значения и сделать динамическую форму, в которую элементы добавляют и удаляют во время работы.

## Обзор реактивных форм {: #overview-of-reactive-forms}

Реактивные формы ведут состояние формы в конкретный момент явно и неизменяемо.
Каждое изменение состояния возвращает новое состояние, и между изменениями модель остаётся цельной.
Реактивные формы строятся вокруг потоков observable: поля и значения формы доступны как потоки, которые можно читать синхронно.

Тестировать такие формы проще: в момент запроса данные согласованы и предсказуемы.
Любой потребитель этих потоков может безопасно работать с данными.

Реактивные формы отличаются от [шаблонных форм](https://angular.dev/guide/forms/template-driven-forms) в нескольких существенных пунктах.
Они дают синхронный доступ к модели данных, неизменяемость вместе с операторами observable и отслеживание изменений через потоки observable.

Шаблонные формы позволяют менять данные прямо из шаблона, но устроены менее явно: они опираются на директивы в шаблоне и на изменяемые данные, а изменения отслеживают асинхронно.
Подробное сравнение двух подходов — в [обзоре форм](overview.md).

## Добавление базового элемента управления {: #adding-a-basic-form-control}

Чтобы пользоваться элементами управления, нужны три шага.

1.  Сгенерировать новый компонент и подключить модуль реактивных форм. Этот модуль объявляет директивы, без которых реактивные формы не работают.
1.  Создать экземпляр `FormControl`.
1.  Зарегистрировать `FormControl` в шаблоне.

После этого форму показывают, добавив компонент в шаблон.

В примерах ниже — как добавить один элемент управления.
Пользователь вводит имя в поле, значение перехватывается, и на экран выводится текущее значение элемента.

### Генерация компонента и импорт ReactiveFormsModule {: #generate-a-new-component-and-import-the-reactiveformsmodule}

Командой CLI `ng generate component` создайте компонент в проекте, импортируйте `ReactiveFormsModule` из пакета `@angular/forms` и добавьте его в массив `imports` компонента.

_name-editor.component.ts (excerpt)_

```ts
import {FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-name-editor',
  templateUrl: './name-editor.component.html',
  styleUrls: ['./name-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class NameEditorComponent {
```

### Объявление экземпляра FormControl {: #declare-a-formcontrol-instance}

Конструктор `FormControl` задаёт начальное значение — здесь это пустая строка. Если создавать элементы управления в классе компонента, состояние поля можно сразу слушать, обновлять и проверять.

_name-editor.component.ts_

```ts
// #docregion create-control
import {Component} from '@angular/core';

import {FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-name-editor',
  templateUrl: './name-editor.component.html',
  styleUrls: ['./name-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class NameEditorComponent {
  name = new FormControl('');
  // #enddocregion create-control

  // #docregion update-value
  updateName() {
    this.name.setValue('Nancy');
  }
  // #enddocregion update-value
  // #docregion create-control
}
// #enddocregion create-control
```

### Регистрация элемента управления в шаблоне {: #register-the-control-in-the-template}

После создания элемента управления в классе компонента его нужно связать с элементом формы в шаблоне. Обновите шаблон привязкой `formControl`, которую даёт `FormControlDirective`. Эта директива тоже входит в `ReactiveFormsModule`.

_name-editor.component.html_

```html
<!-- #docregion control-binding -->
<label for="name">Name: </label>
<input id="name" type="text" [formControl]="name" />
<!-- #enddocregion control-binding -->

<!-- #docregion display-value -->
<p>Value: {{ name.value }}</p>
<!-- #enddocregion display-value -->

<!-- #docregion update-value -->
<button type="button" (click)="updateName()">Update Name</button>
<!-- #enddocregion update-value -->
```

Синтаксис привязки в шаблоне регистрирует элемент управления на поле `name`. Элемент управления и элемент DOM общаются друг с другом: представление отражает изменения модели, а модель — изменения представления.

### Отображение компонента {: #display-the-component}

`FormControl`, записанный в свойство `name`, появляется на экране, когда компонент `<app-name-editor>` добавляют в шаблон.

_app.component.html (name editor)_

```html
<h1>Reactive Forms</h1>

<!-- #docregion app-name-editor-->
<app-name-editor />
<!-- #enddocregion app-name-editor-->

<!-- #docregion app-profile-editor -->
<app-profile-editor />
<!-- #enddocregion app-profile-editor -->
```

### Вывод значения элемента управления {: #displaying-a-form-control-value}

Значение можно показать несколькими способами:

-   Через observable `valueChanges`: изменения значения формы слушают в шаблоне через `AsyncPipe` или в классе компонента через метод `subscribe()`
-   Через свойство `value`, которое даёт снимок текущего значения

В примере ниже текущее значение выводится интерполяцией в шаблоне.

_name-editor.component.html (control value)_

```html
<!-- #docregion control-binding -->
<label for="name">Name: </label>
<input id="name" type="text" [formControl]="name" />
<!-- #enddocregion control-binding -->

<!-- #docregion display-value -->
<p>Value: {{ name.value }}</p>
<!-- #enddocregion display-value -->

<!-- #docregion update-value -->
<button type="button" (click)="updateName()">Update Name</button>
<!-- #enddocregion update-value -->
```

Показанное значение меняется по мере обновления элемента управления.

Реактивные формы отдают сведения об элементе управления через свойства и методы каждого экземпляра.
Эти свойства и методы базового класса [AbstractControl](https://angular.dev/api/forms/AbstractControl 'Справочник API') управляют состоянием формы и решают, когда показывать сообщения при [проверке ввода](#validating-form-input 'Подробнее о проверке ввода формы').

Другие свойства и методы `FormControl` — в [справочнике API](https://angular.dev/api/forms/FormControl 'Подробный справочник синтаксиса').

### Замена значения элемента управления {: #replacing-a-form-control-value}

У реактивных форм есть методы, которые меняют значение элемента управления из кода. Значение можно обновить без участия пользователя.
У экземпляра есть метод `setValue()`: он записывает новое значение и проверяет, что структура переданного значения совпадает со структурой элемента управления.
Например, когда данные формы приходят из бэкенд-API или сервиса, `setValue()` обновляет элемент управления новым значением и полностью заменяет старое.

В примере ниже в класс компонента добавляется метод, который через `setValue()` ставит значение _Nancy_.

_name-editor.component.ts (update value)_

```ts
// #docregion create-control
import {Component} from '@angular/core';

import {FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-name-editor',
  templateUrl: './name-editor.component.html',
  styleUrls: ['./name-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class NameEditorComponent {
  name = new FormControl('');
  // #enddocregion create-control

  // #docregion update-value
  updateName() {
    this.name.setValue('Nancy');
  }
  // #enddocregion update-value
  // #docregion create-control
}
// #enddocregion create-control
```

В шаблон добавляется кнопка, которая имитирует обновление имени.
По нажатию **Update Name** введённое в элемент управления значение становится текущим.

_name-editor.component.html (update value)_

```html
<!-- #docregion control-binding -->
<label for="name">Name: </label>
<input id="name" type="text" [formControl]="name" />
<!-- #enddocregion control-binding -->

<!-- #docregion display-value -->
<p>Value: {{ name.value }}</p>
<!-- #enddocregion display-value -->

<!-- #docregion update-value -->
<button type="button" (click)="updateName()">Update Name</button>
<!-- #enddocregion update-value -->
```

Источник истины для элемента управления — модель формы. По нажатию кнопки значение поля меняется в классе компонента и перекрывает текущее.

!!! tip ""

    В этом примере элемент управления один. Если вызывать `setValue()` у [группы формы](#grouping-form-controls) или [массива формы](#creating-dynamic-forms), значение должно совпадать со структурой группы или массива.

## Группировка элементов управления {: #grouping-form-controls}

Обычно в форме несколько связанных элементов управления.
Реактивные формы дают два способа собрать их в одну форму.

| Группы формы | Подробности                                                                                                                                                                                                                                                |
| :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Группа формы  | Задаёт форму с фиксированным набором элементов, которыми управляют вместе. Основы группы разобраны в этом разделе. Группы можно [вкладывать](#creating-nested-form-groups 'Подробнее о вложенных группах'), чтобы собирать более сложные формы. |
| Массив формы  | Задаёт динамическую форму: элементы можно добавлять и удалять во время работы. Массивы тоже можно вкладывать. Подробнее в разделе [Создание динамических форм](#creating-dynamic-forms).                              |

Экземпляр элемента управления ведёт одно поле, а экземпляр группы — состояние целой группы элементов \(например, формы\).
Каждый элемент в группе отслеживается по имени, заданному при создании группы.
В примере ниже несколько экземпляров собраны в одну группу.

Сгенерируйте компонент `ProfileEditor` и импортируйте классы `FormGroup` и `FormControl` из пакета `@angular/forms`.

```shell
ng generate component ProfileEditor
```

_profile-editor.component.ts (imports)_

```ts
import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class ProfileEditorComponent {
```

Чтобы добавить в компонент группу формы, сделайте следующее.

1.  Создайте экземпляр `FormGroup`.
1.  Свяжите модель `FormGroup` с представлением.
1.  Сохраните данные формы.

### Создание экземпляра FormGroup {: #create-a-formgroup-instance}

В классе компонента заведите свойство `profileForm` и запишите в него новый экземпляр группы. В конструктор группы передайте объект: именованные ключи сопоставлены своим элементам управления.

Для формы профиля добавьте два элемента с именами `firstName` и `lastName`.

_profile-editor.component.ts (form group)_

```ts
  });
  // #enddocregion formgroup, nested-formgroup, formgroup-compare
  // #docregion patch-value
  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #enddocregion patch-value
  // #docregion formgroup, nested-formgroup
}
```

Отдельные элементы управления теперь собраны в группу. Экземпляр `FormGroup` отдаёт значение модели объектом, собранным из значений своих элементов. У группы те же свойства (например, `value` и `untouched`) и методы (например, `setValue()`), что и у отдельного элемента управления.

### Связь модели FormGroup с представлением {: #associate-the-formgroup-model-and-view}

Группа отслеживает статус и изменения каждого своего элемента: если меняется один, родитель тоже сообщает о новом статусе или значении. Модель группы держится на своих участниках. После описания модели обновите шаблон, чтобы модель отразилась в представлении.

_profile-editor.component.html (template form group)_

```html
<form [formGroup]="profileForm">
  <label for="first-name">First Name: </label>
  <input id="first-name" type="text" formControlName="firstName" />

  <label for="last-name">Last Name: </label>
  <input id="last-name" type="text" formControlName="lastName" />

</form>
```

Как группа содержит набор элементов, так `FormGroup` с именем _profileForm_ привязывается к элементу `form` директивой `FormGroup` и создаёт слой связи между моделью и формой с полями. Вход `formControlName` директивы `FormControlName` привязывает каждое поле к элементу управления, описанному в `FormGroup`. Элементы управления общаются со своими элементами DOM и передают изменения экземпляру группы — источнику истины для значения модели.

### Сохранение данных формы {: #save-form-data}

Компонент `ProfileEditor` принимает ввод пользователя, но в настоящем приложении значение формы нужно перехватить и отдать на обработку за пределы компонента. Директива `FormGroup` слушает событие `submit` элемента `form` и порождает событие `ngSubmit`, которое можно привязать к функции обратного вызова. Добавьте на тег `form` обработчик `ngSubmit` с методом `onSubmit()`.

_profile-editor.component.html (submit event)_

```html
<!-- #docregion ng-submit -->
<form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
  <!-- #enddocregion ng-submit -->
  <label for="first-name">First Name: </label>
  <input id="first-name" type="text" formControlName="firstName" required />

  <label for="last-name">Last Name: </label>
  <input id="last-name" type="text" formControlName="lastName" />

  <div formGroupName="address">
    <h2>Address</h2>

    <label for="street">Street: </label>
    <input id="street" type="text" formControlName="street" />

    <label for="city">City: </label>
    <input id="city" type="text" formControlName="city" />

    <label for="state">State: </label>
    <input id="state" type="text" formControlName="state" />

    <label for="zip">Zip Code: </label>
    <input id="zip" type="text" formControlName="zip" />
  </div>

  <div formArrayName="aliases">
    <h2>Aliases</h2>
    <button type="button" (click)="addAlias()">+ Add another alias</button>

    @for (alias of aliases.controls; track $index; let i = $index) {
      <div>
        <!-- The repeated alias template -->
        <label for="alias-{{ i }}">Alias:</label>
        <input id="alias-{{ i }}" type="text" [formControlName]="i" />
      </div>
    }
  </div>

  <!-- #docregion submit-button -->
  <p>Complete the form to enable button.</p>
  <button type="submit" [disabled]="!profileForm.valid">Submit</button>
  <!-- #enddocregion submit-button -->
</form>

<hr />

<p>Form Value: {{ profileForm.value | json }}</p>

<!-- #docregion display-status -->
<p>Form Status: {{ profileForm.status }}</p>
<!-- #enddocregion display-status -->

<button type="button" (click)="updateProfile()">Update Profile</button>
```

Метод `onSubmit()` в компоненте `ProfileEditor` забирает текущее значение `profileForm`. Чтобы форма оставалась инкапсулированной, а значение уходило наружу, используйте `output()`. В примере ниже `console.warn` пишет сообщение в консоль браузера.

_profile-editor.component.ts (submit method)_

```ts
import {Component, inject} from '@angular/core';
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #docregion validator-imports
import {Validators} from '@angular/forms';
// #enddocregion validator-imports
import {FormArray} from '@angular/forms';
import {JsonPipe} from '@angular/common';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule, JsonPipe],
})
export class ProfileEditorComponent {
  // #docregion required-validator, aliases
  private formBuilder = inject(FormBuilder);

  profileForm = this.formBuilder.group({
    firstName: ['', Validators.required],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion required-validator
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion required-validator
  });
  // #enddocregion required-validator, aliases
  // #docregion aliases-getter
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }
  // #enddocregion aliases-getter

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #docregion add-alias
  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
  // #enddocregion add-alias
  // #docregion on-submit
  onSubmit() {
    // TODO: Use output() with form value
    console.warn(this.profileForm.value);
  }
  // #enddocregion on-submit
}
```

Событие `submit` порождает тег `form` встроенным событием DOM. Его вызывает кнопка с типом `submit`. Тогда пользователь может отправить заполненную форму клавишей **Enter**.

Кнопкой `button` добавьте в низ формы кнопку отправки.

_profile-editor.component.html (submit button)_

```html
<!-- #docregion ng-submit -->
<form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
  <!-- #enddocregion ng-submit -->
  <label for="first-name">First Name: </label>
  <input id="first-name" type="text" formControlName="firstName" required />

  <label for="last-name">Last Name: </label>
  <input id="last-name" type="text" formControlName="lastName" />

  <div formGroupName="address">
    <h2>Address</h2>

    <label for="street">Street: </label>
    <input id="street" type="text" formControlName="street" />

    <label for="city">City: </label>
    <input id="city" type="text" formControlName="city" />

    <label for="state">State: </label>
    <input id="state" type="text" formControlName="state" />

    <label for="zip">Zip Code: </label>
    <input id="zip" type="text" formControlName="zip" />
  </div>

  <div formArrayName="aliases">
    <h2>Aliases</h2>
    <button type="button" (click)="addAlias()">+ Add another alias</button>

    @for (alias of aliases.controls; track $index; let i = $index) {
      <div>
        <!-- The repeated alias template -->
        <label for="alias-{{ i }}">Alias:</label>
        <input id="alias-{{ i }}" type="text" [formControlName]="i" />
      </div>
    }
  </div>

  <!-- #docregion submit-button -->
  <p>Complete the form to enable button.</p>
  <button type="submit" [disabled]="!profileForm.valid">Submit</button>
  <!-- #enddocregion submit-button -->
</form>

<hr />

<p>Form Value: {{ profileForm.value | json }}</p>

<!-- #docregion display-status -->
<p>Form Status: {{ profileForm.status }}</p>
<!-- #enddocregion display-status -->

<button type="button" (click)="updateProfile()">Update Profile</button>
```

У кнопки в предыдущем фрагменте есть привязка `disabled`: кнопка отключается, когда `profileForm` невалидна. Проверки пока нет, поэтому кнопка всегда включена. Базовая проверка разобрана в разделе [Проверка ввода формы](#validating-form-input).

### Отображение компонента {: #display-the-component-form-group}

Чтобы показать компонент `ProfileEditor` с формой, добавьте его в шаблон компонента.

_app.component.html (profile editor)_

```html
<h1>Reactive Forms</h1>

<!-- #docregion app-name-editor-->
<app-name-editor />
<!-- #enddocregion app-name-editor-->

<!-- #docregion app-profile-editor -->
<app-profile-editor />
<!-- #enddocregion app-profile-editor -->
```

`ProfileEditor` управляет экземплярами `firstName` и `lastName` внутри экземпляра группы.

### Создание вложенных групп {: #creating-nested-form-groups}

Группа принимает в дети и отдельные элементы управления, и другие группы.
Так сложную модель проще сопровождать и логически раскладывать по частям.

В сложной форме разные области данных удобнее вести небольшими разделами.
Вложенная группа разбивает крупную группу на более мелкие и управляемые.

Чтобы собрать более сложную форму, сделайте следующее.

1.  Создайте вложенную группу.
1.  Соберите вложенную форму в шаблоне.

Некоторые сведения естественно попадают в одну группу.
Имя и адрес — типичный пример таких вложенных групп, он и используется ниже.

### Создание вложенной группы {: #create-a-nested-group}

Чтобы создать вложенную группу в `profileForm`, добавьте в экземпляр группы вложенный элемент `address`.

_profile-editor.component.ts (nested form group)_

```ts
// #docregion formgroup, nested-formgroup
import {Component} from '@angular/core';
import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class ProfileEditorComponent {
  // #docregion formgroup-compare
  profileForm = new FormGroup({
    firstName: new FormControl(''),
    lastName: new FormControl(''),
    address: new FormGroup({
      street: new FormControl(''),
      city: new FormControl(''),
      state: new FormControl(''),
      zip: new FormControl(''),
    }),
  });
  // #enddocregion formgroup, nested-formgroup, formgroup-compare
  // #docregion patch-value
  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #enddocregion patch-value
  // #docregion formgroup, nested-formgroup
}
```

В этом примере `address group` объединяет текущие элементы `firstName` и `lastName` с новыми `street`, `city`, `state` и `zip`. Элемент `address` в группе — ребёнок общего элемента `profileForm`, но правила значения и статуса те же. Изменения статуса и значения вложенной группы поднимаются к родительской и сохраняют согласие со всей моделью.

### Группа вложенной формы в шаблоне {: #group-the-nested-form-in-the-template}

После обновления модели в классе компонента обновите шаблон: свяжите экземпляр группы с полями ввода. Добавьте в шаблон `ProfileEditor` группу `address` с полями `street`, `city`, `state` и `zip`.

_profile-editor.component.html (template nested form group)_

```html
  <div formGroupName="address">
    <h2>Address</h2>

    <label for="street">Street: </label>
    <input id="street" type="text" formControlName="street" />

    <label for="city">City: </label>
    <input id="city" type="text" formControlName="city" />

    <label for="state">State: </label>
    <input id="state" type="text" formControlName="state" />

    <label for="zip">Zip Code: </label>
    <input id="zip" type="text" formControlName="zip" />
  </div>
```

Форма `ProfileEditor` выглядит как одна группа, но модель разложена дальше — по логическим областям.

Значение экземпляра группы выводят в шаблоне компонента через свойство `value` и `JsonPipe`.

### Обновление частей модели данных {: #updating-parts-of-the-data-model}

Когда у группы несколько элементов, часто нужно обновить только часть модели.
В этом разделе — как обновлять отдельные части модели данных элемента управления.

Значение модели обновляют двумя способами:

| Методы        | Подробности                                                                                                                                                               |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `setValue()`   | Задаёт новое значение отдельному элементу. Метод `setValue()` строго следует структуре группы и заменяет значение элемента целиком. |
| `patchValue()` | Заменяет в модели формы те свойства из объекта, которые изменились.                                                                                     |

Строгие проверки `setValue()` помогают поймать ошибки вложенности в сложных формах, а `patchValue()` при таких ошибках молча ничего не делает.

В `ProfileEditorComponent` метод `updateProfile` из примера ниже обновляет имя и улицу пользователя.

_profile-editor.component.ts (patch value)_

```ts
// #docregion formgroup, nested-formgroup
import {Component} from '@angular/core';
import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class ProfileEditorComponent {
  // #docregion formgroup-compare
  profileForm = new FormGroup({
    firstName: new FormControl(''),
    lastName: new FormControl(''),
    address: new FormGroup({
      street: new FormControl(''),
      city: new FormControl(''),
      state: new FormControl(''),
      zip: new FormControl(''),
    }),
  });
  // #enddocregion formgroup, nested-formgroup, formgroup-compare
  // #docregion patch-value
  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #enddocregion patch-value
  // #docregion formgroup, nested-formgroup
}
```

Чтобы имитировать обновление, добавьте в шаблон кнопку: она обновляет профиль по запросу.

_profile-editor.component.html (update value)_

```html
<form [formGroup]="profileForm">
  <label for="first-name">First Name: </label>
  <input id="first-name" type="text" formControlName="firstName" />

  <label for="last-name">Last Name: </label>
  <input id="last-name" type="text" formControlName="lastName" />

  <div formGroupName="address">
    <h2>Address</h2>

    <label for="street">Street: </label>
    <input id="street" type="text" formControlName="street" />

    <label for="city">City: </label>
    <input id="city" type="text" formControlName="city" />

    <label for="state">State: </label>
    <input id="state" type="text" formControlName="state" />

    <label for="zip">Zip Code: </label>
    <input id="zip" type="text" formControlName="zip" />
  </div>

  <div formArrayName="aliases">
    <h2>Aliases</h2>
    <button type="button" (click)="addAlias()">+ Add another alias</button>

    @for (alias of aliases.controls; track $index; let i = $index) {
      <div>
        <!-- The repeated alias template -->
        <label for="alias-{{ i }}">Alias: </label>
        <input id="alias-{{ i }}" type="text" [formControlName]="i" />
      </div>
    }
  </div>
</form>

<p>Form Value: {{ profileForm.value | json }}</p>

<!-- #docregion patch-value -->
<button type="button" (click)="updateProfile()">Update Profile</button>
<!-- #enddocregion patch-value -->
```

По нажатию кнопки модель `profileForm` получает новые значения `firstName` и `street`. Обратите внимание: `street` лежит в объекте внутри свойства `address`.
Так нужно, потому что `patchValue()` накладывает обновление на структуру модели.
`patchValue()` меняет только те свойства, которые модель формы определяет.

## Сервис FormBuilder для создания элементов управления {: #using-the-formbuilder-service-to-generate-controls}

Создавать экземпляры вручную утомительно, когда форм много.
Сервис `FormBuilder` даёт удобные методы для генерации элементов управления.

Чтобы воспользоваться сервисом, сделайте следующее.

1.  Импортируйте класс `FormBuilder`.
1.  Внедрите сервис `FormBuilder`.
1.  Сгенерируйте содержимое формы.

В примерах ниже компонент `ProfileEditor` переписывается на сервис построителя формы: так создаются экземпляры элементов управления и групп.

### Импорт класса FormBuilder {: #import-the-formbuilder-class}

Импортируйте класс `FormBuilder` из пакета `@angular/forms`.

_profile-editor.component.ts (import)_

```ts
import {Component, inject} from '@angular/core';
// #docregion form-builder-imports
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #enddocregion form-builder-imports
// #docregion form-array-imports
import {FormArray} from '@angular/forms';
// #enddocregion form-array-imports

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class ProfileEditorComponent {
  // #docregion inject-form-builder
  private formBuilder = inject(FormBuilder);
  // #enddocregion inject-form-builder
  // #docregion formgroup-compare, form-builder
  profileForm = this.formBuilder.group({
    firstName: [''],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion form-builder, formgroup-compare
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion form-builder, formgroup-compare
  });
  // #enddocregion form-builder, formgroup-compare
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }

  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
}
```

### Внедрение сервиса FormBuilder {: #inject-the-formbuilder-service}

Сервис `FormBuilder` — внедряемый провайдер из модуля реактивных форм. Внедрите эту зависимость в компонент функцией `inject()`.

_profile-editor.component.ts (property init)_

```ts
import {Component, inject} from '@angular/core';
// #docregion form-builder-imports
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #enddocregion form-builder-imports
// #docregion form-array-imports
import {FormArray} from '@angular/forms';
// #enddocregion form-array-imports

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class ProfileEditorComponent {
  // #docregion inject-form-builder
  private formBuilder = inject(FormBuilder);
  // #enddocregion inject-form-builder
  // #docregion formgroup-compare, form-builder
  profileForm = this.formBuilder.group({
    firstName: [''],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion form-builder, formgroup-compare
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion form-builder, formgroup-compare
  });
  // #enddocregion form-builder, formgroup-compare
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }

  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
}
```

### Генерация элементов управления {: #generate-form-controls}

У сервиса `FormBuilder` три метода: `control()`, `group()` и `array()`. Это фабрики: в классе компонента они создают элементы управления, группы и массивы формы. Метод `group` создаёт элементы `profileForm`.

_profile-editor.component.ts (form builder)_

```ts
import {Component, inject} from '@angular/core';
// #docregion form-builder-imports
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #enddocregion form-builder-imports
// #docregion form-array-imports
import {FormArray} from '@angular/forms';
// #enddocregion form-array-imports

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class ProfileEditorComponent {
  // #docregion inject-form-builder
  private formBuilder = inject(FormBuilder);
  // #enddocregion inject-form-builder
  // #docregion formgroup-compare, form-builder
  profileForm = this.formBuilder.group({
    firstName: [''],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion form-builder, formgroup-compare
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion form-builder, formgroup-compare
  });
  // #enddocregion form-builder, formgroup-compare
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }

  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
}
```

В предыдущем примере метод `group()` получает тот же объект и описывает свойства модели. Значение каждого имени элемента — массив, и первый элемент массива задаёт начальное значение.

!!! tip ""

    Элемент управления можно задать одним начальным значением. Если нужны синхронная или асинхронная проверка, добавьте синхронные и асинхронные валидаторы вторым и третьим элементами массива. Сравните построитель формы с ручным созданием экземпляров.

  

=== "profile-editor.component.ts (instances)"

    

```ts
    // #docregion formgroup, nested-formgroup
    import {Component} from '@angular/core';
    import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';

    @Component({
      selector: 'app-profile-editor',
      templateUrl: './profile-editor.component.html',
      styleUrls: ['./profile-editor.component.css'],
      imports: [ReactiveFormsModule],
    })
    export class ProfileEditorComponent {
      // #docregion formgroup-compare
      profileForm = new FormGroup({
        firstName: new FormControl(''),
        lastName: new FormControl(''),
        address: new FormGroup({
          street: new FormControl(''),
          city: new FormControl(''),
          state: new FormControl(''),
          zip: new FormControl(''),
        }),
      });
      // #enddocregion formgroup, nested-formgroup, formgroup-compare
      // #docregion patch-value
      updateProfile() {
        this.profileForm.patchValue({
          firstName: 'Nancy',
          address: {
            street: '123 Drew Street',
          },
        });
      }
      // #enddocregion patch-value
      // #docregion formgroup, nested-formgroup
    }
    
```

=== "profile-editor.component.ts (form builder)"

    

```ts
    import {Component, inject} from '@angular/core';
    // #docregion form-builder-imports
    import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
    // #enddocregion form-builder-imports
    // #docregion form-array-imports
    import {FormArray} from '@angular/forms';
    // #enddocregion form-array-imports

    @Component({
      selector: 'app-profile-editor',
      templateUrl: './profile-editor.component.html',
      styleUrls: ['./profile-editor.component.css'],
      imports: [ReactiveFormsModule],
    })
    export class ProfileEditorComponent {
      // #docregion inject-form-builder
      private formBuilder = inject(FormBuilder);
      // #enddocregion inject-form-builder
      // #docregion formgroup-compare, form-builder
      profileForm = this.formBuilder.group({
        firstName: [''],
        lastName: [''],
        address: this.formBuilder.group({
          street: [''],
          city: [''],
          state: [''],
          zip: [''],
        }),
        // #enddocregion form-builder, formgroup-compare
        aliases: this.formBuilder.array([this.formBuilder.control('')]),
        // #docregion form-builder, formgroup-compare
      });
      // #enddocregion form-builder, formgroup-compare
      get aliases() {
        return this.profileForm.get('aliases') as FormArray;
      }

      updateProfile() {
        this.profileForm.patchValue({
          firstName: 'Nancy',
          address: {
            street: '123 Drew Street',
          },
        });
      }

      addAlias() {
        this.aliases.push(this.formBuilder.control(''));
      }
    }
    
```

## Проверка ввода формы {: #validating-form-input}

_Проверка формы_ нужна, чтобы пользовательский ввод был полным и верным.
В этом разделе к элементу управления добавляется один валидатор и выводится общий статус формы.
Подробнее проверка разобрана в руководстве [Проверка формы](https://angular.dev/guide/forms/form-validation).

Чтобы добавить проверку, сделайте следующее.

1.  Импортируйте функцию-валидатор в компонент формы.
1.  Добавьте валидатор к полю формы.
1.  Добавьте логику обработки статуса проверки.

Самая частая проверка — обязательное поле.
В примере ниже к элементу `firstName` добавляется проверка на заполненность, и результат выводится на экран.

### Импорт функции-валидатора {: #import-a-validator-function}

В реактивных формах есть набор функций-валидаторов для типичных случаев. Функция получает элемент управления и по результату проверки возвращает объект ошибки или `null`.

Импортируйте класс `Validators` из пакета `@angular/forms`.

_profile-editor.component.ts (import)_

```ts
import {Component, inject} from '@angular/core';
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #docregion validator-imports
import {Validators} from '@angular/forms';
// #enddocregion validator-imports
import {FormArray} from '@angular/forms';
import {JsonPipe} from '@angular/common';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule, JsonPipe],
})
export class ProfileEditorComponent {
  // #docregion required-validator, aliases
  private formBuilder = inject(FormBuilder);

  profileForm = this.formBuilder.group({
    firstName: ['', Validators.required],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion required-validator
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion required-validator
  });
  // #enddocregion required-validator, aliases
  // #docregion aliases-getter
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }
  // #enddocregion aliases-getter

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #docregion add-alias
  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
  // #enddocregion add-alias
  // #docregion on-submit
  onSubmit() {
    // TODO: Use output() with form value
    console.warn(this.profileForm.value);
  }
  // #enddocregion on-submit
}
```

### Обязательное поле {: #make-a-field-required}

В компоненте `ProfileEditor` добавьте статический метод `Validators.required` вторым элементом массива у элемента `firstName`.

_profile-editor.component.ts (required validator)_

```ts
import {Component, inject} from '@angular/core';
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #docregion validator-imports
import {Validators} from '@angular/forms';
// #enddocregion validator-imports
import {FormArray} from '@angular/forms';
import {JsonPipe} from '@angular/common';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule, JsonPipe],
})
export class ProfileEditorComponent {
  // #docregion required-validator, aliases
  private formBuilder = inject(FormBuilder);

  profileForm = this.formBuilder.group({
    firstName: ['', Validators.required],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion required-validator
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion required-validator
  });
  // #enddocregion required-validator, aliases
  // #docregion aliases-getter
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }
  // #enddocregion aliases-getter

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #docregion add-alias
  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
  // #enddocregion add-alias
  // #docregion on-submit
  onSubmit() {
    // TODO: Use output() with form value
    console.warn(this.profileForm.value);
  }
  // #enddocregion on-submit
}
```

### Вывод статуса формы {: #display-form-status}

Когда в элемент управления добавляют обязательное поле, начальный статус — невалидный. Этот статус поднимается к родительской группе, и её статус тоже становится невалидным. Текущий статус экземпляра группы читают через свойство `status`.

Текущий статус `profileForm` выводят интерполяцией.

_profile-editor.component.html (display status)_

```html
<!-- #docregion ng-submit -->
<form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
  <!-- #enddocregion ng-submit -->
  <label for="first-name">First Name: </label>
  <input id="first-name" type="text" formControlName="firstName" required />

  <label for="last-name">Last Name: </label>
  <input id="last-name" type="text" formControlName="lastName" />

  <div formGroupName="address">
    <h2>Address</h2>

    <label for="street">Street: </label>
    <input id="street" type="text" formControlName="street" />

    <label for="city">City: </label>
    <input id="city" type="text" formControlName="city" />

    <label for="state">State: </label>
    <input id="state" type="text" formControlName="state" />

    <label for="zip">Zip Code: </label>
    <input id="zip" type="text" formControlName="zip" />
  </div>

  <div formArrayName="aliases">
    <h2>Aliases</h2>
    <button type="button" (click)="addAlias()">+ Add another alias</button>

    @for (alias of aliases.controls; track $index; let i = $index) {
      <div>
        <!-- The repeated alias template -->
        <label for="alias-{{ i }}">Alias:</label>
        <input id="alias-{{ i }}" type="text" [formControlName]="i" />
      </div>
    }
  </div>

  <!-- #docregion submit-button -->
  <p>Complete the form to enable button.</p>
  <button type="submit" [disabled]="!profileForm.valid">Submit</button>
  <!-- #enddocregion submit-button -->
</form>

<hr />

<p>Form Value: {{ profileForm.value | json }}</p>

<!-- #docregion display-status -->
<p>Form Status: {{ profileForm.status }}</p>
<!-- #enddocregion display-status -->

<button type="button" (click)="updateProfile()">Update Profile</button>
```

Кнопка **Submit** отключена, потому что `profileForm` невалидна из-за обязательного элемента `firstName`. После заполнения поля `firstName` форма становится валидной, и кнопка **Submit** включается.

Подробнее о проверке — в руководстве [Проверка формы](https://angular.dev/guide/forms/form-validation).

## Создание динамических форм {: #creating-dynamic-forms}

`FormArray` — альтернатива `FormGroup`, когда нужно вести любое число безымянных элементов управления.
Как и у группы, у массива элементы можно вставлять и удалять динамически, а значение и статус проверки считаются по дочерним элементам.
Ключ по имени для каждого элемента задавать не нужно, поэтому массив удобен, если число дочерних значений заранее неизвестно.

Чтобы описать динамическую форму, сделайте следующее.

1.  Импортируйте класс `FormArray`.
1.  Опишите элемент `FormArray`.
1.  Получите доступ к элементу `FormArray` через геттер.
1.  Выведите массив формы в шаблоне.

В примере ниже в `ProfileEditor` ведётся массив _aliases_.

### Импорт класса `FormArray` {: #import-the-formarray-class}

Импортируйте класс `FormArray` из `@angular/forms`: он нужен для сведений о типе. Сервис `FormBuilder` уже умеет создавать экземпляр `FormArray`.

_profile-editor.component.ts (import)_

```ts
import {Component, inject} from '@angular/core';
// #docregion form-builder-imports
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #enddocregion form-builder-imports
// #docregion form-array-imports
import {FormArray} from '@angular/forms';
// #enddocregion form-array-imports

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule],
})
export class ProfileEditorComponent {
  // #docregion inject-form-builder
  private formBuilder = inject(FormBuilder);
  // #enddocregion inject-form-builder
  // #docregion formgroup-compare, form-builder
  profileForm = this.formBuilder.group({
    firstName: [''],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion form-builder, formgroup-compare
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion form-builder, formgroup-compare
  });
  // #enddocregion form-builder, formgroup-compare
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }

  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
}
```

### Описание элемента `FormArray` {: #define-a-formarray-control}

Массив формы можно инициализировать любым числом элементов, от нуля и больше: их перечисляют в массиве. Добавьте в экземпляр группы `profileForm` свойство `aliases` и опишите им массив формы.

Метод `FormBuilder.array()` задаёт массив, а `FormBuilder.control()` заполняет его начальным элементом.

_profile-editor.component.ts (aliases form array)_

```ts
import {Component, inject} from '@angular/core';
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #docregion validator-imports
import {Validators} from '@angular/forms';
// #enddocregion validator-imports
import {FormArray} from '@angular/forms';
import {JsonPipe} from '@angular/common';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule, JsonPipe],
})
export class ProfileEditorComponent {
  // #docregion required-validator, aliases
  private formBuilder = inject(FormBuilder);

  profileForm = this.formBuilder.group({
    firstName: ['', Validators.required],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion required-validator
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion required-validator
  });
  // #enddocregion required-validator, aliases
  // #docregion aliases-getter
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }
  // #enddocregion aliases-getter

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #docregion add-alias
  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
  // #enddocregion add-alias
  // #docregion on-submit
  onSubmit() {
    // TODO: Use output() with form value
    console.warn(this.profileForm.value);
  }
  // #enddocregion on-submit
}
```

Элемент aliases в экземпляре группы заполнен одним элементом управления, пока динамически не добавят ещё.

### Доступ к элементу `FormArray` {: #access-the-formarray-control}

Геттер открывает доступ к aliases в экземпляре массива и избавляет от повторных вызовов `profileForm.get()`. Экземпляр массива — это неопределённое число элементов в массиве. Удобно доставать элемент через геттер, и тот же приём легко повторить для других элементов.

Синтаксисом геттера заведите свойство класса `aliases`: оно достаёт массив формы псевдонимов из родительской группы.

_profile-editor.component.ts (aliases getter)_

```ts
import {Component, inject} from '@angular/core';
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #docregion validator-imports
import {Validators} from '@angular/forms';
// #enddocregion validator-imports
import {FormArray} from '@angular/forms';
import {JsonPipe} from '@angular/common';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule, JsonPipe],
})
export class ProfileEditorComponent {
  // #docregion required-validator, aliases
  private formBuilder = inject(FormBuilder);

  profileForm = this.formBuilder.group({
    firstName: ['', Validators.required],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion required-validator
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion required-validator
  });
  // #enddocregion required-validator, aliases
  // #docregion aliases-getter
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }
  // #enddocregion aliases-getter

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #docregion add-alias
  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
  // #enddocregion add-alias
  // #docregion on-submit
  onSubmit() {
    // TODO: Use output() with form value
    console.warn(this.profileForm.value);
  }
  // #enddocregion on-submit
}
```

Возвращаемый элемент имеет тип `AbstractControl`, поэтому для методов экземпляра массива нужен явный тип. Опишите метод, который динамически вставляет элемент псевдонима в массив формы. Метод `FormArray.push()` добавляет элемент новым пунктом массива. В `FormArray.push()` можно передать и массив элементов, чтобы зарегистрировать несколько сразу.

_profile-editor.component.ts (add alias)_

```ts
import {Component, inject} from '@angular/core';
import {FormBuilder, ReactiveFormsModule} from '@angular/forms';
// #docregion validator-imports
import {Validators} from '@angular/forms';
// #enddocregion validator-imports
import {FormArray} from '@angular/forms';
import {JsonPipe} from '@angular/common';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css'],
  imports: [ReactiveFormsModule, JsonPipe],
})
export class ProfileEditorComponent {
  // #docregion required-validator, aliases
  private formBuilder = inject(FormBuilder);

  profileForm = this.formBuilder.group({
    firstName: ['', Validators.required],
    lastName: [''],
    address: this.formBuilder.group({
      street: [''],
      city: [''],
      state: [''],
      zip: [''],
    }),
    // #enddocregion required-validator
    aliases: this.formBuilder.array([this.formBuilder.control('')]),
    // #docregion required-validator
  });
  // #enddocregion required-validator, aliases
  // #docregion aliases-getter
  get aliases() {
    return this.profileForm.get('aliases') as FormArray;
  }
  // #enddocregion aliases-getter

  updateProfile() {
    this.profileForm.patchValue({
      firstName: 'Nancy',
      address: {
        street: '123 Drew Street',
      },
    });
  }
  // #docregion add-alias
  addAlias() {
    this.aliases.push(this.formBuilder.control(''));
  }
  // #enddocregion add-alias
  // #docregion on-submit
  onSubmit() {
    // TODO: Use output() with form value
    console.warn(this.profileForm.value);
  }
  // #enddocregion on-submit
}
```

В шаблоне каждый элемент показывается отдельным полем ввода.

### Массив формы в шаблоне {: #display-the-form-array-in-the-template}

Чтобы привязать aliases из модели формы, добавьте их в шаблон. По аналогии со входом `formGroupName` директивы `FormGroupNameDirective`, `formArrayName` связывает экземпляр массива с шаблоном через `FormArrayNameDirective`.

Добавьте следующий HTML шаблона после `
`, закрывающего элемент `formGroupName`.

_profile-editor.component.html (aliases form array template)_

```html
  <div formArrayName="aliases">
    <h2>Aliases</h2>
    <button type="button" (click)="addAlias()">+ Add another alias</button>

    @for (alias of aliases.controls; track $index; let i = $index) {
      <div>
        <!-- The repeated alias template -->
        <label for="alias-{{ i }}">Alias:</label>
        <input id="alias-{{ i }}" type="text" [formControlName]="i" />
      </div>
    }
  </div>
```

Блок `@for` обходит каждый экземпляр элемента управления из массива aliases. У элементов массива нет имён, поэтому индекс записывают в переменную `i` и передают каждому элементу, чтобы привязать его ко входу `formControlName`.

Каждый новый экземпляр псевдонима получает свой элемент по индексу. Так можно отслеживать каждый элемент, когда считаются статус и значение корневого элемента.

!!! info ""

    В приложениях без Zone.js (zoneless) изменение модели реактивных форм (например, вызов `FormArray.push()`) само по себе не планирует обнаружение изменений компонента. Если шаблон зависит от структурных изменений модели, таких как `aliases.controls`, компонент должен сообщить Angular, что нужно запустить обнаружение изменений. Например, свяжите observable формы с `ChangeDetectorRef.markForCheck()`:

```ts
import {ChangeDetectorRef, Component, inject} from '@angular/core';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';

@Component({/* ... */})
export class ProfileEditor {
  private readonly cdr = inject(ChangeDetectorRef);

  constructor() {
    this.profileForm.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe(() => this.cdr.markForCheck());
  }
}
```

### `FormArrayDirective` для массива формы верхнего уровня {: #using-formarraydirective-for-top-level-form-arrays}

`FormArray` можно привязать прямо к элементу `<form>` через `FormArrayDirective`.
Это удобно, когда у формы нет `FormGroup` верхнего уровня и сам массив представляет всю модель формы.

```ts
import {Component} from '@angular/core';
import {FormArray, FormControl} from '@angular/forms';

@Component({
  selector: 'form-array-example',
  template: `
    <form [formArray]="form">
      @for (control of form.controls; track $index) {
        <input [formControlName]="$index" />
      }
    </form>
  `,
})
export class FormArrayExampleComponent {
  controls = [new FormControl('fish'), new FormControl('cat'), new FormControl('dog')];

  form = new FormArray(this.controls);
}
```

### Добавление псевдонима {: #add-an-alias}

Сначала в форме одно поле `Alias`. Чтобы добавить ещё, нажмите кнопку **Add Alias**. Массив псевдонимов можно сверить с моделью формы: её показывает `Form Value` внизу шаблона. Вместо отдельного элемента управления на каждый псевдоним можно собрать ещё одну группу с дополнительными полями. Элемент для каждого пункта описывается так же.

## Единый поток событий изменения состояния {: #unified-control-state-change-events}

Все элементы управления отдают единый поток **событий изменения состояния** через observable `events` у `AbstractControl` (`FormControl`, `FormGroup`, `FormArray` и `FormRecord`).
Этот поток реагирует на изменения **значения**, **статуса**, состояний **pristine**, **touched** и **reset**, а также на **действия уровня формы**, например **submit**. Все обновления можно обработать одной подпиской, не связывая несколько observable.

### Типы событий {: #event-types}

Каждый элемент, который отдаёт `events`, — экземпляр конкретного класса события:

-   **`ValueChangeEvent`** — когда меняется **значение** элемента управления.
-   **`StatusChangeEvent`** — когда **статус проверки** переходит в одно из значений `FormControlStatus` (`VALID`, `INVALID`, `PENDING` или `DISABLED`).
-   **`PristineChangeEvent`** — когда меняется состояние **pristine/dirty**.
-   **`TouchedChangeEvent`** — когда меняется состояние **touched/untouched**.
-   **`FormResetEvent`** — когда элемент или форма сбрасываются через API `reset()` или нативным действием.
-   **`FormSubmittedEvent`** — когда форму отправляют.

Все классы событий расширяют `ControlEvent` и содержат ссылку `source` на `AbstractControl`, от которого пошло изменение. В больших формах это полезно.

```ts
import {Component} from '@angular/core';
import {
  FormControl,
  ValueChangeEvent,
  StatusChangeEvent,
  PristineChangeEvent,
  TouchedChangeEvent,
  FormResetEvent,
  FormSubmittedEvent,
  ReactiveFormsModule,
  FormGroup,
} from '@angular/forms';

@Component(/* ... */)
export class UnifiedEventsBasicComponent {
  form = new FormGroup({
    username: new FormControl(''),
  });

  constructor() {
    this.form.events.subscribe((e) => {
      if (e instanceof ValueChangeEvent) {
        console.log('Value changed to: ', e.value);
      }

      if (e instanceof StatusChangeEvent) {
        console.log('Status changed to: ', e.status);
      }

      if (e instanceof PristineChangeEvent) {
        console.log('Pristine status changed to: ', e.pristine);
      }

      if (e instanceof TouchedChangeEvent) {
        console.log('Touched status changed to: ', e.touched);
      }

      if (e instanceof FormResetEvent) {
        console.log('Form was reset');
      }

      if (e instanceof FormSubmittedEvent) {
        console.log('Form was submitted');
      }
    });
  }
}
```

### Отбор нужных событий {: #filtering-specific-events}

Если нужен только часть типов событий, удобнее операторы RxJS.

```ts
import {filter} from 'rxjs/operators';
import {StatusChangeEvent} from '@angular/forms';

control.events
  .pipe(filter((e) => e instanceof StatusChangeEvent))
  .subscribe((e) => console.log('Status:', e.status));
```

### Сведение нескольких подписок в одну {: #unifying-from-multiple-subscriptions}

**До**

```ts
import {combineLatest} from 'rxjs/operators';

combineLatest([control.valueChanges, control.statusChanges]).subscribe(([value, status]) => {
  /* ... */
});
```

**После**

```ts
control.events.subscribe((e) => {
  // Handle ValueChangeEvent, StatusChangeEvent, etc.
});
```

!!! info ""

    При изменении значения событие уходит сразу после обновления значения этого элемента. Значение родителя (например, если этот `FormControl` входит в `FormGroup`) обновляется позже, поэтому чтение значения родителя (через свойство `value`) из обработчика этого события может вернуть ещё не обновлённое значение. Подпишитесь на `events` родительского элемента.

## Управление состоянием элемента управления {: #managing-form-control-state}

Реактивные формы ведут состояние через **touched/untouched** и **pristine/dirty**. Angular обновляет их сам при взаимодействии с DOM, но ими можно управлять и из кода.

**[`markAsTouched`](https://angular.dev/api/forms/FormControl#markAsTouched)** — помечает элемент или форму как touched по событиям фокуса и потери фокуса, которые не меняют значение. По умолчанию состояние поднимается к родительским элементам.

```ts
// Show validation errors after user leaves a field
onEmailBlur() {
  const email = this.form.get('email');
  email.markAsTouched();
}
```

**[`markAsUntouched`](https://angular.dev/api/forms/FormControl#markAsUntouched)** — помечает элемент или форму как untouched. Спускается ко всем дочерним элементам и заново считает статус touched у всех родителей.

```ts
// Reset form state after successful submission
onSubmitSuccess() {
  this.form.markAsUntouched();
  this.form.markAsPristine();
}
```

**[`markAsDirty`](https://angular.dev/api/forms/FormControl#markAsDirty)** — помечает элемент или форму как dirty: значение изменилось. По умолчанию состояние поднимается к родительским элементам.

```ts
// Mark programmatically changed values as modified
autofillAddress() {
  const previousAddress = getAddress();
  this.form.patchValue(previousAddress, { emitEvent: false });
  this.form.markAsDirty();
}
```

**[`markAsPristine`](https://angular.dev/api/forms/FormControl#markAsPristine)** — помечает элемент или форму как pristine. Помечает все дочерние элементы как pristine и заново считает статус pristine у всех родителей.

```ts
// Reset pristine state after saving to track new changes
saveForm() {
  this.api.save(this.form.value).subscribe(() => {
    this.form.markAsPristine();
  });
}
```

**[`markAllAsDirty`](https://angular.dev/api/forms/FormControl#markAllAsDirty)** — помечает элемент или форму и всех потомков как dirty.

```ts
// Mark imported data as dirty
loadData(data: FormData) {
  this.form.patchValue(data);
  this.form.markAllAsDirty();
}
```

**[`markAllAsTouched`](https://angular.dev/api/forms/FormControl#markAllAsTouched)** — помечает элемент или форму и всех потомков как touched. Удобно, чтобы показать ошибки проверки по всей форме.

```ts
// Show all validation errors before submission
onSubmit() {
  if (this.form.invalid) {
    this.form.markAllAsTouched();
    return;
  }
  this.saveForm();
}
```

## Управление порождением и распространением событий {: #controlling-event-emission-and-propagation}

Когда элементы управления обновляют из кода, можно точно задать, как изменения идут по иерархии формы и порождаются ли события.

### Порождение событий {: #understanding-event-emission}

По умолчанию `emitEvent: true`: любое изменение элемента порождает события в observable `valueChanges` и `statusChanges`. Значение `emitEvent: false` подавляет эти события. Это полезно, когда значение задают из кода и не хотят запускать реактивное поведение вроде автосохранения, когда нужно избежать циклических обновлений между элементами или когда при массовом обновлении событие должно уйти один раз в конце.

```ts
@Component({/* ... */})
export class BlogPostEditor {
  postForm = new FormGroup({
    title: new FormControl(''),
    content: new FormControl(''),
  });

  constructor() {
    // Auto-save draft every time user types
    this.postForm.valueChanges.subscribe((formValue) => {
      this.autosaveDraft(formValue);
    });
  }

  loadExistingDraft(savedDraft: {title: string; content: string}) {
    // Restore draft without triggering auto-save
    this.postForm.setValue(savedDraft, {emitEvent: false});
  }
}
```

### Управление распространением {: #understanding-propagation-control}

По умолчанию `onlySelf: false`: обновления поднимаются к родительским элементам и заново считают их значения и статус проверки. Значение `onlySelf: true` оставляет обновление на текущем элементе и не уведомляет родителя. Это удобно в пакетных операциях, когда родительское обновление запускают вручную один раз.

```ts
updatePostalCodeValidator(country: string) {
  const postal = this.addressForm.get('postalCode');

  const validators = country === 'US'
    ? [Validators.maxLength(5)]
    : [Validators.maxLength(7)];

  postal.setValidators(validators);
  postal.updateValueAndValidity({ onlySelf: true, emitEvent: false });
}
```

!!! tip ""

    Как динамически управлять валидаторами во время работы — в разделе [Динамическое управление валидаторами в реактивных формах](https://angular.dev/guide/forms/form-validation#managing-validators-dynamically-in-reactive-forms) руководства по проверке формы.

## Вспомогательные функции сужения типа элемента управления {: #utility-functions-for-narrowing-form-control-types}

В Angular есть четыре вспомогательные функции: они определяют конкретный тип `AbstractControl`. Эти функции работают как **охранники типа** и сужают тип элемента, когда возвращают `true`. Тогда внутри того же блока можно безопасно обращаться к свойствам конкретного подтипа.

| Вспомогательная функция | Подробности                                             |
| :--------------- | :-------------------------------------------------- |
| `isFormControl`  | Возвращает `true`, если элемент — `FormControl`. |
| `isFormGroup`    | Возвращает `true`, если элемент — `FormGroup`.    |
| `isFormRecord`   | Возвращает `true`, если элемент — `FormRecord`.   |
| `isFormArray`    | Возвращает `true`, если элемент — `FormArray`.    |

Особенно полезны эти функции в **своих валидаторах**: сигнатура получает `AbstractControl`, а логика рассчитана на конкретный вид элемента.

```ts
import {AbstractControl, isFormArray} from '@angular/forms';

export function positiveValues(control: AbstractControl) {
  if (!isFormArray(control)) {
    return null; // Not a FormArray: validator is not applicable.
  }

  // Safe to access FormArray-specific API after narrowing.
  const hasNegative = control.controls.some((c) => c.value < 0);
  return hasNegative ? {positiveValues: true} : null;
}
```

## Сводка API реактивных форм {: #reactive-forms-api-summary}

В таблице ниже — базовые классы и сервисы, которыми создают элементы реактивных форм и управляют ими.
Полный синтаксис — в справочнике API [пакета Forms](https://angular.dev/api#angular_forms 'Справочник API').

### Классы {: #classes}

| Класс             | Подробности                                                                                                                                                                                 |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AbstractControl` | Абстрактный базовый класс для конкретных классов `FormControl`, `FormGroup` и `FormArray`. Задаёт их общее поведение и свойства.                           |
| `FormControl`     | Ведёт значение и статус валидности отдельного элемента управления. Соответствует HTML-элементу формы, например `<input>` или `<select>`.                                            |
| `FormGroup`       | Ведёт значение и состояние валидности группы экземпляров `AbstractControl`. В свойства группы входят дочерние элементы. Форма верхнего уровня в компоненте — это `FormGroup`. |
| `FormArray`       | Ведёт значение и состояние валидности массива экземпляров `AbstractControl` с числовыми индексами.                                                                                     |
| `FormBuilder`     | Внедряемый сервис с фабричными методами для создания экземпляров элементов управления.                                                                                                     |
| `FormRecord`      | Отслеживает значение и состояние валидности набора экземпляров `FormControl` с одним и тем же типом значения.                                                                  |

### Директивы {: #directives}

| Директива              | Подробности                                                                                    |
| :--------------------- | :----------------------------------------------------------------------------------------- |
| `FormControlDirective` | Синхронизирует автономный экземпляр `FormControl` с элементом формы.                       |
| `FormControlName`      | Синхронизирует `FormControl` в существующем экземпляре `FormGroup` с элементом формы по имени. |
| `FormGroupDirective`   | Синхронизирует существующий экземпляр `FormGroup` с элементом DOM.                                   |
| `FormGroupName`        | Синхронизирует вложенный экземпляр `FormGroup` с элементом DOM.                                      |
| `FormArrayName`        | Синхронизирует вложенный экземпляр `FormArray` с элементом DOM.                                      |
| `FormArrayDirective`   | Синхронизирует автономный экземпляр `FormArray` с элементом DOM.                                  |


---

Источник: [https://angular.dev/guide/forms/reactive-forms](https://angular.dev/guide/forms/reactive-forms)
