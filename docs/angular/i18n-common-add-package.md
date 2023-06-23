# Добавьте пакет localize

Чтобы воспользоваться возможностями локализации в Angular, используйте [Angular CLI][aioclimain] для добавления пакета `@angular/localize` в ваш проект.

Чтобы добавить пакет `@angular/localize`, используйте следующую команду для обновления конфигурационных файлов `package.json` и TypeScript в вашем проекте.

<code-example path="i18n/doc-files/commands.sh" region="add-localize"></code-example>.

Это добавляет `типы: ["@angular/localize"]` в конфигурационные файлы TypeScript, а также ссылку на определение типа `@angular/localize` в верхней части файла `main.ts`.

<div class="alert is-helpful">

Дополнительную информацию о файлах `package.json` и `tsconfig.json` смотрите в разделах [Workspace npm dependencies][aioguidenpmpackages] и [TypeScript Configuration][aioguidetsconfig].

</div>

Если `@angular/localize` не установлен и вы пытаетесь собрать локализованную версию вашего проекта (например, при использовании атрибутов `i18n` в шаблонах), [Angular CLI][aioclimain] выдаст ошибку, которая будет содержать шаги, которые вы можете предпринять, чтобы включить i18n для вашего проекта.

## Options

| OPTION | DESCRIPTION | VALUE TYPE | VALUE TYPE | DEFAULT VALUE | | :----------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :------------ |.

| `--project` | Имя проекта. | `string` |

| `--use-at-runtime` | Если установлено, то `$localize` может быть использован во время выполнения. Также `@angular/localize` включается в секцию `dependencies` в `package.json`, а не в `devDependencies`, которая используется по умолчанию. | `boolean` | `false`.

Дополнительные доступные опции см. в [ng add][aiocliadd] в [Angular CLI][aioclimain].

## Что дальше

-   [@angular/localize API][aioapilocalize]

-   [Ссылка на локали по ID][aioguidei18ncommonlocaleid]

<!-- links -->

[aioclimain]: cli 'CLI Overview and Command Reference | Angular'
[aioguidei18ncommonlocaleid]: guide/i18n-common-locale-id 'Refer to locales by ID | Angular'
[aioguidenpmpackages]: guide/npm-packages 'Workspace npm dependencies | Angular'
[aioguidetsconfig]: guide/typescript-configuration 'TypeScript Configuration | Angular'
[aiocliadd]: cli/add 'ng add | CLI | Angular'
[aioapilocalize]: api/localize '$localize | @angular/localize - API | Angular'

<!-- external links -->

<!-- end links -->

:date: 10.03.2023
