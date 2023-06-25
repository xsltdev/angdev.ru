# Template type checking

## Overview of template type checking

Just as TypeScript catches type errors in your code, Angular checks the expressions and bindings within the templates of your application and can report any type errors it finds. Angular currently has three modes of doing this, depending on the value of the `fullTemplateTypeCheck` and `strictTemplates` flags in the [TypeScript configuration file](guide/typescript-configuration).

### Basic mode

In the most basic type-checking mode, with the `fullTemplateTypeCheck` flag set to `false`, Angular validates only top-level expressions in a template.

If you write `<map [city]="user.address.city">`, the compiler verifies the following:

-   `user` is a property on the component class

-   `user` is an object with an address property

-   `user.address` is an object with a city property

The compiler does not verify that the value of `user.address.city` is assignable to the city input of the `<map>` component.

The compiler also has some major limitations in this mode:

-   Importantly, it doesn't check embedded views, such as `*ngIf`, `*ngFor`, other `<ng-template>` embedded view.

-   It doesn't figure out the types of `#refs`, the results of pipes, or the type of `$event` in event bindings.

Во многих случаях эти вещи имеют тип `any`, что может привести к тому, что последующие части выражения останутся без проверки.

### Полный режим

Если флаг `fullTemplateTypeCheck` установлен в `true`, Angular более агрессивно проверяет типы в шаблонах. В частности:

-   Проверяются встроенные представления\ (например, внутри `*ngIf` или `*ngFor`\).

-   Трубы имеют правильный тип возврата

-   Локальные ссылки на директивы и трубы имеют правильный тип\\(за исключением любых общих параметров, которые будут иметь тип `любой`\)

Следующие параметры все еще имеют тип `any`.

-   Локальные ссылки на элементы DOM

-   Объект `$event`

-   Выражения безопасной навигации

<div class="alert is-important">

Флаг `fullTemplateTypeCheck` был устаревшим в Angular 13. Вместо него следует использовать семейство опций компилятора `strictTemplates`.

</div>

<a id="strict-mode"></a>

### Строгий режим

Angular сохраняет поведение флага `fullTemplateTypeCheck` и вводит третий "строгий режим". Строгий режим является супермножеством полного режима, и доступ к нему осуществляется путем установки флага `strictTemplates` в true.

Этот флаг заменяет флаг `fullTemplateTypeCheck`.

В строгом режиме Angular использует проверки, которые выходят за рамки проверки типов версии 8.

<div class="alert is-helpful">

**NOTE**: <br /> Strict mode is only available if using Ivy.

</div>

В дополнение к поведению в полном режиме, Angular делает следующее:

-   Проверяет, что привязки компонентов/директив могут быть назначены на их `@Input()`.

-   Подчиняется флагу TypeScript `strictNullChecks` при проверке предшествующего режима

-   Определяет правильный тип компонентов/директив, включая дженерики

-   Определяет типы контекста шаблона, если это настроено\(например, позволяет правильно проверить тип `NgFor`\)

-   Определяет правильный тип `$event` в привязках компонентов/директив, DOM и анимационных событий

-   Определяет правильный тип локальных ссылок на элементы DOM, основываясь на имени тега\(например, тип, который `document.createElement` вернет для этого тега\)

## Проверка `*ngFor`.

Три режима проверки типов по-разному относятся к встроенным представлениям. Рассмотрим следующий пример.

<code-example language="typescript" header="User interface">

интерфейс User { имя: строка;
адрес: {

город: строка;

штат: string;

}

}

</code-example>

<code-example format="html" language="html">

&lt;div \*ngFor="let user of users"&gt; &lt;h2&gt;{{config.title}}&lt;/h2&gt;
&lt;span&gt;Город: {{user.address.city}}&lt;/span&gt;

&lt;/div&gt;

</code-example>

The `<h2>` and the `<span>` are in the `*ngFor` embedded view. In basic mode, Angular doesn't check either of them.
However, in full mode, Angular checks that `config` and `user` exist and assumes a type of `any`.

In strict mode, Angular knows that the `user` in the `<span>` has a type of `User`, and that `address` is an object with a `city` property of type `string`.

<a id="troubleshooting-template-errors"></a>

## Устранение ошибок шаблонов

В строгом режиме вы можете столкнуться с ошибками шаблонов, которые не возникали ни в одном из предыдущих режимов. Эти ошибки часто представляют собой настоящие несоответствия типов в шаблонах, которые не были пойманы предыдущими инструментами.

