# Типизированные формы

:date: 10.05.2022

Начиная с Angular 14, реактивные формы по умолчанию строго типизированы.

## Предварительные условия

В качестве основы для этого руководства вы должны быть знакомы с [Angular Reactive Forms](reactive-forms.md).

## Обзор типизированных форм {: #intro}

<iframe width="100%" height="400" src="https://www.youtube.com/embed/L-odCf4MfJc" title="YouTube video player" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

В реактивных формах Angular вы явно указываете _модель формы_. В качестве простого примера рассмотрим базовую форму входа пользователя в систему:

```ts
const login = new FormGroup({
    email: new FormControl(''),
    password: new FormControl(''),
});
```

Angular предоставляет множество API для взаимодействия с этой `FormGroup`. Например, вы можете вызвать `login.value`, `login.controls`, `login.patchValue` и т. д. (Полное описание API см. в [документации API](https://angular.io/api/forms/FormGroup)).

В предыдущих версиях Angular большинство этих API включали `any` в свои типы, и взаимодействие со структурой элементов управления или самих значений не было безопасным с точки зрения типов. Например, вы могли написать следующий некорректный код:

```ts
const emailDomain = login.value.email.domain;
```

При использовании строго типизированных реактивных форм приведенный выше код не компилируется, поскольку у `email` нет свойства `domain`.

В дополнение к дополнительной безопасности, типы позволяют получить ряд других улучшений, таких как улучшенное автозаполнение в IDE и явный способ задания структуры формы.

В настоящее время эти улучшения применяются только к _реактивным_ формам (не к [_шаблонным_ формам](forms.md)).

## Автоматическая миграция нетипизированных форм {: #automated-migration}

При обновлении до Angular 14 включенная миграция автоматически заменит все классы форм в вашем коде на соответствующие нетипизированные версии. Например, фрагмент, приведенный выше, станет:

```ts
const login = new UntypedFormGroup({
    email: new UntypedFormControl(''),
    password: new UntypedFormControl(''),
});
```

Каждый символ `Untyped` имеет точно такую же семантику, как и в предыдущих версиях Angular, поэтому ваше приложение должно компилироваться как и раньше. Удалив префиксы `Untyped`, вы можете постепенно включать типы.

## `FormControl`: Начало работы {: #form-control-inference}

Самая простая форма состоит из одного элемента управления:

```ts
const email = new FormControl('angularrox@gmail.com');
```

Этот элемент управления будет автоматически считаться имеющим тип `FormControl<string|null>`. TypeScript будет автоматически применять этот тип во всем API [`FormControl`](https://angular.io/api/forms/FormControl), например, `email.value`, `email.valueChanges`, `email.setValue(...)` и т. д.

### Nullability

Вы можете задаться вопросом: почему тип этого элемента управления включает `null`? Это потому, что элемент управления может стать `null` в любое время, вызвав команду reset:

```ts
const email = new FormControl('angularrox@gmail.com');
email.reset();
console.log(email.value); // null
```

TypeScript требует, чтобы вы всегда обрабатывали возможность того, что элемент управления стал `null`. Если вы хотите сделать этот элемент управления ненулевым, вы можете использовать опцию `nonNullable`. Это приведет к тому, что элемент управления сбросится на свое начальное значение, а не на `null`:

```ts
const email = new FormControl('angularrox@gmail.com', {
    nonNullable: true,
});
email.reset();
console.log(email.value); // angularrox@gmail.com
```

Повторимся, что этот параметр влияет на поведение вашей формы во время выполнения, когда вызывается `.reset()`, и его следует использовать с осторожностью.

### Указание явного типа

Можно указать тип, вместо того чтобы полагаться на умозаключение. Рассмотрим элемент управления, который инициализируется значением `null`. Поскольку начальное значение равно `null`, TypeScript выведет `FormControl<null>`, что является более узким, чем мы хотим.

```ts
const email = new FormControl(null);
email.setValue('angularrox@gmail.com'); // Error!
```

Чтобы предотвратить это, мы явно указываем тип как `string|null`:

```ts
const email = new FormControl<string | null>(null);
email.setValue('angularrox@gmail.com');
```

## `FormArray`: Динамические, однородные коллекции {: #form-array}

Массив `FormArray` содержит неограниченный список элементов управления. Параметр `type` соответствует типу каждого внутреннего элемента управления:

```ts
const names = new FormArray([new FormControl('Alex')]);
names.push(new FormControl('Jess'));
```

Этот `FormArray` будет иметь внутренний элемент управления типа `FormControl<string|null>`.

Если вы хотите иметь несколько различных типов элементов внутри массива, вы должны использовать `UntypedFormArray`, потому что TypeScript не может определить, какой тип элемента будет встречаться в той или иной позиции.

## `FormGroup` и `FormRecord` {: #form-group-record}

Angular предоставляет тип `FormGroup` для форм с перечислимым набором ключей и тип `FormRecord` для открытых или динамических групп.

### Частичные значения

Рассмотрим еще раз форму входа в систему:

```ts
const login = new FormGroup({
    email: new FormControl('', { nonNullable: true }),
    password: new FormControl('', { nonNullable: true }),
});
```

В любой `FormGroup` можно [отключить элементы управления](https://angular.io/api/forms/FormGroup). Любой отключенный элемент управления не будет отображаться в значении группы.

Как следствие, тип `login.value` — `Partial<{email: string, password: string}>`. `Partial` в этом типе означает, что каждый член может быть неопределенным.

Более конкретно, тип `login.value.email` — `string|undefined`, и TypeScript будет принудительно обрабатывать возможно `неопределенное` значение (если у вас включена `strictNullChecks`).

Если вы хотите получить доступ к значению _включая_ отключенные элементы управления, и таким образом обойти возможные `неопределенные` поля, вы можете использовать `login.getRawValue()`.

### Дополнительные элементы управления и динамические группы

В некоторых формах есть элементы управления, которые могут присутствовать или не присутствовать, которые могут быть добавлены и удалены во время выполнения. Вы можете представить эти элементы управления с помощью _опциональных полей_:

```ts
interface LoginForm {
    email: FormControl<string>;
    password?: FormControl<string>;
}

const login = new FormGroup<LoginForm>({
    email: new FormControl('', { nonNullable: true }),
    password: new FormControl('', { nonNullable: true }),
});

login.removeControl('password');
```

В этой форме мы явно указываем тип, что позволяет нам сделать элемент управления `password` необязательным. TypeScript будет следить за тем, чтобы можно было добавлять или удалять только необязательные элементы управления.

### `FormRecord`

Некоторые случаи использования `FormGroup` не соответствуют приведенному выше шаблону, поскольку ключи не известны заранее. Класс `FormRecord` предназначен для этого случая:

```ts
const addresses = new FormRecord<
    FormControl<string | null>
>({});
addresses.addControl(
    'Andrew',
    new FormControl('2340 Folsom St')
);
```

Любой элемент управления типа `string|null` может быть добавлен к этой `FormRecord`.

Если вам нужна `FormGroup`, которая является одновременно динамической (открытой) и неоднородной (элементы управления разных типов), то улучшенная безопасность типов невозможна, и вам следует использовать `UntypedFormGroup`.

Запись `FormRecord` также может быть построена с помощью `FormBuilder`:

```ts
const addresses = fb.record({ Andrew: '2340 Folsom St' });
```

## `FormBuilder` и `NonNullableFormBuilder`

Класс `FormBuilder` был модернизирован для поддержки новых типов, аналогично приведенным выше примерам.

Кроме того, доступен дополнительный конструктор: `NonNullableFormBuilder`. Этот тип является сокращением для указания `{nonNullable: true}` на каждом элементе управления, и может устранить значительную часть шаблонов из больших форм с недействительными элементами. Вы можете получить к нему доступ, используя свойство `nonNullable` на `FormBuilder`:

```ts
const fb = new FormBuilder();
const login = fb.nonNullable.group({
    email: '',
    password: '',
});
```

В приведенном выше примере оба внутренних элемента управления будут non-nullable (т.е. будет установлено значение `nonNullable`).

Вы также можете внедрить его, используя имя `NonNullableFormBuilder`.

[ninjasquadtypedformsblog]: https://blog.ninja-squad.com/2022/04/21/strictly-typed-forms-angular/s
