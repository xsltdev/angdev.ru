# Рабочее пространство и структура файлов проекта

Вы разрабатываете приложения в контексте рабочего пространства Angular [workspace](guide/glossary#workspace). Рабочее пространство содержит файлы для одного или нескольких [проектов](guide/glossary#project).

Проект - это набор файлов, из которых состоит отдельное приложение или библиотека, доступная для совместного использования.

Команда Angular CLI `ng new` создает рабочее пространство.

<code-example format="shell" language="shell">

ng new &lt;my-project&gt;

</code-example>

Когда вы выполняете эту команду, CLI устанавливает необходимые пакеты Angular npm и другие зависимости в новое рабочее пространство с приложением корневого уровня с именем _my-project_. Корневая папка рабочего пространства содержит различные файлы поддержки и конфигурации, а также файл README со сгенерированным описательным текстом, который вы можете настроить.

По умолчанию `ng new` создает начальное скелетное приложение на корневом уровне рабочего пространства вместе с его сквозными тестами. Этот скелет предназначен для простого приложения Welcome, которое готово к запуску и легко модифицируется.

Приложение корневого уровня имеет то же имя, что и рабочее пространство, а исходные файлы находятся в подпапке `src/` рабочего пространства.

Такое поведение по умолчанию подходит для типичного стиля разработки "multi-repo", когда каждое приложение находится в своем собственном рабочем пространстве. Начинающим и средним пользователям рекомендуется использовать `ng new` для создания отдельного рабочего пространства для каждого приложения.

Angular также поддерживает рабочие пространства с [несколькими проектами](#multiple-projects). Этот тип среды разработки подходит для опытных пользователей, которые разрабатывают [разделяемые библиотеки](руководство/глоссарий#библиотека),

и для предприятий, использующих "монорепо" стиль разработки, с единым репозиторием и глобальной конфигурацией для всех проектов Angular.

Для настройки рабочего пространства монорепо следует пропустить создание корневого приложения. Смотрите [Настройка рабочего пространства для мультипроекта](#multiple-projects) ниже.

## Файлы конфигурации рабочего пространства

Все проекты в рабочем пространстве имеют общий [CLI-контекст конфигурации](guide/workspace-config). Верхний уровень рабочего пространства содержит файлы конфигурации всего рабочего пространства, файлы конфигурации для приложения корневого уровня и вложенные папки для исходных и тестовых файлов приложения корневого уровня.

| Workspace configuration files | Purpose | |:--- |:--- |
| `.editorconfig` | Configuration for code editors. See [EditorConfig](https://editorconfig.org). |
| `.gitignore` | Specifies intentionally untracked files that [Git](https://git-scm.com) should ignore. |
| `README.md` | Introductory documentation for the root application. |
| `angular.json` | CLI configuration defaults for all projects in the workspace, including configuration options for build, serve, and test tools that the CLI uses, such as [Karma](https://karma-runner.github.io), and [Protractor](https://www.protractortest.org). For details, see [Angular Workspace Configuration](guide/workspace-config). |
| `package.json` | Configures [npm package dependencies](guide/npm-packages) that are available to all projects in the workspace. See [npm documentation](https://docs.npmjs.com/files/package.json) for the specific format and contents of this file. |
| `package-lock.json` | Provides version information for all packages installed into `node_modules` by the npm client. See [npm documentation](https://docs.npmjs.com/files/package-lock.json) for details. If you use the yarn client, this file will be [yarn.lock](https://yarnpkg.com/lang/en/docs/yarn-lock) instead. |
| `src/` | Source files for the root-level application project. |
| `node_modules/` | Provides [npm packages](guide/npm-packages) to the entire workspace. Workspace-wide `node_modules` dependencies are visible to all projects. |
| `tsconfig.json` | The base [TypeScript](https://www.typescriptlang.org) configuration for projects in the workspace. All other configuration files inherit from this base file. For more information, see the [Configuration inheritance with extends](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html#configuration-inheritance-with-extends) section of the TypeScript documentation.|

## Файлы проекта приложения

По умолчанию команда CLI `ng new my-app` создает папку рабочего пространства с именем "my-app" и генерирует скелет нового приложения в папке `src/` на верхнем уровне рабочего пространства. Вновь созданное приложение содержит исходные файлы для корневого модуля, с корневым компонентом и шаблоном.

Когда файловая структура рабочего пространства создана, вы можете использовать команду `ng generate` в командной строке для добавления функциональности и данных в приложение. Это начальное приложение корневого уровня является _приложением по умолчанию_ для команд CLI\ (если вы не измените значение по умолчанию после создания [дополнительных приложений](#multiple-projects)\).

<div class="alert is-helpful">

Помимо использования CLI в командной строке, вы также можете работать с файлами непосредственно в исходной папке приложения и конфигурационными файлами.

</div>

Для рабочего пространства с одним приложением подпапка `src` рабочего пространства содержит исходные файлы\(логика приложения, данные и активы\) для корневого приложения. Для многопроектного рабочего пространства дополнительные проекты в папке `projects` содержат подпапку `project-name/src/` с такой же структурой.

### Исходные файлы приложения

Файлы верхнего уровня `src/` поддерживают тестирование и запуск вашего приложения. Вложенные папки содержат исходный код приложения и конфигурацию, специфичную для приложения.

| Application support files | Purpose | |:--- |:--- |
| `app/` | Contains the component files in which your application logic and data are defined. See details [below](#app-src). |
| `assets/` | Contains image and other asset files to be copied as-is when you build your application. |
| `favicon.ico` | An icon to use for this application in the bookmark bar. |
| `index.html` | The main HTML page that is served when someone visits your site. The CLI automatically adds all JavaScript and CSS files when building your app, so you typically don't need to add any `<script>` or` <link>` tags here manually. |
| `main.ts` | The main entry point for your application. Compiles the application with the [JIT compiler](guide/glossary#jit) and bootstraps the application's root module \(AppModule\) to run in the browser. You can also use the [AOT compiler](guide/aot-compiler) without changing any code by appending the `--aot` flag to the CLI `build` and `serve` commands. |
| `styles.css` | Lists CSS files that supply styles for a project. The extension reflects the style preprocessor you have configured for the project. |

<div class="alert is-helpful">

Новые проекты Angular по умолчанию используют строгий режим. Если это нежелательно, вы можете отказаться от него при создании проекта.
Для получения дополнительной информации смотрите [Строгий режим](guide/strict-mode).

</div>

<a id="app-src"></a>

Inside the `src` folder, the `app` folder contains your project's logic and data. Angular components, templates, and styles go here.

| `src/app/` files | Purpose | |---|---|

| `app/app.config.ts` | Defines the application config logic that tells Angular how to assemble the application. As you add more providers to the app, they must be declared here.<br><br>_Only generated when using the `--standalone` option._ |

| `app/app.component.ts` | Defines the logic for the application's root component, named `AppComponent`. The view associated with this root component becomes the root of the [view hierarchy](guide/glossary#view-hierarchy) as you add components and services to your application. |

| `app/app.component.html` | Defines the HTML template associated with the root `AppComponent`. |

| `app/app.component.css` | Defines the base CSS stylesheet for the root `AppComponent`. |

| `app/app.component.spec.ts` | Defines a unit test for the root `AppComponent`. |

| `app/app.module.ts` | Defines the root module, named `AppModule`, that tells Angular how to assemble the application. Initially declares only the `AppComponent`. По мере добавления новых компонентов в приложение, они должны быть объявлены здесь.<br><br>_Он создается только при использовании опции `--standalone`._ |

### Файлы конфигурации приложения

Конфигурационные файлы, специфичные для корневого приложения, находятся на уровне корня рабочего пространства. Для многопроектного рабочего пространства файлы конфигурации, специфичные для проекта, находятся в корне проекта, в разделе `projects/project-name/`.

Конфигурационные файлы для конкретного проекта [TypeScript](https://www.typescriptlang.org) наследуются от конфигурационного файла рабочего пространства `tsconfig.json`.

| Файлы конфигурации для конкретного приложения | Цель | | |:--- |:--- |:--- |
| `tsconfig.app.json` | Конфигурация для конкретного приложения [TypeScript](https://www.typescriptlang.org), включая параметры компилятора шаблонов TypeScript и Angular. Смотрите [TypeScript Configuration](guide/typescript-configuration) и [Angular Compiler Options](guide/angular-compiler-options). |

| `tsconfig.spec.json` | [TypeScript](https://www.typescriptlang.org) конфигурация для тестов приложения. Смотрите [TypeScript Configuration](guide/typescript-configuration). |

<a id="multiple-projects"></a>

## Несколько проектов

Многопроектное рабочее пространство подходит для предприятия, которое использует единое хранилище и глобальную конфигурацию для всех проектов Angular\ (модель "monorepo"\). Многопроектное рабочее пространство также поддерживает разработку библиотек.

### Настройка многопроектного рабочего пространства

Если вы планируете иметь несколько проектов в рабочем пространстве, вы можете пропустить начальную генерацию приложения при создании рабочего пространства и дать рабочему пространству уникальное имя. Следующая команда создает рабочую область со всеми конфигурационными файлами рабочей области, но без приложения корневого уровня.

<code-example format="shell" language="shell">

ng new my-workspace --no-create-application

</code-example>

Затем вы можете создавать приложения и библиотеки с именами, уникальными в пределах рабочей области.

<code-example format="shell" language="shell">

cd my-workspace ng generate application my-first-app

</code-example>

### Структура файлов нескольких проектов

Первое явно созданное приложение попадает в папку `projects` вместе со всеми остальными проектами в рабочей области. Вновь созданные библиотеки также добавляются в папку `projects`.

Когда вы создаете проекты таким образом, файловая структура рабочего пространства полностью соответствует структуре [файла конфигурации рабочего пространства] (guide/workspace-config), `angular.json`.

<div class="filetree">     <div class="file">
        my-workspace
    </div>
    <div class="children">
        <div class="file">
          &hellip; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (workspace-wide config files)
        </div>
        <div class="file">
          projects &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (generated applications and libraries)
        </div>
        <div class="children">
            <div class="file">
              my-first-app &nbsp; --(an explicitly generated application)
            </div>
            <div class="children">
                <div class="file">
                  &hellip; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --(application-specific config)
                </div>
                <div class="file">
                  src &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --(source and support files for application)
                </div>
            </div>
            <div class="file">
              my-lib &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --(a generated library)
            </div>
            <div class="children">
                <div class="file">
                  &hellip; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --(library-specific config)
                </div>
                <div class="file">
                  src &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --(source and support files for library)
                </div>
            </div>
        </div>
    </div>
</div>

## Файлы проекта библиотеки

Когда вы создаете библиотеку с помощью CLI \(с помощью такой команды, как `ng generate library my-lib`\), созданные файлы помещаются в папку `projects/` рабочего пространства. Более подробную информацию о создании собственных библиотек смотрите в [Создание библиотек](guide/creating-libraries).

Библиотеки, в отличие от приложений, имеют свой собственный конфигурационный файл `package.json`.

В папке `projects/` находится папка `my-lib`, содержащая код вашей библиотеки.

| Library source files | Purpose | |:--- |:--- |
| `src/lib` | Contains your library project's logic and data. Like an application project, a library project can contain components, services, modules, directives, and pipes. |
| `src/public-api.ts` | Specifies all files that are exported from your library. |
| `ng-package.json` | Configuration file used by [ng-packagr](https://github.com/ng-packagr/ng-packagr) for building your library. |
| `package.json` | Configures [npm package dependencies](guide/npm-packages) that are required for this library. |
| `tsconfig.lib.json` | Library-specific [TypeScript](https://www.typescriptlang.org) configuration, including TypeScript and Angular template compiler options. See [TypeScript Configuration](guide/typescript-configuration). |
| `tsconfig.lib.prod.json` | Library-specific [TypeScript](https://www.typescriptlang.org) configuration that is used when building the library in production mode. |
| `tsconfig.spec.json` | [TypeScript](https://www.typescriptlang.org) configuration for the library tests. See [TypeScript Configuration](guide/typescript-configuration). |

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2023-04-24