В этом случае в сообщении об ошибке должно быть ясно, в каком месте шаблона возникла проблема.

Также возможны ложные срабатывания, когда типизация библиотеки Angular неполная или неправильная, или когда типизация не совсем соответствует ожиданиям, как в следующих случаях.

-   Когда типизация библиотеки неверна или неполна\ (например, отсутствует `null | undefined`, если библиотека не была написана с `strictNullChecks` в уме\).

-   Когда типы ввода библиотеки слишком узкие, и библиотека не добавила соответствующие метаданные, чтобы Angular мог это понять.

    Обычно это происходит при использовании атрибутов disabled или других распространенных булевых входов, например, `<input disabled>`.

-   При использовании `$event.target` для событий DOM\ (из-за возможности пузырения событий, `$event.target` в типизации DOM не имеет того типа, который вы могли бы ожидать\).

В случае ложных срабатываний, подобных этим, есть несколько вариантов:

-   Использовать функцию [`$any()` type-cast function](guide/template-expression-operators#any-type-cast-function) в определенных контекстах, чтобы отказаться от проверки типов для части выражения.

-   Отключить строгую проверку полностью, установив `strictTemplates: false` в конфигурационном файле TypeScript приложения, `tsconfig.json`.

-   Отключить определенные операции проверки типов по отдельности, сохраняя строгость в других аспектах, установив флаг _строгости_ в `false`.

-   Если вы хотите использовать `strictTemplates` и `strictNullChecks` вместе, откажитесь от строгой проверки нулевого типа специально для входных привязок, используя `strictNullInputTypes`.

Если не указано иное, каждый следующий параметр устанавливается в значение для `strictTemplates` \(`true`, когда `strictTemplates` - `true` и наоборот\).

| Strictness flag | Effect | | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `strictInputTypes` | Whether the assignability of a binding expression to the `@Input()` field is checked. Also affects the inference of directive generic types. |
| `strictInputAccessModifiers` | Whether access modifiers such as `private`/`protected`/`readonly` are honored when assigning a binding expression to an `@Input()`. If disabled, the access modifiers of the `@Input` are ignored; only the type is checked. This option is `false` by default, even with `strictTemplates` set to `true`. |
| `strictNullInputTypes` | Whether `strictNullChecks` is honored when checking `@Input()` bindings \(per `strictInputTypes`\). Turning this off can be useful when using a library that was not built with `strictNullChecks` in mind. |
| `strictAttributeTypes` | Whether to check `@Input()` bindings that are made using text attributes. For example, <code-example format="html" hideCopy language="html"> &lt;input matInput disabled="true"&gt; </code-example> \(setting the `disabled` property to the string `'true'`\) vs <code-example format="html" hideCopy language="html"> &lt;input matInput [disabled]="true"&gt; </code-example> \(setting the `disabled` property to the boolean `true`\). |
| `strictSafeNavigationTypes` | Whether the return type of safe navigation operations \(for example, `user?.name` will be correctly inferred based on the type of `user`\). If disabled, `user?.name` will be of type `any`. |
| `strictDomLocalRefTypes` | Whether local references to DOM elements will have the correct type. If disabled `ref` will be of type `any` for `<input #ref>`. |
| `strictOutputEventTypes` | Whether `$event` will have the correct type for event bindings to component/directive an `@Output()`, or to animation events. If disabled, it will be `any`. |
| `strictDomEventTypes` | Whether `$event` will have the correct type for event bindings to DOM events. If disabled, it will be `any`. |
| `strictContextGenerics` | Whether the type parameters of generic components will be inferred correctly \(including any generic bounds\). If disabled, any type parameters will be `any`. |
| `strictLiteralTypes` | Whether object and array literals declared in the template will have their type inferred. If disabled, the type of such literals will be `any`. This flag is `true` when _either_ `fullTemplateTypeCheck` or `strictTemplates` is set to `true`. |

Если после устранения неполадок с помощью этих флагов у вас все еще возникают проблемы, вернитесь к полному режиму, отключив `strictTemplates`.

Если это не сработает, то в крайнем случае можно полностью отключить полный режим с помощью `fullTemplateTypeCheck: false`.

Ошибка проверки типов, которую вы не можете устранить ни одним из рекомендуемых методов, может быть результатом ошибки в самой системе проверки типов шаблонов. Если вы получаете ошибки, требующие возврата в базовый режим, то, скорее всего, это именно такая ошибка.

Если это произошло, [file an issue](https://github.com/angular/angular/issues), чтобы команда могла решить эту проблему.

## Вводы и проверка типов

Средство проверки типов шаблонов проверяет, совместим ли тип выражения привязки с типом соответствующего входа директивы. В качестве примера рассмотрим следующий компонент:

<code-example format="typescript" language="typescript">

export interface User { name: string;
}

&commat;Component({ selector: 'user-detail',

template: '{ { user.name }}',

})

export class UserDetailComponent {

&commat;Input() user: User;

}

</code-example>

Шаблон `AppComponent` использует этот компонент следующим образом:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'app-root',
template: '&lt;user-detail [user]="selectedUser"&gt;&lt;/user-detail&gt;',

})

