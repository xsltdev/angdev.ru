# Add the localize package

To take advantage of the localization features of Angular, use the [Angular CLI][aioclimain] to add the `@angular/localize` package to your project.

To add the `@angular/localize` package, use the following command to update the `package.json` and TypeScript configuration files in your project.

<code-example path="i18n/doc-files/commands.sh" region="add-localize"></code-example>

It adds `types: ["@angular/localize"]` in the TypeScript configuration files as well as the reference to the type definition of `@angular/localize` at the top of the `main.ts` file.

<div class="alert is-helpful">

For more information about `package.json` and `tsconfig.json` files, see [Workspace npm dependencies][aioguidenpmpackages] and [TypeScript Configuration][aioguidetsconfig].

</div>

If `@angular/localize` is not installed and you try to build a localized version of your project (for example, while using the `i18n` attributes in templates), the [Angular CLI][aioclimain] will generate an error, which would contain the steps that you can take to enable i18n for your project.

## Options

| OPTION             | DESCRIPTION                                                                                                                                                                                   | VALUE TYPE | DEFAULT VALUE |
| :----------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :------------ |
| `--project`        | The name of the project.                                                                                                                                                                      | `string`   |
| `--use-at-runtime` | If set, then `$localize` can be used at runtime. Also `@angular/localize` gets included in the `dependencies` section of `package.json`, rather than `devDependencies`, which is the default. | `boolean`  | `false`       |

For more available options, see [ng add][aiocliadd] in [Angular CLI][aioclimain].

## What's next

-   [@angular/localize API][aioapilocalize]
-   [Refer to locales by ID][aioguidei18ncommonlocaleid]

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
