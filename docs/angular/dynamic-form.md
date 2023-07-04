# Построение динамических форм

:date: 28.02.2022

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
2.  Создайте модель данных для представления элементов управления формы.
3.  Наполните модель данными образца.
4.  Разработайте компонент для динамического создания элементов управления формы.

Созданная вами форма использует валидацию ввода и стилизацию для улучшения пользовательского опыта. В ней есть кнопка "Отправить", которая активируется только в том случае, если все введенные пользователем данные достоверны, а недопустимые данные отмечаются цветовой маркировкой и сообщениями об ошибках.

Базовая версия может развиваться, чтобы поддерживать более богатое разнообразие вопросов, более изящный рендеринг и улучшать пользовательский опыт.

!!!note ""

    См. [пример](https://angular.io/generated/live-examples/dynamic-form/stackblitz.html).

## Предварительные условия

Перед выполнением этого руководства вы должны иметь базовое представление о следующем.

-   [TypeScript](https://www.typescriptlang.org/ 'Язык TypeScript') и программирование на HTML5
-   Фундаментальные концепции [Angular app design](architecture.md)
-   Базовые знания [реактивных форм](reactive-forms.md)

## Включите реактивные формы для вашего проекта

Динамические формы основаны на реактивных формах. Чтобы предоставить приложению доступ к директивам реактивных форм, [корневой модуль](bootstrapping.md) импортирует `ReactiveFormsModule` из библиотеки `@angular/forms`.

Следующий код из примера показывает настройку в корневом модуле.

=== "app.module.ts"

```ts
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { DynamicFormComponent } from './dynamic-form.component';
import { DynamicFormQuestionComponent } from './dynamic-form-question.component';

@NgModule({
    imports: [BrowserModule, ReactiveFormsModule],
    declarations: [
        AppComponent,
        DynamicFormComponent,
        DynamicFormQuestionComponent,
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

=== "main.ts"

```ts
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';

platformBrowserDynamic()
    .bootstrapModule(AppModule)
    .catch((err) => console.error(err));
```

## Создание объектной модели формы {: #object-model}

Динамическая форма требует объектной модели, которая может описать все сценарии, необходимые для функциональности формы. Пример формы hero-application представляет собой набор вопросов &mdash; то есть каждый элемент управления в форме должен задавать вопрос и принимать ответ.

Модель данных для этого типа формы должна представлять вопрос. Пример включает `DynamicFormQuestionComponent`, который определяет вопрос как основной объект в модели.

Следующий `QuestionBase` является базовым классом для набора элементов управления, которые могут представлять вопрос и ответ на него в форме.

```ts
export class QuestionBase<T> {
    value: T | undefined;
    key: string;
    label: string;
    required: boolean;
    order: number;
    controlType: string;
    type: string;
    options: { key: string; value: string }[];

    constructor(
        options: {
            value?: T;
            key?: string;
            label?: string;
            required?: boolean;
            order?: number;
            controlType?: string;
            type?: string;
            options?: { key: string; value: string }[];
        } = {}
    ) {
        this.value = options.value;
        this.key = options.key || '';
        this.label = options.label || '';
        this.required = !!options.required;
        this.order =
            options.order === undefined ? 1 : options.order;
        this.controlType = options.controlType || '';
        this.type = options.type || '';
        this.options = options.options || [];
    }
}
```

### Определите классы управления

Из этой базы пример выводит два новых класса, `TextboxQuestion` и `DropdownQuestion`, которые представляют различные типы элементов управления. Когда вы создаете шаблон формы на следующем этапе, вы инстанцируете эти конкретные типы вопросов, чтобы динамически отобразить соответствующие элементы управления.

Тип элемента управления **`TextboxQuestion`**.

Представляет вопрос и позволяет пользователям вводить данные.

```ts
import { QuestionBase } from './question-base';

export class TextboxQuestion extends QuestionBase<string> {
  override controlType = 'textbox';
}
```

Тип управления `TextboxQuestion` представлен в шаблоне формы с помощью элемента `<input>`. Атрибут `type` элемента определяется на основе поля `type`, указанного в аргументе `options` (например, `text`, `email`, `url`).

Тип элемента управления **`DropdownQuestion`**.

Представляет список вариантов выбора в поле выбора.

```ts
import { QuestionBase } from './question-base';

export class DropdownQuestion extends QuestionBase<string> {
  override controlType = 'dropdown';
}
```

### Составление групп форм

Динамическая форма использует сервис для создания сгруппированных наборов элементов управления вводом на основе модели формы. Следующий `QuestionControlService` собирает набор экземпляров `FormGroup`, которые потребляют метаданные из модели вопроса.
Вы можете указать значения по умолчанию и правила проверки.

```ts
import { Injectable } from '@angular/core';
import {
    FormControl,
    FormGroup,
    Validators,
} from '@angular/forms';

import { QuestionBase } from './question-base';

@Injectable()
export class QuestionControlService {
    toFormGroup(questions: QuestionBase<string>[]) {
        const group: any = {};

        questions.forEach((question) => {
            group[question.key] = question.required
                ? new FormControl(
                      question.value || '',
                      Validators.required
                  )
                : new FormControl(question.value || '');
        });
        return new FormGroup(group);
    }
}
```

## Составление содержимого динамической формы {: #form-component}

Сама динамическая форма представлена компонентом-контейнером, который вы добавите на следующем этапе. Каждый вопрос представлен в шаблоне компонента формы тегом `<app-question>`, который соответствует экземпляру `DynamicFormQuestionComponent`.

Компонент `DynamicFormQuestionComponent` отвечает за отображение деталей отдельного вопроса на основе значений в связанном с данными объекте вопроса. Форма полагается на директиву [`[formGroup]`](https://angular.io/api/forms/FormGroupDirective) для соединения HTML шаблона с базовыми объектами управления.

Компонент `DynamicFormQuestionComponent` создает группы форм и заполняет их элементами управления, определенными в модели вопроса, задавая правила отображения и проверки.

=== "dynamic-form-question.component.html"

```html
<div [formGroup]="form">
    <label [attr.for]="question.key"
        >{{question.label}}</label
    >

    <div [ngSwitch]="question.controlType">
        <input
            *ngSwitchCase="'textbox'"
            [formControlName]="question.key"
            [id]="question.key"
            [type]="question.type"
        />

        <select
            [id]="question.key"
            *ngSwitchCase="'dropdown'"
            [formControlName]="question.key"
        >
            <option
                *ngFor="let opt of question.options"
                [value]="opt.key"
            >
                {{opt.value}}
            </option>
        </select>
    </div>

    <div class="errorMessage" *ngIf="!isValid">
        {{question.label}} is required
    </div>
</div>
```

=== "dynamic-form-question.component.ts"

```ts
import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

import { QuestionBase } from './question-base';

@Component({
    selector: 'app-question',
    templateUrl: './dynamic-form-question.component.html',
})
export class DynamicFormQuestionComponent {
    @Input() question!: QuestionBase<string>;
    @Input() form!: FormGroup;
    get isValid() {
        return this.form.controls[this.question.key].valid;
    }
}
```

Цель `DynamicFormQuestionComponent` - представить типы вопросов, определенные в вашей модели. На данный момент у вас есть только два типа вопросов, но вы можете придумать гораздо больше.
Оператор `ngSwitch` в шаблоне определяет, какой тип вопроса отображать.

Переключатель использует директивы с селекторами [`formControlName`](https://angular.io/api/forms/FormControlName) и [`formGroup`](https://angular.io/api/forms/FormGroupDirective).

Обе директивы определены в `ReactiveFormsModule`.

### Предоставление данных {: #questionnaire-data}

Еще один сервис необходим для предоставления определенного набора вопросов, из которых можно построить индивидуальную форму. В этом упражнении вы создадите `QuestionService`, который будет предоставлять массив вопросов из жестко закодированных данных образца.

В реальном приложении сервис может получать данные из внутренней системы.

Ключевым моментом, однако, является то, что вы полностью контролируете вопросы героя анкеты через объекты, возвращаемые из `QuestionService`.

Чтобы поддерживать анкету по мере изменения требований, вам нужно только добавлять, обновлять и удалять объекты из массива `questions`.

Сервис `QuestionService` предоставляет набор вопросов в виде массива, связанного с `@Input()` вопросами.

```ts
import { Injectable } from '@angular/core';

import { DropdownQuestion } from './question-dropdown';
import { QuestionBase } from './question-base';
import { TextboxQuestion } from './question-textbox';
import { of } from 'rxjs';

@Injectable()
export class QuestionService {
    // TODO: get from a remote source of question metadata
    getQuestions() {
        const questions: QuestionBase<string>[] = [
            new DropdownQuestion({
                key: 'brave',
                label: 'Bravery Rating',
                options: [
                    { key: 'solid', value: 'Solid' },
                    { key: 'great', value: 'Great' },
                    { key: 'good', value: 'Good' },
                    { key: 'unproven', value: 'Unproven' },
                ],
                order: 3,
            }),

            new TextboxQuestion({
                key: 'firstName',
                label: 'First name',
                value: 'Bombasto',
                required: true,
                order: 1,
            }),

            new TextboxQuestion({
                key: 'emailAddress',
                label: 'Email',
                type: 'email',
                order: 2,
            }),
        ];

        return of(
            questions.sort((a, b) => a.order - b.order)
        );
    }
}
```

## Создание шаблона динамической формы {: #dynamic-template}

Компонент `DynamicFormComponent` является точкой входа и основным контейнером для формы, которая представлена с помощью `<app-dynamic-form>` в шаблоне.

Компонент `DynamicFormComponent` представляет список вопросов, связывая каждый из них с элементом `<app-question>`, который соответствует `DynamicFormQuestionComponent`.

=== "dynamic-form.component.html"

```html
<div>
    <form (ngSubmit)="onSubmit()" [formGroup]="form">
        <div
            *ngFor="let question of questions"
            class="form-row"
        >
            <app-question
                [question]="question"
                [form]="form"
            ></app-question>
        </div>

        <div class="form-row">
            <button type="submit" [disabled]="!form.valid">
                Save
            </button>
        </div>
    </form>

    <div *ngIf="payLoad" class="form-row">
        <strong>Saved the following values</strong
        ><br />{{payLoad}}
    </div>
</div>
```

=== "dynamic-form.component.ts"

```ts
import { Component, Input, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';

import { QuestionBase } from './question-base';
import { QuestionControlService } from './question-control.service';

@Component({
    selector: 'app-dynamic-form',
    templateUrl: './dynamic-form.component.html',
    providers: [QuestionControlService],
})
export class DynamicFormComponent implements OnInit {
    @Input() questions: QuestionBase<string>[] | null = [];
    form!: FormGroup;
    payLoad = '';

    constructor(private qcs: QuestionControlService) {}

    ngOnInit() {
        this.form = this.qcs.toFormGroup(
            this.questions as QuestionBase<string>[]
        );
    }

    onSubmit() {
        this.payLoad = JSON.stringify(
            this.form.getRawValue()
        );
    }
}
```

### Отображение формы

Для отображения экземпляра динамической формы шаблон оболочки `AppComponent` передает массив `questions`, возвращаемый `QuestionService`, компоненту-контейнеру формы, `<app-dynamic-form>`.

```ts
import { Component } from '@angular/core';

import { QuestionService } from './question.service';
import { QuestionBase } from './question-base';
import { Observable } from 'rxjs';

@Component({
    selector: 'app-root',
    template: `
        <div>
            <h2>Job Application for Heroes</h2>
            <app-dynamic-form
                [questions]="questions$ | async"
            ></app-dynamic-form>
        </div>
    `,
    providers: [QuestionService],
})
export class AppComponent {
    questions$: Observable<QuestionBase<any>[]>;

    constructor(service: QuestionService) {
        this.questions$ = service.getQuestions();
    }
}
```

Пример предоставляет модель приложения для работы с героями, но в нем нет ссылок на какой-либо конкретный вопрос героя, кроме объектов, возвращаемых `QuestionService`. Такое разделение модели и данных позволяет вам перепрофилировать компоненты для любого типа опросов, если они совместимы с объектной моделью _question_.

### Обеспечение достоверности данных

Шаблон формы использует динамическое связывание метаданных для отображения формы, не делая никаких жестких предположений о конкретных вопросах. Он добавляет метаданные элементов управления и критерии проверки динамически.

Для обеспечения корректного ввода данных кнопка _Сохранить_ отключена до тех пор, пока форма не перейдет в корректное состояние. Когда форма становится валидной, нажмите кнопку _Сохранить_, и приложение отобразит текущие значения формы в виде JSON.

На следующем рисунке показана окончательная форма.

![Dynamic-Form](dynamic-form.png)

## Следующие шаги

**Различные типы форм и коллекция элементов управления**.

В этом уроке показано, как создать анкету, которая является одним из видов динамических форм. В примере используется `FormGroup` для сбора набора элементов управления. Пример динамической формы другого типа см. в разделе [Создание динамических форм] (reactive-forms.md#creating-dynamic-forms) в руководстве Reactive Forms. В том примере также показано, как использовать `FormArray` вместо `FormGroup` для сбора набора элементов управления.

**Валидация пользовательского ввода**

Раздел [Проверка ввода формы](reactive-forms.md#validating-form-input) знакомит с основами работы проверки ввода в реактивных формах.

В руководстве [Form validation guide](form-validation.md) эта тема рассматривается более подробно.