export class AppComponent {

selectedUser: User &verbar; null = null;

}

</code-example>

Здесь, во время проверки типа шаблона для `AppComponent`, привязка `[user]="selectedUser"` соответствует входу `UserDetailComponent.user`. Поэтому Angular присваивает свойство `selectedUser` свойству `UserDetailComponent.user`, что привело бы к ошибке, если бы их типы были несовместимы.
TypeScript проверяет присвоение в соответствии со своей системой типов, подчиняясь таким флагам, как `strictNullChecks`, поскольку они настроены в приложении.

Избегайте ошибок типа во время выполнения, предоставляя более конкретные требования к типу в шаблоне для проверки типа шаблона. Сделайте требования к входным типам для ваших собственных директив как можно более конкретными, предоставив функции защиты шаблона в определении директивы.

Смотрите [Улучшение проверки типов шаблонов для пользовательских директив](guide/structural-directives#directive-type-checks) в этом руководстве.

### Строгие проверки нуля

Когда вы включаете `strictTemplates` и флаг TypeScript `strictNullChecks`, в некоторых ситуациях могут возникать ошибки проверки типов, которых нелегко избежать. Например:

-   Нулевое значение, связанное с директивой из библиотеки, в которой не включена `strictNullChecks`.

    Для библиотеки, скомпилированной без `strictNullChecks`, ее файлы объявлений не будут указывать, может ли поле быть `null` или нет.

    Для ситуаций, когда библиотека корректно обрабатывает `null`, это проблематично, так как компилятор будет проверять значение с нулевым значением на соответствие файлам объявления, в которых тип `null` опущен.

    Таким образом, компилятор выдает ошибку проверки типов, поскольку он придерживается `strictNullChecks`.

-   Использование трубы `async` с Observable, который, как вы знаете, будет испускаться синхронно.

    Труба `async` в настоящее время предполагает, что Observable, на которую она подписывается, может быть асинхронной, что означает, что возможно, что значение еще не доступно.

    В этом случае она все равно должна возвращать что-то &mdash; это `null`.

    Другими словами, тип возврата трубы `async` включает `null`, что может привести к ошибкам в ситуациях, когда известно, что Observable синхронно выдает значение, не являющееся nullable.

Существует два возможных обходных пути решения вышеупомянутых проблем:

-   В шаблоне включите оператор утверждения `!` в конце выражения с нулевым значением, например

      <code-example format="html" hideCopy language="html">

    &lt;user-detail [user]="user!"&gt;&lt;/user-detail&gt;

      </code-example>

    В этом примере компилятор игнорирует несовместимость типов в nullability, как и в коде TypeScript.

    В случае с трубой `async` обратите внимание, что выражение необходимо обернуть круглыми скобками, как в примере

      <code-example format="html" hideCopy language="html">

    &lt;user-detail [user]="(user\$ &verbar; async)!"&gt;&lt;/user-detail&gt;

      </code-example>

-   Полностью отключить строгую проверку нуля в шаблонах Angular.

    Когда включена опция `strictTemplates`, все еще можно отключить некоторые аспекты проверки типов.

    Установка опции `strictNullInputTypes` в `false` отключает строгую проверку нулевых типов в шаблонах Angular.

    Этот флаг применяется для всех компонентов, которые являются частью приложения.

### Советы для авторов библиотек

Как автор библиотеки, вы можете предпринять несколько мер, чтобы обеспечить оптимальный опыт для ваших пользователей. Во-первых, включение `strictNullChecks` и включение `null` в тип ввода, по мере необходимости, сообщает вашим потребителям, могут ли они предоставить значение с нулевым значением или нет.

Кроме того, можно предоставлять подсказки типов, специфичные для проверки типов шаблонов.

Смотрите [Улучшение проверки типов шаблонов для пользовательских директив](guide/structural-directives#directive-type-checks), и [Коэрцитивность входных сеттеров](#input-setter-coercion).

<a id="input-setter-coercion"></a>

## Принуждение входного сеттера

Иногда желательно, чтобы `@Input()` директивы или компонента изменял привязанное к нему значение, обычно используя пару getter/setter для ввода. В качестве примера рассмотрим компонент пользовательской кнопки:

Рассмотрим следующую директиву:

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'submit-button',
template: &grave;

&lt;div class="wrapper"&gt;

&lt;button [disabled]="disabled"&gt;Submit&lt;/button&gt;

&lt;/div&gt;

&grave;,

})

