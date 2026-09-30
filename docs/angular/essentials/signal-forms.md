---
description: "Сигнальные формы хранят состояние в сигналах Angular и сами синхронизируют модель данных с интерфейсом."
---

# Формы с сигналами {: #forms-with-signals}

:date: 30.09.2026

Сигнальные формы хранят состояние в сигналах Angular и сами синхронизируют модель данных с интерфейсом.

Это руководство проводит по основным понятиям сигнальных форм. Как это устроено:

## Первая форма {: #creating-your-first-form}

### 1. Модель формы через `signal()` {: #1-create-a-form-model-with-signal}

Любая форма начинается с сигнала, в котором лежит модель данных:

```ts
interface LoginData {
  email: string;
  password: string;
}

const loginModel = signal<LoginData>({
  email: '',
  password: '',
});
```

### 2. Передача модели в `form()` и получение `FieldTree` {: #2-pass-the-form-model-to-form-to-create-a-fieldtree}

Затем модель передают в функцию `form()` и получают **дерево полей** — структуру, которая повторяет форму модели. К полям обращаются через точку.

И корневой объект формы, и вложенные свойства — это узлы `FieldTree`:

```ts
const loginForm = form(loginModel);

loginForm; // is a FieldTree
loginForm.email; // is also a FieldTree
```

### 3. Привязка полей HTML директивой `[formField]` {: #3-bind-html-inputs-with-formfield-directive}

Дальше поля HTML привязывают к форме директивой `[formField]`. Между полем и моделью появляется двусторонняя привязка:

```html
<input type="email" [formField]="loginForm.email" />
<input type="password" [formField]="loginForm.password" />
```

Ввод пользователя, например набор текста в поле, сам обновляет форму.

!!! info ""

    Директива `[formField]` также синхронизирует состояние поля с атрибутами `required`, `disabled` и `readonly`, когда это уместно.

### 4. Чтение состояния через сигналы `FieldTree` {: #4-read-state-with-fieldtree-signals}

Состояние любой части дерева читают вызовом узла `FieldTree` как функции. Вернётся объект состояния с реактивными сигналами значения, статуса проверки и взаимодействия:

```ts
loginForm(); // Returns state for the whole form
loginForm.email(); // Returns state for the email field
```

Текущее значение лежит в сигнале `value()`:

```html
<!-- Render values that update automatically as user types -->
<p>Form value: {{ loginForm().value() | json }}</p>
<p>Email: {{ loginForm.email().value() }}</p>
```

```ts
// Get the current value
const currentEmail = loginForm.email().value();
```

### 5. Обновление значений через `set()` {: #5-update-values-with-set}

Значение можно задать из кода методом `value.set()` на любом узле. Так обновляются и `FieldTree`, и сигнал модели под ним:

```ts
// Update the value programmatically
loginForm.email().value.set('alice@wonderland.com');
```

В итоге и значение поля, и сигнал модели обновляются сами:

```ts
// The model signal is also updated
console.log(loginModel().email); // 'alice@wonderland.com'
```

### Полный пример {: #complete-example}

=== "app.ts"

    ```ts
    import {Component, signal} from '@angular/core';
    import {form, FormField} from '@angular/forms/signals';

    interface LoginData {
      email: string;
      password: string;
    }

    @Component({
      selector: 'app-root',
      templateUrl: 'app.html',
      styleUrl: 'app.css',
      imports: [FormField],
    })
    export class App {
      loginModel = signal<LoginData>({
        email: '',
        password: '',
      });

      loginForm = form(this.loginModel);

      onSubmit(event: Event) {
        event.preventDefault();

        // Perform login logic here
        const credentials = this.loginModel();
        console.log('Logging in with:', credentials);

        // e.g., await this.authService.login(credentials);
      }
    }
    ```

=== "app.html"

    ```html
    <form (submit)="onSubmit($event)">
      <label>
        Email:
        <input type="email" [formField]="loginForm.email" />
      </label>

      <label>
        Password:
        <input type="password" [formField]="loginForm.password" />
      </label>

      <p>Hello {{ loginForm.email().value() }}!</p>
      <p>Password length: {{ loginForm.password().value().length }}</p>

      <button type="submit">Log In</button>
    </form>
    ```

=== "app.css"

    ```css
    form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      max-width: 400px;
      padding: 1rem;
      font-family: Inter, system-ui, -apple-system, sans-serif;
    }

    label {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }

    input {
      padding: 0.5rem;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1rem;
      font-family: inherit;
    }

    p {
      margin: 0.5rem 0;
      color: #666;
    }
    ```

