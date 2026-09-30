---
description: Модули JavaScript и модули NgModules могут помочь вам в модульном построении кода, но они очень разные. В приложениях Angular используются оба вида модулей
---

# Модули JavaScript против NgModules

:date: 28.02.2022

Модули JavaScript и модули NgModules могут помочь вам в модульном построении кода, но они очень разные. В приложениях Angular используются оба вида модулей.

## Модули JavaScript: Файлы, содержащие код

Модуль [JavaScript](https://learn.javascript.ru/modules) — это отдельный файл с кодом JavaScript, обычно содержащий класс или библиотеку функций для конкретной цели в вашем приложении. Модули JavaScript позволяют распределить работу по нескольким файлам.

!!!note ""

    Подробнее о модулях JavaScript см. в статье [ES6 In Depth: Modules](https://hacks.mozilla.org/2015/08/es6-in-depth-modules). Спецификацию модулей см. в [6th Edition of the ECMAScript standard](https://www.ecma-international.org/ecma-262/6.0/#sec-modules).

Чтобы сделать код в модуле JavaScript доступным для других модулей, используйте оператор `export` в конце соответствующего кода модуля, как, например, в следующем примере:

```ts
export class AppComponent {
    /* … */
}
```

Если код этого модуля нужен в другом модуле, используйте оператор `import` следующим образом:

```ts
import { AppComponent } from './app.component';
```

Каждый модуль имеет свою собственную область видимости верхнего уровня. Другими словами, переменные и функции верхнего уровня в модуле не видны в других скриптах или модулях. Каждый модуль предоставляет пространство имен для идентификаторов, чтобы предотвратить их столкновение с идентификаторами в других модулях. При наличии нескольких модулей можно предотвратить случайное появление глобальных переменных, создав единое глобальное пространство имен и добавив к нему подмодули.

Сам фреймворк Angular загружается как набор JavaScript-модулей.

## NgModules: Классы с метаданными для компиляции

[NgModule](glossary.md#ngmodule 'Определение NgModule') — это класс, помеченный декоратором `@NgModule` с объектом метаданных, который описывает, как данная часть приложения сочетается с другими частями. NgModules специфичны для Angular. Хотя классы с декоратором `@NgModule` по традиции хранятся в собственных файлах, они отличаются от модулей JavaScript тем, что включают в себя эти метаданные.

Метаданные `@NgModule` играют важную роль в управлении процессом компиляции Angular, который преобразует написанный вами код приложения в высокопроизводительный JavaScript-код. Метаданные описывают, как скомпилировать шаблон компонента и как создать [инжектор](glossary.md#injector 'Определение инжектора') во время выполнения. Она определяет [компоненты](glossary.md#component 'Определение компонента'), [директивы](glossary.md#directive 'Определение директивы') и [пайпы](glossary.md#pipe 'Определение пайпа') NgModule, а также делает некоторые из них общедоступными через свойство `exports`, чтобы внешние компоненты могли их использовать. Вы также можете использовать NgModule для добавления провайдеров [providers](glossary.md#provider 'Определение провайдера') для сервисов [services](glossary.md#service 'Определение сервиса'), чтобы эти сервисы были доступны в других частях вашего приложения.

Вместо того чтобы определять все классы-члены в одном огромном файле в виде JavaScript-модуля, объявите, какие компоненты, директивы и пайпы принадлежат модулю NgModule, в списке `@NgModule.declarations`. Такие классы называются [declarables](glossary.md#declarable 'Определение declarable'). Модуль NgModule может экспортировать только те декларируемые классы, которыми он владеет сам или импортирует из других модулей NgModules. Он не может объявлять или экспортировать классы другого типа. Декларируемые классы — это единственные классы, которые имеют значение для процесса компиляции Angular.

Полное описание свойств метаданных NgModule приведено в разделе [Использование метаданных NgModule](ngmodule-api.md 'Using the NgModule metadata').

## Пример, в котором используются оба варианта

Корневой NgModule `AppModule`, сгенерированный с помощью [Angular CLI](https://angular.io/cli) для нового проекта приложения, демонстрирует использование обоих видов модулей:

```ts
// imports
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';

// @NgModule decorator with its metadata
@NgModule({
    declarations: [AppComponent],
    imports: [BrowserModule],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

Корневой модуль NgModule начинается с операторов `import` для импорта модулей JavaScript.
Затем он конфигурирует `@NgModule` со следующими массивами:

-   `declarations`: Компоненты, директивы и пайпы, принадлежащие NgModule.
    Корневой NgModule нового проекта приложения имеет только один компонент, называемый `AppComponent`.

-   `imports`: Другие используемые вами NgModules, чтобы вы могли использовать их декларируемые элементы.
    Вновь созданный корневой NgModule импортирует [`BrowserModule`](https://angular.io/api/platform-browser/BrowserModule 'BrowserModule NgModule'), чтобы использовать специфические для браузера сервисы, такие как [DOM](https://www.w3.org/TR/DOM-Level-2-Core/introduction.html 'Definition of Document Object Model') рендеринг, санация и размещение.

-   `providers`: Провайдеры сервисов, которые могут использовать компоненты других NgModules.
    В новом корневом NgModule провайдеры отсутствуют.

-   `bootstrap`: Компонент, который Angular создает и вставляет в хост-страницу `index.html`, тем самым загружая приложение.
    Этот компонент, `AppComponent`, появляется как в массивах `declarations`, так и в массиве `bootstrap`.

## Следующие шаги

-   Подробнее о модулях NgModules см. в разделе [Organizing your app with NgModules](ngmodules.md 'Organizing your app with NgModules').
-   Подробнее о корневом NgModule см. в разделе [Запуск приложения с корневым NgModule](bootstrapping.md 'Запуск приложения с корневым NgModule').
-   О часто используемых модулях Angular NgModules и о том, как импортировать их в свое приложение, читайте в разделе [Frequently-used modules](frequent-ngmodules.md 'Часто используемые модули').

## Ссылки

-   [JavaScript modules vs. NgModules](https://angular.io/guide/ngmodule-vs-jsmodule)