class SubmitButton {

private \_disabled: boolean;

&commat;Input() get disabled(): boolean {

return this.\_disabled;

}

set disabled(value: boolean) { this.\_disabled = value;

}

}

</code-example>

Здесь вход `disabled` компонента передается на `<button>` в шаблоне. Все это работает, как и ожидалось, пока к входу привязано значение `boolean`.
Но, предположим, потребитель использует этот вход в шаблоне в качестве атрибута:

<code-example format="html" language="html">

&lt;submit-button disabled&gt;&lt;/submit-button&gt;

</code-example>

Это имеет тот же эффект, что и связывание:

<code-example format="html" language="html">

&lt;submit-button [disabled]="''"&gt;&lt;/submit-button&gt;

</code-example>

Во время выполнения входное значение будет установлено в пустую строку, которая не является значением типа `boolean`. Библиотеки компонентов Angular, которые решают эту проблему, часто "принуждают" значение к нужному типу в сеттере:

<code-example format="typescript" language="typescript">

set disabled(value: boolean) { this.\_disabled = (value === '')&verbar;&verbar; value;
}

</code-example>

Идеально было бы изменить здесь тип `value` с `boolean` на `boolean|''`, чтобы соответствовать набору значений, которые фактически принимаются сеттером. TypeScript до версии 4.3 требует, чтобы и геттер, и сеттер имели одинаковый тип, поэтому если геттер должен вернуть `boolean`, то сеттер будет иметь более узкий тип.

Если у потребителя включена самая строгая проверка типов шаблонов Angular, это создает проблему: пустая строка \(````\) не может быть присвоена полю `disabled`, что создает ошибку типа при использовании формы атрибута.

В качестве обходного пути решения этой проблемы Angular поддерживает проверку более широкого, более допустимого типа для `@Input()`, чем объявлено для самого поля ввода. Включите эту возможность, добавив в класс компонента статическое свойство с префиксом `ngAcceptInputType_`:

<code-example format="typescript" language="typescript">

class SubmitButton { private \_disabled: boolean;

&commat;Input() get disabled(): boolean {

return this.\_disabled;

}

set disabled(value: boolean) { this.\_disabled = (value === '') &verbar;&verbar; value;

}

static ngAcceptInputType_disabled: boolean&verbar;''; }

</code-example>

<div class="alert is-important">

Начиная с TypeScript 4.3, сеттер может быть объявлен как принимающий `boolean|''` в качестве типа, что делает поле принуждения входного сеттера устаревшим. Таким образом, поля принуждения входных сеттеров были устаревшими.

</div>

Это поле не обязательно должно иметь значение. Его существование сообщает системе проверки типов Angular, что вход `disabled` следует рассматривать как принимающий привязки, соответствующие типу `boolean|''`.
Суффиксом должно быть имя _поля_ `@Input`.

Следует обратить внимание на то, что если для данного входа существует переопределение `ngAcceptInputType_`, то сеттер должен быть способен обрабатывать любые значения переопределенного типа.

## Отключение проверки типов с помощью `$any()`.

Отключите проверку выражения привязки, окружив выражение вызовом псевдофункции [`$any()` cast pseudo-function](guide/template-expression-operators). Компилятор рассматривает это как приведение к типу `any`, как в TypeScript, когда используется приведение `<any>` или `as any`.

В следующем примере приведение `person` к типу `any` подавляет ошибку `Property address does not exist`.

<code-example format="typescript" language="typescript">

&commat;Component({ selector: 'my-component',
template: '{ {\$any(person).address.street}}'

})

class MyComponent {

person? Person;

}

</code-example>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