## Базовое использование {: #basic-usage}

Директива `[formField]` работает со всеми стандартными типами полей HTML. Ниже самые частые схемы.

### Текстовые поля {: #text-inputs}

Текстовые поля работают с разными атрибутами `type` и с `textarea`:

```html
<!-- Text and email -->
<input type="text" [formField]="form.name" />
<input type="email" [formField]="form.email" />
```

#### Числа {: #numbers}

Числовые поля сами переводят строку в число и обратно:

```html
<!-- Number - automatically converts to number type -->
<input type="number" [formField]="form.age" />
```

#### Дата и время {: #date-and-time}

Поля даты хранят значение строкой `YYYY-MM-DD`, поля времени — в формате `HH:mm`:

```html
<!-- Date and time - stores as ISO format strings -->
<input type="date" [formField]="form.eventDate" />
<input type="time" [formField]="form.eventTime" />
```

Чтобы превратить строку даты в объект `Date`, передайте значение поля в `Date()`:

```ts
const dateObject = new Date(form.eventDate().value());
```

#### Многострочный текст {: #multiline-text}

`textarea` работает так же, как текстовое поле:

```html
<!-- Textarea -->
<textarea [formField]="form.message" rows="4"></textarea>
```

### Флажки {: #checkboxes}

Флажки привязываются к логическим значениям:

```html
<!-- Single checkbox -->
<label>
  <input type="checkbox" [formField]="form.agreeToTerms" />
  I agree to the terms
</label>
```

#### Несколько флажков {: #multiple-checkboxes}

Для нескольких вариантов заведите отдельное логическое поле `formField` на каждый:

```html
<label>
  <input type="checkbox" [formField]="form.emailNotifications" />
  Email notifications
</label>
<label>
  <input type="checkbox" [formField]="form.smsNotifications" />
  SMS notifications
</label>
```

### Переключатели {: #radio-buttons}

Переключатели устроены похоже на флажки. Если у них один и тот же `[formField]`, сигнальные формы сами проставят всем один атрибут `name`:

```html
<label>
  <input type="radio" value="free" [formField]="form.plan" />
  Free
</label>
<label>
  <input type="radio" value="premium" [formField]="form.plan" />
  Premium
</label>
```

Когда пользователь выбирает переключатель, `formField` формы сохраняет значение из атрибута `value` этого переключателя. Например, выбор «Premium» записывает в `form.plan().value()` значение `"premium"`.

### Выпадающие списки {: #select-dropdowns}

Элемент `select` работает и со статическими, и с динамическими вариантами:

```html
<!-- Static options -->
<select [formField]="form.country">
  <option value="">Select a country</option>
  <option value="us">United States</option>
  <option value="ca">Canada</option>
</select>

<!-- Dynamic options with @for -->
<select [formField]="form.productId">
  <option value="">Select a product</option>
  @for (product of products; track product.id) {
    <option [value]="product.id">{{ product.name }}</option>
  }
</select>
```

!!! info ""

    Множественный выбор (`<select multiple>`) директива `[formField]` пока не поддерживает.

## Проверка и состояние {: #validation-and-state}

В сигнальных формах есть встроенные валидаторы для полей. Чтобы включить проверку, передайте функцию схемы вторым аргументом `form()`:

```ts
const loginForm = form(loginModel, (schemaPath) => {
  debounce(schemaPath.email, 500);
  required(schemaPath.email);
  email(schemaPath.email);
});
```

Функция схемы получает параметр **пути схемы**: через него задают правила проверки для полей.

Частые валидаторы:

-   **`required()`** — поле обязательно должно иметь значение
-   **`email()`** — проверяет формат адреса электронной почты
-   **`min()`** / **`max()`** — проверяет диапазон числа
-   **`minLength()`** / **`maxLength()`** — проверяет длину строки или коллекции
-   **`pattern()`** — проверяет значение по регулярному выражению

Текст ошибки задают объектом параметров вторым аргументом валидатора:

```ts
required(schemaPath.email, {message: 'Email is required'});
email(schemaPath.email, {message: 'Please enter a valid email address'});
```

Каждый узел `FieldTree` отдаёт состояние проверки и взаимодействия реактивными сигналами.

### Сигналы состояния FieldTree {: #fieldtree-state-signals}

