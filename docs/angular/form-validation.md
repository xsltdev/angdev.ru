# Проверка вводимых данных

:date: 28.02.2022

Вы можете улучшить общее качество данных, проверяя вводимые пользователем данные на точность и полноту. На этой странице показано, как проверять пользовательский ввод из пользовательского интерфейса и отображать полезные сообщения о проверке как в реактивных формах, так и в формах, управляемых шаблонами.

## Предварительные условия

Прежде чем читать о валидации форм, вы должны иметь базовое представление о следующем.

-   [TypeScript](https://www.typescriptlang.org/) и программирование на HTML5.
-   Фундаментальные концепции [дизайна приложений Angular](architecture.md)
-   [два типа форм, которые поддерживает Angular](forms-overview.md)
-   Основы [Template-driven Forms](forms.md) или [Reactive Forms](reactive-forms.md)

!!!note ""

    Получите полный код примера для реактивных и управляемых шаблонами форм, используемых здесь для иллюстрации валидации формы. Запустите [пример](https://angular.io/generated/live-examples/form-validation/stackblitz.html).

## Валидация ввода в формах, управляемых шаблонами {: #template-driven-validation}

Чтобы добавить валидацию в форму, управляемую шаблоном, вы добавляете те же атрибуты валидации, что и в [встроенная валидация HTML-формы](https://developer.mozilla.org/docs/Web/Guide/HTML/HTML5/Constraint_validation). Angular использует директивы для согласования этих атрибутов с функциями валидатора во фреймворке.

Каждый раз, когда значение элемента управления формы изменяется, Angular выполняет валидацию и генерирует либо список ошибок валидации, что приводит к статусу `INVALID`, либо `null`, что приводит к статусу `VALID`.

Затем вы можете проверить состояние элемента управления, экспортировав `ngModel` в локальную переменную шаблона. Следующий пример экспортирует `NgModel` в переменную с именем `name`:

```html
<input
    type="text"
    id="name"
    name="name"
    class="form-control"
    required
    minlength="4"
    appForbiddenName="bob"
    [(ngModel)]="hero.name"
    #name="ngModel"
/>

<div
    *ngIf="name.invalid && (name.dirty || name.touched)"
    class="alert"
>
    <div *ngIf="name.errors?.['required']">
        Name is required.
    </div>
    <div *ngIf="name.errors?.['minlength']">
        Name must be at least 4 characters long.
    </div>
    <div *ngIf="name.errors?.['forbiddenName']">
        Name cannot be Bob.
    </div>
</div>
```

Обратите внимание на следующие особенности, проиллюстрированные в примере.

-   Элемент `input` несет атрибуты проверки HTML: `required` и `minlength`.

    Он также содержит пользовательскую директиву валидатора, `forbiddenName`.

    Для получения дополнительной информации смотрите раздел [Пользовательские валидаторы](#custom-validators).

-   `#name="ngModel"` экспортирует `NgModel` в локальную переменную `name`.

    `NgModel` отражает многие свойства своего базового экземпляра `FormControl`, поэтому вы можете использовать его в шаблоне для проверки состояний элемента управления, таких как `valid` и `dirty`.

    Полный список свойств элементов управления приведен в справочнике API [AbstractControl](https://angular.io/api/forms/AbstractControl).

    -   Функция `*ngIf` на элементе `div` раскрывает набор вложенных сообщений `div`, но только если `name` недействительно и элемент управления либо `dirty`, либо `touched`.

    -   Каждый вложенный `div` может представлять пользовательское сообщение для одной из возможных ошибок валидации.

        Существуют сообщения для `required`, `minlength` и `forbiddenName`.

!!!note ""

    Чтобы валидатор не выводил ошибки до того, как у пользователя появится возможность редактировать форму, необходимо проверить наличие у элемента управления состояния `dirty` или `touched`.

    -   Когда пользователь изменяет значение в наблюдаемом поле, элемент управления помечается как "грязный".

    -   Когда пользователь размывает элемент управления формы, элемент управления помечается как "тронутый".

## Проверка ввода в реактивных формах {: #reactive-form-validation}

В реактивной форме источником истины является класс компонента. Вместо того чтобы добавлять валидаторы через атрибуты в шаблоне, вы добавляете функции валидатора непосредственно в модель элемента управления формы в классе компонента.

Затем Angular вызывает эти функции при каждом изменении значения элемента управления.

### Функции валидатора

Функции валидатора могут быть как синхронными, так и асинхронными.

| Тип валидатора         | Подробности                                                                                                                                                                                                                                         |
| :--------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Синхронные валидаторы  | Синхронные функции, которые принимают экземпляр элемента управления и немедленно возвращают либо набор ошибок валидации, либо `null`. Передайте их в качестве второго аргумента при инстанцировании `FormControl`.                                  |
| Асинхронные валидаторы | Асинхронные функции, которые принимают экземпляр элемента управления и возвращают `Promise` или `Observable`, которые позже выдают набор ошибок валидации или `null`. Передайте их в качестве третьего аргумента при инстанцировании `FormControl`. |

По соображениям производительности, Angular запускает асинхронные валидаторы только в том случае, если все синхронные валидаторы прошли. Каждый из них должен завершиться до появления ошибок.

### Встроенные функции валидатора

Вы можете выбрать [написать свои собственные функции валидатора](#custom-validators) или использовать некоторые встроенные валидаторы Angular.

Те же встроенные валидаторы, которые доступны как атрибуты в формах, управляемых шаблонами, такие как `required` и `minlength`, доступны для использования в качестве функций класса `Validators`. Полный список встроенных валидаторов приведен в справочнике API [Validators](https://angular.io/api/forms/Validators).

Чтобы обновить форму героя и сделать ее реактивной, используйте некоторые из тех же встроенных валидаторов &mdash; на этот раз в форме функции, как в следующем примере.

```ts
ngOnInit(): void {
  this.heroForm = new FormGroup({
    name: new FormControl(this.hero.name, [
      Validators.required,
      Validators.minLength(4),
      forbiddenNameValidator(/bob/i) // <-- Here's how you pass in the custom validator.
    ]),
    alterEgo: new FormControl(this.hero.alterEgo),
    power: new FormControl(this.hero.power, Validators.required)
  });

}

get name() { return this.heroForm.get('name'); }

get power() { return this.heroForm.get('power'); }
```

В этом примере элемент управления `name` устанавливает два встроенных валидатора &mdash; `Validators.required` и `Validators.minLength(4)` &mdash; и один пользовательский валидатор, `forbiddenNameValidator`. (Подробнее смотрите [пользовательские валидаторы](#custom-validators).)

Все эти валидаторы являются синхронными, поэтому они передаются в качестве второго аргумента. Обратите внимание, что вы можете поддерживать несколько валидаторов, передавая функции в виде массива.

Этот пример также добавляет несколько методов getter. В реактивной форме вы всегда можете получить доступ к любому элементу управления формы через метод `get` его родительской группы, но иногда полезно определить геттеры как сокращение шаблона.

Если вы снова посмотрите на шаблон для ввода `name`, то он довольно похож на пример с шаблоном.

```html
<input
    type="text"
    id="name"
    class="form-control"
    formControlName="name"
    required
/>

<div
    *ngIf="name.invalid && (name.dirty || name.touched)"
    class="alert alert-danger"
>
    <div *ngIf="name.errors?.['required']">
        Name is required.
    </div>
    <div *ngIf="name.errors?.['minlength']">
        Name must be at least 4 characters long.
    </div>
    <div *ngIf="name.errors?.['forbiddenName']">
        Name cannot be Bob.
    </div>
</div>
```

Эта форма отличается от версии, основанной на шаблонах, тем, что она больше не экспортирует никаких директив. Вместо этого она использует геттер `name`, определенный в классе компонента.

Обратите внимание, что атрибут `required` все еще присутствует в шаблоне. Хотя он не нужен для валидации, его следует сохранить в целях доступности.

## Определение пользовательских валидаторов {: #custom-validators}

Встроенные валидаторы не всегда соответствуют конкретному случаю использования вашего приложения, поэтому иногда необходимо создать пользовательский валидатор.

Рассмотрим функцию `forbiddenNameValidator` из предыдущих примеров [reactive-form](#reactive-component-class). Вот как выглядит определение этой функции.

```ts
/** A hero's name can't match the given regular expression */
export function forbiddenNameValidator(
    nameRe: RegExp
): ValidatorFn {
    return (
        control: AbstractControl
    ): ValidationErrors | null => {
        const forbidden = nameRe.test(control.value);
        return forbidden
            ? { forbiddenName: { value: control.value } }
            : null;
    };
}
```

Функция представляет собой фабрику, которая принимает регулярное выражение для определения _конкретного_ запрещенного имени и возвращает функцию валидатора.

В данном примере запрещенным именем является "bob", поэтому валидатор отклоняет любое имя героя, содержащее "bob". В других местах он может отклонить "alice" или любое имя, которому соответствует конфигурирующее регулярное выражение.

Фабрика `forbiddenNameValidator` возвращает настроенную функцию валидатора. Эта функция принимает объект управления Angular и возвращает либо `null`, если значение элемента управления действительно, либо объект ошибки валидации.

Объект ошибки валидации обычно имеет свойство, имя которого — ключ валидации, `'forbiddenName'`, а значение — произвольный словарь значений, которые можно вставить в сообщение об ошибке, `{name}`.

Пользовательские валидаторы async похожи на валидаторы sync, но вместо этого они должны возвращать Promise или наблюдаемую, которая позже выдает `null` или объект ошибки валидации. В случае с наблюдаемой, она должна завершиться, после чего форма использует последнее выданное значение для валидации.

### Добавление пользовательских валидаторов в реактивные формы {: #adding-to-reactive-forms}

В реактивные формы можно добавить пользовательский валидатор, передав функцию непосредственно в `FormControl`.

```ts
this.heroForm = new FormGroup({
    name: new FormControl(this.hero.name, [
        Validators.required,
        Validators.minLength(4),
        forbiddenNameValidator(/bob/i), // <-- Here's how you pass in the custom validator.
    ]),
    alterEgo: new FormControl(this.hero.alterEgo),
    power: new FormControl(
        this.hero.power,
        Validators.required
    ),
});
```

### Добавление пользовательских валидаторов в формы, управляемые шаблонами {: #adding-to-template-driven-forms}

В формах, управляемых шаблонами, добавьте директиву в шаблон, где директива обертывает функцию валидатора. Например, соответствующая директива `ForbiddenValidatorDirective` служит оберткой для `forbiddenNameValidator`.

Angular распознает роль директивы в процессе валидации, поскольку директива регистрирует себя с провайдером `NG_VALIDATORS`, как показано в следующем примере. `NG_VALIDATORS` — это предопределенный провайдер с расширяемой коллекцией валидаторов.

```ts
providers: [
    {
        provide: NG_VALIDATORS,
        useExisting: ForbiddenValidatorDirective,
        multi: true,
    },
];
```

Затем класс директивы реализует интерфейс `Validator`, чтобы его можно было легко интегрировать с формами Angular. Ниже приведена остальная часть директивы, чтобы вы могли получить представление о том, как все это работает.

```ts
@Directive({
    selector: '[appForbiddenName]',
    providers: [
        {
            provide: NG_VALIDATORS,
            useExisting: ForbiddenValidatorDirective,
            multi: true,
        },
    ],
})
export class ForbiddenValidatorDirective
    implements Validator {
    @Input('appForbiddenName') forbiddenName = '';

    validate(
        control: AbstractControl
    ): ValidationErrors | null {
        return this.forbiddenName
            ? forbiddenNameValidator(
                  new RegExp(this.forbiddenName, 'i')
              )(control)
            : null;
    }
}
```

Когда `ForbiddenValidatorDirective` готова, вы можете добавить ее селектор, `appForbiddenName`, к любому элементу ввода, чтобы активировать его. Например:

```html
<input
    type="text"
    id="name"
    name="name"
    class="form-control"
    required
    minlength="4"
    appForbiddenName="bob"
    [(ngModel)]="hero.name"
    #name="ngModel"
/>
```

!!!note ""

    Обратите внимание, что пользовательская директива валидации инстанцируется с помощью `useExisting`, а не `useClass`. Зарегистрированный валидатор должен быть _этим экземпляром_ директивы `ForbiddenValidatorDirective` &mdash; экземпляром в форме с его свойством `forbiddenName`, привязанным к "bob".

    Если вы замените `useExisting` на `useClass`, то вы зарегистрируете новый экземпляр класса, у которого нет `forbiddenName`.

## CSS-классы состояния элемента управления

Angular автоматически отображает многие свойства элементов управления на элемент управления формы в виде классов CSS. Используйте эти классы для стилизации элементов управления формой в зависимости от состояния формы.

В настоящее время поддерживаются следующие классы.

-   `.ng-valid`
-   `.ng-invalid`
-   `.ng-pending`
-   `.ng-pristine`
-   `.ng-dirty`
-   `.ng-untouched`
-   `.ng-touched`
-   `.ng-submitted` (заключающий элемент формы только)

В следующем примере форма героя использует классы `.ng-valid` и `.ng-invalid` для установки цвета границы каждого элемента формы.

```css
.ng-valid[required],
.ng-valid.required {
    border-left: 5px solid #42a948; /* green */
}

.ng-invalid:not(form) {
    border-left: 5px solid #a94442; /* red */
}

.alert div {
    background-color: #fed3d3;
    color: #820000;
    padding: 1rem;
    margin-bottom: 1rem;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
}

select {
    width: 100%;
    padding: 0.5rem;
}
```

## Валидация перекрестных полей

Межполевой валидатор — это [пользовательский валидатор](#custom-validators), который сравнивает значения различных полей в форме и принимает или отвергает их в комбинации. Например, у вас может быть форма, предлагающая взаимно несовместимые варианты, так что пользователь может выбрать A или B, но не оба.

Значения одних полей могут зависеть от других; пользователю может быть разрешено выбрать B только в том случае, если он также выбрал A.

Следующие примеры перекрестной валидации показывают, как сделать следующее:

-   Валидировать реактивный или основанный на шаблоне ввод формы на основе значений двух родственных элементов управления,
-   показать описательное сообщение об ошибке после того, как пользователь взаимодействовал с формой и проверка не прошла.

В примерах используется перекрестная валидация, чтобы убедиться, что герои не раскрывают свою истинную личность, заполняя форму героя. Валидаторы проверяют, что имена героев и их альтер-эго не совпадают.

### Добавление перекрестной проверки в реактивные формы

Форма имеет следующую структуру:

```js
const heroForm = new FormGroup({
    name: new FormControl(),
    alterEgo: new FormControl(),
    power: new FormControl(),
});
```

Обратите внимание, что элементы управления `name` и `alterEgo` являются родственными элементами управления. Чтобы оценить оба элемента управления в одном пользовательском валидаторе, вы должны выполнить проверку в общем элементе управления-предке: `FormGroup`.
Вы запрашиваете `FormGroup` для его дочерних элементов управления, чтобы сравнить их значения.

Чтобы добавить валидатор в `FormGroup`, передайте новый валидатор в качестве второго аргумента при создании.

```js
const heroForm = new FormGroup(
    {
        name: new FormControl(),
        alterEgo: new FormControl(),
        power: new FormControl(),
    },
    { validators: identityRevealedValidator }
);
```

Код валидатора выглядит следующим образом.

```ts
/** A hero's name can't match the hero's alter ego */
export const identityRevealedValidator: ValidatorFn = (
    control: AbstractControl
): ValidationErrors | null => {
    const name = control.get('name');
    const alterEgo = control.get('alterEgo');

    return name && alterEgo && name.value === alterEgo.value
        ? { identityRevealed: true }
        : null;
};
```

Валидатор `identity` реализует интерфейс `ValidatorFn`. Он принимает в качестве аргумента объект элемента управления Angular и возвращает либо null, если форма валидна, либо `ValidationErrors` в противном случае.

Валидатор получает дочерние элементы управления, вызывая метод `FormGroup` [get](https://angular.io/api/forms/AbstractControl#get), затем сравнивает значения элементов управления `name` и `alterEgo`.

Если значения не совпадают, личность героя остается тайной, оба элемента являются действительными, и валидатор возвращает null. Если они совпадают, личность героя раскрывается, и валидатор должен пометить форму как недействительную, вернув объект ошибки.

Для улучшения пользовательского опыта шаблон показывает соответствующее сообщение об ошибке, если форма недействительна.

```html
<div
    *ngIf="heroForm.errors?.['identityRevealed'] && (heroForm.touched || heroForm.dirty)"
    class="cross-validation-error-message alert alert-danger"
>
    Name cannot match alter ego.
</div>
```

Этот `*ngIf` выводит ошибку, если `FormGroup` имеет ошибку кросс-валидации, возвращенную валидатором `identityRevealed`, но только если пользователь закончил [взаимодействие с формой](#dirty-or-touched).

### Добавление перекрестной валидации в формы, управляемые шаблонами

Для формы, управляемой шаблоном, вы должны создать директиву для обертывания функции валидатора. Вы предоставляете эту директиву в качестве валидатора, используя токен [`NG_VALIDATORS`](#adding-to-template-driven-forms), как показано в следующем примере.

```ts
@Directive({
    selector: '[appIdentityRevealed]',
    providers: [
        {
            provide: NG_VALIDATORS,
            useExisting: IdentityRevealedValidatorDirective,
            multi: true,
        },
    ],
})
export class IdentityRevealedValidatorDirective
    implements Validator {
    validate(
        control: AbstractControl
    ): ValidationErrors | null {
        return identityRevealedValidator(control);
    }
}
```

Вы должны добавить новую директиву в HTML-шаблон. Поскольку валидатор должен быть зарегистрирован на самом высоком уровне в форме, следующий шаблон помещает директиву в тег `form`.

```html
<form #heroForm="ngForm" appIdentityRevealed></form>
```

Для повышения удобства пользователей при недействительности формы появляется соответствующее сообщение об ошибке.

```html
<div
    *ngIf="heroForm.errors?.['identityRevealed'] && (heroForm.touched || heroForm.dirty)"
    class="cross-validation-error-message alert"
>
    Name cannot match alter ego.
</div>
```

Это одинаково как для форм, управляемых шаблонами, так и для реактивных форм.

## Создание асинхронных валидаторов

Асинхронные валидаторы реализуют интерфейсы `AsyncValidatorFn` и `AsyncValidator`. Они очень похожи на свои синхронные аналоги, со следующими отличиями.

-   Функции `validate()` должны возвращать Promise или наблюдаемую,

-   Возвращаемая наблюдаемая должна быть конечной, то есть она должна завершиться в какой-то момент.

    Чтобы преобразовать бесконечную наблюдаемую в конечную, пропустите наблюдаемую через оператор фильтрации, такой как `first`, `last`, `take` или `takeUntil`.

Асинхронная проверка происходит после синхронной проверки и выполняется только в случае успешной синхронной проверки. Эта проверка позволяет формам избежать потенциально дорогостоящих процессов асинхронной валидации (таких как HTTP запрос), если более простые методы валидации уже обнаружили недопустимый ввод.

После начала асинхронной проверки элемент управления формой переходит в состояние `отложена`. Проверьте свойство `pending` элемента управления и используйте его для визуальной обратной связи о текущей операции проверки.

Распространенным шаблоном пользовательского интерфейса является отображение спиннера во время выполнения асинхронной валидации. В следующем примере показано, как этого добиться в форме, управляемой шаблоном.

```html
<input
    [(ngModel)]="name"
    #model="ngModel"
    appSomeAsyncValidator
/>
<app-spinner *ngIf="model.pending"></app-spinner>
```

### Реализация пользовательского асинхронного валидатора

В следующем примере асинхронный валидатор гарантирует, что герои выберут альтер-эго, которое еще не занято. Новые герои постоянно поступают на службу, а старые покидают ее, поэтому список доступных альтер-эго невозможно получить заранее.

Для проверки потенциального альтер-эго валидатор должен инициировать асинхронную операцию, чтобы обратиться к центральной базе данных всех ныне зачисленных героев.

Следующий код создает класс валидатора, `UniqueAlterEgoValidator`, который реализует интерфейс `AsyncValidator`.

```ts
@Injectable({ providedIn: 'root' })
export class UniqueAlterEgoValidator
    implements AsyncValidator {
    constructor(private heroesService: HeroesService) {}

    validate(
        control: AbstractControl
    ): Observable<ValidationErrors | null> {
        return this.heroesService
            .isAlterEgoTaken(control.value)
            .pipe(
                map((isTaken) =>
                    isTaken
                        ? { uniqueAlterEgo: true }
                        : null
                ),
                catchError(() => of(null))
            );
    }
}
```

Конструктор инжектирует `HeroesService`, который определяет следующий интерфейс.

```ts
interface HeroesService {
    isAlterEgoTaken: (
        alterEgo: string
    ) => Observable<boolean>;
}
```

В реальном приложении `HeroesService` будет отвечать за выполнение HTTP-запроса к базе данных героев, чтобы проверить, доступен ли альтер-эго. С точки зрения валидатора, фактическая реализация сервиса не важна, поэтому в примере можно просто написать код на основе интерфейса `HeroesService`.

Когда начинается проверка, `UniqueAlterEgoValidator` делегирует методу `HeroesService` `isAlterEgoTaken()` текущее значение элемента управления. В этот момент элемент управления помечается как `pending` и остается в этом состоянии до тех пор, пока не завершится цепочка наблюдаемых, возвращенная из метода `validate()`.

Метод `isAlterEgoTaken()` отправляет HTTP-запрос, который проверяет, доступен ли альтер-эго, и возвращает `Observable<boolean>` в качестве результата. Метод `validate()` передает ответ через оператор `map` и преобразует его в результат проверки.

Затем метод, как и любой другой валидатор, возвращает `null`, если форма действительна, и `ValidationErrors`, если нет. Этот валидатор обрабатывает любые потенциальные ошибки с помощью оператора `catchError`.

В данном случае валидатор рассматривает ошибку `isAlterEgoTaken()` как успешную валидацию, потому что неспособность выполнить запрос валидации не обязательно означает, что альтер-эго недействительно.

Вы можете обработать ошибку по-другому и вернуть вместо нее объект `ValidationError`.

По истечении некоторого времени цепочка наблюдаемых завершается, и асинхронная валидация завершается. Флаг `pending` устанавливается в `false`, а валидность формы обновляется.

### Добавление асинхронных валидаторов в реактивные формы

Чтобы использовать асинхронный валидатор в реактивных формах, начните с инъекции валидатора в конструктор класса компонента.

```ts
constructor(private alterEgoValidator: UniqueAlterEgoValidator) {}
```

Затем передайте функцию валидатора непосредственно в `FormControl`, чтобы применить ее.

В следующем примере функция `validate` функции `UniqueAlterEgoValidator` применяется к `alterEgoControl` путем передачи ей опции `asyncValidators` элемента управления и привязки ее к экземпляру `UniqueAlterEgoValidator`, который был инжектирован в `HeroFormReactiveComponent`. Значение `asyncValidators` может быть либо одной функцией асинхронного валидатора, либо массивом функций.

Чтобы узнать больше об опциях `FormControl`, смотрите API-справочник [AbstractControlOptions](https://angular.io/api/forms/AbstractControlOptions).

```ts
const alterEgoControl = new FormControl('', {
    asyncValidators: [
        this.alterEgoValidator.validate.bind(
            this.alterEgoValidator
        ),
    ],
    updateOn: 'blur',
});
```

### Добавление асинхронных валидаторов в формы, управляемые шаблонами

Чтобы использовать асинхронный валидатор в формах, управляемых шаблонами, создайте новую директиву и зарегистрируйте на ней провайдер `NG_ASYNC_VALIDATORS`.

В примере ниже директива инжектирует класс `UniqueAlterEgoValidator`, содержащий логику валидации, и вызывает его в функции `validate`, запускаемой Angular, когда валидация должна произойти.

```ts
@Directive({
    selector: '[appUniqueAlterEgo]',
    providers: [
        {
            provide: NG_ASYNC_VALIDATORS,
            useExisting: forwardRef(
                () => UniqueAlterEgoValidatorDirective
            ),
            multi: true,
        },
    ],
})
export class UniqueAlterEgoValidatorDirective
    implements AsyncValidator {
    constructor(
        private validator: UniqueAlterEgoValidator
    ) {}

    validate(
        control: AbstractControl
    ): Observable<ValidationErrors | null> {
        return this.validator.validate(control);
    }
}
```

Затем, как и в случае с синхронными валидаторами, добавьте селектор директивы к входу, чтобы активировать ее.

```html
<input
    type="text"
    id="alterEgo"
    name="alterEgo"
    #alterEgo="ngModel"
    [(ngModel)]="hero.alterEgo"
    [ngModelOptions]="{ updateOn: 'blur' }"
    appUniqueAlterEgo
/>
```

### Оптимизация производительности асинхронных валидаторов

По умолчанию все валидаторы запускаются после каждого изменения значения формы. В случае синхронных валидаторов это обычно не оказывает заметного влияния на производительность приложения.

Асинхронные валидаторы, однако, обычно выполняют какой-либо HTTP-запрос для проверки элемента управления.

Отправка HTTP-запроса после каждого нажатия клавиши может создать нагрузку на API бэкенда, и по возможности ее следует избегать.

Вы можете отложить обновление валидности формы, изменив свойство `updateOn` с `change` (default) на `ubmit` или `blur`.

Для форм, управляемых шаблонами, установите это свойство в шаблоне.

```html
<input
    [(ngModel)]="name"
    [ngModelOptions]="{updateOn: 'blur'}"
/>
```

В реактивных формах установите свойство в экземпляре `FormControl`.

```ts
new FormControl('', { updateOn: 'blur' });
```

## Взаимодействие с собственной валидацией HTML-формы

По умолчанию Angular отключает [родную валидацию HTML-формы](https://developer.mozilla.org/docs/Web/Guide/HTML/Constraint_validation), добавляя атрибут `novalidate` на вложенную `<form>`, и использует директивы для согласования этих атрибутов с функциями валидатора во фреймворке. Если вы хотите использовать родную валидацию **в сочетании** с валидацией на основе Angular, вы можете снова включить ее с помощью директивы `ngNativeValidate`.

Подробности смотрите в [API docs](https://angular.io/api/forms/NgForm#native-dom-validation-ui).
