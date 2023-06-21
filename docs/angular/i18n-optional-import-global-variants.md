# Import global variants of the locale data

The [Angular CLI][aioclimain] automatically includes locale data if you run the [`ng build`][aioclibuild] command with the `--localize` option.

<!--todo: replace with code-example -->

<code-example format="shell" language="shell">

ng build --localize

</code-example>

The `@angular/common` package on npm contains the locale data files.
Global variants of the locale data are available in [`@angular/common/locales/global`][unpkgbrowseangularcommonlocalesglobal].

## `import` example for French

The following example imports the global variants for French \(`fr`\).

<code-example header="src/app/app.module.ts" path="i18n/doc-files/app.module.ts" region="global-locale"></code-example>

<!-- links -->

[aioclimain]: cli 'CLI Overview and Command Reference | Angular'
[aioclibuild]: cli/build 'ng build | CLI | Angular'

<!-- external links -->

[unpkgbrowseangularcommonlocalesglobal]: https://unpkg.com/browse/@angular/common/locales/global '@angular/common/locales/global | Unpkg'

<!-- end links -->

:date: 28.02.2022