У каждого узла дерева, включая корневой объект формы, один и тот же набор сигналов. Поскольку каждый узел — это `FieldTree`, API проверки и отслеживания взаимодействия одинаков на любом уровне.

| Состояние | Описание |
| --------- | -------- |
| `valid()` | Возвращает `true`, если узел проходит все правила проверки |
| `invalid()` | Возвращает `true`, если есть ошибки проверки |
| `pending()` | Возвращает `true`, если идёт асинхронная проверка |
| `touched()` | Возвращает `true`, если пользователь фокусировал поле или любое дочернее поле и уводил с него фокус |
| `dirty()` | Возвращает `true`, если пользователь изменил значение |
| `disabled()` | Возвращает `true`, если узел отключён |
| `readonly()` | Возвращает `true`, если узел только для чтения |
| `errors()` | Возвращает массив ошибок проверки со свойствами `kind` и `message` |

### Полный пример {: #complete-example-validation}

=== "app.ts"

    ```ts
    import {Component, signal} from '@angular/core';
    import {email, form, FormField, required} from '@angular/forms/signals';

    interface LoginData {
      email: string;
      password: string;
    }

    @Component({
      selector: 'app-root',
      templateUrl: 'app.html',
      styleUrl: 'app.css',
      imports: [FormField],
    })
    export class App {
      loginModel = signal<LoginData>({
        email: '',
        password: '',
      });

      loginForm = form(this.loginModel, (schemaPath) => {
        required(schemaPath.email, {message: 'Email is required'});
        email(schemaPath.email, {message: 'Enter a valid email address'});

        required(schemaPath.password, {message: 'Password is required'});
      });

      onSubmit(event: Event) {
        event.preventDefault();
        // Perform login logic here
        const credentials = this.loginModel();
        console.log('Logging in with:', credentials);
        // e.g., await this.authService.login(credentials);
      }
    }
    ```

=== "app.html"

    ```html
    <form (submit)="onSubmit($event)">
      <div>
        <label>
          Email:
          <input type="email" [formField]="loginForm.email" />
        </label>

        @if (loginForm.email().touched() && loginForm.email().invalid()) {
          <ul class="error-list">
            @for (error of loginForm.email().errors(); track error) {
              <li>{{ error.message }}</li>
            }
          </ul>
        }
      </div>

      <div>
        <label>
          Password:
          <input type="password" [formField]="loginForm.password" />
        </label>

        @if (loginForm.password().touched() && loginForm.password().invalid()) {
          <div class="error-list">
            @for (error of loginForm.password().errors(); track error) {
              <p>{{ error.message }}</p>
            }
          </div>
        }
      </div>

      <button type="submit">Log In</button>
    </form>
    ```

=== "app.css"

    ```css
    form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      max-width: 400px;
      padding: 1rem;
      font-family:
        Inter,
        system-ui,
        -apple-system,
        sans-serif;
    }

    div {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }

    label {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      font-weight: 500;
    }

    input {
      padding: 0.5rem;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1rem;
      font-family: inherit;
    }

    input:focus {
      outline: none;
      border-color: #4285f4;
    }

    button {
      padding: 0.75rem 1.5rem;
      background-color: #4285f4;
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 1rem;
      font-family: inherit;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    button:hover {
      background-color: #357ae8;
    }

    button:active {
      background-color: #2a65c8;
    }

    .error-list {
      color: red;
      font-size: 0.875rem;
      margin: 0.25rem 0 0 0;
      padding-left: 0;
      list-style-position: inside;
    }

    .error-list p {
      margin: 0;
    }
    ```

## Следующие шаги {: #next-steps}

Подробнее о сигнальных формах и о том, как они устроены, — в подробных руководствах:

-   [Обзор](../forms/signals/overview.md) — введение в сигнальные формы и когда их использовать
-   [Модели форм](https://angular.dev/guide/forms/signals/models) — создание данных формы и работа с ними через сигналы
-   [Управление состоянием полей](https://angular.dev/guide/forms/signals/field-state-management) — проверка, отслеживание взаимодействия и видимость полей
-   [Проверка](https://angular.dev/guide/forms/signals/validation) — встроенные валидаторы, свои правила и асинхронная проверка

-   [Модульное устройство через инъекцию зависимостей](dependency-injection.md)


---

Источник: [https://angular.dev/essentials/signal-forms](https://angular.dev/essentials/signal-forms)
